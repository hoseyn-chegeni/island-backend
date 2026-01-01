from django.contrib import admin
from .models import VehicleAvailability, VehicleRental
# Register your models here.
admin.site.register(VehicleAvailability)
admin.site.register(VehicleRental)