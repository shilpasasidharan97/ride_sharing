from apps.booking.models import Booking
from apps.customer.models import Customer
from django.db.models import F, Value
from django.db.models.functions import Concat
from django_filters import rest_framework as filters


class BookingFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    status = filters.ChoiceFilter(choices=Booking.status.field.choices)
    customer = filters.ModelChoiceFilter(
        queryset=Customer.objects.all(), null_label="Any"
    )
    customer_name = filters.CharFilter(method="filter_by_customer_name")

    def filter_by_customer_name(self, queryset, name, value):
        return queryset.annotate(
            full_name=Concat(
                F("customer__user__first_name"),
                Value(" "),
                F("customer__user__last_name"),
            )
        ).filter(full_name__icontains=value)

    class Meta:
        model = Booking
        fields = ["created_at", "status", "customer_name"]
