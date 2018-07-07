from django.shortcuts import render, get_object_or_404
from projectmanager.models import Organization


def dashboard(request):
    return render(request, 'projectmanager/base/dashboard.html')
