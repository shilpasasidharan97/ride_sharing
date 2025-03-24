from django.contrib.gis.db.models import PointField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class AbstractAddress(models.Model):
    """
    Abstract address fields.
    """

    label = models.CharField(
        max_length=45,
        help_text="Something like 'Southern Warehouse', or 'Mama's Kitchen' ",
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=100, help_text="flat/apartment/building name", null=True, blank=True
    )
    landmark = models.CharField(
        max_length=100, help_text=" landmark/ area roar etc", null=True, blank=True
    )
    contact_person = models.CharField(max_length=80, null=True, blank=True)
    address = models.CharField(max_length=80)
    street = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    location = PointField(null=True, blank=True)
    building_number = models.CharField(max_length=100, null=True, blank=True)
    zone = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class AbstractContactPoint(AbstractAddress):
    contact_number = PhoneNumberField()
    contact_number_secondary = PhoneNumberField(null=True, blank=True)
    contact_email = models.EmailField(blank=True, null=True)

    class Meta:
        abstract = True
