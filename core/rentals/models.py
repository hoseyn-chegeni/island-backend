from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# Create your models here.


class VehicleAvailability(models.Model):
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ("vehicle", "date")

    def clean(self):
        today = timezone.now().date()
        max_date = today + timedelta(days=90)

        if self.date < today:
            raise ValidationError("You cannot pick a date in the past.")
        if self.date > max_date:
            raise ValidationError("You can only block dates up to 90 days in advance.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This ensures clean() is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rental #{self.date} - Vehicle {self.vehicle.id}"


class VehicleRental(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey("accounts.UserV2", on_delete=models.CASCADE)
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    total_price = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rental #{self.id} - Vehicle {self.vehicle_id}"
