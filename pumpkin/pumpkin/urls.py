from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from pumpkin.wizards import NEW_PROJECT_FORMS, NewProjectWizard

admin.autodiscover()

urlpatterns = patterns('pumpkin.views',
    url(r'^$','home', name='home'),
)


urlpatterns += patterns('',

    # Examples:
    # url(r'^pumpkin/', include('pumpkin.foo.urls')),
    url(r'^project/create/$',
        NewProjectWizard.as_view(NEW_PROJECT_FORMS)),
    url(r'^project/(?P<identifier>\w+)$', 'pumpkin.views.project'),
    url(r'^project/(?P<identifier>\w+)/configure$',
        'pumpkin.views.project_configure'),

    url(r'^project/(?P<identifier>\w+)/jobs$',
        'pumpkin.views.project_jobs', name='pumpkin_project_jobs'),

    url(r'^project/(?P<identifier>\w+)/job/create$',
        'pumpkin.views.project_job_create', name='pumpkin_project_job_create'),

    url(r'^project/(?P<identifier>\w+)/job/(?P<job_id>\d+)/run$',
        'pumpkin.views.project_job_run', name='pumpkin_project_job_run'),

    url(r'^project/(?P<identifier>\w+)/job/(?P<job_id>\d+)/logs$',
        'pumpkin.views.project_job_logs'),

    url(r'accounts/', include('django.contrib.auth.urls')),

    #url(r'^git/', include('django_git.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
