from django.shortcuts import get_object_or_404, render, redirect

from pumpkin import models, forms, tasks

def home(request):

    return render(request, 'home.html', {})


def project(request, identifier):
    """
    :param request:
    :param identifier:
    :return:
    """
    project = models.Project.objects.get(identifier=identifier)
    return render(request, 'project_home.html', {
        'project': project
    })

def project_create(request):

    return render(request, 'project_create.html', {

    })

def project_jobs(request, identifier):
    project = models.Project.objects.get(identifier=identifier)
    return render(request, 'project_jobs.html', {
        'project': project,
        'jobs': project.jobs.all(),
    })

def project_job_run(request, identifier, job_id):
    job = models.Job.objects.get(id=job_id)
    tasks.run_job.delay(job)
    return redirect('pumpkin_project_jobs', identifier=identifier)


def project_job_logs(request, identifier, job_id):
    job = models.Job.objects.get(id=job_id)
    logs = job.logs.order_by('-end').all()
    return render(request, 'project_job_logs.html', {
        'project': job.project,
        'job': job,
        'logs': logs
    })

def project_configure(request, identifier):
    project = models.Project.objects.get(identifier=identifier)
    #ProjectFormset = modelformset_factory(models.Project)
    if request.method == "POST":
        project_form = forms.ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
    else:
        project_form = forms.ProjectForm(instance=project)
    return render(request, 'project_configure.html', {
        'project': project,
        'project_form': project_form,
    })
