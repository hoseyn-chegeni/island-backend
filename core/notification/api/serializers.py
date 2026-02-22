# serializers.py
from rest_framework import serializers
from ..models import ReserveRequest, ReserveRequestStatus


class ReserveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveRequest
        fields = ["id", "input", "status", "created_date", "updated_date"]

    def validate_status(self, value):
        # Ensure the status is one of the predefined choices
        if value not in ReserveRequestStatus.values:
            raise serializers.ValidationError("Invalid status.")
        return value
