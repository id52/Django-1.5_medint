import os
from django.conf.urls import patterns, include, url
from medint import urls as medint

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from common import api as common_api
from messaging import api as messaging_api
from medint import api as medint_api
from wiki import urls as wiki
from staff import urls as staff

from common.forms import YubikeyAuthenticationForm
admin.site.login_form = YubikeyAuthenticationForm
admin.site.login_template = 'yubi_admin_login.html'


admin.autodiscover()

#static = os.path.join(os.path.dirname(__file__), 'old')

#STATICFILES_DIRS = (
#    static,
#)

static = os.path.join(os.path.dirname(__file__), 'static')

urlpatterns = patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': static}),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wiki/', include(wiki)),
    url(r'^staff/', include(staff)),
    # url(r'^postman/', include(postman)),

    (r'^api/messaging/*', include(messaging_api)),
    (r'^api/medint/*', include(medint_api)),
    (r'^api/*', include(common_api)),

    (r'/*', include(medint)),
)

