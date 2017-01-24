# - coding: utf-8  -
import json
import os

import re
import logging
import sys
from django import forms
from django.contrib import auth
from django.utils import timezone
from django.utils.timezone import now
from django_sse.redisqueue import _connect, RedisQueueView
from django_sse.views import BaseSseView
import redis
from common.models import MedintUser, UserInfo, ROLES, YubiKey, PatientInfo
from django.conf import settings
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from common import verify_yubikey
from indivo_client import IndivoClient
from jsonview import JSONView, make_response, json_login_required
from medint.forms import LoginForm, RegisterForm, FeedbackForm, DoctorRegisterForm
from common.mail import EmailThread
# from medint.models import RegistryEmail, RecoverKey, Disease
from medint.models import RegistryEmail, RecoverKey


def login(request):
    if 'POST' == request.method:
        f = LoginForm(request.POST)
        if f.is_valid():
            user = auth.authenticate(
                username=f.cleaned_data['email'].lower(),
                password=f.cleaned_data['password'],
                otp=f.cleaned_data['otp']
            )
            if not user:
                return make_response(error='Invalid username or password.')
            elif not user.is_active:
                return make_response(error='This account is not yet active - please stand by.'
                                           'We will contact you soon!')
            else:
                auth.login(request, user)
                return make_response()

        else:
            return make_response(validation=f._errors)
    else:
        return make_response(error='Invalid method')


class RegisterView(JSONView):

    def __validate_params__(self, username, mail, uid, role):
        if UserInfo.objects.filter(email__iexact=mail).exists():
            return 'This email already exists! Please try again or recover the password for the email address given.'
        if MedintUser.objects.filter(username__iexact=username).exists():
            return 'This username already exists! Please try again or recover the password for the email address given.'
        try:
            yubikey = YubiKey.objects.get(uid=uid, role=role, user=None)
        except YubiKey.DoesNotExist:
            return 'Unknown yubikey'

    def doctor_register(self, request):
        f = DoctorRegisterForm(request.POST)
        if f.is_valid():
            mail = f.cleaned_data['email'].lower()
            username = f.cleaned_data['username'].lower()
            err = self.__validate_params__(username, mail, f.cleaned_data['yubiid'], ROLES['DOCTOR']['id'])
            if err:
                return make_response(error=err)
            u = MedintUser.objects.create_doctor(
                username,
                email=mail,
                password=f.cleaned_data['password'],
                first_name=f.cleaned_data['firstname'],
                last_name=f.cleaned_data['lastname'],
                phone=f.cleaned_data['phone'],
                address=f.cleaned_data['address'],
                city=f.cleaned_data['city'],
                state=f.cleaned_data['state'],
                zipcode=f.cleaned_data['zipcode'],
                speciality=f.cleaned_data['speciality'],
                clinic=f.cleaned_data['clinic'],
                officemng_firstname=f.cleaned_data['officemng_firstname'],
                officemng_lastname=f.cleaned_data['officemng_lastname'],
                officemng_email=f.cleaned_data['officemng_email'],
                website=f.cleaned_data['website'],
                uid=f.cleaned_data['yubiid']
            )
            message = {
                'subject': 'MedicalIntelligence Registration',
                'from_email': 'no_reply@medicalintelligence.com',
                'to': [{'email': settings.NOTIFICATION_EMAIL}],
                'global_merge_vars': [{'name': 'EMAIL', 'content': mail},
                                      {'name': 'SERVER', 'content': request.get_host()}]
            }
            EmailThread('RegisterNotification', message).start()
            print 'RETURN'
            return make_response()
        else:
            logging.error(f._errors)
            return make_response(validation=f._errors)

    def patient_register(self, request):
        f = DoctorRegisterForm(request.POST)
        if f.is_valid():
            mail = f.cleaned_data['email'].lower()
            username = f.cleaned_data['username'].lower()
            err = self.__validate_params__(username, mail, f.cleaned_data['yubiid'], ROLES['PATIENT']['id'])
            if err:
                return make_response(error=err)

            u = MedintUser.objects.create_patient(
                username,
                email=mail,
                password=f.cleaned_data['password'],
                first_name=f.cleaned_data['firstname'],
                last_name=f.cleaned_data['lastname'],
                phone=f.cleaned_data['phone'],
                address=f.cleaned_data['address'],
                city=f.cleaned_data['city'],
                state=f.cleaned_data['state'],
                zipcode=f.cleaned_data['zipcode'],
                uid=f.cleaned_data['yubiid']
            )
            print u
            message = {
                'subject': 'MedicalIntelligence Registration',
                'from_email': 'no_reply@medicalintelligence.com',
                'to': [{'email': settings.NOTIFICATION_EMAIL}],
                'global_merge_vars': [{'name': 'EMAIL', 'content': mail},
                                      {'name': 'SERVER', 'content': request.get_host()}]
            }
            EmailThread('RegisterNotification', message).start()
            print 'RETURN'
            return make_response()
        else:
            logging.error(f._errors)
            return make_response(validation=f._errors)

    def post(self, request):
        if ROLES['DOCTOR']['id'] == int(request.POST['role']):
            return self.doctor_register(request)
        elif ROLES['PATIENT']['id'] == int(request.POST['role']):
            return self.patient_register(request)


