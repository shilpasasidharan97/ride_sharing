from apps.booking.api.serailizers import (
    BookingSerializer,
    TripConfirmSerializer,
    TripStatusUpdateSerializer,
)
from apps.booking.filters import BookingFilter
from apps.booking.models import Booking, Trip
from apps.user.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CreateBookingAPIView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BookingSerializer
    queryset = Booking.objects.none()


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = BookingSerializer
    filterset_class = BookingFilter

    def get_queryset(self):
        user = self.request.user
        if user.user_role == User.CUSTOMER:
            return Booking.objects.filter(customer__user=user)

        if user.user_role in User.DRIVER:
            return Booking.objects.filter(status=Booking.STATUS_PLANNING)
        return Booking.objects.none()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            request.user.user_role == User.CUSTOMER
            and instance.customer.user != request.user
        ):
            return Response(
                {"error": "You do not have permission to view this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if (
            request.user.user_role == User.CUSTOMER
            and instance.status != Booking.STATUS_PLANNING
        ):
            return Response(
                {"error": "You can only update bookings that are in trip planning."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)


class TripConfirmView(CreateAPIView):
    """
    API for drivers to accept a booking and create a trip.
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TripConfirmSerializer

    def perform_create(self, serializer):
        driver = getattr(self.request.user, "driver", None)

        if not driver:
            raise ValidationError({"driver": "User is not registered as a driver."})

        serializer.save(driver=driver)


class TripStatusUpdateAPI(UpdateAPIView):
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TripStatusUpdateSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(driver__user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response = serializer.data
        return Response({"respobse": response})
