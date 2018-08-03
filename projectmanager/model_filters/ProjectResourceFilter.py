import django_filters

from projectmanager.models import ProjectResource


class ProjectResourceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = ProjectResource
        fields = ['employee', 'resource_type']
