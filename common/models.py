# - coding: utf-8  -
import os
import re
from django.core import validators
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from common.mail import EmailThread
from utils import random_string
from django.conf import settings
from datetime import date
from indivo_client import IndivoClient, IndivoClientError
import xml.etree.ElementTree as ET
from django_boto.s3.storage import S3Storage
import time


ROLES = {
    'ADMIN': {'id': 1, 'title': 'Admin'},
    'STAFF': {'id': 2, 'title': 'Staff'},
    'DOCTOR': {'id': 3, 'title': 'Doctor'},
    'PATIENT': {'id': 4, 'title': 'Patient'},
}
ROLES_CHOICES = [(r['id'], r['title']) for r in ROLES.values()]


class YubiKey(models.Model):
    uid = models.CharField(max_length=12, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    role = models.IntegerField(choices=ROLES_CHOICES, default=ROLES['PATIENT']['id'])
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='created_key')
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='child_key', blank=True,
                               on_delete=models.SET_NULL)

    def __unicode__(self):
        if self.user:
            return '%s (%s), User: %s' % (self.uid, self.get_role_display(),  self.user.username)
        return '%s (%s)' % (self.uid, self.get_role_display())

s3 = S3Storage()


class UserInfo(models.Model):
    def file_location_cover(self, arg):
        path = "userinfo_cover/%s" % str(time.time())
        ext_regex = re.compile("\.(\w+)$")
        m = ext_regex.search(arg)
        if m:
            path = path + "." + m.group(1).lower()
        return path

    def file_location_photo(self, arg):
        path = "userinfo_photo/%s" % str(time.time())
        ext_regex = re.compile("\.(\w+)$")
        m = ext_regex.search(arg)
        if m:
            path = path + "." + m.group(1).lower()
        return path

    SEX_MALE = 'male'
    SEX_FEMALE = 'female'
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    phone = models.CharField(max_length=100, null=True)
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    sex = models.CharField(max_length=10, default=SEX_MALE)
    birth_date = models.DateField('birth date', default=date(1972, 1, 27))
    cover = models.ImageField(storage=s3, upload_to=file_location_cover, null=True, blank=True)
    photo = models.ImageField(storage=s3, upload_to=file_location_photo, null=True, blank=True)

    def calculateAge(self):
        today = date.today()
        try:
            birthday = date(today.year, self.birth_date.month, self.birth_date.day)
        except ValueError:
            birthday = date(today.year, self.birth_date.month, self.birth_date.day - 1)
        if birthday > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year

    def serialize_as_json(self):
        return {
            'full_name': self.get_full_name(),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'sex': self.sex,
            'age': self.calculateAge(),
        }

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class PatientInfo(UserInfo):
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    indivo_record_id = models.CharField(max_length=50, null=True, blank=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def serialize_as_json(self):
        res = super(PatientInfo, self).serialize_as_json()
        res.update({
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
        })
        return res

    # def serialize_as_json(self):
    #     return super(PatientInfo, self).serialize_as_json()


class DoctorInfo(UserInfo):
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    speciality = models.CharField(max_length=100, null=True)
    clinic = models.CharField(max_length=100, null=True)
    officemng_firstname = models.CharField(max_length=100, null=True)
    officemng_lastname = models.CharField(max_length=100, null=True)
    officemng_email = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100, null=True)


class MailValidationKey(models.Model):
    user = models.OneToOneField('MedintUser')
    key = models.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super(MailValidationKey, self).__init__(*args, **kwargs)
        self.key = random_string(20)


