 # # - coding: utf-8  -
import json
import logging
from django.conf.urls import patterns
from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.db.models import Q, Max, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone, simplejson
from django.utils.decorators import method_decorator
import time
from django_boto.s3.storage import S3Storage
from common.models import MedintUser, UserInfo, ROLES
from jsonview import make_response, JSONView, json_login_required
from messaging.models import Discussion, DiscussionMessage, DiscussionAccess, DiscussionFolder, FOLDER_TYPES, DiscussionMember, MessageFile
from django.conf import settings
from common.mail import EmailThread
import datetime
import re
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image



# class InboxView(JSONView):
#     def get(self, request):
#         messages = [
#             {'id':m.id, 'subject': m.subject, 'sender': m.sender.username, 'recipient': m.recipient.username,
#              'subject': m.subject, 'date': m.send_at.strftime('%m/%d/%y %H:%M')}
#             for m in Message.objects.filter(recipient=request.user)]
#         return make_response(messages)
#
#
# class SentView(JSONView):
#     def get(self, request):
#         messages = [
#             {'id':m.id, 'subject': m.subject, 'sender': m.sender.username, 'recipient': m.recipient.username,
#              'subject': m.subject, 'date': m.send_at.strftime('%m/%d/%y %H:%M')}
#             for m in Message.objects.filter(sender=request.user)]
#         return make_response(messages)
#
#
# class TrashView(JSONView):
#     def get(self, request):
#         messages = [
#             {'id':m.id, 'subject': m.subject, 'sender': m.sender.username, 'recipient': m.recipient.username,
#              'subject': m.subject, 'date': m.send_at.strftime('%m/%d/%y %H:%M')}
#             for m in Message.objects.filter(
#                 (Q(recipient=request.user) & Q(deleted_by_recipient=True)) |
#                 (Q(sender=request.user) & Q(deleted_by_sender=True)))
#         ]
#         return make_response(messages)
#
#
# class MessageView(JSONView):
#     def get(self, request, message_id):
#         try:
#             m = Message.objects.get(id=int(message_id))
#         except Message.DoesNotExist:
#             return make_response(error='Invalid message id')
#         else:
#             return make_response(m.serialize_as_json())
#
#     def delete(self, request, message_id):
#         try:
#             msg = Message.objects.get(id=int(message_id))
#             if msg.recipient == request.user:
#                 msg.deleted_by_recipient = True
#             elif msg.sender == request.user:
#                 msg.deleted_by_sender = True
#             else:
#                 return make_response(error='Message not found')
#         except Message.DoesNotExist:
#             return make_response(error='Message not found')
#         msg.save()
#         return make_response()
#
#
# class MessageForm(forms.Form):
#     subject = forms.CharField(required=False)
#     to = forms.CharField(required=True)
#     text = forms.CharField(required=False)
#
#
# class WriteView(JSONView):
#     def post(self, request):
#         f = MessageForm(request.POST)
#         if not f.is_valid():
#             return make_response(validation=f._errors)
#         try:
#             recipient = MedintUser.objects.get(username__iexact=f.cleaned_data['to'].strip())
#         except MedintUser.DoesNotExist:
#             return make_response(validation={'to': ['Invalid user']})
#         else:
#             Message.objects.create(
#                 sender=request.user,
#                 recipient=recipient,
#                 subject=f.cleaned_data['subject'],
#                 text=f.cleaned_data['text']
#             )
#         return make_response()


class MessageForm(forms.Form):
    text = forms.CharField(required=False)
    filename = forms.FileField(required=False)


class NewDiscussuinForm(MessageForm):
    # to = forms.CharField()
    subject = forms.CharField()


