from datetime import datetime
import importlib

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.contrib.auth.models import User


import paramiko
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

class TestServer(BaseModel):
    '''
    Model ini untuk menyimpan informasi server untuk kebutuhan testing
    '''
    name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=32)
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=255)

    def status(self):
        pass

    def connect(self):
        if not hasattr(self, '_ssh'):
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko\
                                                  .AutoAddPolicy())
            self._ssh.connect(hostname=self.hostname,
                              port=self.port,
                              username=self.username,
                              password=self.password)

    def command(self, cmd):
        return self._ssh.exec_command(cmd)

    def close(self):
        self._ssh.close()


class Repository(BaseModel):
    name = models.CharField(max_length=255)


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
    test_server = models.ForeignKey(TestServer)

    def after_create(self):
        pass

    def update_repo(self):
        pass

    def get_absolute_url(self):
        return reverse('pumpkin.views.project',
                       args=[str(self.identifier)])


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

class Job(BaseModel):
    name = models.CharField(max_length=255)
    runner = models.CharField(max_length=255,
                              default='pumpkin.runners.Runner')
    project = models.ForeignKey(Project, related_name='jobs')

    def pre_run(self):
        if not hasattr(self, '_runner'):
            module_path, runner_class_str = self.runner.rsplit('.',1)
            module = importlib.import_module(module_path)
            runner_class = getattr(module, runner_class_str)
            self._runner = runner_class(self)
        self.project.test_server.connect()
        self._runner.pre_run_job()


    def run(self):
        self.pre_run()
        job_log = JobLog()
        job_log.job = self
        job_log.begin = current_tz.localize(datetime.now())
        job_log.save()
        build_count = self.builds.count()
        statuses = []
        for build in self.builds.all():
            build_log = build.run(runner=self._runner, job_log=job_log)
            statuses.append(build_log.status)
        if build_count == len(statuses) and 'success' in statuses:
            job_log.status = 'success'
        elif build_count == len(statuses) and 'failure' in statuses:
            job_log.status = 'failure'
        else:
            job_log.status = 'partial'
        job_log.end = current_tz.localize(datetime.now())
        job_log.save()
        self.post_run()

    def post_run(self):
        self._runner.post_run_job()
        self.project.test_server.close()

    def get_last_build(self):
        lasts = self.builds.order_by('-sequence')
        if len(lasts) > 0:
            return lasts[0]


class Queue(BaseModel):
    name = models.CharField(max_length=255)
    done = models.BooleanField()
    job = models.ForeignKey(Job, related_name='+')


class BuildTemplate(BaseModel):
    '''
    Model ini untuk menampung template build
    '''
    name = models.CharField(max_length=255)


class BuildLog(BaseModel):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failure','Failure'),
    )

    build = models.ForeignKey('Build', related_name='logs')
    job = models.ForeignKey(Job, related_name='build_logs')
    job_log = models.ForeignKey(JobLog, related_name='build_logs')
    command = models.TextField()
    output = models.TextField()
    error = models.TextField()
    sequence = models.PositiveIntegerField(default=1)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)

    def __unicode__(self):
        return 'Build Log #%s: %s' % (self.id, self.begin)

class Build(BaseModel):
    '''
    Model ini untuk menampung perintah yang akan dilakukan terhadap
    project yang dikelola
    '''
    job = models.ForeignKey(Job, related_name='builds')
    command = models.TextField()
    sequence = models.PositiveIntegerField(default=1)

    def save(self):
        last_build = self.job.get_last_build()
        if last_build is not None:
            self.sequence = last_build.sequence  + 1

        print 'Last Build: %s' % last_build

        return super(Build, self).save()

    def run(self, runner, job_log):
        build_log = BuildLog()
        build_log.build = self
        build_log.sequence = self.sequence
        build_log.job = self.job
        build_log.job_log = job_log
        build_log.command = self.command
        build_log.begin = current_tz.localize(datetime.now())
        stdin, stdout, stderr  = self.job.project.test_server\
                                     .command(self.command)
        # melakukan pengecekan terhadap status build.
        output_list, error_list = stdout.readlines(), stderr.readlines()
        build_log.status = runner.get_status_build(output_list,
                                                   error_list)
        build_log.output = ''.join(output_list)
        build_log.error = ''.join(error_list)
        runner.process_output_build(build_log.output)
        build_log.end = current_tz.localize(datetime.now())
        build_log.save()
        return build_log



