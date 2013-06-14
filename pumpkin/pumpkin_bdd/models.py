from django.db import models

from pumpkin.models import BaseModel as Base
from pumpkin.models import Project, ProjectBranch

STATUS_CHOICES = (
    ('untested', 'Untested'),
    ('skipped', 'Skipped'),
    ('passed', 'Skipped'),
    ('failed', 'Failed')
)

class BaseModel(Base):
    project = models.ForeignKey(Project, related_name='+',
                                null=True, blank=True)
    project_branch = models.ForeignKey(Project, related_name='+',
                                       null=True, blank=True)
    class Meta:
        abstract = True

    def __unicode__(self):
        if hasattr(self, 'keyword'):
            return '%s: %s' % (self.keyword, self.name)
        return super(BaseModel, self).__unicode__()


class Tag(BaseModel):
    name = models.CharField(max_length=255)


class Feature(BaseModel):
    keyword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='features')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default='untested')
    filename = models.CharField(max_length=255)
    line = models.IntegerField(blank=True, null=True)


class Background(BaseModel):
    keyword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    line = models.IntegerField(blank=True, null=True)
    feature = models.OneToOneField(Feature, related_name='background')


class Scenario(BaseModel):
    keyword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    feature = models.ForeignKey(Feature, related_name='scenario')
    tags = models.ManyToManyField(Tag, related_name='scenarios')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default='untested')
    filename = models.CharField(max_length=255)
    line = models.IntegerField()


class ScenarioOutline(BaseModel):
    keyword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    feature = models.ForeignKey(Feature,
                                related_name='scenario_outlines')
    tags = models.ManyToManyField(Tag,
                                  related_name='scenarios_outlines')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default='untested')
    filename = models.CharField(max_length=255)
    line = models.IntegerField()


class Example(BaseModel):
    keyword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    table = models.TextField(blank=True)
    filename = models.CharField(max_length=255)
    line = models.IntegerField(blank=True, null=True)
    scenario_outline = models.ForeignKey(ScenarioOutline,
                                         related_name='examples',
                                         blank=True, null=True)


class Step(BaseModel):
    keyword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    step_type = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    table = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES,
                              default='untested')
    error_message = models.TextField(blank=True)
    filename = models.CharField(max_length=255)
    line = models.IntegerField(blank=True, null=True)

    background = models.ForeignKey(Background, related_name='steps',
                                   null=True, blank=True)
    scenario = models.ForeignKey(Scenario, related_name='steps',
                                 null=True, blank=True)
    scenario_outline = models.ForeignKey(ScenarioOutline,
                                         related_name='steps',
                                         null=True, blank=True)