class DiscussionView(JSONView):
    def __create_discussion__(self, request):
        form = NewDiscussuinForm(request.POST)
        if form.is_valid():
            starter = DiscussionMember.objects.create(user=request.user, join=timezone.now())
            discussion = Discussion.objects.create(subject=form.cleaned_data['subject'], starter=starter)


            DiscussionAccess.objects.create(discussion=discussion, user=request.user, access_time=timezone.now())
            DiscussionFolder.objects.add_discussion(request.user, FOLDER_TYPES['INBOX'], discussion)
            for u in request.POST.getlist('members[]'):
                user = MedintUser.objects.get(username__iexact=u)
                DiscussionFolder.objects.add_discussion(user, FOLDER_TYPES['INBOX'], discussion)
                discussion.participants.add(DiscussionMember.objects.create(user=user, join=timezone.now()))

            return discussion

    def __create_message__(self, user, discussion, text='', filenames=None, file_message_id=None, message_type=DiscussionMessage.MESSAGE):
        msg = DiscussionMessage.objects.create(
            sender=user,
            text=text,
            sent=timezone.now(),
            discussion=discussion,
            message_type=message_type
        )
        if file_message_id:
            MessageFile.objects.filter(file_message_id=file_message_id).update(message=msg)
        # if filenames and file_message_id:
        #     for f in filenames:
        #         file = MessageFile.objects.get_or_create(file_message_id=file_message_id, original_filename=f)[0]
        #         file.message = msg
        #         f.save()
        return msg

    @json_login_required
    def get(self, request, discussion_id=None):

        if discussion_id:
            discussion_id = int(discussion_id)
            d = Discussion.objects.get(id=discussion_id)

            da = DiscussionAccess.objects.get_or_create(discussion=d, user=request.user)[0]
            da.access_time = timezone.now()
            da.save()

            t = ""
            last_messages = DiscussionMessage.objects.filter(discussion=d).order_by('-sent')[:1]
            for last_message in last_messages:
                diff = datetime.datetime.now()-last_message.sent
                if diff.days >= 1:
                    timeago = False
                else:
                    timeago = True

                t = last_message.sent.__str__()
                last_msg_time = t[:19]
                last_msg_date = t[:10]

            members = [m.serialize_as_json() for m in d.participants.filter(is_active=True)]

            messages = [m.serialize_as_json() for m in DiscussionMessage.objects.filter(discussion=d)]
            for m in messages:
                m['editable'] = m['sender_id'] == request.user.id

            return make_response({'id': d.id, 'subject': d.subject, 'starter': d.starter.serialize_as_json(),
                                  'members': members, 'messages': messages, 'last_msg_time': last_msg_time,
                                  'last_msg_date': last_msg_date, 'timeago':timeago})

        f = request.GET.get('folder', 'unknown').lower()
        if 'inbox' == f:
            folder, created = DiscussionFolder.objects.get_or_create(user=request.user,
                                                                     name=FOLDER_TYPES['INBOX']['name'],
                                                                     type=FOLDER_TYPES['INBOX']['id'])

            answer = []
            discussions = folder.discussions.all().annotate(
                last_msg_time=Max('discussionmessage__sent')).order_by('-last_msg_time')
            t=""
            for d in discussions:

                diff=datetime.datetime.now()-d.last_msg_time
                if diff.days >= 1:
                    timeago = False
                else:
                    timeago = True

                t=d.last_msg_time.__str__()
                d.last_msg_time=t[:19]
                d.last_msg_date=t[:10]
                ans = {'timeago':timeago, 'last_msg_date':d.last_msg_date, 'last_msg_time': d.last_msg_time, 'id': d.id,
                       'subject': d.subject, 'count': 0,  'starter': d.starter.serialize_as_json()}
                answer.append(ans)

            return make_response(answer)
            #return make_response([{'id': d.id, 'subject': d.subject, 'count': 0, 'starter': d.starter.serialize_as_json(),}
            #    for d in folder.discussions.all().annotate(s=Max('discussionmessage__sent')).order_by('-s')])

        if 'archive' == f:
            folder, created = DiscussionFolder.objects.get_or_create(user=request.user,
                                                                     name=FOLDER_TYPES['ARCHIVE']['name'],
                                                                     type=FOLDER_TYPES['ARCHIVE']['id'])
            return make_response([
                {'id': d.id, 'subject': d.subject, 'count': 0, 'starter': d.starter.serialize_as_json()}
                for d in folder.discussions.all().annotate(s=Max('discussionmessage__sent')).order_by('-s')])
        if 'trash' == f:
            folder, created = DiscussionFolder.objects.get_or_create(user=request.user,
                                                                     name=FOLDER_TYPES['TRASH']['name'],
                                                                     type=FOLDER_TYPES['TRASH']['id'])
            return make_response([{'id': d.id, 'subject': d.subject, 'count': 0, 'starter': d.starter.serialize_as_json()}
                          for d in folder.discussions.all().annotate(s=Max('discussionmessage__sent')).order_by('-s')])
        return make_response([])

    @json_login_required
    def post(self, request, discussion_id=None):
        if not discussion_id:
            discussion = self.__create_discussion__(request)
        else:
            try:
                discussion = Discussion.objects.get(id=discussion_id)
            except Discussion.DoesNotExist:
                return make_response(error='Invalid discussion')
        f = MessageForm(request.POST)
        if f.is_valid():
            message = self.__create_message__(request.user, discussion, request.POST.get('text', '').strip(),
                                              file_message_id=request.POST.get('filemessageid', None))

            #email notifications
            subject = 'Medical+Intelligence. You have a new message in a discussion \"' + discussion.subject + '\".'
            text = f.cleaned_data['text']
            sender = request.user

            if sender != discussion.starter.user:
                msg = {
                        'subject': subject,
                        'from_email': 'no_reply@medicalintelligence.com',
                        'to': [{'email': discussion.starter.user.user_info.email}],
                        'global_merge_vars': [
                            {'name': 'SENDER', 'content': sender.__str__()},
                            {'name': 'DISCUSSION', 'content':  discussion.subject},
                            {'name': 'MESSAGE', 'content':  text},
                        ]
                }
                EmailThread('newMessage', msg).start()

            for member in discussion.participants.filter(is_active=True):
                if sender != member.user:
                    msg = {
                        'subject': subject,
                        'from_email':'no_reply@medicalintelligence.com',
                        'to': [{'email': member.user.user_info.email}],
                        'global_merge_vars': [
                            {'name': 'SENDER', 'content': sender.__str__()},
                            {'name': 'DISCUSSION', 'content':  discussion.subject},
                            {'name': 'MESSAGE', 'content':  text},
                        ]
                    }
                    EmailThread('newMessage', msg).start()

            for f in discussion.discussionfolder_set.filter(
                    ~Q(type=FOLDER_TYPES['INBOX']['id']), ~Q(type=FOLDER_TYPES['TRASH']['id'])):
                f.discussions.remove(discussion)
                DiscussionFolder.objects.add_discussion(f.user, FOLDER_TYPES['INBOX'], discussion)

            return make_response({'messageId': message.id})

    @json_login_required
    def put(self, request, discussion_id=None):
        f = request.PUT.get('folder', None)

        if not f:
            return make_response(error='Folder is not specified')
        d = Discussion.objects.get(id=discussion_id)
        exist_folder_type = None
        try:
            folder = DiscussionFolder.objects.get(Q(discussions=d), Q(user=request.user))
            folder.discussions.remove(d)
            exist_folder_type = folder.type
        except DiscussionFolder.DoesNotExist:
            pass
        if 'archive' == f.lower():
            DiscussionFolder.objects.add_discussion(request.user, FOLDER_TYPES['ARCHIVE'], d)
            d.participants.filter(user=request.user).update(is_active=True)
        if 'trash' == f.lower():
            d.participants.filter(user=request.user).update(is_active=False)

            if FOLDER_TYPES['TRASH']['id'] != exist_folder_type:
                self.__create_message__(request.user, d, 'has left discussion', message_type=DiscussionMessage.LEFT)
                DiscussionFolder.objects.add_discussion(request.user, FOLDER_TYPES['TRASH'], d)

        if 'inbox' == f.lower():
            d.participants.filter(user=request.user).update(is_active=True)
            DiscussionFolder.objects.add_discussion(request.user, FOLDER_TYPES['INBOX'], d)
            if FOLDER_TYPES['TRASH']['id'] == exist_folder_type:
                self.__create_message__(request.user, d, 'has joined discussion', message_type=DiscussionMessage.JOIN)
        return make_response()


