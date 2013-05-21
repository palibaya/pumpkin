# -*- coding: utf-8 -*-

from django.contrib import admin
from pumpkin import models

admin.site.register(models.TestServer)
admin.site.register(models.Project)


class BuildInline(admin.TabularInline):
    model = models.Build

class JobAdmin(admin.ModelAdmin):
    inlines = [
        BuildInline,
    ]

admin.site.register(models.Job, JobAdmin)

class BuildLogInline(admin.TabularInline):
    model = models.BuildLog
    fields = ('command', 'output', 'error')
    readonly_fields = ('command', 'output', 'error')

class JobLogAdmin(admin.ModelAdmin):
    inlines = [
        BuildLogInline,
    ]

admin.site.register(models.JobLog, JobLogAdmin)

