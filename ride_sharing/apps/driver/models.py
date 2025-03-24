from apps.user.models import User
from django.conf import settings
from django.db import models
from django_extensions.db.models import ActivatorModel

# Create your models here.


class Driver(ActivatorModel):

    STATUS__ACTIVE = ActivatorModel.ACTIVE_STATUS
    STATUS__BANNED = 125
    STATUS__REJECTED = 126
    STATUS__DISCONTINUED = 127

    STATUS_CHOICES = (
        (STATUS__ACTIVE, "Active"),
        (STATUS__BANNED, "Banned"),
        (STATUS__REJECTED, "Rejected"),
        (STATUS__DISCONTINUED, "Discontinued"),
    )

    user: User = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="driver",
        null=True,
    )

    hash_of_user_phone_number = models.CharField(max_length=128, null=True, blank=True)
    driver_score = models.IntegerField(default=80)

    def __str__(self):
        return self.label()
