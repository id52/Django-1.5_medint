# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserInfo.sex'
        db.add_column(u'common_userinfo', 'sex',
                      self.gf('django.db.models.fields.CharField')(default='male', max_length=10),
                      keep_default=False)

        # Adding field 'UserInfo.birth_date'
        db.add_column(u'common_userinfo', 'birth_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1972, 1, 27, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserInfo.sex'
        db.delete_column(u'common_userinfo', 'sex')

        # Deleting field 'UserInfo.birth_date'
        db.delete_column(u'common_userinfo', 'birth_date')


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
        u'common.admininfo': {
            'Meta': {'object_name': 'AdminInfo', '_ormbases': [u'common.UserInfo']},
            u'userinfo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.UserInfo']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'common.doctorinfo': {
            'Meta': {'object_name': 'DoctorInfo', '_ormbases': [u'common.UserInfo']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'clinic': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'officemng_email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'officemng_firstname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'officemng_lastname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'speciality': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'userinfo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.UserInfo']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'common.mailvalidationkey': {
            'Meta': {'object_name': 'MailValidationKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.MedintUser']", 'unique': 'True'})
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
            'user_info': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user'", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['common.UserInfo']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.patientinfo': {
            'Meta': {'object_name': 'PatientInfo', '_ormbases': [u'common.UserInfo']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'doctor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']", 'null': 'True'}),
            'indivo_record_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'userinfo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.UserInfo']", 'unique': 'True', 'primary_key': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'common.signabledocument': {
            'Meta': {'object_name': 'SignableDocument'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '100'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']"})
        },
        u'common.staffinfo': {
            'Meta': {'object_name': 'StaffInfo', '_ormbases': [u'common.UserInfo']},
            'staff_role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.StaffRole']"}),
            u'userinfo_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.UserInfo']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'common.staffrole': {
            'Meta': {'object_name': 'StaffRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'common.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'birth_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1972, 1, 27, 0, 0)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.MedintUser']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'male'", 'max_length': '10'})
        },
        u'common.yubikey': {
            'Meta': {'object_name': 'YubiKey'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_key'", 'null': 'True', 'to': u"orm['common.MedintUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_key'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['common.MedintUser']"}),
            'role': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.MedintUser']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']