from apps.booking.api.views import (
    BookingViewSet,
    CreateBookingAPIView,
    TripConfirmView,
    TripStatusUpdateAPI,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"bookings", BookingViewSet, basename="booking")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "booking/",
        include(
            [
                path(
                    "create/",
                    CreateBookingAPIView.as_view(),
                    name="operator_apis.create_booking",
                ),
            ]
        ),
    ),
    path(
        "trip/",
        include(
            [
                path(
                    "confirm/", TripConfirmView.as_view(), name="booking_alert_confirm"
                ),
                path(
                    "<int:pk>/start-trip/",
                    TripStatusUpdateAPI.as_view(),
                    name="driver-start-trip",
                ),
            ]
        ),
    ),
]
