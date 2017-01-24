import json
import logging
import sys
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
import simplejson
from decorators import roles_required

from forms import RegisterForm, LoginForm
from common.hellosign import send_document
# from models import RecoverKey, MailValidationKey, SignableDocument
from common.models import ROLES, MailValidationKey, SignableDocument, MedintUser
from indivo_client import IndivoClient
from medint.models import RecoverKey
from xml.dom import minidom as XML
import xml.etree.ElementTree as ET
from django_boto.s3.storage import S3Storage
from django.http import HttpResponseRedirect, HttpResponse
from common.models import UserInfo
import datetime
import re
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image





class IndexView(View):
    def get(self, request):
        ctx = RequestContext(request, {'roles': ROLES})
        if request.user.is_authenticated():
            return render_to_response('medint/intro.html', ctx)
        return render_to_response('medint/index.html', RequestContext(request, {'roles': ROLES}))


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect("/")


class ConfirmView(View):
    def send_doctor_documents(self, user):
        user_info = user.user_info
        fields = {'years1': '2', 'years_begin': '2013', 'years_end': '2015', 'years2': '3',
                  'name': '%s %s' % (user_info.first_name, user_info.last_name)}
        res = send_document(
            '6843966546d30d2f33fae35f1b87de9f24b1ab6a', user_info.email,
            '%s %s' % (user_info.first_name, user_info.last_name),
            role='Doctor', fields=fields
        )

        if 'signature_request' in res:
            SignableDocument.objects.create(
                user=user,
                request_id=res['signature_request']['signature_request_id'],
                template='DOCUMENT_CONTRACT1')

        res = send_document(
            '4bc1931b6974ec4bd09be5091aa9e4a0d52e2001', user_info.email,
            '%s %s' % (user_info.first_name, user_info.last_name),
            role='Doctor', fields={'name': '%s %s' % (user_info.first_name, user_info.last_name)}
        )

        if 'signature_request' in res:
            SignableDocument.objects.create(
                user=user,
                request_id=res['signature_request']['signature_request_id'],
                template='DOCUMENT_CONTRACT')

    def send_patient_documents(self, user):
        user_info = user.user_info
        fields = {'fee_number': '2', 'fee_text': 'two',
                  'name': '%s %s' % (user_info.first_name, user_info.last_name)}
        res = send_document(
            '6fd12a1b3963ab04231129536a72011b83a27ce0', user_info.email,
            '%s %s' % (user_info.first_name, user_info.last_name),
            role='Patient', fields=fields
        )

        if 'signature_request' in res:
            SignableDocument.objects.create(
                user=user,
                request_id=res['signature_request']['signature_request_id'],
                template='DOCUMENT_CONTRACT1')

        res = send_document(
            '8a5c539d8b10fea02d478f21e66445e62222e627', user_info.email,
            '%s %s' % (user_info.first_name, user_info.last_name),
            role='Patient', fields={}
        )

        if 'signature_request' in res:
            SignableDocument.objects.create(
                user=user,
                request_id=res['signature_request']['signature_request_id'],
                template='DOCUMENT_CONTRACT')

    def get(self, request):
        ctx = RequestContext(request)
        if 'GET' == request.method:
            if 'key' in request.GET:
                try:
                    key = MailValidationKey.objects.get(key__exact=request.GET['key'])
                except MailValidationKey.DoesNotExist:
                    pass
                else:
                    user = key.user
                    user.is_active = True
                    user.save()

                    print 'Sending contract'
                    if user.role == ROLES['DOCTOR']['id']:
                        self.send_doctor_documents(user)
                    elif user.role == ROLES['PATIENT']['id']:
                        self.send_patient_documents(user)

            return render_to_response('confirm.html', ctx)


class PatientView(View):
    @method_decorator(login_required)
    @roles_required(('PATIENT',))
    def get(self, request):
        return render_to_response('medint/patient.html', RequestContext(request))


class DoctorView(View):
    @method_decorator(login_required)
    @roles_required(('DOCTOR',))
    def get(self, request):
        return render_to_response('medint/doctor.html', RequestContext(request))


class RecoverView(View):
    def get(self, request):
        ctx = RequestContext(request)
        if 'key' in request.GET:
            key = request.GET['key']
            rk = RecoverKey.objects.filter(key__exact=key)
            if rk:
                ctx['key'] = key
        return render_to_response('recover.html', ctx)

    def post(self, request):
        rk = RecoverKey.objects.filter(key__exact=request.POST['key'])
        passwd = request.POST['password']
        u = rk[0].user
        u.set_password(passwd)
        u.save()
        return HttpResponseRedirect("/")


