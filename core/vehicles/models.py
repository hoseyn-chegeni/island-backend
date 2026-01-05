from django.db import models
from .choices import VehicleType, VehicleStatus
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    vendor = models.ForeignKey(
        "accounts.Vendor", on_delete=models.CASCADE, related_name="vehicles"
    )

    type = models.CharField(max_length=20, choices=VehicleType.choices)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="vehicles")
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=200)
    plate_number = models.CharField(max_length=20, unique=True)
    price_per_hour = models.PositiveIntegerField()
    price_per_day = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=VehicleStatus.choices, default=VehicleStatus.AVAILABLE
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="vehicles"
    )
    extra_features = models.JSONField(default=dict, blank=True)
    is_top = models.BooleanField(default=False)
    primary_image = models.ImageField(
        upload_to="vehicle_primary_images/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.plate_number}"


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        "vehicles.Vehicle", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="vehicles/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Vehicle #{self.vehicle_id}"


class VehicleLocation(models.Model):
    vehicle = models.ForeignKey(
        "vehicles.Vehicle", on_delete=models.CASCADE, related_name="locations"
    )
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    manual_address = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle.id} at {self.latitude}, {self.longitude}"


class VehicleReview(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("vehicle", "user")

    def __str__(self):
        return f"Review by {self.user} for {self.vehicle} (Score: {self.score})"
