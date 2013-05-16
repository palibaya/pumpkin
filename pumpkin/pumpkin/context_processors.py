from pumpkin import models

def projects(request):
    projects = models.Project.objects.all()
    return {'projects':projects}
