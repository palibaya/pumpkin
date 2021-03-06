# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Builder.template'
        db.delete_column(u'pumpkin_builder', 'template')

        # Adding field 'Builder.html_template'
        db.add_column(u'pumpkin_builder', 'html_template',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'PostBuilder.template'
        db.delete_column(u'pumpkin_postbuilder', 'template')

        # Adding field 'PostBuilder.html_template'
        db.add_column(u'pumpkin_postbuilder', 'html_template',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Builder.template'
        db.add_column(u'pumpkin_builder', 'template',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Builder.html_template'
        db.delete_column(u'pumpkin_builder', 'html_template')

        # Adding field 'PostBuilder.template'
        db.add_column(u'pumpkin_postbuilder', 'template',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'PostBuilder.html_template'
        db.delete_column(u'pumpkin_postbuilder', 'html_template')


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
        u'pumpkin.build': {
            'Meta': {'object_name': 'Build'},
            'builder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['pumpkin.Builder']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'builds'", 'to': u"orm['pumpkin.Job']"}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'pumpkin.builder': {
            'Meta': {'object_name': 'Builder'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html_template': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pumpkin.buildlog': {
            'Meta': {'object_name': 'BuildLog'},
            'begin': ('django.db.models.fields.DateTimeField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pumpkin.ProjectBranch']", 'null': 'True', 'blank': 'True'}),
            'build': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': u"orm['pumpkin.Build']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'error': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'build_logs'", 'to': u"orm['pumpkin.Job']"}),
            'job_log': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'build_logs'", 'null': 'True', 'to': u"orm['pumpkin.JobLog']"}),
            'output': ('django.db.models.fields.TextField', [], {}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'pumpkin.buildtemplate': {
            'Meta': {'object_name': 'BuildTemplate'},
            'builder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['pumpkin.Builder']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'builds'", 'to': u"orm['pumpkin.JobTemplate']"}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'pumpkin.job': {
            'Meta': {'object_name': 'Job'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': u"orm['pumpkin.Project']"})
        },
        u'pumpkin.joblog': {
            'Meta': {'object_name': 'JobLog'},
            'begin': ('django.db.models.fields.DateTimeField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pumpkin.ProjectBranch']", 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': u"orm['pumpkin.Job']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'pumpkin.jobtemplate': {
            'Meta': {'object_name': 'JobTemplate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['pumpkin.Project']"}),
            'project_template': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'job_templates'", 'null': 'True', 'to': u"orm['pumpkin.ProjectTemplate']"})
        },
        u'pumpkin.jobtrigger': {
            'Meta': {'object_name': 'JobTrigger'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pumpkin.postbuild': {
            'Meta': {'object_name': 'PostBuild'},
            'builder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['pumpkin.PostBuilder']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_builds'", 'to': u"orm['pumpkin.Job']"}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'pumpkin.postbuilder': {
            'Meta': {'object_name': 'PostBuilder'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'condition': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html_template': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pumpkin.postbuildtemplate': {
            'Meta': {'object_name': 'PostBuildTemplate'},
            'builder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['pumpkin.PostBuilder']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_builds'", 'to': u"orm['pumpkin.JobTemplate']"}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
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
        u'pumpkin.projectbranch': {
            'Meta': {'object_name': 'ProjectBranch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pumpkin.Project']"})
        },
        u'pumpkin.projectparam': {
            'Meta': {'object_name': 'ProjectParam'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'params'", 'to': u"orm['pumpkin.Project']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pumpkin.projecttemplate': {
            'Meta': {'object_name': 'ProjectTemplate'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        }
    }

    complete_apps = ['pumpkin']