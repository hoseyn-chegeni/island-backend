from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import VehicleAvailability, VehicleRental

# Helper function to get dates between start and end
def get_date_range(start_date, end_date):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

@receiver(pre_save, sender=VehicleRental)
def check_vehicle_availability(sender, instance, **kwargs):
    # Convert datetimes to dates for the check
    start_date = instance.start_time.date()
    end_date = instance.end_time.date()
    
    dates_to_check = get_date_range(start_date, end_date)
    
    # Check if any of these dates are already in VehicleAvailability for THIS vehicle
    conflicting_dates = VehicleAvailability.objects.filter(
        vehicle=instance.vehicle,
        date__in=dates_to_check
    )
    
    if conflicting_dates.exists():
        # List the first conflicting date in the error message
        first_conflict = conflicting_dates.first().date
        raise ValueError(
            f"Vehicle is already booked or unavailable on {first_conflict}."
        )

@receiver(post_save, sender=VehicleRental)
def block_availability_dates(sender, instance, created, **kwargs):
    if created:
        # If the rental was successfully created, block the dates in the availability table
        start_date = instance.start_time.date()
        end_date = instance.end_time.date()
        dates_to_block = get_date_range(start_date, end_date)
        
        # Create VehicleAvailability objects for each day
        availability_objects = [
            VehicleAvailability(vehicle=instance.vehicle, date=d)
            for d in dates_to_block
        ]
        
        # bulk_create is much faster than saving one by one
        VehicleAvailability.objects.bulk_create(availability_objects, ignore_conflicts=True)