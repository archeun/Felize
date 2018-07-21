from django.urls import path

from projectmanager import views

urlpatterns = [
    path('task_breakdown/project_resource/<int:pk>', views.ProjectResourceTaskUpdate.as_view(),
         name='update_project_resource_task_breakdown'),
    path('task_breakdown/project_resource/create', views.ProjectResourceTaskCreate.as_view(),
         name='create_project_resource_task_breakdown'),
]
