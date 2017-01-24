from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
import os
from django.conf.urls import patterns, include, url
# from medint.views import index, register, logout, lost_password, recover_password, webgl_model, dashboard, body_view, dashboard_mri, dashboard_patient, dashboard_risk, dashboard_risk_red, LoginView, install_chrome, CallbackView, confirm, PatientView, DoctorView

from medint.views import IndexView, LogoutView, ConfirmView, DoctorView, PatientView, RecoverView, PatientInfoView,\
    TimeLineView, uploadPhoto, getPhoto, getCover
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()




static = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static}),

    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^logout$', LogoutView.as_view()),
    url(r'^confirm$', ConfirmView.as_view()),
    url(r'^doctor/?$', DoctorView.as_view(), name='doctor'),
    url(r'^patient/?$', PatientView.as_view(), name='patient'),
    url(r'^recover$', RecoverView.as_view()),
    url(r'^3dmodel', login_required (TemplateView.as_view(template_name="3dmodel.html"))),
    url(r'^bodyview', login_required(TemplateView.as_view(template_name="dashboard_bodyview.html"))),
    url(r'^register/?$', TemplateView.as_view(template_name='success_register.html')),
    url(r'^saved_email/?$', TemplateView.as_view(template_name='saved_email.html')),
    url(r'^patientinfo/(?P<patient_id>(\d+))?$', PatientInfoView.as_view()),
    url(r'^patienttimeline/(?P<patient_id>(\d+))?$', TimeLineView.as_view()),
    url(r'^doctor/uploadPhoto$', uploadPhoto),
    url(r'^doctor/getPhoto$', getPhoto),
    url(r'^doctor/getCover$', getCover),


    # url(r'^register$', register),
    # url(r'^confirm$', confirm),
    # url(r'^lostpassword$', lost_password),
    # url(r'^recover$', recover_password),
    # url(r'^3dmodel', webgl_model),
    # url(r'^bodyview', body_view),
    # url(r'^dashboardmri', dashboard_mri),
    # url(r'^dashboard/?$', dashboard),
    # url(r'^dashboardpatient/?$', dashboard_patient),
    # (r'^dashboardpatientnew/?$', login_required(TemplateView.as_view(template_name="dashboard_patient_new.html"))),
    # url(r'^dashboardriskred', dashboard_risk_red),
    # url(r'^dashboardrisk$', dashboard_risk),
    # url(r'^login/?', LoginView.as_view()),
    # url(r'^installchrome/?', install_chrome),
    # url(r'^callback/signed/?', CallbackView.as_view()),
    # url(r'demo/?$', TemplateView.as_view(template_name="demo.html")),


)

