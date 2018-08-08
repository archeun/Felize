from django.urls import path

from projectmanager import views

urlpatterns = [
    path('reports/project_resources', views.project_resources_chart, name='reports_project_resources'),
]
