# - coding: utf-8  -
from django.core.management import BaseCommand
from common.models import PatientInfo
from django.conf import settings
from datetime import date
from indivo_client import IndivoClient, IndivoClientError
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = IndivoClient(settings.INDIVO_SERVER_PARAMS, settings.INDIVO_CONSUMER_PARAMS,
                              pha_email=settings.INDIVO_USER_EMAIL)
        for i in PatientInfo.objects.filter(indivo_record_id=None):
            u = i.user
            print u
            values = {
                'email': i.email,
                'last_name': i.last_name,
                'first_name': i.first_name,
                'phone': i.phone,
                'city': i.city,
                'zipcode': i.zipcode,
                'state': i.state,
                'address': i.address}
            demographics = ('<Demographics xmlns=\"http://indivo.org/vocab/xml/documents#\">'
                            '<dateOfBirth><![CDATA[1965-06-22]]></dateOfBirth>'
                            '<gender><![CDATA[male]]></gender>'
                            '<email><![CDATA[%(email)s]]></email>'
                            '<preferredLanguage>EN</preferredLanguage>'
                            '<Name>'
                            '<familyName><![CDATA[%(last_name)s]]></familyName>'
                            '<givenName><![CDATA[%(first_name)s]]></givenName>'
                            '</Name>'
                            '<Telephone>'
                            '<type>h</type><number><![CDATA[%(phone)s]]></number><preferred>true</preferred>'
                            '</Telephone>'
                            '<Address>'
                            '<country><![CDATA[USA]]></country>'
                            '<city><![CDATA[%(city)s]]></city>'
                            '<postalCode><![CDATA[%(zipcode)s]]></postalCode>'
                            '<region><![CDATA[%(state)s]]></region>'
                            '<street><![CDATA[%(address)s]]></street>'
                            '</Address>'
                            '</Demographics>') % values
            res, content = client.record_create(body=demographics)
            if 200 != int(res['status']):
                raise Exception('Cannot create record in indivo')
            tree = ET.fromstring(content or '<Record/>')
            if tree is None:
                raise Exception('Cannot create user in indivo')
            record_id = tree.attrib.get('id')
            res, content = client.record_set_owner(record_id=record_id, body=settings.INDIVO_USER_EMAIL)
            if 200 != int(res['status']):
                raise Exception('Cannot change owner in indivo')
            i.indivo_record_id=record_id
            i.save()
