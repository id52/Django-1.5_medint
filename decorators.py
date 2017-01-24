# - coding: utf-8  -
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from common.models import ROLES


def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


ROLES_BACK = {v['id']: k for k, v in ROLES.iteritems()}


def roles_required(roles):
    def wrapper(f):
        def wrapper1(func, request, *args, **kw):
            roles_ids = [ROLES[r]['id'] for r in roles]
            if request.user.role in roles_ids:
                return f(func, request, *args, **kw)
            else:
                raise PermissionDenied

        return wrapper1
    return wrapper


# def roles_required(roles):
#     roles_ids = [ROLES[r]['id'] for r in roles]
#
#     def f(view_func):
#         def _wrapped_view_func(clazz, request, *args, **kwargs):
#             if request.user.get_profile().role in roles_ids:
#                 print 'ALLOW'
#             else:
#                 print 'DENY'
#             return view_func(request, *args, **kwargs)
#         return _wrapped_view_func
#     return f
