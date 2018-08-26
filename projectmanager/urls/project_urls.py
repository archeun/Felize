from django.urls import path

from projectmanager import views

urlpatterns = [
    path('projects/create', views.ProjectCreateView.as_view(), name='create_project'),
    path('projects/list', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectUpdateView.as_view(), name='update_project'),
    path('projects/<int:pk>/worksheet', views.ProjectWorksheetView.as_view(), name='project_worksheet'),
]