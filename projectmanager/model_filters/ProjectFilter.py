import django_filters

from projectmanager.models import Project


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Project
        fields = ['code', 'name', 'client']
