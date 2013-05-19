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
admin.site.register(models.JobLog)
admin.site.register(models.BuildLog)

