from .base_urls import urlpatterns as base_urlpatterns
from .organization_urls import urlpatterns as organization_urlpatterns
from .project_urls import urlpatterns as project_urlpatterns
from .project_resources_urls import urlpatterns as task_breakdown_urlpatterns
from .work_entries_urls import urlpatterns as work_entries_urlpatterns
from .api_urls import urlpatterns as api_urlpatterns
from .report_urls import urlpatterns as report_urlpatterns
from .sprint_milestones_urls import urlpatterns as sprint_milestones_urlpatterns

app_name = 'projectmanager'
urlpatterns = base_urlpatterns \
              + organization_urlpatterns \
              + project_urlpatterns \
              + task_breakdown_urlpatterns \
              + work_entries_urlpatterns \
              + api_urlpatterns \
              + report_urlpatterns \
              + sprint_milestones_urlpatterns
