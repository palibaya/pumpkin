from datetime import datetime
import pytz

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.loading import get_model
from django.contrib.auth.models import User

from pumpkin.tools import get_obj

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
    host = models.CharField(max_length=32, verbose_name='Host Address')
    port = models.PositiveIntegerField(verbose_name='SSH Port')
    superuser_login = models.CharField(max_length=32,
                                       verbose_name='Root')
    superuser_password = models.CharField(max_length=255,
                                          verbose_name='Root Password')
    user_login = models.CharField(max_length=32,
                                  verbose_name='User Login')
    user_password = models.CharField(max_length=255,
                                     verbose_name='User Password')
    ssh_key_pub = models.TextField(blank=True, null=True)


class SCM(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)


class Repository(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255,
                               verbose_name='Repository Address')
    scm = models.ForeignKey(SCM, related_name='+', default=1,
                            verbose_name='Repository SCM')


class ProjectBase(BaseModel):
    """
    Model ini untuk menampung project yang akan dikelola
    """
    name = models.CharField(max_length=255, unique=True)
    identifier = models.SlugField(unique=True)
    description = models.TextField(blank=True)


    def get_params(self):
        params = {
            '%s_REPOSITORY_ADDRESS' % self.repository.scm.code: \
                    self.repository.address,
            'PROJECT_ID': '%s' % self.identifier,
            'PROJECT_WORKSPACE': self.get_workspace_path(),
        }
        #extra = dict([(p.key, p.value) for p in self.params.all()])
        #params.update(extra)
        return params

    def get_absolute_url(self):
        return reverse('pumpkin.views.project',
                       args=[str(self.identifier)])

    def get_workspace_path(self):
        return '$HOME/%s' % self.identifier.replace('-','_')

    class Meta:
        abstract = True


class Project(ProjectBase):
    managers = models.ManyToManyField(User,
                                      related_name='managered_projects')
    members = models.ManyToManyField(User, null=True, blank=True,
                                     related_name='membered_projects')

    server = models.OneToOneField(Server)
    repository = models.OneToOneField(Repository,
                                      related_name='project')

class ProjectTemplate(ProjectBase):
    pass


class ProjectBranch(BaseModel):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project)


class ProjectParam(BaseModel):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='params')


class JobTrigger(BaseModel):
    name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)


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
    branch = models.ForeignKey(ProjectBranch, null=True, blank=True)

    def duration(self):
        return self.end - self.begin


    def __unicode__(self):
        return 'Job Log #%s: %s' % (self.id, self.job)


class JobBase(BaseModel):
    name = models.CharField(max_length=255)

    def _create_log(self, branch):
        job_log = JobLog()
        job_log.job = self
        job_log.branch = branch
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

    def run(self, branch=None):
        job_log = self._create_log(branch)
        build_statuses = []
        for build in self.builds.order_by('sequence'):
            build_statuses.append(build.run(job_log))
        self._save_log(job_log, build_statuses)


    def get_last_build(self):
        lasts = self.builds.order_by('-sequence')
        if len(lasts) > 0:
            return lasts[0]

    def last_success(self):
        logs = self.logs.filter(status='success').order_by('-begin')
        if len(logs) > 0:
            return logs[0]


    def last_failure(self):
        logs =  self.logs.filter(status='failure').order_by('-begin')
        if len(logs) > 0:
            return logs[0]

    def last_run(self):
        if hasattr(self, '_last_run'):
            return self._last_run
        else:
            logs =  self.logs.order_by('-begin')
            if len(logs) > 0:
                self._last_run = logs[0]
            else:
                self._last_run = None
        return self._last_run

    def last_duration(self):
        if self.last_run() is not None:
            return self.last_run().duration()

    class Meta:
        abstract = True


class JobTemplate(JobBase):
    project_template = models.ForeignKey(ProjectTemplate,
                                         related_name='job_templates',
                                         blank=True, null=True)
    project = models.ForeignKey(Project, related_name='+',
                                blank=True, null=True)

class Job(JobBase):
    project = models.ForeignKey(Project, related_name='jobs')


class BaseBuilder(BaseModel):
    name = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)
    content = models.TextField(blank=True) # for template or other
    html_template = models.TextField(blank=True)
    class Meta:
        abstract = True


class Builder(BaseBuilder):
    pass


class PostBuilder(BaseBuilder):
    condition = models.TextField()


class BuildLog(BaseModel):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failure','Failure'),
    )

    build = models.ForeignKey('Build', related_name='logs')
    job = models.ForeignKey(Job, related_name='build_logs')
    job_log = models.ForeignKey(JobLog, related_name='build_logs',
                                null=True)
    content = models.TextField() #for save command etc
    output = models.TextField()
    error = models.TextField()
    sequence = models.PositiveIntegerField(default=1)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    branch = models.ForeignKey(ProjectBranch, null=True, blank=True)


class BaseBuild(BaseModel):
    """
    Model ini untuk menampung perintah yang akan dilakukan terhadap
    project yang dikelola
    """

    content = models.TextField()
    sequence = models.PositiveIntegerField(default=1)

    def save(self):
        if self.id is None:
            last_build = self.job.get_last_build()
            if last_build is not None:
                self.sequence = last_build.sequence + 1

        self.content = self.content.replace('\r\n', '\n')
        self.content = self.content.replace('\r', '\n')
        return super(Build, self).save()

    def get_builder_object(self, job_log):
        if not hasattr(self, '_builder_object'):
            self._builder_object = get_obj(self.builder.class_name,
                                           [self, job_log])
        return self._builder_object

    def run(self, job_log):
        builder = self.get_builder_object(job_log)
        builder.build_run()
        return builder.get_log().status

    class Meta:
        abstract = True


class BuildTemplate(BaseBuild):
    job = models.ForeignKey(JobTemplate, related_name='builds')
    builder = models.ForeignKey(Builder, related_name='+')

class PostBuildTemplate(BaseBuild):
    job = models.ForeignKey(JobTemplate, related_name='post_builds')
    builder = models.ForeignKey(PostBuilder, related_name='+')

class Build(BaseBuild):
    job = models.ForeignKey(Job, related_name='builds')
    builder = models.ForeignKey(Builder, related_name='+')

class PostBuild(BaseBuild):
    job = models.ForeignKey(Job, related_name='post_builds')
    builder = models.ForeignKey(PostBuilder, related_name='+')