class PatientInfoView (View):
    def __init__(self):
        self.client = IndivoClient(settings.INDIVO_SERVER_PARAMS, settings.INDIVO_CONSUMER_PARAMS,
                              pha_email=settings.INDIVO_USER_EMAIL)

    def get(self, request, patient_id=None):
        ctx = RequestContext(request)
        user = MedintUser.objects.get(id=patient_id)
        record_id = user.user_info.patientinfo.indivo_record_id
        ctx['record'] = record_id

        result = {}

        for d in ['problem', 'allergy', 'AllergyExclusion', 'equipment', 'immunization', 'LabResult', 'measurement', 'medication', 'procedure', 'SimpleClinicalNote', 'VitalSigns', 'Encounter']:
            resp, content = self.client.generic_list(record_id=record_id, data_model=d)
            print '%s:' % d
            content = json.loads(content)
            if content:
                result[d] = content
        ctx['result'] = result
        return render_to_response('medint/patient_info.html', ctx)

    def post(self, request, patient_id=None):
        print request.FILES.getlist('file')
        # data = request.FILES['file'].read()
        user = MedintUser.objects.get(id=patient_id)
        record_id = user.user_info.patientinfo.indivo_record_id
        ctx = RequestContext(request)
        ctx['record'] = record_id
        for f in request.FILES.getlist('file'):
            data = f.read()
            resp, content = self.client.document_create(record_id=record_id, body=data, content_type='application/xml')
        # print resp
        # print content
        return self.get(request, patient_id)

        # return render_to_response('medint/patient_info.html', ctx)


class TimeLineView (View):
    def __init__(self):
        self.client = IndivoClient(settings.INDIVO_SERVER_PARAMS, settings.INDIVO_CONSUMER_PARAMS,
                              pha_email=settings.INDIVO_USER_EMAIL)
    def get(self, request, patient_id=None):
        ctx = RequestContext(request)
        user = MedintUser.objects.get(id=patient_id)
        record_id = user.user_info.patientinfo.indivo_record_id
        ctx['record'] = record_id

        result = {}

        for d in ['problem', 'immunization', 'medication']:
            resp, content = self.client.generic_list(record_id=record_id, data_model=d)
            print '%s:' % d
            content = json.loads(content)
            if content:
                result[d] = content
        ctx['result'] = result
        return render_to_response('medint/patient_timeline.html', ctx)


def uploadPhoto(request):
        user=UserInfo.objects.get(id=request.user.user_info.id)
        if request.FILES.get(u'cover'):
            f = request.FILES.get(u'cover')

            img = Image.open(f)
            img = img.convert('RGBA')
            w = w_resize = 960
            h = h_resize = 294
            h_resize = img.size[1] * w / img.size[0].__float__()
            img = img.resize((w_resize.__int__(), h_resize.__int__()), Image.ANTIALIAS)
            h_start=(img.size[1]-h)/2
            img = img.crop((0,h_start,w,h_start+h))
            img = img.resize((w.__int__(), h.__int__()), Image.ANTIALIAS)

            img_io = StringIO.StringIO()
            img.save(img_io, format='JPEG', quality=85)
            img_file = InMemoryUploadedFile(img_io, None, 'foo.jpeg', 'image/jpeg', img_io.len, None)
            user.cover = img_file

        if request.FILES.get(u'photo'):
            f = request.FILES.get(u'photo')
            img = Image.open(f)
            img = img.convert('RGBA')
            w = w_resize = 200
            h = h_resize = 200

            if img.size[0] > img.size[1]:
                w_resize = img.size[0] * h / img.size[1].__float__()
                img = img.resize((w_resize.__int__(), h_resize.__int__()), Image.ANTIALIAS)
                w_start=(img.size[0]-w)/2
                img = img.crop((w_start,0,w_start+w,h))
            else:
                h_resize = img.size[1] * w / img.size[0].__float__()
                img = img.resize((w_resize.__int__(), h_resize.__int__()), Image.ANTIALIAS)
                img = img.crop((0,0,w,h))

            img = img.resize((w.__int__(), h.__int__()), Image.ANTIALIAS)

            img_io = StringIO.StringIO()
            img.save(img_io, format='JPEG', quality=85)
            img_file = InMemoryUploadedFile(img_io, None, 'foo.jpg', 'image/jpeg', img_io.len, None)
            user.photo = img_file

        user.save()
        return HttpResponseRedirect("/doctor#profile")


def getCover(request):
        user = UserInfo.objects.get(id=request.user.user_info.id)
        s3 = S3Storage()
        if user.cover:
            return HttpResponseRedirect(s3.s3.generate_url(60, 'GET', bucket=s3.bucket.name, key='/%s' % user.cover.name))
        else:
            return HttpResponseRedirect("/static/img/profile/cover.jpg")


