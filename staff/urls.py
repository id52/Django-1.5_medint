from django.conf.urls import patterns, url

from staff.api import RegisterView, KeyView
from staff.views import IndexView, LogoutView, uploadPhoto, getCover, getPhoto

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^logout$', LogoutView.as_view()),

    url('^api/register$', RegisterView.as_view()),
    url('^api/key/(?P<parent>(\d+))?$', KeyView.as_view()),

    url(r'^uploadPhoto$', uploadPhoto),
    url(r'^getPhoto$', getPhoto),
    url(r'^getCover$', getCover),

)