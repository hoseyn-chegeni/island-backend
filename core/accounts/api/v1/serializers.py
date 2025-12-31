from rest_framework import serializers
from accounts.models import User, Profile, Vendor
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class UserReadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserReadUpdateSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "avatar_url",
            "national_id",
            "date_of_birth",
            "gender",
            "created_date",
            "updated_date",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Password Doesnt match."})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()





class VendorRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError(
                {"detail": "Passwords do not match"}
            )

        try:
            validate_password(attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password1")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            is_vendor=True,
        )
        return user
    

class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_active", "is_vendor"]


class VendorSerializer(serializers.ModelSerializer):
    user = VendorUserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = "__all__"
        read_only_fields = ["user", "created_at"]
        ref_name = "AccountsVendor"