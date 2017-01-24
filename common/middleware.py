# - coding: utf-8  -
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class SecureRequiredMiddleware:

    def __init__(self):
        self.enabled = getattr(settings, 'HTTPS_SUPPORT')

    def process_request(self, request):
        # request.META['secure'] = True
        if self.enabled:
            request_url = request.build_absolute_uri(request.get_full_path())
            if request_url.startswith('http://'):
                return HttpResponsePermanentRedirect(request_url.replace('http://', 'https://'))
            else:
                request.META['secure'] = True
        return None
