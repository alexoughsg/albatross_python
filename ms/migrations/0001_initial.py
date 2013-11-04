# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Region'
        db.create_table('ms_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('root_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_master', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ms', ['Region'])

        # Adding model 'EventLog'
        db.create_table('ms_eventlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('routing_key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 4, 12, 27, 55, 302288), null=True, blank=True)),
            ('processed_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('result', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('ms', ['EventLog'])


    def backwards(self, orm):
        
        # Deleting model 'Region'
        db.delete_table('ms_region')

        # Deleting model 'EventLog'
        db.delete_table('ms_eventlog')


    models = {
        'ms.eventlog': {
            'Meta': {'object_name': 'EventLog'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 4, 12, 27, 55, 302288)', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'processed_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'routing_key': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ms.region': {
            'Meta': {'object_name': 'Region'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_master': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'root_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['ms']
