from django.urls import path

from projectmanager import views

urlpatterns = [
    # ex: /pm/projects

    path('projects', views.ProjectListView.as_view(), name='project_list'),
    # ex: /pm/projects/5/
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_details'),
]