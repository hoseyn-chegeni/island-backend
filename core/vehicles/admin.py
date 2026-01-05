from django.contrib import admin
from .models import (
    Vehicle,
    VehicleImage,
    VehicleLocation,
    Category,
    Brand,
    VehicleReview,
)

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleImage)
admin.site.register(VehicleLocation)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(VehicleReview)
