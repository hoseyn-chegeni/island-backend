from rest_framework import serializers
from ...models import UserV2, ProfileV2,VendorV2
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

        # Retrieve the latest OTP for this user
        otp_record = Otp.objects.filter(user=user).order_by('-otp_time').first()

        # Check if OTP exists and if it matches
        if not otp_record:
            raise ValidationError("No OTP found for this user.")

        if otp_record.code != otp:
            raise ValidationError("Invalid OTP.")

        # If OTP function is 'register' and user is already active, raise an error
        if otp_record.otp_function == 'register' and user.is_active:
            raise ValidationError("User is already verified.")

        # If OTP function is 'register' and user is not active, no issue, proceed
        if otp_record.otp_function == 'register' and not user.is_active:
            # User is being marked as active here if it's a registration process
            user.is_active = True
            user.save()

        # Optionally, if you want to update the OTP status to 'verified'
        otp_record.otp_status = 'verified'
        otp_record.save()

        return data


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    
    def validate_phone_number(self, value):
        # Check if the phone number exists and if the user is active
        try:
            user = UserV2.objects.get(phone_number=value)
            if not user.is_active:
                raise ValidationError("Something went wrong.")
        except UserV2.DoesNotExist:
            raise ValidationError("User with this phone number does not exist.")
        
        return value
    


class ProfileV2Serializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileV2
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar_url",
            "national_id",
            "date_of_birth",
            "gender",
            "created_date",
            "updated_date",
        ]


class VendorUserSerV2ializer(serializers.ModelSerializer):
    class Meta:
        model = UserV2
        fields = ["id", "phone_number", "is_active", "is_vendor"]


class VendorV2Serializer(serializers.ModelSerializer):
    user = VendorUserSerV2ializer(read_only=True)

    class Meta:
        model = VendorV2
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
        ref_name = "AccountsVendorV2"




class SimpleUserV2Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserV2
        fields =  "__all__"
        read_only_fields = ["phone_number", "created_date","updated_date"]

    def update(self, instance, validated_data):
        """
        Update the user instance with validated data.
        """
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_vendor = validated_data.get('is_vendor', instance.is_vendor)
        instance.save()
        return instance