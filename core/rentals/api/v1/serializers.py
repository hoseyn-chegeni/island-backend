from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from rentals.models import VehicleAvailability

class VehicleAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAvailability
        fields = ['id', 'vehicle', 'date']