def getPhoto(request):
        user = UserInfo.objects.get(id=request.user.user_info.id)
        s3 = S3Storage()
        if user.photo:
            return HttpResponseRedirect(s3.s3.generate_url(60, 'GET', bucket=s3.bucket.name, key='/%s' % user.photo.name))
        else:
            return HttpResponseRedirect("/static/img/profile/profile-thumb.jpg")





# def index(request):
#     if request.user.is_authenticated():
#         r = request.user.get_profile().role
#         # if ROLES['DOCTOR']['id'] == r:
#         #     return redirect('doctor')
#         # elif ROLES['PATIENT']['id'] == r:
#         #     return redirect('patient')
#         return render_to_response('medint/intro.html', RequestContext(request, {'roles': ROLES}))
#     return render_to_response('medint/index.html', RequestContext(request, {'roles': ROLES}))



#
#
# def confirm(request):
#     ctx = RequestContext(request)
#     if 'GET' == request.method:
#         if 'key' in request.GET:
#             try:
#                 key = MailValidationKey.objects.get(key__exact=request.GET['key'])
#             except MailValidationKey.DoesNotExist:
#                 pass
#             else:
#                 user = key.user
#                 user.is_active = True
#                 user.save()
#
#                 print 'Sending contract'
#                 if user.get_profile().role == ROLES['DOCTOR']['id']:
#                     fields = {'years1': '2', 'years_begin': '2013', 'years_end': '2015', 'years2': '3',
#                               'name': '%s %s' % (user.first_name, user.last_name)}
#                     res = send_document(
#                         '6843966546d30d2f33fae35f1b87de9f24b1ab6a', user.email, '%s %s' % (user.first_name, user.last_name),
#                         role='Doctor', fields=fields
#                     )
#
#                     if 'signature_request' in res:
#                         SignableDocument.objects.create(
#                             user=user,
#                             request_id=res['signature_request']['signature_request_id'],
#                             template='DOCUMENT_CONTRACT1')
#
#                     res = send_document(
#                         '4bc1931b6974ec4bd09be5091aa9e4a0d52e2001', user.email, '%s %s' % (user.first_name, user.last_name),
#                         role='Doctor', fields={'name': '%s %s' % (user.first_name, user.last_name)}
#                     )
#
#                     if 'signature_request' in res:
#                         SignableDocument.objects.create(
#                             user=user,
#                             request_id=res['signature_request']['signature_request_id'],
#                             template='DOCUMENT_CONTRACT')
#                 elif user.get_profile().role == ROLES['PATIENT']['id']:
#                     fields = {'fee_number': '2', 'fee_text': 'two',
#                               'name': '%s %s' % (user.first_name, user.last_name)}
#                     res = send_document(
#                         '6fd12a1b3963ab04231129536a72011b83a27ce0', user.email, '%s %s' % (user.first_name, user.last_name),
#                         role='Patient', fields=fields
#                     )
#
#                     if 'signature_request' in res:
#                         SignableDocument.objects.create(
#                             user=user,
#                             request_id=res['signature_request']['signature_request_id'],
#                             template='DOCUMENT_CONTRACT1')
#
#                     res = send_document(
#                         '8a5c539d8b10fea02d478f21e66445e62222e627', user.email, '%s %s' % (user.first_name, user.last_name),
#                         role='Patient', fields={}
#                     )
#
#                     if 'signature_request' in res:
#                         SignableDocument.objects.create(
#                             user=user,
#                             request_id=res['signature_request']['signature_request_id'],
#                             template='DOCUMENT_CONTRACT')
#
#         return render_to_response('confirm.html', ctx)
#
#

