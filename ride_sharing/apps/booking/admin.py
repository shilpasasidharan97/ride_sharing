from apps.booking.models import Booking
from django.contrib import admin

from ride_sharing.apps.booking.models import Trip

admin.site.register(Booking)
admin.site.register(Trip)
