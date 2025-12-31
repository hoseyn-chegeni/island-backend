from rest_framework import serializers
from vehicles.models import Vehicle, VehicleImage, VehicleLocation
from accounts.models import Vendor


class VehicleLocationSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(),write_only=True)

    class Meta:
        model = VehicleLocation
        fields = [
            "id",
            "name",
            "manual_address",
            "vehicle",
            "latitude",
            "longitude",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


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

class VendorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Vendor
        fields = ["id", "name", "email", "type", "status"]

class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    locations = VehicleLocationSerializer(many=True, read_only=True)
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model = Vehicle
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['vendor'] = VendorSerializer(instance.vendor).data
        return representation

class VehicleImageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ["id", "vehicle", "image", "created_at"]
        read_only_fields = ["id", "created_at"]
    
    image = serializers.ImageField()


