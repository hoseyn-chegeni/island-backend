from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import timedelta
from .models import VehicleAvailability, VehicleRental


def get_date_range(start_date, end_date):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]


@receiver(pre_save, sender=VehicleRental)
def check_vehicle_availability(sender, instance, **kwargs):
    start_date = instance.start_time.date()
    end_date = instance.end_time.date()

    dates_to_check = get_date_range(start_date, end_date)

    conflicting_dates = VehicleAvailability.objects.filter(
        vehicle=instance.vehicle, date__in=dates_to_check
    )

    if conflicting_dates.exists():
        first_conflict = conflicting_dates.first().date
        raise ValueError(
            f"Vehicle is already booked or unavailable on {first_conflict}."
        )


@receiver(post_save, sender=VehicleRental)
def block_availability_dates(sender, instance, created, **kwargs):
    if created:
        start_date = instance.start_time.date()
        end_date = instance.end_time.date()
        dates_to_block = get_date_range(start_date, end_date)

        availability_objects = [
            VehicleAvailability(vehicle=instance.vehicle, date=d)
            for d in dates_to_block
        ]
        VehicleAvailability.objects.bulk_create(
            availability_objects, ignore_conflicts=True
        )
