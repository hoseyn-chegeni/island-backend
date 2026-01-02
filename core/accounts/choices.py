from django.db import models


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class VendorType(models.TextChoices):
    INDIVIDUAL = "IND", "Individual"
    COMPANY = "COM", "Company"


class VendorStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    SUSPENDED = "SUSPENDED", "Suspended"
