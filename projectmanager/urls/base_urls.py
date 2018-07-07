from django.urls import path

from projectmanager import views

urlpatterns = [
    # ex: /pm
    path('', views.dashboard, name='base_dashboard'),
]