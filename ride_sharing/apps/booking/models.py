from apps.utils.exception import InvalidTripStatus
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class BookingPathPoint(models.Model):
    """
    BookingPathPoint model stores the points for a booking trip in the order of points to visit along with labels.
    """

    LABEL_PICKUP = "PickUpLocation"
    LABEL_DROP_OFF = "DeliveryOffLocation"

    label = models.CharField(
        max_length=120,
        choices=[
            (LABEL_PICKUP, LABEL_PICKUP),
            (LABEL_DROP_OFF, LABEL_DROP_OFF),
        ],
        help_text=(
            "Either how customer wants it, ie: labels will be like PickUpLocation, "
            "DeliveryOffLocation"
        ),
    )
    point = PointField()  # geo-location.
    address = models.ForeignKey(
        "user.ContactPointAddress", on_delete=models.SET_NULL, null=True, blank=True
    )
    location = models.CharField(
        max_length=120, help_text="Just to know the location", null=True, blank=True
    )
    display_order = models.PositiveSmallIntegerField(default=100)
    # country = CountryField()

    def __str__(self):
        return self.label

    class Meta:
        ordering = ("display_order",)


class Booking(TimeStampedModel):
    """
    Stores and Manages Booking.
    Considering Each Booking as a Consignment.
    """

    # payment type
    CREDIT = "credit"
    CASH = "cash"
    ONLINE = "online"

    # booking type
    IMPORT = "import"
    EXPORT = "export"
    LOCAL = "local"

    STATUS_PLANNING = "planning"
    STATUS_ONGOING = "ongoing"
    STATUS_HALT = "halt"
    STATUS_PARTIALLY_COMPLETED = "partially-completed"
    STATUS_COMPLETED = "completed"

    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    # in case we do not have customer, we need to collect them
    customer_email = models.CharField(max_length=30, null=True, blank=True)
    customer_contact = PhoneNumberField(null=True, blank=True)
    customer_name = models.CharField(max_length=30, null=True, blank=True)
    customer_location = models.CharField(max_length=30, null=True, blank=True)

    # initial booking fields
    booking_flow = models.CharField(
        max_length=10,
        choices=[
            (IMPORT, IMPORT),
            (EXPORT, EXPORT),
            (LOCAL, LOCAL),
        ],
        default=LOCAL,
    )
    path = models.ManyToManyField(
        "BookingPathPoint",
        help_text="Connects to path from initial point to final point.",
    )

    payment_type = models.CharField(
        max_length=8,
        choices=[
            (CREDIT, CREDIT),
            (CASH, CASH),
            (ONLINE, ONLINE),
        ],
        default=CREDIT,
    )

    billing_address = models.ForeignKey(
        "user.Address", on_delete=models.CASCADE, null=True, blank=True
    )
    recommended_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0
    )
    base_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0
    )
    final_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False, default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_bookings",
    )

    status = models.CharField(
        db_index=True,
        max_length=30,
        choices=[
            (STATUS_PLANNING, "Trip Planning"),
            (STATUS_ONGOING, "Ongoing"),
            (STATUS_HALT, "Halt / Cancelled"),
            (STATUS_PARTIALLY_COMPLETED, "Partially Completed"),
            (STATUS_COMPLETED, "Completed"),
        ],
        default=STATUS_PLANNING,
        help_text="This status is just for a reference and status should be dependent on corresponding Trips.",
    )

    def update_final_amount(
        self, base_charge=0, additional_charges=0, discount=0, request_user=None
    ):
        if base_charge:
            self.base_amount = base_charge
        self.final_amount = self.base_amount + additional_charges - discount
        self.save()