class StaffRole(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class StaffInfo(UserInfo):
    staff_role = models.ForeignKey(StaffRole)


class AdminInfo(UserInfo):
    pass


class MedintUserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_user(self, username, password=None, uid=None, role=None, active=True, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not role:
            raise ValueError('Role is not defined')

        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, role=role, is_staff=False, is_active=active,
                          is_superuser=False, last_login=now, date_joined=now)

        user.set_password(password)
        user.save(using=self._db)

        if YubiKey.objects.all().filter(uid=uid).exists():
            yubikey = YubiKey.objects.get(uid=uid)
            yubikey.role = role

        else:
            yubikey = YubiKey.objects.create(uid=uid, role=role)
        yubikey.user = user
        yubikey.save()
        return user

    def create_superuser(self, username, **extra_fields):
        u = self.create_user(username,  role=ROLES['ADMIN']['id'], **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.user_info = AdminInfo()
        u.save(using=self._db)
        return u

    def send_confirmation_mail(self, user):
        if 'TEST_MODE' in os.environ:
            return
        key = MailValidationKey.objects.create(user=user)
        message = {
            'subject': 'Medical+Intelligence registration confirmation',
            'from_email': 'no_reply@medicalintelligence.com',
            'to': [{'email': user.user_info.email}],
            'global_merge_vars': [
                {'name': 'CURRENT_YEAR', 'content':  timezone.now().year},
                {'name': 'KEY', 'content':  key.key},
                {'name': 'SERVER', 'content':  settings.SITE},
            ]
        }
        EmailThread('confirmation', message).start()

    def create_patient(self, username, **extra_fields):
        print settings.INDIVO_SERVER_PARAMS
        client = IndivoClient(settings.INDIVO_SERVER_PARAMS, settings.INDIVO_CONSUMER_PARAMS,
                              pha_email=settings.INDIVO_USER_EMAIL)
        values = {'email': '', 'last_name': '', 'first_name': '', 'phone': '', 'city': '', 'zipcode': '',
                      'state': '', 'address': ''}
        values.update(extra_fields)
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

        u = self.create_user(username,  role=ROLES['PATIENT']['id'], active=False, **extra_fields)
        doctor = u.yubikey.parent
        u.user_info = PatientInfo.objects.create(
            email=extra_fields['email'],
            first_name=extra_fields['first_name'],
            last_name=extra_fields['last_name'],
            phone=extra_fields['phone'],
            address=extra_fields['address'],
            city=extra_fields['city'],
            state=extra_fields['state'],
            zipcode=extra_fields['zipcode'],
            indivo_record_id=record_id,
            doctor=doctor
        )
        u.save(using=self._db)
        self.send_confirmation_mail(u)


        return u

    def create_doctor(self, username, **extra_fields):
        u = self.create_user(username,  role=ROLES['DOCTOR']['id'], active=False, **extra_fields)
        u.user_info = DoctorInfo.objects.create(
            email=extra_fields['email'],
            first_name=extra_fields['first_name'],
            last_name=extra_fields['last_name'],
            phone=extra_fields['phone'],
            address=extra_fields['address'],
            city=extra_fields['city'],
            state=extra_fields['state'],
            zipcode=extra_fields['zipcode'],
            speciality=extra_fields['speciality'],
            clinic=extra_fields['clinic'],
            officemng_firstname=extra_fields['officemng_firstname'],
            officemng_lastname=extra_fields['officemng_lastname'],
            officemng_email=extra_fields['officemng_email'],
            website=extra_fields['website']
        )
        u.save(using=self._db)
        self.send_confirmation_mail(u)
        return u

    def create_staff(self, username, **extra_fields):
        u = self.create_user(username,  role=ROLES['STAFF']['id'], **extra_fields)
        r = StaffRole.objects.get(id=extra_fields['staff_role'])
        u.user_info = StaffInfo.objects.create(
            email=extra_fields['email'],
            first_name=extra_fields['first_name'],
            last_name=extra_fields['last_name'],
            phone=extra_fields['phone'],
            staff_role=r
        )
        u.save(using=self._db)
        return u


class MedintUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True,
                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                            '@/./+/-/_ characters'),
                validators=[
                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
                ])
    user_info = models.OneToOneField(UserInfo, null=True, on_delete=models.SET_NULL, related_name='user')
    # yubikey = models.ForeignKey(YubiKey, null=True, blank=True, related_name='user')
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    role = models.IntegerField(choices=ROLES_CHOICES)
    USERNAME_FIELD = 'username'
    objects = MedintUserManager()

    def get_full_name(self):
        return self.user_info.get_full_name()

    def get_short_name(self):
        return ''

    def serialize_as_json(self):
        json = {
            'id': self.id,
            'username': self.username,
        }
        try:
            if ROLES['PATIENT']['id'] == self.role:
                userinfo = PatientInfo.objects.get(id=self.user_info.id).serialize_as_json()
            else:
                userinfo = self.user_info.serialize_as_json()
            json.update(userinfo)
        except AttributeError as e:
            print e
        # if 'serialize_as_json' in self.user_info:
        #     json.update(self.user_info.serialize_as_json())
        return json


@receiver(pre_delete, sender=MedintUser, dispatch_uid="delete_user_info")
def delete_user_info(sender, instance, **kwargs):
    instance.user_info.delete()


class SignableDocument(models.Model):
    request_id = models.CharField(max_length=100)
    user = models.ForeignKey(MedintUser)
    template = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='new')

