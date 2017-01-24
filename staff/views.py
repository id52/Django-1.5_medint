# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.views.generic import View
from common.models import ROLES, StaffRole
from django_boto.s3.storage import S3Storage
from common.models import UserInfo
import datetime
import re
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image



class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return render_to_response('staff/content.html', RequestContext(request))
        ctx = RequestContext(request)
        ctx['staff_roles'] = StaffRole.objects.all()
        ctx['roles'] = ROLES
        return render_to_response('staff/index.html', ctx)


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect("/")





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
        return HttpResponseRedirect("/staff/#profile")


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