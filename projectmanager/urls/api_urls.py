from django.urls import path

from projectmanager import views

urlpatterns = [
    path('api/reports/project_resources', views.ProjectResourcesChartJsView.as_view(),
         name='api_reports_project_resources'),
    path('api/dashboard/pending_item_data', views.DashboardPendingItemsPanelDataView.as_view(),
         name='api_dashboard_pending_item_data'),
]
