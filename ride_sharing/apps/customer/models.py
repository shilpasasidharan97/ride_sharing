from apps.utils.hashing import hash_contact_number
from django.conf import settings
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    """
    Customer Profile.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="customer",
    )
    hash_of_user_phone_number = models.CharField(max_length=128, null=True, blank=True)

    business_name = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = PhoneNumberField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_customers",
    )
    created = CreationDateTimeField("created", null=True)
    modified = ModificationDateTimeField("modified", null=True)

    @property
    def get_account_label(self):
        return f"Customer: {self.user.get_full_name() if self.user else 'Unknown Customer'}"

    def save(self, **kwargs):
        if self.user_id and self.user.mobile_number:
            self.hash_of_user_phone_number = hash_contact_number(
                self.user.mobile_number.as_international
            )
        elif self.mobile_number:
            self.hash_of_user_phone_number = hash_contact_number(
                self.mobile_number.as_international
            )
        super().save(**kwargs)