class MessageView(JSONView):
    @json_login_required
    def get(self, request, message_id=None):
        m = DiscussionMessage.objects.get(id=message_id).serialize_as_json()
        m['editable'] = m['sender_id'] == request.user.id
        return make_response(m)

    @json_login_required
    def put(self, request, message_id=None):
        try:
            message = DiscussionMessage.objects.get(id=message_id)
        except DiscussionMessage.DoesNotExist:
            return make_response(error='Invalid Discussion Message')
        else:
            if request.PUT.get('text'):
                message.text = request.PUT.get('text')
                message.save()

            return make_response()

    @json_login_required
    def delete(self, request, message_id=None):
        try:
            message=DiscussionMessage.objects.get(id=message_id)
            if message.sender==request.user:
                message.delete()
            return make_response()
        except DiscussionMessage.DoesNotExist:
            return make_response(error='Invalid discussion message')


class DiscussionMembersView(JSONView):
    @json_login_required
    def post(self, request, discussion_id):
        try:
            discussion = Discussion.objects.get(id=discussion_id)
        except Discussion.DoesNotExist:
            return make_response(error='Invalid discussion')
        u = MedintUser.objects.get(username__iexact=request.POST.get('username'))
        discussion.participants.add(DiscussionMember.objects.create(user=u, join=timezone.now()))
        DiscussionFolder.objects.add_discussion(u, FOLDER_TYPES['INBOX'], discussion)
        DiscussionMessage.objects.create(
            sender=u,
            text='has joined discussion',
            sent=timezone.now(),
            discussion=discussion,
            message_type=DiscussionMessage.JOIN)
        return make_response()


