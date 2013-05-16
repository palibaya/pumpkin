import threading
import time
import subprocess
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from pumpkin import models
from pumpkin import forms

def home(request):

    return render(request, 'home.html', {})


def project(request, identifier):
    project = models.Project.objects.get(identifier=identifier)
    return render(request, 'project.html', {
        'project': project
    })

def project_jobs(request, identifier):
    project = models.Project.objects.get(identifier=identifier)
    return render(request, 'project_jobs.html', {
        'project': project
    })

def project_configure(request, identifier):
    project = models.Project.objects.get(identifier=identifier)
    project_form = forms.ProjectForm(instance=project)
    #ProjectFormset = modelformset_factory(models.Project)
    #if request.method == "POST":
        #formset = ProjectFormset(request.POST, request.FILES,
                                 #queryset=models.Project\
                                #.objects.filter(identifier=identifier))
        #if formset.is_valid():
            #formset.save()
    #else:
        #formset = ProjectFormset(queryset=models.Project\
                                 #.objects.filter(identifier=identifier))

    return render(request, 'project_configure.html', {
        'project': project,
        'project_form': project_form,
    })
