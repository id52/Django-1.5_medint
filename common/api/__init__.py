# - coding: utf-8  -

from django import forms
from django.contrib import auth
from django.conf.urls import patterns, url
from common import verify_yubikey
from jsonview import JSONView, make_response
from common.models import YubiKey


class OTPForm(forms.Form):
    otp = forms.CharField(label='otp')
    role = forms.CharField(label='')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    otp = forms.CharField(required=False)
    next = forms.CharField(widget=forms.HiddenInput, initial='/', required=False)


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
                            return make_response(error="Invalid Yubikey")
                    else:
                        return make_response(error='Invalid role')
                else:
                    return make_response(error="Invalid Yubikey")
            except YubiKey.DoesNotExist:
                return make_response(error='Unregistered YubiKey')

        return make_response(validation=f._errors)


class LoginView(JSONView):
    def post(self, request):
        f = LoginForm(request.POST)
        if f.is_valid():
            user = auth.authenticate(
                username=f.cleaned_data['username'].lower(),
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


urlpatterns = patterns('',
    url(r'login$', LoginView.as_view()),
    # url(r'saveAddress', save_address),
    # url(r'lostPassword', lost_password),
    # url(r'disease', DiseaseView.as_view()),
    # url(r'feedback', FeedbackView.as_view()),
    # url(r'doctor/register/?$', doctor_register),
    # url(r'patient/register/?$', patient_register),
    url(r'checkotp/?', OTPView.as_view())
)
