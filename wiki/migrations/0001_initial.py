# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table(u'wiki_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('current_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.ArticleRevision'])),
        ))
        db.send_create_signal(u'wiki', ['Article'])

        # Adding model 'ArticleRevision'
        db.create_table(u'wiki_articlerevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MedintUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.ArticleRevision'], null=True)),
        ))
        db.send_create_signal(u'wiki', ['ArticleRevision'])

        # Adding M2M table for field fields on 'ArticleRevision'
        db.create_table(u'wiki_articlerevision_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('articlerevision', models.ForeignKey(orm[u'wiki.articlerevision'], null=False)),
            ('fieldcontent', models.ForeignKey(orm[u'wiki.fieldcontent'], null=False))
        ))
        db.create_unique(u'wiki_articlerevision_fields', ['articlerevision_id', 'fieldcontent_id'])

        # Adding M2M table for field attachments on 'ArticleRevision'
        db.create_table(u'wiki_articlerevision_attachments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('articlerevision', models.ForeignKey(orm[u'wiki.articlerevision'], null=False)),
            ('attachment', models.ForeignKey(orm[u'wiki.attachment'], null=False))
        ))
        db.create_unique(u'wiki_articlerevision_attachments', ['articlerevision_id', 'attachment_id'])

        # Adding model 'Field'
        db.create_table(u'wiki_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'wiki', ['Field'])

        # Adding model 'FieldContent'
        db.create_table(u'wiki_fieldcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MedintUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.FieldContent'], null=True)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Field'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'wiki', ['FieldContent'])

        # Adding model 'Disease'
        db.create_table(u'wiki_disease', (
            (u'article_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wiki.Article'], unique=True, primary_key=True)),
            ('icd9', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('icd10', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'wiki', ['Disease'])

        # Adding model 'Attachment'
        db.create_table(u'wiki_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MedintUser'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('previous_revision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Attachment'], null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wiki', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table(u'wiki_article')

        # Deleting model 'ArticleRevision'
        db.delete_table(u'wiki_articlerevision')

        # Removing M2M table for field fields on 'ArticleRevision'
        db.delete_table('wiki_articlerevision_fields')

        # Removing M2M table for field attachments on 'ArticleRevision'
        db.delete_table('wiki_articlerevision_attachments')

        # Deleting model 'Field'
        db.delete_table(u'wiki_field')

        # Deleting model 'FieldContent'
        db.delete_table(u'wiki_fieldcontent')

        # Deleting model 'Disease'
        db.delete_table(u'wiki_disease')

        # Deleting model 'Attachment'
        db.delete_table(u'wiki_attachment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'common.medintuser': {
            'Meta': {'object_name': 'MedintUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'user_info': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user'", 'unique': 'True', 'null': 'True', 'to': u"orm['common.UserInfo']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'wiki.article': {
            'Meta': {'object_name': 'Article'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.ArticleRevision']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'wiki.articlerevision': {
            'Meta': {'object_name': 'ArticleRevision'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'article_revision'", 'symmetrical': 'False', 'to': u"orm['wiki.Attachment']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'article_revision'", 'symmetrical': 'False', 'to': u"orm['wiki.FieldContent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.ArticleRevision']", 'null': 'True'})
        },
        u'wiki.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.Attachment']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'wiki.disease': {
            'Meta': {'object_name': 'Disease', '_ormbases': [u'wiki.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wiki.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'icd10': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'icd9': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'wiki.field': {
            'Meta': {'object_name': 'Field'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'wiki.fieldcontent': {
            'Meta': {'object_name': 'FieldContent'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wiki.FieldContent']", 'null': 'True'})
        }
    }

    complete_apps = ['wiki']