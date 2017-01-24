# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'YubiKey'
        db.create_table(u'common_yubikey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.MedintUser'], unique=True, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.IntegerField')(default=4)),
        ))
        db.send_create_signal(u'common', ['YubiKey'])

        # Adding model 'UserInfo'
        db.create_table(u'common_userinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'common', ['UserInfo'])

        # Adding model 'PatientInfo'
        db.create_table(u'common_patientinfo', (
            (u'userinfo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.UserInfo'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'common', ['PatientInfo'])

        # Adding model 'DoctorInfo'
        db.create_table(u'common_doctorinfo', (
            (u'userinfo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.UserInfo'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('speciality', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('clinic', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('officemng_firstname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('officemng_lastname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('officemng_email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'common', ['DoctorInfo'])

        # Adding model 'MailValidationKey'
        db.create_table(u'common_mailvalidationkey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.MedintUser'], unique=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'common', ['MailValidationKey'])

        # Adding model 'StaffRole'
        db.create_table(u'common_staffrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'common', ['StaffRole'])

        # Adding model 'StaffInfo'
        db.create_table(u'common_staffinfo', (
            (u'userinfo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.UserInfo'], unique=True, primary_key=True)),
            ('staff_role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.StaffRole'])),
        ))
        db.send_create_signal(u'common', ['StaffInfo'])

        # Adding model 'AdminInfo'
        db.create_table(u'common_admininfo', (
            (u'userinfo_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.UserInfo'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'common', ['AdminInfo'])

        # Adding model 'MedintUser'
        db.create_table(u'common_medintuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('user_info', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user', unique=True, null=True, to=orm['common.UserInfo'])),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('role', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'common', ['MedintUser'])

        # Adding M2M table for field groups on 'MedintUser'
        db.create_table(u'common_medintuser_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medintuser', models.ForeignKey(orm[u'common.medintuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'common_medintuser_groups', ['medintuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'MedintUser'
        db.create_table(u'common_medintuser_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medintuser', models.ForeignKey(orm[u'common.medintuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'common_medintuser_user_permissions', ['medintuser_id', 'permission_id'])

        # Adding model 'SignableDocument'
        db.create_table(u'common_signabledocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.MedintUser'])),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=100)),
        ))
        db.send_create_signal(u'common', ['SignableDocument'])


    def backwards(self, orm):
        # Deleting model 'YubiKey'
        db.delete_table(u'common_yubikey')

        # Deleting model 'UserInfo'
        db.delete_table(u'common_userinfo')

        # Deleting model 'PatientInfo'
        db.delete_table(u'common_patientinfo')

        # Deleting model 'DoctorInfo'
        db.delete_table(u'common_doctorinfo')

        # Deleting model 'MailValidationKey'
        db.delete_table(u'common_mailvalidationkey')

        # Deleting model 'StaffRole'
        db.delete_table(u'common_staffrole')

        # Deleting model 'StaffInfo'
        db.delete_table(u'common_staffinfo')

        # Deleting model 'AdminInfo'
        db.delete_table(u'common_admininfo')

        # Deleting model 'MedintUser'
        db.delete_table(u'common_medintuser')

        # Removing M2M table for field groups on 'MedintUser'
        db.delete_table('common_medintuser_groups')

        # Removing M2M table for field user_permissions on 'MedintUser'
        db.delete_table('common_medintuser_user_permissions')

        # Deleting model 'SignableDocument'
        db.delete_table(u'common_signabledocument')


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
            'user_info': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user'", 'unique': 'True', 'null': 'True', 'to': u"orm['common.UserInfo']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.patientinfo': {
            'Meta': {'object_name': 'PatientInfo', '_ormbases': [u'common.UserInfo']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'common.yubikey': {
            'Meta': {'object_name': 'YubiKey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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