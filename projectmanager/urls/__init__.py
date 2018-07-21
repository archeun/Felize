from .base_urls import urlpatterns as base_urlpatterns
from .organization_urls import urlpatterns as organization_urlpatterns
from .project_urls import urlpatterns as project_urlpatterns
from .task_breakdown_urls import urlpatterns as task_breakdown_urlpatterns

app_name = 'projectmanager'
urlpatterns = base_urlpatterns + organization_urlpatterns + project_urlpatterns + task_breakdown_urlpatterns
