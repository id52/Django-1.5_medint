import os
import re
import json
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import date
import time
from django_boto.s3.storage import S3Storage
from django_sse.redisqueue import send_event
import redis

from common.models import MedintUser
from django.utils import timezone


class DiscussionMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(default=True)
    join = models.DateTimeField(auto_created=True)

    def serialize_as_json(self):
        u = {'username': self.user.username, 'role': self.user.role}
        if self.user.user_info:
                u['firstName'] = self.user.user_info.first_name
                u['lastName'] = self.user.user_info.last_name
        return u


class Discussion(models.Model):
    subject = models.CharField(max_length=512, blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    starter = models.ForeignKey(DiscussionMember, related_name='user_discussion', null=True)
    participants = models.ManyToManyField(DiscussionMember)


class DiscussionMessage(models.Model):
    MESSAGE = 0
    JOIN = 1
    LEFT = 2
    MESSAGE_TYPE_CHOICES = ((MESSAGE, 'message'), (JOIN, 'join'), (LEFT, 'left'))

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages')
    text = models.TextField(blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)
    discussion = models.ForeignKey(Discussion)
    message_type = models.IntegerField(choices=MESSAGE_TYPE_CHOICES, default=MESSAGE)
    file_message_id = models.CharField(null=True, blank=True, max_length=20)

    class Meta:
        ordering = ["sent"]
    # now = timezone.now()

    def serialize_as_json(self):
        json = {
            'id': self.id,
            'sender': '%s %s' % (self.sender.user_info.first_name, self.sender.user_info.last_name)
            if hasattr(self.sender, 'user_info') else self.sender.username,
            'sender_id': self.sender.id,
            'text': self.text,
            'sent': self.sent.strftime('%d %b %Y %H:%M:%S'),
            #'sent': self.sent.strftime('%d %b %Y-%m-%d %H:%M:%S'),
            'type': self.message_type
        }
        if self.messagefile_set.all():
            files = []
            for f in self.messagefile_set.all():
                if f.file and f.file.name:
                    if re.match('image/*',f.mime_type):
                        isImage=True
                    else:
                        isImage=False
                    files.append({'id': f.id, 'isImage':isImage, 'original_filename':f.original_filename, 'name': f.file.name[f.file.name.index('/', 1)+1:]})
            if files:
                json['files'] = files
        return json


@receiver(post_save, sender=DiscussionMessage, dispatch_uid="send_notification")
def send_notification(instance, created, **kwargs):
    if created:
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        client = redis.from_url(redis_url)
        msg = instance.serialize_as_json()
        discussion = instance.discussion
        msg = {'message': msg, 'discussionId': discussion.id}
        client.publish('user_%s' % discussion.starter.user.id, json.dumps(['message', msg]))
        for m in discussion.participants.all():
            client.publish('user_%s' % m.user.id, json.dumps(['message', msg]))


class DiscussionAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    discussion = models.ForeignKey(Discussion)
    access_time = models.DateTimeField(default=date.fromtimestamp(0))


FOLDER_TYPES = {
    'INBOX': {'id': 1, 'name': 'Inbox'},
    'ARCHIVE': {'id': 2, 'name': 'Archive'},
    'TRASH': {'id': 3, 'name': 'Trash'},
}
FOLDER_CHOICES = [(c['id'], c['name']) for c in FOLDER_TYPES.values()]


class DiscussionFolderManager(models.Manager):
    def get_folder(self, user, folder_type):
        return self.get_or_create(user=user, name=folder_type['name'], type=folder_type['id'])[0]

    def add_discussion(self, user, folder_type, discussion):
        folder = self.get_folder(user, folder_type)
        folder.discussions.add(discussion)
        folder.save()


class DiscussionFolder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=256)
    discussions = models.ManyToManyField(Discussion)
    type = models.IntegerField(choices=FOLDER_CHOICES)

    objects = DiscussionFolderManager()


class ContactItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='in_contacts')

s3 = S3Storage()


class MessageFile(models.Model):

    THUMBNAIL_SIZE = (300, 200)

    def file_location(self, arg):
        path = "discussion_message/%s" % str(time.time())
        ext_regex = re.compile("\.(\w+)$")
        m = ext_regex.search(arg)
        if m:
            path = path + "." + m.group(1).lower()
        return path

    def file_location_thumbnail(self, arg):
        path = "discussion_message_thumbnail/%s" % str(time.time())
        ext_regex = re.compile("\.(\w+)$")
        m = ext_regex.search(arg)
        if m:
            path = path + "." + m.group(1).lower()
        return path

    file = models.FileField(storage=s3, upload_to=file_location, null=True, blank=True)
    message = models.ForeignKey(DiscussionMessage, null=True)
    mime_type = models.CharField(blank=True, null=True, max_length=100)
    original_filename = models.CharField(blank=True, null=True, max_length=255)
    file_message_id = models.CharField(null=True, blank=True, max_length=20)
    upload_time = models.DateTimeField(auto_now_add=True)
    thumbnail = models.FileField(storage=s3, upload_to=file_location_thumbnail, null=True, blank=True)


# class DiscussionAttach(models.Model):
#     def file_location(self, arg):
#         path = "discussion_message/%s" % str(time.time())
#         ext_regex = re.compile("\.(\w+)$")
#         m = ext_regex.search(arg)
#         if m:
#             path = path + "." + m.group(1).lower()
#         return path
#     file = models.FileField(storage=s3, upload_to=file_location, null=True, blank=True)
#     mime_type = models.CharField(blank=True, null=True, max_length=100)