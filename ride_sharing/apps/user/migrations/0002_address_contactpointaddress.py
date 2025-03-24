# Generated by Django 5.1.7 on 2025-03-23 15:45

import django.contrib.gis.db.models.fields
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                        blank=True,
                        help_text="Something like 'Southern Warehouse', or 'Mama's Kitchen' ",
                        max_length=45,
                        null=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="flat/apartment/building name",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "landmark",
                    models.CharField(
                        blank=True,
                        help_text=" landmark/ area roar etc",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "contact_person",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                ("address", models.CharField(max_length=80)),
                ("street", models.CharField(blank=True, max_length=80, null=True)),
                ("city", models.CharField(blank=True, max_length=30, null=True)),
                ("state", models.CharField(blank=True, max_length=30, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                (
                    "building_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("zone", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ContactPointAddress",
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
                        blank=True,
                        help_text="Something like 'Southern Warehouse', or 'Mama's Kitchen' ",
                        max_length=45,
                        null=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="flat/apartment/building name",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "landmark",
                    models.CharField(
                        blank=True,
                        help_text=" landmark/ area roar etc",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "contact_person",
                    models.CharField(blank=True, max_length=80, null=True),
                ),
                ("address", models.CharField(max_length=80)),
                ("street", models.CharField(blank=True, max_length=80, null=True)),
                ("city", models.CharField(blank=True, max_length=30, null=True)),
                ("state", models.CharField(blank=True, max_length=30, null=True)),
                ("zipcode", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, null=True, srid=4326
                    ),
                ),
                (
                    "building_number",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("zone", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "contact_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None
                    ),
                ),
                (
                    "contact_number_secondary",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
