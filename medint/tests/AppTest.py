import os
from django.contrib.auth.models import User
from django.test import Client
import unittest


class AppTestCase(unittest.TestCase):

    def __fix_active__(self, email):
        User.objects.filter(email__iexact=email).update(is_active=True)

    def setUp(self):
        self.c = Client()

    def runTest(self):
        os.environ['TEST_MODE'] = 'ON'
        response = self.c.get('/', **{'wsgi.url_scheme': 'https'})
        self.assertEqual(200, response.status_code)
        # response = self.c.post('/api/doctor/register', {
        #     'firstname': 'Abay',
        #     'lastname': 'Kunanbaeff',
        #     'email': 'abay@mailinator.com',
        #     'phone': '123456',
        #     'username': 'abay',
        #     'address': 'Abay ave 1',
        #     'city': 'Teguldet',
        #     'state': 'TE',
        #     'zipcode': '123456',
        #     'speciality': 'House M. D.',
        #     'clinic': 'Place',
        #     'officemng_firstname': '??',
        #     'officemng_lastname': '??',
        #     'officemng_email': '??',
        #     'website': '??',
        #
        # }, **{'wsgi.url_scheme': 'https'})
        # self.assertEqual(200, response.status_code)
        # self.__fix_active__('pofig@mailinator.com')
        # response = self.c.post('/api/login', {
        #     'password': 'pofig',
        #     'email': 'pofig@mailinator.com',
        # }, **{'wsgi.url_scheme': 'https'})
        # self.assertEqual(200, response.status_code)
        # response = self.c.get('/', **{'wsgi.url_scheme': 'https'})
        # self.assertEqual(200, response.status_code)
        # response = self.c.get('/dashboard/', **{'wsgi.url_scheme': 'https'})
        # self.assertEqual(200, response.status_code)
