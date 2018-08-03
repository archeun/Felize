from django.urls import path

from projectmanager import views

urlpatterns = [
    path('project_resource/<int:pk>', views.ProjectResourceUpdateView.as_view(),
         name='update_project_resource'),
    path('project_resource/create', views.ProjectResourceCreateView.as_view(),
         name='create_project_resource'),
    path('project_resource/list/<int:pk>', views.ProjectResourceListView.as_view(),
         name='project_resource_list'),
]