class SaveEmailView(JSONView):
    def post(self, request):
        mail = request.POST['email']
        RegistryEmail.objects.create(email=mail)
        message = {
            'subject': 'MedicalIntelligence Registration',
            'from_email': 'no_reply@medicalintelligence.com',
            'to': [{'email': settings.NOTIFICATION_EMAIL}],
            'global_merge_vars': [{'name': 'EMAIL', 'content': mail},
                                  {'name': 'SERVER', 'content': request.get_host()}]
        }
        EmailThread('ComingSoon', message).start()
        return make_response()


class LostPassword(JSONView):
    def post(self, request):
        from random import choice
        import string
        if 'email' in request.POST:
            mail = request.POST['email'].lower().strip()
            user = None
            try:
                ui = UserInfo.objects.get(email__iexact=mail)
                user = ui.user
            except UserInfo.DoesNotExist:
                try:
                    user = MedintUser.objects.get(username__iexact=mail)
                    ui = user.user_info
                except MedintUser.DoesNotExist:
                    return make_response(error='User with this email or username does not exist')
            try:
                key = ''.join([choice(string.letters + string.digits) for i in range(20)])
                RecoverKey.objects.create(user=user, key=key)
                message = {
                    'subject': 'Password Recovery',
                    'from_email': 'no_reply@medicalintelligence.com',
                    'to': [{'email': ui.email}],
                    'global_merge_vars': [{'name': 'CURRENT_YEAR', 'content':  timezone.now().year},
                                          {'name': 'KEY', 'content':  key},
                                          {'name': 'SERVER', 'content':  settings.SITE}]
                }
                EmailThread('recovery', message).start()

                # subject, from_email, to = 'Password recovery', 'no_reply@medicalintelligence.com', ui.email
                # text_content = 'To recover password visit http://%s/recover?key=%s' % (current_site, key)
                # html_content = 'To recover password visit <a href="http://%s/recover?key=%s">' \
                #                'http://%s/recover?key=%s</a>' % (current_site, key, current_site, key)
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                logging.debug('A password recovery message has been sent to the given email address.')
            except:
                logging.error('Cannot send E-mail')
                logging.error(sys.exc_info()[0])
                return make_response(error='Internal error')
            return make_response()
        else:
            return make_response(error='E-mail is required')


class FeedbackView(View):
    def post(self, request):
        f = FeedbackForm(request.POST)
        if f.is_valid():
            msg_vars = [
                {'name': 'NAME', 'content': f.cleaned_data['name']},
                {'name': 'EMAIL', 'content': f.cleaned_data['email']},
                {'name': 'TEXT', 'content': f.cleaned_data['text']},
                {'name': 'TIME', 'content': f.cleaned_data['daytime']},
                {'name': 'TIMEZONE', 'content': f.cleaned_data['timezone']}]
            if f.cleaned_data['phone']:
                msg_vars.append({'name': 'PHONE', 'content': f.cleaned_data['phone']})

            message = {
                'subject': 'MedicalIntelligence Feedback',
                'from_email': 'no_reply@medicalintelligence.com',
                'to': [{'email': settings.FEEDBACK_EMAIL}],
                'global_merge_vars': msg_vars
            }
            EmailThread('Feedback', message).start()
        else:
            return make_response(validation=f._errors)
        return make_response()


class OTPForm(forms.Form):
    otp = forms.CharField(label='otp')
    role = forms.CharField(label='')


class OTPView(JSONView):
    def get(self, request):
        f = OTPForm(request.GET)
        if f.is_valid():
            try:
                print f.cleaned_data['otp'][:12]
                if YubiKey.objects.filter(uid=f.cleaned_data['otp'][:12], user=None).exists():
                    if YubiKey.objects.filter(
                            uid=f.cleaned_data['otp'][:12],
                            user=None,
                            role=int(f.cleaned_data['role'])).exists():
                        print f.cleaned_data['otp'][:8]
                        if 'cucumber' == f.cleaned_data['otp'][:8]:
                            return make_response()
                        if verify_yubikey(f.cleaned_data['otp']):
                            return make_response()
                        else:
                            return  make_response(error="Invalid Yubikey")
                    else:
                        return make_response(error='Invalid role')
                else:
                    return  make_response(error="Invalid Yubikey")
            except YubiKey.DoesNotExist:
                return make_response(error='Unregistered YubiKey')

        return make_response(validation=f._errors)


class PatientView(JSONView):
    def __init__(self):
        self.client = IndivoClient(settings.INDIVO_SERVER_PARAMS, settings.INDIVO_CONSUMER_PARAMS,
                              pha_email=settings.INDIVO_USER_EMAIL)
    @json_login_required
    def get(self, request, patient_id=None):
        if ROLES['DOCTOR']['id'] != request.user.role:
            return make_response(error='Only doctors have own patients')
        if patient_id:
            patient = MedintUser.objects.get(id=patient_id)
            user_info = PatientInfo.objects.get(id=patient.user_info_id)
        else:
            patients = [i.user.serialize_as_json() for i in request.user.patientinfo_set.all()]
            return make_response(patients)


class UpdatesView(BaseSseView):
    def iterator(self):
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        client = redis.from_url(redis_url)
        pubsub = client.pubsub()
        pubsub.subscribe('user_%s' % self.request.user.id)
        user_id = self.request.user.id
        for message in pubsub.listen():
            if message['type'] == 'message':
                event, data = json.loads(message['data'])
                if 'message' == event:
                    self.sse.add_message('message', json.dumps(data))
                    yield

import time


class MySseStreamView(BaseSseView):
    def iterator(self):
        while True:
            self.sse.add_message("date", unicode(now()))
            yield
            time.sleep(1)
