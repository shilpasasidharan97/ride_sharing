from apps.user.abstract_models import AbstractAddress, AbstractContactPoint
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
    """
    User Account which handles login and other authorization.
    """

    # User Role
    ADMIN_STAFF = 10
    DRIVER = 30
    CUSTOMER = 40
    DEFAULT = 100

    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("Unknown", "Unknown"),
    ]

    mobile_number = PhoneNumberField()
    email = models.EmailField(blank=True, null=True)
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="display_pictures/"
    )
    user_role = models.PositiveSmallIntegerField(
        choices=[
            (DRIVER, "Driver"),
            (CUSTOMER, "Customer"),
        ],
        default=DEFAULT,
        db_index=True,
    )
    blood_group = models.CharField(
        max_length=10,
        choices=BLOOD_GROUP_CHOICES,
        default="Unknown",
        help_text="Driver's blood group",
    )

    objects = UserManager()
    REQUIRED_FIELDS = ["mobile_number", "user_role", "password"]

    def __str__(self):
        return f"{self.username} ({self.role()})"

    def save(self, *args, **kwargs):
        if not self.username and self.mobile_number:
            self.username = self.mobile_number
        super().save(*args, **kwargs)

    def role(self):
        role_mappings = {
            self.ADMIN_STAFF: "admin",
            self.DRIVER: "driver",
            self.CUSTOMER: "customer",
            self.DEFAULT: "default",
        }

        return role_mappings.get(self.user_role, "default")

    def role_label(self):
        role_mappings = {
            self.ADMIN_STAFF: "Admin Staff",
            self.DRIVER: " Driver",
            self.CUSTOMER: "Customer",
            self.DEFAULT: "default",
        }

        return role_mappings.get(self.user_role, "default")

    def user_role_label(self):
        return self.get_user_role_display()


class Address(AbstractAddress):
    pass


class ContactPointAddress(AbstractContactPoint):
    pass
