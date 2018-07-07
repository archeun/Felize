from django.urls import path

from projectmanager import views

urlpatterns = [
    # ex: /pm/organizations
    path('organizations', views.organization_list, name='organization_list'),
    # ex: /pm/organizations/5/
    path('organizations/<int:organization_id>/', views.organization_details, name='organization_details'),
]