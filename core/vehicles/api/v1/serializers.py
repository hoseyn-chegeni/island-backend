from rest_framework import serializers
from vehicles.models import Vehicle, VehicleImage
from django.contrib.auth import get_user_model



class VehicleImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = VehicleImage
        fields = ["id", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    

User = get_user_model()
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]



class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Vehicle

        fields = '__all__'





class VehicleImageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ["id", "vehicle", "image", "created_at"]
        read_only_fields = ["id", "created_at"]
    image = serializers.ImageField()