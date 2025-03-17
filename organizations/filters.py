import django_filters
from .models import Organization


class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Organization
        fields = {
            'name': ['exact', 'icontains'],
            'owner__username': ['exact', 'icontains'],
            'created_at': ['exact', 'gt', 'lt'],
        }
