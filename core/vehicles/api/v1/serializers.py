from rest_framework import serializers
from vehicles.models import (
    Vehicle,
    VehicleImage,
    VehicleLocation,
    Category,
    Brand,
    VehicleReview,
)
from accounts.models import Vendor
from rentals.models import VehicleAvailability
from rentals.models import VehicleRental


class VehicleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class VehicleAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAvailability
        fields = ["date"]


class VehicleLocationSerializer(serializers.ModelSerializer):
    vehicle = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(), write_only=True
    )

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
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Vendor
        fields = ["id", "name", "email", "type", "status"]


class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    locations = VehicleLocationSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
    unavailable_dates = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="date", source="vehicleavailability_set"
    )

    class Meta:
        model = Vehicle
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["vendor"] = VendorSerializer(instance.vendor).data
        representation["category"] = VehicleCategorySerializer(instance.category).data
        representation["brand"] = VehicleBrandSerializer(instance.brand).data
        return representation


class VehicleImageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ["id", "vehicle", "image", "created_at"]
        read_only_fields = ["id", "created_at"]

    image = serializers.ImageField()


class VehicleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleReview
        fields = ['id', 'vehicle', 'user', 'score', 'content', 'created_at', 'updated_at']  # Include 'id' field

    def validate(self, data):
        # Ensuring the vehicle exists and the user has rented it
        user = data.get('user')
        vehicle = data.get('vehicle')

        rental_exists = VehicleRental.objects.filter(
            user=user,
            vehicle=vehicle,
            status="CONFIRMED"
        ).exists()

        if not rental_exists:
            raise serializers.ValidationError("You can only leave a review for a vehicle you have rented.")

        return data
