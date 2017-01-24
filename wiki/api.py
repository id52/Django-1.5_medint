# - coding: utf-8  -
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django_boto.s3 import upload
import re
from xml.dom.minidom import parseString
from django.http import HttpResponse
import html2text
import markdown
import urllib2
from jsonview import make_response
from models import Field, Disease, ArticleRevision, FieldContent, Attachment
from django.conf import settings

DATE_FORMAT = '%m/%d/%Y %H:%M'


def preview(request):
    m = markdown.Markdown(extensions=['extra', 'wikilinks'])
    return HttpResponse(m.convert(request.POST['data']))


def search(request):
    q = request.GET['q']
    res = [{'id': d.id, 'title': d.title} for d in Disease.objects.filter(icd9__icontains=q)[:10]]
    if not res:
        u = 'http://apps.nlm.nih.gov/medlineplus/services/mpconnect_service.cfm?mainSearchCriteria.v.c=%s' % q
        print u
        f = urllib2.urlopen(u)
        xml = '\n'.join(f)
        d = parseString(xml)
        e = d.getElementsByTagName('entry')

        if e:
            t = e[0].getElementsByTagName('title')[0].childNodes[0].data
            s = e[0].getElementsByTagName('summary')[0].childNodes[0].data
            s = html2text.html2text(s)

            disease = Disease()
            rev = ArticleRevision.objects.create(author=request.user)
            disease.icd9 = q
            disease.icd10 = ''
            disease.title = t
            field, created = Field.objects.get_or_create(name__iexact='', defaults={'name': ''})
            content = FieldContent.objects.create(
                content=s,
                field=field,
                author=request.user,
                active=True,
                previous_revision=None,
            )
            rev.fields.add(content)
            rev.save()
            disease.current_revision = rev
            disease.save()
            #            l = d.getElementsByTagName('link')[0].getAttribute('href') if d.getElementsByTagName('link') else ''
            print t
            print s
            res = [{'id': disease.id, 'title': disease.title}]
    return make_response(res)


def disease(request, id=None):
    disease = Disease.objects.get(id=int(id))
    r = disease.current_revision
    revisions = [{'id': r.id, 'author': r.author.username, 'date': r.date.strftime(DATE_FORMAT)}]
    while r.previous_revision is not None:
        r = r.previous_revision
        revisions.append({'id': r.id, 'author': r.author.username, 'date': r.date.strftime(DATE_FORMAT)})
    res = disease.to_json()
    res['revisions'] = revisions
    print revisions
    return make_response(res)


def revision(request, id):
    rev = ArticleRevision.objects.get(id=int(id))
    return make_response(rev.to_json())


def article(request, id):
    revision_id = int(request.POST['revision_id'])
    disease = Disease.objects.get(id=int(id))
    r = disease.current_revision
    while r and revision_id != r.id:
        r = r.previous_revision
    if not r:
        return make_response(error='Invalid revision')
    disease.current_revision = ArticleRevision.objects.get(id=revision_id)
    disease.save()
    r = disease.current_revision
    revisions = [{'id': r.id, 'author': r.author.username, 'date': r.date.strftime(DATE_FORMAT)}]
    while r.previous_revision is not None:
        r = r.previous_revision
        revisions.append({'id': r.id, 'author': r.author.username, 'date': r.date.strftime(DATE_FORMAT)})
    res = disease.to_json()
    res['revisions'] = revisions

    return make_response(res)


def save(request):
    a = request.POST['data'].strip()
    id = request.POST['id'] if 'id' in request.POST else None
    disease = Disease.objects.get(id=int(id)) if id else Disease()
    previous_revision = disease.current_revision if hasattr(disease, 'current_revision') else None
    rev = ArticleRevision.objects.create(author=request.user, previous_revision=previous_revision)
    disease.icd9 = request.POST['icd9']
    disease.icd10 = request.POST['icd10']
    disease.title = request.POST['name']
    headers = re.findall('#.*\n', a)
    headers.insert(0, '')
    attachments = previous_revision.attachments.all() if previous_revision else []

    def create_field(field, content, prev=None):
        return FieldContent.objects.create(
            content=content,
            field=field,
            author=request.user,
            active=True,
            previous_revision=prev,
        )

    for (i, r) in enumerate(re.split('#.*\n', a)):
        if 0 == i and 0 == len(r.strip()):
            continue
        name = headers[i][1:].strip() if i < len(headers) else ''
        field, created = Field.objects.get_or_create(name__iexact=name, defaults={'name': name})
        f = FieldContent.objects.filter(field=field).filter(article_revision=previous_revision)
        if not f:
            rev.fields.add(create_field(field, r.strip()))
        elif f[0].content == r.strip():
            rev.fields.add(f[0])
        else:
            f.active = False
            f[0].save()
            rev.fields.add(create_field(field, r.strip(), f[0]))
    rev.attachments = attachments
    rev.save()

    disease.current_revision = rev
    disease.save()
    r = disease.current_revision
    revisions = [{'id': r.id, 'author': r.author.username, 'date': r.date.strftime(DATE_FORMAT)}]
    while r.previous_revision is not None:
        r = r.previous_revision
        revisions.append({'id': r.id, 'author': r.author.username, 'date': r.date.strftime(DATE_FORMAT)})
    res = disease.to_json()
    res['revisions'] = revisions

    return make_response(res)


class UploadFileForm(forms.Form):
    articleid = forms.IntegerField()
    title = forms.CharField(max_length=50, required=False)
    file = forms.FileField()
    license = forms.CharField(required=False, widget=forms.Textarea)


def handle_uploaded_file(f):
    upload(f, prefix=False, bucket_name=False, key=None, secret=None)
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class ImageView(View):
    def post(self, request, id=None):
        if request.FILES and request.FILES['file']:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    revision = ArticleRevision.objects.get(article=form.cleaned_data['articleid'])
                except ObjectDoesNotExist as e:
                    return make_response(error='Invalid article id')
                except:
                    return make_response(error='Internal error')
                else:

                    revision.attachments.add(Attachment.objects.create(
                        file=form.cleaned_data['file'],
                        author=request.user,
                        title=form.cleaned_data['title'],
                        license=form.cleaned_data['license']))
                    revision.save()
                    return make_response()
            else:
                return make_response(validation=form._errors)
        else:
            return make_response(error='No files selected')

    def get(self, request, id=None):
        res = [a.to_json() for a in ArticleRevision.objects.get(article=int(id)).attachments.all()]
        return make_response(res)

    def delete(self, request, id=None):
        Attachment.objects.get(id=int(id)).delete()
        return make_response()