class Trip(models.Model):

    TRIP_CREATED = "initial"
    TRIP_ONGOING = "ongoing"
    TRIP_COMPLETED = "completed"
    TRIP_HALT = "halt"  # cancelled

    # trip ongoing statues
    TRIP_LOCATION_REACHED = "pickup_reached"

    TRIP_LOCATION_PICKUP_DEPART = "pickup_departed"

    TRIP_REACHED_DROPOFF = "dropoff_reached"

    TRIP_LOCATION_REACHED_DEPART = "dropoff_departed"

    driver = models.ForeignKey(
        "driver.Driver", on_delete=models.SET_NULL, null=True, blank=True
    )
    booking = models.OneToOneField(
        "Booking", on_delete=models.CASCADE, related_name="trip", null=True, blank=True
    )

    status = models.CharField(
        db_index=True,
        max_length=30,
        choices=[
            (TRIP_CREATED, "Initial"),
            (TRIP_ONGOING, "Ongoing"),
            (TRIP_COMPLETED, "Completed"),
            (TRIP_HALT, "Halt"),
        ],
        default=TRIP_CREATED,
    )

    ongoing_status = models.CharField(
        db_index=True,
        max_length=30,
        choices=[
            (TRIP_LOCATION_REACHED, "Reached Pickup Location"),
            (TRIP_REACHED_DROPOFF, "Reached Dropoff Location"),
            (TRIP_LOCATION_PICKUP_DEPART, "pickup_departed"),
            (TRIP_LOCATION_REACHED_DEPART, "dropoff_departed"),
        ],
        blank=True,
        null=True,
    )

    completed_statuses = (TRIP_COMPLETED, TRIP_HALT)

    created_at = models.DateTimeField(auto_now_add=True)
    driver_assigned_at = models.DateTimeField(null=True, blank=True)

    pipeline = {
        TRIP_CREATED: (
            TRIP_ONGOING,
            TRIP_HALT,
        ),
        TRIP_ONGOING: (
            TRIP_ONGOING,
            TRIP_COMPLETED,
            TRIP_HALT,
        ),
        TRIP_COMPLETED: (),
        TRIP_HALT: (),
    }

    ongoing_pipeline = {
        None: (TRIP_LOCATION_REACHED,),
        TRIP_LOCATION_REACHED: (TRIP_LOCATION_PICKUP_DEPART,),
        # TRIP_LOADING_GOODS: (TRIP_REACHED_DROPOFF, ),
        TRIP_LOCATION_PICKUP_DEPART: (TRIP_REACHED_DROPOFF,),
        TRIP_REACHED_DROPOFF: (TRIP_LOCATION_REACHED_DEPART,),
    }

    def set_ongoing_status(
        self, new_status, point, request_user=None, description=None
    ):
        old_status = self.ongoing_status

        if old_status == new_status:
            return
        if old_status and new_status not in self.ongoing_pipeline[old_status]:
            raise InvalidTripStatus(
                "'%(new_status)s' is not a valid status for this trip "
                "(current status: '%(old_status)s')"
                % (
                    {
                        "new_status": new_status,
                        "status": self.status,
                    }
                )
            )
        self.ongoing_status = new_status
        self.save()

        ongoing_terminal_map = {
            self.TRIP_LOCATION_REACHED: "arrived",
            self.TRIP_LOCATION_PICKUP_DEPART: "departed",
            self.TRIP_REACHED_DROPOFF: "arrived",
            self.TRIP_LOCATION_REACHED_DEPART: "departed",
        }

    def set_booking_status(self, request_user=None, desc=None):
        update_status = lambda current_statuses, new_status, request_user, desc: [
            booking.set_status(
                new_status,
                description=desc or "Trip status got updated.",
                request_user=request_user,
            )
            for booking in self.all_bookings().filter(status__in=current_statuses)
        ]

        if self.status == Trip.TRIP_CREATED:
            pass
        elif self.status == Trip.TRIP_ONGOING:
            update_status(
                current_statuses=[Booking.STATUS_PLANNING],
                new_status=Booking.STATUS_ONGOING,
                request_user=request_user,
                desc=desc,
            )
        elif self.status == Trip.TRIP_COMPLETED:
            for booking in self.all_bookings():
                new_status = Booking.STATUS_PARTIALLY_COMPLETED
                if booking.check_num_trips_pending_to_complete() == 0:
                    new_status = Booking.STATUS_COMPLETED
                update_status(
                    current_statuses=[
                        Booking.STATUS_ONGOING,
                        Booking.STATUS_PARTIALLY_COMPLETED,
                    ],
                    new_status=new_status,
                    request_user=request_user,
                    desc=desc,
                )

        elif self.status == Trip.TRIP_HALT:
            update_status(
                current_statuses=[
                    Booking.STATUS_ONGOING,
                    Booking.STATUS_PLANNING,
                ],
                new_status=Booking.STATUS_HALT,
                request_user=request_user,
                desc=desc,
            )

    def set_status(self, new_status, request_user=None, description=None):
        old_status = self.status

        # HOOKS FOR PRE_STATUS_UPDATE
        if old_status == new_status:
            return
        if new_status not in self.pipeline[old_status]:
            raise InvalidTripStatus(
                "'%(new_status)s' is not a valid status for this trip "
                "(current status: '%(status)s')"
                % (
                    {
                        "new_status": new_status,
                        "status": self.status,
                    }
                )
            )

        self.status = new_status
        self.save()

        # HOOKS FOR POST_STATUS_UPDATE
        self.status_logs.create(
            old_status=old_status,
            new_status=new_status,
            updated_by=request_user,
        )

        self.set_booking_status(request_user, description)


class TripStatusLog(models.Model):
    """
    Setting Trip Logs.
    """

    trip = models.ForeignKey(
        "Trip", on_delete=models.CASCADE, related_name="status_logs"
    )
    old_status = models.CharField(max_length=30)
    new_status = models.CharField(max_length=30)

    description = models.TextField(null=True, blank=True)
    updated_by = models.ForeignKey(
        "user.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
