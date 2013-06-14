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
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('project_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Tag'])

        # Adding model 'Feature'
        db.create_table(u'pumpkin_bdd_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('project_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
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
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('project_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
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
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('project_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
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
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('project_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
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
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('project_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('table', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('scenario_outline', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='examples', null=True, to=orm['pumpkin_bdd.ScenarioOutline'])),
        ))
        db.send_create_signal(u'pumpkin_bdd', ['Example'])

        # Adding model 'Step'
        db.create_table(u'pumpkin_bdd_step', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
            ('project_branch', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['pumpkin.Project'])),
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
            ('scenario_outline', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='steps', null=True, to=orm['pumpkin_bdd.ScenarioOutline'])),
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pumpkin.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'managered_projects'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'membered_projects'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'repository': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'project'", 'unique': 'True', 'to': u"orm['pumpkin.Repository']"}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pumpkin.Server']"})
        },
        u'pumpkin.repository': {
            'Meta': {'object_name': 'Repository'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'scm': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['pumpkin.SCM']"})
        },
        u'pumpkin.scm': {
            'Meta': {'object_name': 'SCM'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pumpkin.server': {
            'Meta': {'object_name': 'Server'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ssh_key_pub': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'superuser_login': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'superuser_password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_login': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user_password': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pumpkin_bdd.background': {
            'Meta': {'object_name': 'Background'},
            'feature': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'background'", 'unique': 'True', 'to': u"orm['pumpkin_bdd.Feature']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"})
        },
        u'pumpkin_bdd.example': {
            'Meta': {'object_name': 'Example'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'scenario_outline': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'examples'", 'null': 'True', 'to': u"orm['pumpkin_bdd.ScenarioOutline']"}),
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'scenario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'steps'", 'null': 'True', 'to': u"orm['pumpkin_bdd.Scenario']"}),
            'scenario_outline': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'steps'", 'null': 'True', 'to': u"orm['pumpkin_bdd.ScenarioOutline']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'untested'", 'max_length': '16'}),
            'step_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'table': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'pumpkin_bdd.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_branch': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"})
        }
    }

    complete_apps = ['pumpkin_bdd']