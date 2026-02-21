from rest_framework import serializers
from ...models import UserV2
from django.core.exceptions import ValidationError

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
    otp = serializers.CharField(max_length=5)

    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        # Validate OTP (In this case, it's always '12345')
        if otp != '12345':
            raise ValidationError("Invalid OTP.")

        # Check if the user exists with the provided phone number and is not active
        try:
            user = UserV2.objects.get(phone_number=phone_number)
            if user.is_active:
                raise ValidationError("User is already verified.")
        except UserV2.DoesNotExist:
            raise ValidationError("User with this phone number does not exist.")

        return data