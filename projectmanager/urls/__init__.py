from .base_urls import urlpatterns as base_urlpatterns
from .organization_urls import urlpatterns as organization_urlpatterns

urlpatterns = base_urlpatterns + organization_urlpatterns
