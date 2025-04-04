# Generated by Django 5.1.7 on 2025-03-23 13:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Driver",
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
                    models.IntegerField(
                        choices=[(0, "Inactive"), (1, "Active")],
                        default=1,
                        verbose_name="status",
                    ),
                ),
                (
                    "activate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for an immediate activation",
                        null=True,
                    ),
                ),
                (
                    "deactivate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for indefinite activation",
                        null=True,
                    ),
                ),
                (
                    "hash_of_user_phone_number",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("driver_score", models.IntegerField(default=80)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="driver",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("status", "-activate_date"),
                "abstract": False,
            },
        ),
    ]
