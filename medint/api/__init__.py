# - coding: utf-8  -
from django.conf.urls import patterns, url
from jsonview import json_login_required
from medint.api.handlers import RegisterView, SaveEmailView, LostPassword, PatientView, UpdatesView, MySseStreamView


urlpatterns = patterns(
   url(r'register', RegisterView.as_view()),
    # url(r'login$', login),
    url(r'saveAddress', SaveEmailView.as_view()),
    url(r'lostPassword', LostPassword.as_view()),
    url(r'^patient/(?P<patient_id>(\d+))?$', PatientView.as_view()),
    url(r'^updates/?$', UpdatesView.as_view(),  name="updates"),

    # url(r'^patient/?', json_login_required(PatientView.as_view())),
    # url(r'disease', DiseaseView.as_view()),
    # url(r'feedback', FeedbackView.as_view()),
    # url(r'doctor/register/?$', doctor_register),
    # url(r'patient/register/?$', patient_register),
    # url(r'checkotp/?', OTPView.as_view())
)
