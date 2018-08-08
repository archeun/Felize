from django.shortcuts import render


def project_resources_chart(request):
    return render(request, 'projectmanager/reports/project_resources_chart.html')
