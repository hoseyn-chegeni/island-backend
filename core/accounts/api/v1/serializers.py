from rest_framework import serializers
from accounts.models import User,Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
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