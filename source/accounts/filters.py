import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model


class StudentFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(method='my_custom_filter', label='')

    class Meta:
        model = get_user_model()
        fields = ['student']

    def my_custom_filter(self, queryset, name, value):
        parts = value.split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''
        if first_name and last_name:
            queryset = get_user_model().objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name,
                role='user',
                enrolled_courses__isnull=False
            ).distinct()
        else:
            queryset = get_user_model().objects.none()
        return queryset
