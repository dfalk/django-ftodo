# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskTag'
        db.create_table(u'ftodo_tasktag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'ftodo', ['TaskTag'])

        # Adding model 'Task'
        db.create_table(u'ftodo_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_due', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ftodo.Task'], null=True, blank=True)),
        ))
        db.send_create_signal(u'ftodo', ['Task'])

        # Adding M2M table for field tags on 'Task'
        m2m_table_name = db.shorten_name(u'ftodo_task_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm[u'ftodo.task'], null=False)),
            ('tasktag', models.ForeignKey(orm[u'ftodo.tasktag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'tasktag_id'])


    def backwards(self, orm):
        # Deleting model 'TaskTag'
        db.delete_table(u'ftodo_tasktag')

        # Deleting model 'Task'
        db.delete_table(u'ftodo_task')

        # Removing M2M table for field tags on 'Task'
        db.delete_table(db.shorten_name(u'ftodo_task_tags'))


    models = {
        u'ftodo.task': {
            'Meta': {'ordering': "['date_due']", 'object_name': 'Task'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_due': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ftodo.Task']", 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['ftodo.TaskTag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'ftodo.tasktag': {
            'Meta': {'ordering': "['category', 'title']", 'object_name': 'TaskTag'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['ftodo']