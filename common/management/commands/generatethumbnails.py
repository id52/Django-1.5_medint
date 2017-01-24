# - coding: utf-8  -
from django.core.management import BaseCommand
from messaging.models import MessageFile
import re
import urllib, StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django_boto.s3.storage import S3Storage


class Command(BaseCommand):
    def handle(self, *args, **options):
        messagefiles=MessageFile.objects.all()
        for messagefile in messagefiles:
            if re.match("image/*", messagefile.mime_type.__str__()):
                s3 = S3Storage()
                url = s3.s3.generate_url(60, 'GET', bucket=s3.bucket.name, key='/%s' % messagefile.file.name)
                file = StringIO.StringIO(urllib.urlopen(url).read())
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
                thumb.save(thumb_io, format='JPEG', quality=70)
                thumb_file = InMemoryUploadedFile(thumb_io, None, 'foo.jpg', 'image/jpeg', thumb_io.len, None)
                messagefile.thumbnail = thumb_file
                print messagefile.id, messagefile.file
                messagefile.save()
