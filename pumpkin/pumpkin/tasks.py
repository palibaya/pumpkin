from celery import task

@task
def add(x, y):
    return x + y

@task
def project_setup(project):
    project.setup()

@task
def run_job(job):
    job.run()
    return job.last_run()
