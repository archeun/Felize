from django.urls import path

from projectmanager import views

urlpatterns = [
    path('', views.dashboard, name='base_dashboard'),
]