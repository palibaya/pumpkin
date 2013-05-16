import paramiko
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class BaseModel(models.Model):

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

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


class Job(BaseModel):
    name = models.CharField(max_length=255)
    runner = models.CharField(max_length=255)
    project = models.ForeignKey(Project)

    def pre_run(self):
        self.project.test_server.connect()


    def post_run(self):
        self.project.test_server.close()


class Queue(BaseModel):
    name = models.CharField(max_length=255)
    done = models.BooleanField()


class BuildTemplate(BaseModel):
    '''
    Model ini untuk menampung template build
    '''
    name = models.CharField(max_length=255)


class Build(BaseModel):
    '''
    Model ini untuk menampung perintah yang akan dilakukan terhadap
    project yang dikelola
    '''
    job = models.ForeignKey(Job)
    project = models.ForeignKey(Project)
    command = models.TextField()
    output = models.TextField()
