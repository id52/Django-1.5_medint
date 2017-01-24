# # - coding: utf-8  -
from django.conf.urls import patterns, url
from api import preview, save, search, disease, revision, article, ImageView
from wiki.views import index

urlpatterns = patterns(
    '',
    url(r'^$', index, name='home'),
    url(r'^api/preview?$', preview),
    url(r'^api/save?$', save),
    url(r'^api/search?$', search),
    url(r'^api/disease/(?P<id>\d+)$', disease),
    url(r'^api/revision/(?P<id>\d+)$', revision),
    url(r'^api/article/(?P<id>\d+)$', article),
    url(r'^api/image/(?P<id>\d+)?$', ImageView.as_view()),
#	url(r'^login/?', ImageView.as_view()),
)
