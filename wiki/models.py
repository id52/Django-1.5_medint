# # - coding: utf-8  -
import re
from django.db import models
from django.conf import settings
from django_boto.s3.storage import S3Storage
import markdown
import time


s3 = S3Storage()


class RevisionMixin(models.Model):
    active = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(auto_now_add=True)
    previous_revision = models.ForeignKey('self', null=True)

    class Meta:
        abstract = True


class Article(models.Model):
    title = models.CharField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    current_revision = models.ForeignKey('ArticleRevision')

    def to_json(self):
        content = ''
        for f in self.current_revision.fields.all():
            content = '%s\n%s\n%s' % (content, f.field.name, f.content)
        return {
            'id': self.id,
            'title': self.title,
            'data': content.strip(),
            'html': markdown.markdown(content.strip(), ['wikilinks'])}


class ArticleRevision(RevisionMixin, models.Model):
    fields = models.ManyToManyField('FieldContent', related_name='article_revision')
    attachments = models.ManyToManyField('Attachment', related_name='article_revision')

    def to_json(self):
        content = ''
        html = ''
        for f in self.fields.all():
            content = '%s\n# %s\n%s' % (content, f.field.name, f.content)
            html = '%s\n<h2>%s</h2>\n%s' % (html, f.field.name, markdown.markdown(f.content, ['wikilinks']))
        return {'id': self.id, 'html': html, 'content': content}


class Field(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return 'Field: %s (%s)' % (self.name, self.id)


class FieldContent(RevisionMixin, models.Model):
    field = models.ForeignKey(Field)
    content = models.TextField()


class Disease(Article):
    icd9 = models.CharField(max_length=50)
    icd10 = models.CharField(max_length=50)

    def to_json(self):
        content = ''
        html = ''
        for f in self.current_revision.fields.all():
            content = '%s\n# %s\n%s' % (content, f.field.name, f.content)
            html = '%s\n<h2>%s</h2>\n%s' % (html, f.field.name, markdown.markdown(f.content, ['wikilinks']))
        return {
            'id': self.id,
            'title': self.title,
            'icd9': self.icd9,
            'icd10': self.icd10,
            'data': content.strip(),
            'html': html,
            'attachments': [f.to_json() for f in self.current_revision.attachments.all()],
            }


ext_regex = re.compile("\.(\w+)$")


#class AttachmentRevision(RevisionMixin):
#
#    def file_cocation(self, arg):
#        path = "images/%s" % str(time.time())
#        m = ext_regex.search(arg)
#        if m:
#            path = path + "." + m.group(1).lower()
#        return path
#
#    file = models.FileField(storage=s3, upload_to=file_cocation)
#
#
#class ImageAttachmentRevision(AttachmentRevision):
#    license = models.TextField(null=True, blank=True)


class Attachment(RevisionMixin, models.Model):
    def file_location(self, arg):
        path = "images/%s" % str(time.time())
        m = ext_regex.search(arg)
        if m:
            path = path + "." + m.group(1).lower()
        return path
    title = models.CharField(max_length=255, null=True, blank=True)
    license = models.TextField(null=True, blank=True)
    file = models.FileField(storage=s3, upload_to=file_location)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'license': self.license,
            'url': self.file.url
        }
#    current_revision = models.ForeignKey(AttachmentRevision)
