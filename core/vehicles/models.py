from django.db import models
from .choices import VehicleType, VehicleStatus


class Vehicle(models.Model):
    vendor = models.ForeignKey("accounts.Vendor",on_delete=models.CASCADE,related_name="vehicles")

    type = models.CharField( max_length=20,choices=VehicleType.choices)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=200)
    plate_number = models.CharField(max_length=20, unique=True)
    price_per_hour = models.PositiveIntegerField()
    price_per_day = models.PositiveIntegerField()
    status = models.CharField(max_length=20,choices=VehicleStatus.choices, default=VehicleStatus.AVAILABLE)
    extra_features = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.plate_number}"
    


class VehicleImage(models.Model):
    vehicle = models.ForeignKey("vehicles.Vehicle",on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="vehicles/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Vehicle #{self.vehicle_id}"
    


class VehicleLocation(models.Model):
    vehicle = models.ForeignKey("vehicles.Vehicle",on_delete=models.CASCADE,related_name="locations")
    name = models.CharField(max_length = 255)
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.vehicle.id} at {self.latitude}, {self.longitude}"
