from django.urls import path

from projectmanager import views

urlpatterns = [
    path('projects', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_details'),
]