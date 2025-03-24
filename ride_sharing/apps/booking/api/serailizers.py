from apps.booking.models import Booking, BookingPathPoint, Trip
from apps.user.api.serializers import ContactAddressSerializer
from apps.user.models import ContactPointAddress, User
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class BookingPathPointSerializer(GeoFeatureModelSerializer):
    address = ContactAddressSerializer()

    def validate(self, attrs):
        if "point" not in attrs:
            raise serializers.ValidationError("Either 'point'")
        return attrs

    class Meta:
        model = BookingPathPoint
        geo_field = "point"
        fields = (
            "id",
            "label",
            "point",
            "location",
            "display_order",
            "address",
        )


class BookingSerializer(serializers.ModelSerializer):
    path = BookingPathPointSerializer(many=True)
    customer_profile_picture = serializers.ImageField(
        read_only=True, source="customer.user.profile_picture"
    )
    customer_mobile_number = serializers.ReadOnlyField(
        read_only=True, source="customer.user.mobile_number.as_international"
    )
    base_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )
    new_status = serializers.ChoiceField(
        choices=Booking.status.field.choices, write_only=True, required=False
    )

    @transaction.atomic()
    def create(self, validated_data):
        paths = validated_data.pop("path")
        booking = Booking.objects.create(**validated_data)
        if "base_amount" in validated_data:
            booking.update_final_amount(
                base_charge=validated_data["base_amount"],
                request_user=self.context["request"].user,
            )
        is_customer = self.context["request"].user.user_role == User.CUSTOMER
        print(is_customer, "*********************")
        # customer can only create booking for himself
        if is_customer:
            booking.customer = self.context["request"].customer

        for path in paths:
            addr_data = path.pop("address")
            cpa = ContactPointAddress.objects.create(**addr_data)

            p = BookingPathPoint.objects.create(address=cpa, **path)
            booking.path.add(p)

        booking.save()
        return booking

    @transaction.atomic()
    def update(self, instance, validated_data):
        base_amount = validated_data.pop("base_amount", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if base_amount:
            instance.update_final_amount(
                base_amount, request_user=self.context["request"].user
            )
        instance.save()
        return instance

    class Meta:
        model = Booking
        fields = (
            "id",
            "customer",
            "customer_email",
            "customer_name",
            "customer_location",
            "path",
            "created_at",
            "payment_type",
            "billing_address",
            "customer_mobile_number",
            "new_status",
            "status",
            "customer_profile_picture",
            "final_amount",
            "base_amount",
        )

        extra_kwargs = {"payment_type": {"required": True}}


class TripConfirmSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all(), required=True, write_only=True
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "driver",
            "booking",
            "status",
            "created_at",
            "driver_assigned_at",
            "booking_id",
        ]
        read_only_fields = [
            "id",
            "driver",
            "status",
            "created_at",
            "driver_assigned_at",
        ]

    def validate_booking(self, booking):
        """Ensure the booking exists and is available for a trip."""
        if booking.status != Booking.STATUS_PLANNING:
            raise serializers.ValidationError(
                "Booking is not available or doesn't exist."
            )

        if Trip.objects.filter(booking=booking).exists():
            raise serializers.ValidationError("A trip already exists for this booking.")

        return booking

    def create(self, validated_data):
        driver = self.context["request"].user.driver
        booking = validated_data["booking_id"]

        with transaction.atomic():
            # Create the trip
            trip = Trip.objects.create(
                booking=booking,
                driver=driver,
                status=Trip.TRIP_CREATED,
                driver_assigned_at=timezone.now(),
            )

            # Update booking status
            booking.status = Booking.STATUS_ONGOING
            booking.save(update_fields=["status"])

        return trip


class TripStatusUpdateSerializer(serializers.ModelSerializer):
    point = serializers.PrimaryKeyRelatedField(
        queryset=BookingPathPoint.objects.all(), many=False, write_only=True
    )
    description = serializers.CharField(required=False, write_only=True)

    def validate(self, attrs):
        status = attrs.get("status")
        ongoing_status = attrs.get("ongoing_status")
        driver = getattr(self.context["request"], "driver_profile", None)

        if status == Trip.TRIP_ONGOING:
            ongoing_trip = Trip.objects.filter(
                driver=driver, status=Trip.TRIP_ONGOING
            ).exists()
            if ongoing_trip:
                raise serializers.ValidationError(
                    {
                        "status": "You already have an ongoing trip. Cannot start another trip."
                    }
                )

        if ongoing_status is not None:
            point = attrs.get("point")
            attrs.get("action")

            if not point:
                raise serializers.ValidationError({"point": "This field is required."})

        if not self.instance:
            raise serializers.ValidationError("Update only Serializer!")
        if status and status not in Trip.pipeline[self.instance.status]:
            raise serializers.ValidationError(
                {
                    "status": "'%(new_status)s' is not a valid status for this trip at this point"
                    "(current status: '%(status)s')"
                    % (
                        {
                            "new_status": status,
                            "status": self.instance.status,
                        }
                    )
                }
            )
        if (
            ongoing_status
            and ongoing_status
            not in Trip.ongoing_pipeline[self.instance.ongoing_status]
        ):
            raise serializers.ValidationError(
                {
                    "ongoing_status": "'%(new_status)s' is not a valid status for this trip at this point"
                    "(current status: '%(status)s')"
                    % (
                        {
                            "new_status": status,
                            "status": self.instance.ongoing_status,
                        }
                    )
                }
            )

        return attrs

    class Meta:
        model = Trip
        fields = (
            "status",
            "ongoing_status",
            "point",
            "description",
        )

    def create(self, validated_data):
        raise serializers.ValidationError("Update only Serializer!")

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        ongoing_status = validated_data.get("ongoing_status")
        point = validated_data.get("point")
        description = validated_data.get("description", "")
        if status:
            instance.set_status(
                status,
                request_user=self.context["request"].user,
                description=description,
            )
        if ongoing_status:
            instance.set_ongoing_status(
                ongoing_status, point, request_user=self.context["request"].user
            )
        return instance
