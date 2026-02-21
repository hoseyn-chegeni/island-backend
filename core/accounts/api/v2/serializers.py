from rest_framework import serializers
from ...models import UserV2
from django.core.exceptions import ValidationError
from notification.models import Otp
class UserV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserV2
        fields = ['phone_number']

    def validate_phone_number(self, value):
        # Ensure that the phone number is valid (length check as an example, you can customize it)
        if len(value) < 10:
            raise ValidationError("Phone number must be at least 10 digits.")
        
        # Check if phone number already exists in the database
        if UserV2.objects.filter(phone_number=value).exists():
            raise ValidationError("Phone number already exists.")
        
        return value
    





class VerifyOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)  # Assuming OTP is 6 digits long
    
    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        # Check if the user exists
        try:
            user = UserV2.objects.get(phone_number=phone_number)
        except UserV2.DoesNotExist:
            raise ValidationError("User with this phone number does not exist.")

        # Check if the user is already active
        if user.is_active:
            raise ValidationError("User is already verified.")

        # Retrieve the latest OTP for this phone number
        otp_record = Otp.objects.filter(user=user).order_by('-otp_time').first()

        # Check if OTP exists and if it matches
        if not otp_record:
            raise ValidationError("No OTP found for this user.")

        if otp_record.code != otp:
            raise ValidationError("Invalid OTP.")

        return data