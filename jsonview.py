# - coding: utf-8  -
from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import available_attrs
from django.views.generic import View
import simplejson



def load_put_and_files(request):
    """
    Populates request.PUT and request.FILES from
    request.raw_post_data. PUT and POST requests differ
    only in REQUEST_METHOD, not in the way data is encoded.
    Therefore we can use Django's POST data retrieval method
    for PUT.
    """
    request.method = 'POST'
    request._load_post_and_files()
    request.method = 'PUT'
    request.PUT = request.POST
    del request._post


def json_login_required(f, *args, **kw):
    def wrapper(self, request, *args, **kw):
        u = request.user
        if u and u.is_authenticated():
            return f(self, request, *args, **kw)
        else:
            return make_response(error='User is not authenticated')
    return wrapper


class JSONView(View):
    def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(), None)
        if not handler:
            return make_response(error='Method is not allowed')
        if 'PUT' == request.method.upper():
            load_put_and_files(request)

        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)


def make_response(json=None, error=None, validation=None):
    if validation:
        fields = {}
        for n in validation:
            l = []
            for i in validation[n]:
                l.append(i)
            fields[n] = l
        return HttpResponse(simplejson.dumps({'result': 'validation', 'fields': fields}), mimetype='text/json',
                            status=200)
    if error:
        return HttpResponse(simplejson.dumps({'result': 'error', 'description': error}), mimetype='text/json',
                            status=200)
    if json:
        return HttpResponse(simplejson.dumps({'result': 'ok', 'data': json}), mimetype='text/json', status=200)
    else:
        return HttpResponse(simplejson.dumps({'result': 'ok'}), mimetype='text/json', status=200)
