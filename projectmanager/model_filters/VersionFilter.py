import django_filters
from reversion.models import Version


class VersionFilter(django_filters.FilterSet):
    class Meta:
        model = Version
        fields = '__all__'
