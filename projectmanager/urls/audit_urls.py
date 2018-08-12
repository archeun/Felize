from django.urls import path

from projectmanager import views

urlpatterns = [
    path('audit/list', views.AuditListView.as_view(), name='audit_list'),
    path('audit/details/<int:pk>', views.AuditDetailView.as_view(), name='audit_detail'),
]
