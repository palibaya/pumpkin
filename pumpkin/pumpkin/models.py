from datetime import datetime
import importlib

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.contrib.auth.models import User

import pytz

current_tz =  pytz.timezone(settings.TIME_ZONE)

class BaseModel(models.Model):

    class Meta:
        abstract = True

    def __unicode__(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return '%s ID:%s' % (type(self).__name__, self.id)


class Server(BaseModel):
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=32)
    port = models.PositiveIntegerField()
    superuser_login = models.CharField(max_length=32)
    superuser_password = models.CharField(max_length=255)
    user_login = models.CharField(max_length=32)
    user_password = models.CharField(max_length=255)
    ssh_key_pub = models.TextField(blank=True, null=True)


class SCM(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)


class Repository(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    scm = models.ForeignKey(SCM, related_name='+')


class Project(BaseModel):
    '''
    Model ini untuk menampung project yang akan dikelola
    '''
    name = models.CharField(max_length=255)
    identifier = models.SlugField()
    description = models.TextField(blank=True)
    managers = models.ManyToManyField(User,
                                      related_name='managered_projects')
    members = models.ManyToManyField(User,
                                     related_name='membered_projects')

    server = models.ForeignKey(Server)
    repository = models.OneToOneField(Repository,
                                      related_name='project')


    def get_params(self):
        return {
            '%s_REPOSITORY_ADDRESS' % (self.repository.scm.code): \
                    self.repository.address,
            'PROJECT_ID': '%s' % self.identifier,
            'PROJECT_WORKSPACE': self.get_workspace_path(),
        }


    def get_absolute_url(self):
        return reverse('pumpkin.views.project',
                       args=[str(self.identifier)])

    def get_workspace_path(self):
        return '$HOME/%s' % self.identifier.replace('-','_')


class JobLog(BaseModel):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failure','Failure'),
        ('partial', 'Partial'),
    )
    job = models.ForeignKey('Job', related_name='logs')
    begin = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)


    def duration(self):
        return self.end - self.begin


    def __unicode__(self):
        return 'Job Log #%s: %s' % (self.id, self.job)

class Job(BaseModel):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='jobs')

    def _create_log(self):
        job_log = JobLog()
        job_log.job = self
        job_log.begin = current_tz.localize(datetime.now())
        job_log.save()
        return job_log

    def _save_log(self, job_log, build_statuses):
        status_set = set(build_statuses)
        if len(status_set) == 1 and 'success' in status_set:
            job_log.status = 'success'
        elif len(status_set) == 1 and 'failure' in status_set:
            job_log.status = 'failure'
        else:
            job_log.status = 'partial'
        job_log.end = current_tz.localize(datetime.now())
        job_log.save()


    #def run(self):
        #ssh_client = SSHClient(self.project.server)
        #ssh_client.set_params(self.project.get_params())
        #job_log = self._create_log()
        #build_statuses = []
        #for build in self.builds.order_by('sequence'):
            #build_statuses.append(build.run(ssh_client, job_log))
        #self._save_log(job_log, build_statuses)

    def run(self):
        job_log = self._create_log()
        build_statuses = []
        for build in self.builds.order_by('sequence'):
            build_statuses.append(build.run(job_log))
        self._save_log(job_log, build_statuses)


    def get_last_build(self):
        lasts = self.builds.order_by('-sequence')
        if len(lasts) > 0:
            return lasts[0]

    def last_success(self):
        logs = self.logs.filter(status='success').order_by('-end')
        if len(logs) > 0:
            return logs[0]


    def last_failure(self):
        logs =  self.logs.filter(status='failure').order_by('-end')
        if len(logs) > 0:
            return logs[0]

    def last_run(self):
        if hasattr(self, '_last_run'):
            return self._last_run
        else:
            logs =  self.logs.order_by('-end')
            if len(logs) > 0:
                self._last_run = logs[0]
            else:
                self._last_run = None
        return self._last_run

    def last_duration(self):
        if self.last_run() is not None:
            return self.last_run().duration()

class Builder(BaseModel):
    name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)


class BuildLog(BaseModel):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failure','Failure'),
    )

    build = models.ForeignKey('Build', related_name='logs')
    job = models.ForeignKey(Job, related_name='build_logs')
    job_log = models.ForeignKey(JobLog, related_name='build_logs',
                                null=True)
    command = models.TextField()
    output = models.TextField()
    error = models.TextField()
    sequence = models.PositiveIntegerField(default=1)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)


class Build(BaseModel):
    '''
    Model ini untuk menampung perintah yang akan dilakukan terhadap
    project yang dikelola
    '''

    COMMAND_TYPE_CHOICES = (
        ('bash', 'BASH'),
        ('python', 'Python Command'),
        ('python_function', 'Python Function Module'),
        ('python_class', 'Python Class Module')
    )

    job = models.ForeignKey(Job, related_name='builds')
    builder = models.ForeignKey(Builder, related_name='+')
    command = models.TextField()
    sequence = models.PositiveIntegerField(default=1)

    def save(self):
        if self.id is None:
            last_build = self.job.get_last_build()
            if last_build is not None:
                self.sequence = last_build.sequence  + 1
        return super(Build, self).save()


    def _create_log(self, job_log):
        build_log = BuildLog()
        build_log.build = self
        build_log.sequence = self.sequence
        build_log.job = self.job
        build_log.job_log = job_log
        build_log.command = self.command
        build_log.begin = current_tz.localize(datetime.now())
        return build_log

    def _save_log(self, build_log, output_list, error_list):
        if len(error_list) > 0:
            build_log.status = 'failure'
        else:
            build_log.status = 'success'
        build_log.output = ''.join(output_list)
        build_log.error = ''.join(error_list)
        build_log.end = current_tz.localize(datetime.now())
        build_log.save()


    def _run_bash(self, ssh_client, job_log):
        build_log = self._create_log(job_log)
        ssh_client.connect()
        ssh_client.add_command(self.command)
        stdin, stdout, stderr = ssh_client.execute()
        output_list, error_list = stdout.readlines(), stderr.readlines()
        ssh_client.close()
        self._save_log(build_log, output_list, error_list)
        return build_log.status

    #def run(self, ssh_client, job_log):
        #if type(ssh_client) is not SSHClient:
            #raise TypeError("'client' wrong type")
        #if self.command_type == 'bash':
            #return self._run_bash(ssh_client, job_log)

    def get_builder_object(self, job_log):
        if not hasattr(self, '_builder_object'):
            module_path, builder_class_str = self.builder.class_name\
                                                 .rsplit('.', 1)
            module = importlib.import_module(module_path)
            builder_class = getattr(module, builder_class_str)
            self._builder_object = builder_class(self, job_log)
        return self._builder_object

    def run(self, job_log):
        builder = self.get_builder_object(job_log)
        builder.run()
        return builder.get_log().status



