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
    root_password = models.CharField(max_length=255)
    ssh_key_pub = models.TextField(blank=True)

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



    def root_connect(self):
        if not hasattr(self, '_root_ssh'):
            self._root_ssh = paramiko.SSHClient()
            self._root_ssh.set_missing_host_key_policy(paramiko\
                                                  .AutoAddPolicy())
            self._root_ssh.connect(hostname=self.hostname,
                              port=self.port,
                              username='root',
                              password=self.root_password)

    def set_params(self, params={}):
        if not hasattr(self, '_params_cmd'):
            self._params_cmd = ''
        for k in params.keys():
            self._params_cmd += 'export %s=%s\n' % (k, params[k])


    def command(self, cmd):
        self.set_params()
        return self._ssh.exec_command(self._params_cmd + cmd)

    def close(self):
        self._ssh.close()
        delattr(self, '_ssh')


    def update_ssh_key(self):
        cmd = '''
              rm -rf ~/.ssh
              mkdir ~/.ssh
              echo -e  'y\n'|ssh-keygen -q -t rsa -N '' -f .ssh/id_rsa
              cat ~/.ssh/id_rsa.pub
              '''
        stdin, stdout, stderr = self.command(str(cmd))
        self.ssh_key_pub = ''.join(stdout.readlines())
        self.save()


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
    git_remote_address = models.CharField(max_length=255, blank=True)
    setup_command = models.TextField(blank=True)
    setup_log = models.TextField(blank=True)

    def after_create(self):
        pass

    def update_repo(self):
        pass

    def get_absolute_url(self):
        return reverse('pumpkin.views.project',
                       args=[str(self.identifier)])

    def get_workspace_path(self):
        return '$HOME/%s' % self.identifier.replace('-','_')

    def set_params(self):
        self.test_server.set_params({
            'GIT_REMOTE_ADDRESS': self.git_remote_address,
            'PROJECT_ID': '%s' % self.identifier,
            'VIRTUALENV_PATH': '$HOME/.virtualenvs/%s' % self.identifier,
            'PROJECT_WORKSPACE': self.get_workspace_path(),
        })

    def setup(self):
        self.test_server.connect()
        self.set_params()
        stdin, stdout, stderr = self.test_server\
                                    .command(self.setup_command)
        self.setup_log = ''.join(stdout.readlines() + \
                                 stderr.readlines())
        self.test_server.close()
        self.save()


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
    runner = models.CharField(max_length=255,
                              default='pumpkin.runners.Runner')
    project = models.ForeignKey(Project, related_name='jobs')
    pre_job = models.ForeignKey('self', related_name='+', null=True,
                                blank=True)
    post_job = models.ForeignKey('self', related_name='+', null=True,
                                 blank=True)

    def pre_run(self):
        if self.pre_job:
            last_pre_job = self.pre_job.last_run()
            if last_pre_job is None:
                self.pre_job.run()
            elif last_pre_job.status != 'success':
                self.pre_job.run()

        if not hasattr(self, '_runner'):
            module_path, runner_class_str = self.runner.rsplit('.',1)
            module = importlib.import_module(module_path)
            runner_class = getattr(module, runner_class_str)
            self._runner = runner_class(self)
        self.project.test_server.connect()
        self.project.set_params()
        self._runner.pre_run_job()


    def run(self):
        self.pre_run()
        job_log = JobLog()
        job_log.job = self
        job_log.begin = current_tz.localize(datetime.now())
        job_log.save()
        build_count = self.builds.count()
        success_count = 0
        failure_count = 0
        for build in self.builds.all():
            build_log = build.run(runner=self._runner, job_log=job_log,
                                  test_server=self.project.test_server)
            if build_log.status == 'success':
                success_count += 1
            if build_log.status == 'failure':
                failure_count += 1

        if build_count == success_count:
            job_log.status = 'success'
        elif build_count == failure_count:
            job_log.status = 'failure'
        else:
            job_log.status = 'partial'
        job_log.end = current_tz.localize(datetime.now())
        job_log.save()
        self.post_run()

    def post_run(self):
        if self.post_job:
            self.post_job.run()
        self._runner.post_run_job()
        self.project.test_server.close()

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

    def run(self, runner, job_log, test_server):
        build_log = BuildLog()
        build_log.build = self
        build_log.sequence = self.sequence
        build_log.job = self.job
        build_log.job_log = job_log
        build_log.command = self.command
        build_log.begin = current_tz.localize(datetime.now())
        stdin, stdout, stderr  = test_server.command(self.command)
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



