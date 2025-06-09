import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    start_time = django_filters(
        field_name='timestamp', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(
        field_name='timestamp', lookup_expr='lte')
    sender_id = django_filters.CharFilter(field_name='sender__user_id')

    class Meta:
        model = Message
        fields = ['start_time', 'end_time', 'sender_id']
