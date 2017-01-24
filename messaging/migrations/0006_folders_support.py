# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DiscussionFolder'
        db.create_table(u'messaging_discussionfolder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MedintUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'messaging', ['DiscussionFolder'])

        # Adding M2M table for field discussions on 'DiscussionFolder'
        db.create_table(u'messaging_discussionfolder_discussions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('discussionfolder', models.ForeignKey(orm[u'messaging.discussionfolder'], null=False)),
            ('discussion', models.ForeignKey(orm[u'messaging.discussion'], null=False))
        ))
        db.create_unique(u'messaging_discussionfolder_discussions', ['discussionfolder_id', 'discussion_id'])
        for u in orm['common.MedintUser'].objects.all():
            f = orm['messaging.DiscussionFolder'].objects.create(name='Inbox', type=1, user=u)
            for d in u.discussion_set.all():
                f.discussions.add(d)
            f.save()
            orm['messaging.DiscussionFolder'].objects.create(name='Archive', type=2, user=u)
            orm['messaging.DiscussionFolder'].objects.create(name='Trash', type=3, user=u)


    def backwards(self, orm):
        # Deleting model 'DiscussionFolder'
        db.delete_table(u'messaging_discussionfolder')

        # Removing M2M table for field discussions on 'DiscussionFolder'
        db.delete_table('messaging_discussionfolder_discussions')


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
        u'messaging.contactitem': {
            'Meta': {'object_name': 'ContactItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': u"orm['common.MedintUser']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'in_contacts'", 'to': u"orm['common.MedintUser']"})
        },
        u'messaging.discussion': {
            'Meta': {'object_name': 'Discussion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.MedintUser']", 'symmetrical': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        u'messaging.discussionaccess': {
            'Meta': {'object_name': 'DiscussionAccess'},
            'access_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1969, 12, 31, 0, 0)'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['messaging.Discussion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']"})
        },
        u'messaging.discussionfolder': {
            'Meta': {'object_name': 'DiscussionFolder'},
            'discussions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['messaging.Discussion']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']"})
        },
        u'messaging.discussionmessage': {
            'Meta': {'object_name': 'DiscussionMessage'},
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['messaging.Discussion']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_messages'", 'to': u"orm['common.MedintUser']"}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['messaging']