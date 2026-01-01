from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from rentals.models import VehicleAvailability, VehicleRental

class VehicleAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAvailability
        fields = ['id', 'vehicle', 'date']



class VehicleRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRental
        fields = '__all__'
        read_only_fields = ['total_price', 'status', 'created_at']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        vehicle = data.get('vehicle')

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        today = timezone.now().date()
        max_date = today + timedelta(days=90)
        if start_time > max_date:
            raise serializers.ValidationError(f"You can only book up to 90 days in advance (until {max_date}).")

        delta = end_time - start_time
        days_to_check = [start_time + timedelta(days=i) for i in range(delta.days + 1)]
        
        conflicts = VehicleAvailability.objects.filter(
            vehicle=vehicle,
            date__in=days_to_check
        ).exists()

        if conflicts:
            raise serializers.ValidationError("One or more dates in your selection are already booked.")

        return data

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        start = validated_data['start_time']
        end = validated_data['end_time']
        
        duration = end - start
        hours = duration.total_seconds() / 3600
        days = duration.days if duration.days > 0 else 1
        
        if hours > 24:
            validated_data['total_price'] = days * vehicle.price_per_day
        else:
            validated_data['total_price'] = int(hours) * vehicle.price_per_hour
            
        return super().create(validated_data)