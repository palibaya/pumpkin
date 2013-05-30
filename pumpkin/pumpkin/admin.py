# -*- coding: utf-8 -*-

from django.contrib import admin
from pumpkin import models

admin.site.register(models.Server)
admin.site.register(models.SCM)
admin.site.register(models.Repository)
admin.site.register(models.Project)
admin.site.register(models.Builder)


class BuildInline(admin.TabularInline):
    model = models.Build

class JobAdmin(admin.ModelAdmin):
    inlines = [
        BuildInline,
    ]

admin.site.register(models.Job, JobAdmin)

class BuildLogInline(admin.TabularInline):
    model = models.BuildLog
    fields = ('command', 'output', 'error', 'status')
    readonly_fields = ('status',)

class JobLogAdmin(admin.ModelAdmin):
    inlines = [
        BuildLogInline,
    ]

admin.site.register(models.JobLog, JobLogAdmin)

