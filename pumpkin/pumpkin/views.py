import threading
import time
import subprocess
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    return render(request, 'home.html', {})
