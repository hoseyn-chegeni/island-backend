from django.db import models
from .choices import VehicleType, VehicleStatus


class Vehicle(models.Model):
    vendor = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name="vehicles")

    type = models.CharField( max_length=20,choices=VehicleType.choices)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=200)
    plate_number = models.CharField(max_length=20, unique=True)
    price_per_hour = models.PositiveIntegerField()
    price_per_day = models.PositiveIntegerField()
    status = models.CharField(max_length=20,choices=VehicleStatus.choices, default=VehicleStatus.AVAILABLE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.plate_number}"
    

from django.db import models


class VehicleImage(models.Model):
    vehicle = models.ForeignKey("vehicles.Vehicle",on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="vehicles/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Vehicle #{self.vehicle_id}"