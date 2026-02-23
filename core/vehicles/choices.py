from django.db import models


class VehicleType(models.TextChoices):
    # Land Vehicles
    CAR = "CAR", "Car"
    SCOOTER = "SCOOTER", "Scooter"
    MOTORBIKE = "MOTORBIKE", "Motorbike"
    BICYCLE = "BICYCLE", "Bicycle"
    ATV_QUAD = "ATV_QUAD", "ATV / Quad"
    BUGGY = "BUGGY", "Dune Buggy"

    # Water Vehicles
    JET_SKI = "JET_SKI", "Jet Ski"
    BOAT = "BOAT", "Motor Boat"
    KAYAK = "KAYAK", "Kayak / Canoe"
    YACHT = "YACHT", "Yacht"


class VehicleStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    RENTED = "RENTED", "Rented"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
