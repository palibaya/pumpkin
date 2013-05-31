# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'pumpkin_bdd_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Tag'])

        # Adding model 'Feature'
        db.create_table(u'pumpkin_bdd_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='untested', max_length=16)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Feature'])

        # Adding M2M table for field tags on 'Feature'
        db.create_table(u'pumpkin_bdd_feature_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm[u'pumpkin_bdd.feature'], null=False)),
            ('tag', models.ForeignKey(orm[u'pumpkin_bdd.tag'], null=False))
        ))
        db.create_unique(u'pumpkin_bdd_feature_tags', ['feature_id', 'tag_id'])

        # Adding model 'Background'
        db.create_table(u'pumpkin_bdd_background', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('feature', self.gf('django.db.models.fields.related.OneToOneField')(related_name='background', unique=True, to=orm['pumpkin_bdd.Feature'])),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Background'])

        # Adding model 'Scenario'
        db.create_table(u'pumpkin_bdd_scenario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scenario', to=orm['pumpkin_bdd.Feature'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='untested', max_length=16)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Scenario'])

        # Adding M2M table for field tags on 'Scenario'
        db.create_table(u'pumpkin_bdd_scenario_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('scenario', models.ForeignKey(orm[u'pumpkin_bdd.scenario'], null=False)),
            ('tag', models.ForeignKey(orm[u'pumpkin_bdd.tag'], null=False))
        ))
        db.create_unique(u'pumpkin_bdd_scenario_tags', ['scenario_id', 'tag_id'])

        # Adding model 'ScenarioOutline'
        db.create_table(u'pumpkin_bdd_scenariooutline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scenario_outlines', to=orm['pumpkin_bdd.Feature'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='untested', max_length=16)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['ScenarioOutline'])

        # Adding M2M table for field tags on 'ScenarioOutline'
        db.create_table(u'pumpkin_bdd_scenariooutline_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('scenariooutline', models.ForeignKey(orm[u'pumpkin_bdd.scenariooutline'], null=False)),
            ('tag', models.ForeignKey(orm[u'pumpkin_bdd.tag'], null=False))
        ))
        db.create_unique(u'pumpkin_bdd_scenariooutline_tags', ['scenariooutline_id', 'tag_id'])

        # Adding model 'Example'
        db.create_table(u'pumpkin_bdd_example', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('table', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('outline', self.gf('django.db.models.fields.related.ForeignKey')(related_name='examples', to=orm['pumpkin_bdd.ScenarioOutline'])),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Example'])

        # Adding model 'Step'
        db.create_table(u'pumpkin_bdd_step', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('step_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('table', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='untested', max_length=16)),
            ('error_message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('background', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='steps', null=True, to=orm['pumpkin_bdd.Background'])),
            ('scenario', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='steps', null=True, to=orm['pumpkin_bdd.Scenario'])),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Step'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'pumpkin_bdd_tag')

        # Deleting model 'Feature'
        db.delete_table(u'pumpkin_bdd_feature')

        # Removing M2M table for field tags on 'Feature'
        db.delete_table('pumpkin_bdd_feature_tags')

        # Deleting model 'Background'
        db.delete_table(u'pumpkin_bdd_background')

        # Deleting model 'Scenario'
        db.delete_table(u'pumpkin_bdd_scenario')

        # Removing M2M table for field tags on 'Scenario'
        db.delete_table('pumpkin_bdd_scenario_tags')

        # Deleting model 'ScenarioOutline'
        db.delete_table(u'pumpkin_bdd_scenariooutline')

        # Removing M2M table for field tags on 'ScenarioOutline'
        db.delete_table('pumpkin_bdd_scenariooutline_tags')

        # Deleting model 'Example'
        db.delete_table(u'pumpkin_bdd_example')

        # Deleting model 'Step'
        db.delete_table(u'pumpkin_bdd_step')


    models = {
        u'pumpkin_bdd.background': {
            'Meta': {'object_name': 'Background'},
            'feature': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'background'", 'unique': 'True', 'to': u"orm['pumpkin_bdd.Feature']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pumpkin_bdd.example': {
            'Meta': {'object_name': 'Example'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'outline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'examples'", 'to': u"orm['pumpkin_bdd.ScenarioOutline']"}),
            'table': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'pumpkin_bdd.feature': {
            'Meta': {'object_name': 'Feature'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'untested'", 'max_length': '16'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'features'", 'symmetrical': 'False', 'to': u"orm['pumpkin_bdd.Tag']"})
        },
        u'pumpkin_bdd.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scenario'", 'to': u"orm['pumpkin_bdd.Feature']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'untested'", 'max_length': '16'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'scenarios'", 'symmetrical': 'False', 'to': u"orm['pumpkin_bdd.Tag']"})
        },
        u'pumpkin_bdd.scenariooutline': {
            'Meta': {'object_name': 'ScenarioOutline'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scenario_outlines'", 'to': u"orm['pumpkin_bdd.Feature']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'untested'", 'max_length': '16'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'scenarios_outlines'", 'symmetrical': 'False', 'to': u"orm['pumpkin_bdd.Tag']"})
        },
        u'pumpkin_bdd.step': {
            'Meta': {'object_name': 'Step'},
            'background': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'steps'", 'null': 'True', 'to': u"orm['pumpkin_bdd.Background']"}),
            'error_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'scenario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'steps'", 'null': 'True', 'to': u"orm['pumpkin_bdd.Scenario']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'untested'", 'max_length': '16'}),
            'step_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'table': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'pumpkin_bdd.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['pumpkin_bdd']