#
#
# @login_required
# def webgl_model(request):
#     return render_to_response('3dmodel.html', RequestContext(request))
#
#
# def install_chrome(request):
#     return render_to_response('install_chrome.html', RequestContext(request))
#
#
# def register(request):
#     ctx = RequestContext(request)
#     if 'GET' == request.method:
#         f = RegisterForm()
#         ctx['form'] = f
#         return render_to_response('register.html', ctx)
#     if 'POST' == request.method:
#         f = RegisterForm(request.POST)
#         if f.is_valid():
#             mail = f.cleaned_data['email'].lower()
#             passwd = f.cleaned_data['password']
#             u = User.objects.create_user(mail, mail, passwd)
#             u.is_active = False
#             u.first_name=f.cleaned_data['first_name']
#             u.last_name=f.cleaned_data['last_name']
#             u.save()
#             p = u.get_profile()
#             p.middleName = f.cleaned_data['middle_name']
#             p.ph = f.cleaned_data['ph']
#             p.save()
#             subject, from_email, to = 'Password recovery', 'no_reply@medicalintelligence.com', mail
#             text_content = 'Congratulations! You have successfully registered at Medical Intelligence.'
#             html_content = '<p>Congratulations! You have successfully registered at Medical Intelligence.</p>'
#             msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
# #            user = auth.authenticate(username = u.username, password=f.cleaned_data['password'])
# #            auth.login(request, user)
#             return HttpResponseRedirect("/")
#         else:
#             ctx['form'] = f
#             return render_to_response('register.html', ctx)
#
#
# def lost_password(request):
#     from random import choice
#     import string
#     ctx = RequestContext(request)
#     if request.method == 'GET':
#         return render_to_response('lost.html', ctx)
#     if 'email' in request.POST:
#         mail = request.POST['email'].lower().strip()
#         u = User.objects.filter(email__iexact = mail)
#         if u:
#             try:
#                 logging.debug('wanna send')
#                 user = u[0]
#                 key = ''.join([choice(string.letters + string.digits) for i in range(20)])
#                 RecoverKey.objects.create( user = user, key= key)
#                 from django.contrib.sites.models import Site
#
#                 current_site = Site.objects.get_current()
#                 current_site = request.get_host()
#
#                 subject, from_email, to = 'Password recovery', 'no_reply@medicalintelligence.com', user.email
#                 text_content = 'To recover password visit http://%s/recover?key=%s' % (current_site, key)
#                 html_content = 'To recover password visit <a href="http://%s/recover?key=%s">http://%s/recover?key=%s</a>' % (current_site, key, current_site, key)
#                 msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()
#                 logging.debug('Recovery mail sent')
#
#             except:
#                 logging.error('Cannot send mail')
#                 logging.error(sys.exc_info()[0])
#         else:
#             logging.error('User not found')
#
#         return render_to_response('lost.html', ctx)
#
#
# def recover_password(request):
#     ctx = RequestContext(request)
#     if 'GET' == request.method:
#         if 'key' in request.GET:
#             key = request.GET['key']
#             rk = RecoverKey.objects.filter(key__exact = key)
#             if rk:
#                 ctx['key'] = key
#         return render_to_response('recover.html', ctx)
#     if 'POST' == request.method:
#         rk = RecoverKey.objects.filter(key__exact = request.POST['key'])
#         passwd  = request.POST['password']
#         u = rk[0].user
#         u.set_password(passwd)
#         u.save()
#         return  HttpResponseRedirect("/")
#
#
# @login_required
# def dashboard(request):
#     ctx = RequestContext(request)
#     return  render_to_response('dashboard.html', ctx)
#
#
# @login_required
# def dashboard_mri(request):
#     ctx = RequestContext(request)
#     return  render_to_response('dashboard_mri.html', ctx)
#
#
# @login_required
# def body_view(request):
#     ctx = RequestContext(request)
#     return  render_to_response('dashboard_bodyview.html', ctx)
#
#
# @login_required
# def dashboard_risk(request):
#     ctx = RequestContext(request)
#     return  render_to_response('dashboard_risk.html', ctx)
#
#
# @login_required
# def dashboard_risk_red(request):
#     ctx = RequestContext(request)
#     return  render_to_response('dashboard_risk_red.html', ctx)
#
#
# @login_required
# def dashboard_patient(request):
#     ctx = RequestContext(request)
#     return  render_to_response('dashboard_patient.html', ctx)
#
#
# class LoginView(View):
#     def get(self, request):
#         ctx = RequestContext(request)
#         f = LoginForm()
#         if 'next' in request.GET:
#             f = LoginForm(initial={'next': request.GET['next']})
#         ctx['form'] = f
#         return  render_to_response('login.html', ctx)
#
#     def post(self, request):
#         ctx = RequestContext(request)
#         f = LoginForm(request.POST)
#         if f.is_valid():
#             user = auth.authenticate(username=f.cleaned_data['email'].lower(), password=f.cleaned_data['password'])
#             if not user:
#                 return render_to_response('login.html', ctx)
#             elif not user.is_active:
#                 return render_to_response('login.html', ctx)
#             else:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(f.cleaned_data['next'])
#         else:
#             ctx['form'] = f
#             return  render_to_response('login.html', ctx)
#
#
# class CallbackView(View):
#     def get(self, request):
#         print 'GET', request.GET
#         return HttpResponse('', mimetype='text/plain', status=200)
#
#     def post(self, request):
#         json = simplejson.loads(request.POST['json'])
#         # print json['signature_request']
#         req_id = json['signature_request']['signature_request_id']
#         # doc = SignableDocument.objects.filter(request_id__exact=req_id)
#         # if doc:
#         SignableDocument.objects.filter(request_id=req_id).update(
#             status=json['signature_request']['signatures'][0]['status_code']
#         )
#
#         return HttpResponse('', mimetype='text/plain', status=200)
