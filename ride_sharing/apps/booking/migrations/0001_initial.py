# Generated by Django 5.1.7 on 2025-03-23 15:48

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django_extensions.db.fields
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customer", "0001_initial"),
        ("driver", "0001_initial"),
        ("user", "0002_address_contactpointaddress"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BookingPathPoint",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        choices=[
                            ("PickUpLocation", "PickUpLocation"),
                            ("DeliveryOffLocation", "DeliveryOffLocation"),
                        ],
                        help_text="Either how customer wants it, ie: labels will be like PickUpLocation, DeliveryOffLocation",
                        max_length=120,
                    ),
                ),
                ("point", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Just to know the location",
                        max_length=120,
                        null=True,
                    ),
                ),
                ("display_order", models.PositiveSmallIntegerField(default=100)),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="user.contactpointaddress",
                    ),
                ),
            ],
            options={
                "ordering": ("display_order",),
            },
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "customer_email",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                (
                    "customer_contact",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                (
                    "customer_name",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                (
                    "customer_location",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                (
                    "booking_flow",
                    models.CharField(
                        choices=[
                            ("import", "import"),
                            ("export", "export"),
                            ("local", "local"),
                        ],
                        default="local",
                        max_length=10,
                    ),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("credit", "credit"),
                            ("cash", "cash"),
                            ("online", "online"),
                        ],
                        default="credit",
                        max_length=8,
                    ),
                ),
                (
                    "recommended_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "base_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "final_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("planning", "Trip Planning"),
                            ("ongoing", "Ongoing"),
                            ("halt/cancelled", "Halt / Cancelled"),
                            ("partially-completed", "Partially Completed"),
                            ("completed", "Completed"),
                        ],
                        db_index=True,
                        default="planning",
                        help_text="This status is just for a reference and status should be dependent on corresponding Trips.",
                        max_length=30,
                    ),
                ),
                (
                    "billing_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.address",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_bookings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="customer.customer",
                    ),
                ),
                (
                    "path",
                    models.ManyToManyField(
                        help_text="Connects to path from initial point to final point.",
                        to="booking.bookingpathpoint",
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("initial", "Initial"),
                            ("ongoing", "Ongoing"),
                            ("completed", "Completed"),
                            ("halt", "Halt"),
                        ],
                        db_index=True,
                        default="initial",
                        max_length=30,
                    ),
                ),
                (
                    "ongoing_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("pickup_reached", "Reached Pickup Location"),
                            ("dropoff_reached", "Reached Dropoff Location"),
                            ("pickup_departed", "pickup_departed"),
                            ("dropoff_departed", "dropoff_departed"),
                        ],
                        db_index=True,
                        max_length=30,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("driver_assigned_at", models.DateTimeField(blank=True, null=True)),
                (
                    "driver",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="driver.driver",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TripStatusLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("old_status", models.CharField(max_length=30)),
                ("new_status", models.CharField(max_length=30)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="status_logs",
                        to="booking.trip",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
