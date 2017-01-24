# from datetime import datetime
# import os
#
from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from common.mail import EmailThread
# from django.conf import settings
# from common.hellosign import send_document
# from utils import random_string
# from common.models import UserProfile
#
#
#
from common.models import MedintUser


class RecoverKey(models.Model):
    key = models.CharField(max_length=20)
    user = models.ForeignKey(MedintUser)
    creation_date = models.DateTimeField(auto_now_add=True)
#
#


class RegistryEmail(models.Model):
    email = models.EmailField()
#
#
# class MailValidationKey(models.Model):
#     user = models.OneToOneField(User)
#     key = models.CharField(max_length=20)
#
#     def __init__(self, *args, **kwargs):
#         super(MailValidationKey, self).__init__(*args, **kwargs)
#         self.key = random_string(20)
#
#
# class SignableDocument(models.Model):
#     request_id = models.CharField(max_length=100)
#     user = models.ForeignKey(User)
#     template = models.CharField(max_length=100)
#     status = models.CharField(max_length=100, default='new')
#
#
# @receiver(post_save, sender=User, dispatch_uid="send_mail")
# def create_user_profile(instance, created, **kwargs):
#     if 'TEST_MODE' in os.environ:
#         return
#     if created:
#         UserProfile.objects.create(user=instance)
#         key = MailValidationKey.objects.create(user=instance)
#         message = {
#             'subject': 'Medical+Intelligence registration confirmation',
#             'from_email': 'no_reply@medicalintelligence.com',
#             'to': [{'email': instance.email}],
#             'global_merge_vars': [
#                 {'name': 'CURRENT_YEAR', 'content':  datetime.now().year},
#                 {'name': 'KEY', 'content':  key.key},
#                 {'name': 'SERVER', 'content':  settings.SITE},
#             ]
#         }
#         EmailThread('confirmation', message).start()
#
#
# class MailTemplate(models.Model):
#     name = models.CharField(max_length=255)
#     subject = models.CharField(max_length=255)
#     mail_text = models.TextField()
#     creation_date = models.DateTimeField(auto_now_add=True)
#
#
# class Disease(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     link = models.CharField(max_length=255)
#     icd9 = models.CharField(max_length=255)
#     icd10 = models.CharField(max_length=255, null=True)
#
#     def to_json(self):
#         return {
#             'name': self.name,
#             'description': self.description,
#             'link': self.link,
#             'icd9': self.icd9,
#             'icd10': self.icd10,
#         }