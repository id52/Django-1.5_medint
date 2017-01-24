# - coding: utf-8  -
import urllib
import simplejson
import os
import urllib2
import base64
from django.conf import settings


def send_document(template_id, email, name, role, fields=None):
    # request = urllib2.Request("http://api.foursquare.com/v1/user")
    base64string = base64.encodestring('%s:%s' %
                                       (settings.HELLOSIGN_USER, settings.HELLOSIGN_PASSWORD)).replace('\n', '')
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain",
               "Authorization": "Basic %s" % base64string}
    # 'signers[Doctor][email_address]'=name@email.com'
    # 'signers[Doctor][name]=DR'
    # 'custom_fields[name]=Dr John Doe'
    data = {
        'signers[%s][email_address]' % role: email,
        'signers[%s][name]' % role: name,
        'title': 'Doctors form',
        'subject': 'Sign the contract',
        'reusable_form_id': template_id,
    }

    if fields:
        for key, value in fields.iteritems():
            data['custom_fields[%s]' % key] = value
    print data

    # request.add_header()
    # result = urllib2.urlopen(request)
    msg_vars = urllib.urlencode(data)
    url = 'https://api.hellosign.com/v3/signature_request/send_with_reusable_form'
    req = urllib2.Request(url, msg_vars, headers)
    try:
        response = urllib2.urlopen(req)
        print response
        r = response.read()
        print r
        return simplejson.loads(r)
    except Exception as e:
        print e
        return {'error': {'error_msg': 'Http error'}}
