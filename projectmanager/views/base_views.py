from django.shortcuts import render, get_object_or_404
from projectmanager.models import Organization

from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, 'projectmanager/base/dashboard.html')
