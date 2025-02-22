import django_filters

from .models import Message


class MessageFilter(django_filters.FilterSet):
    start_sent_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    end_sent_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["start_sent_date", "end_sent_date"]
