from django.db import models


class VehicleType(models.TextChoices):
    CAR = "CAR", "Car"
    MOTORCYCLE = "MOTORCYCLE", "Motorcycle"
    VAN = "VAN", "Van"



class VehicleStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    RENTED = "RENTED", "Rented"
    MAINTENANCE = "MAINTENANCE", "Maintenance"