class CountView(JSONView):
    @json_login_required
    def get(self, request):
        res = []
        for f in DiscussionFolder.objects.filter(Q(user=request.user) & ~Q(type=FOLDER_TYPES['TRASH']['id'])):
            for d in f.discussions.all():  #TODO rewite it with raw sql!
                da, created = DiscussionAccess.objects.get_or_create(user=request.user, discussion=d)
                c = d.discussionmessage_set.filter(sent__gt=da.access_time).aggregate(count=Count('sent'))
                c['max_date'] = d.discussionmessage_set.aggregate(max_date=Max('sent'))['max_date']
                diff=datetime.datetime.now()-c['max_date']
                if diff.days>=1:
                    timeago=False
                else:
                    timeago=True

                t = c['max_date']
                t = t.__str__()

                last_msg_time= t[:19]
                last_msg_date= t[:10]

                res.append({'discussion': d.id, 'count': c['count'], 'lastMessage': int(time.mktime(c['max_date'].timetuple())),
                            'folder': f.name.lower(), 'last_msg_time':last_msg_time, 'last_msg_date':last_msg_date, 'timeago':timeago})
        return make_response(res)


class ContactView(JSONView):
    @json_login_required
    def get(self, request):
        res = []
        for user in MedintUser.objects.filter(Q(role=ROLES['DOCTOR']['id']) | Q(role=ROLES['STAFF']['id'])):
            u = {'username': user.username, 'role': user.role}
            if user.user_info:
                u['firstName'] = user.user_info.first_name
                u['lastName'] = user.user_info.last_name
            res.append(u)
        return make_response(res)

    def post(self, request):
        return make_response()


class FileView(JSONView):
    def get(self, request, file_id):
        f = MessageFile.objects.get(id=file_id)
        s3 = S3Storage()
        return HttpResponseRedirect(s3.s3.generate_url(60, 'GET', bucket=s3.bucket.name, key='/%s' % f.file.name))

    @json_login_required
    def post(self, request, file_id=None):
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        logging.info('Got file: "'+str(filename)+'"')
        f = MessageFile.objects.create(file=file)
        result = []
        result.append({"name": filename,
                       "size": file_size,
                       "url":  '/api/messaging/file/%s' % f.id,
                       "thumbnail_url": '/api/messaging/file/%s' % f.id,
                       "delete_url": '/api/messaging/file/%s' % f.id,
                       "delete_type": "DELETE",})
        response_data = json.dumps(result)
        return HttpResponse(response_data, mimetype='application/json')


