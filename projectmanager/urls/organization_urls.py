from django.urls import path

from projectmanager import views

urlpatterns = [
    path('organizations', views.organization_list, name='organization_list'),
    path('organizations/<int:organization_id>/', views.organization_details, name='organization_details'),
]