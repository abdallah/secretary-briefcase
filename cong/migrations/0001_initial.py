# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Congregation'
        db.create_table(u'cong_congregation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'cong', ['Congregation'])

        # Adding model 'Attendance'
        db.create_table(u'cong_attendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meeting', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'cong', ['Attendance'])

        # Adding model 'Group'
        db.create_table(u'cong_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('overseer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='overseer', to=orm['cong.Publisher'])),
        ))
        db.send_create_signal(u'cong', ['Group'])

        # Adding model 'Publisher'
        db.create_table(u'cong_publisher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_immersed', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_annointed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_elder', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_ministerial_servant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cong.Group'], null=True, blank=True)),
        ))
        db.send_create_signal(u'cong', ['Publisher'])

        # Adding model 'Pioneer'
        db.create_table(u'cong_pioneer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cong.Publisher'])),
            ('pioneer_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('date_started', self.gf('django.db.models.fields.DateField')()),
            ('date_stopped', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'cong', ['Pioneer'])

        # Adding model 'ServiceReport'
        db.create_table(u'cong_servicereport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cong.Publisher'])),
            ('month', self.gf('django.db.models.fields.DateField')()),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('magazines', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('visits', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('studies', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('books', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('booklets_brochures', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('auxiliary_pioneer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'cong', ['ServiceReport'])


    def backwards(self, orm):
        # Deleting model 'Congregation'
        db.delete_table(u'cong_congregation')

        # Deleting model 'Attendance'
        db.delete_table(u'cong_attendance')

        # Deleting model 'Group'
        db.delete_table(u'cong_group')

        # Deleting model 'Publisher'
        db.delete_table(u'cong_publisher')

        # Deleting model 'Pioneer'
        db.delete_table(u'cong_pioneer')

        # Deleting model 'ServiceReport'
        db.delete_table(u'cong_servicereport')


    models = {
        u'cong.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'cong.congregation': {
            'Meta': {'object_name': 'Congregation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'cong.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'overseer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'overseer'", 'to': u"orm['cong.Publisher']"})
        },
        u'cong.pioneer': {
            'Meta': {'object_name': 'Pioneer'},
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'date_stopped': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pioneer_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cong.Publisher']"})
        },
        u'cong.publisher': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Publisher'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_immersed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cong.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_annointed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_elder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_ministerial_servant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'cong.servicereport': {
            'Meta': {'ordering': "['-month']", 'object_name': 'ServiceReport'},
            'auxiliary_pioneer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'booklets_brochures': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'books': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'magazines': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.DateField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cong.Publisher']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'studies': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cong']