class FileViewThumbnail(JSONView):
    def get(self, request, file_id):
        f = MessageFile.objects.get(id=file_id)
        s3 = S3Storage()
        return HttpResponseRedirect(s3.s3.generate_url(60, 'GET', bucket=s3.bucket.name, key='/%s' % f.thumbnail.name))


class AttachForm(forms.Form):
    text = forms.CharField()
    filename = forms.FileField(required=False)


class AttachView(JSONView):
    def post(self, request):
        files = request.FILES.getlist(u'file')
        result = []

        msg = None
        file_message_id = request.POST['filemessageid']
        try:
            msg = DiscussionMessage.objects.get(file_message_id=file_message_id)
        except DiscussionMessage.DoesNotExist:
            pass

        for file in files:
            wrapped_file = UploadedFile(file)
            filename = wrapped_file.name
            file_size = wrapped_file.file.size

            f = MessageFile.objects.get_or_create(message=msg, original_filename=filename,
                                                  file_message_id=file_message_id)[0]
            f.file = file
            f.mime_type = file.content_type

            if re.match('image/*',f.mime_type):
                img = Image.open(file)
                if img.mode not in ('L', 'RGB'):
                    img = img.convert('RGB')
                w = MessageFile.THUMBNAIL_SIZE[0]
                h = MessageFile.THUMBNAIL_SIZE[1]
                if img.size[0] > img.size[1]:
                    h = img.size[1]*w/img.size[0].__float__()
                else:
                    w = img.size[0]*h/img.size[1].__float__()
                thumb = img.resize((w.__int__(), h.__int__()), Image.ANTIALIAS)
                thumb_io = StringIO.StringIO()
                thumb.save(thumb_io, format='JPEG', quality=90)
                thumb_file = InMemoryUploadedFile(thumb_io, None, 'foo.jpg', 'image/jpeg', thumb_io.len, None)
                f.thumbnail = thumb_file

            f.save()

            result.append({"name": filename,
                           "size": file_size,
                           "url":  '/api/messaging/file/%s' % f.id,
                           "thumbnail_url": '/api/messaging/file/%s' % f.id,
                           "delete_url": '/api/messaging/file/%s' % f.id,
                           "delete_type": "DELETE"})
            # result = {"name": filename,
            #                "size": file_size,
            #                "url":  '/api/messaging/file/%s' % f.id,
            #                "thumbnail_url": '/api/messaging/file/%s' % f.id,
            #                "delete_url": '/api/messaging/file/%s' % f.id,
            #                "delete_type": "DELETE"}
        response_data = json.dumps({'files': result})
        return HttpResponse(response_data, mimetype='application/json')


urlpatterns = patterns(
    '',
    (r'^discussion/(?P<discussion_id>(\d+))?$', DiscussionView.as_view()),
    (r'^message/(?P<message_id>(\d+))/?$', MessageView.as_view()),
    (r'^discussion/(?P<discussion_id>(\d+))/members$', DiscussionMembersView.as_view()),
    (r'^count/?', CountView.as_view()),
    (r'^contact/?', ContactView.as_view()),
    (r'^file/(?P<file_id>(\d+))', FileView.as_view()),
    (r'^file/thumbnail/(?P<file_id>(\d+))', FileViewThumbnail.as_view()),
    (r'^attach/?$', AttachView.as_view()),
    # (r'^inbox/?$', InboxView.as_view()),
    # (r'^sent/?$', SentView.as_view()),
    # (r'^trash/?$', TrashView.as_view()),
    # (r'^write/?$', WriteView.as_view()),
    # (r'^message/(?P<message_id>(\d+))$', MessageView.as_view()),
)