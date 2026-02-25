from rest_framework import serializers
from vehicles.models import (
    Vehicle,
    VehicleImage,
    VehicleLocation,
    Category,
    Brand,
    VehicleReview,
)
from accounts.models import VendorV2
from rentals.models import VehicleAvailability
from rentals.models import VehicleRental
from ...choices import VehicleType

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
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = VendorV2
        fields = ["id", "name", "phone_number", "type", "status"]


class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    locations = VehicleLocationSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    average_score = serializers.ReadOnlyField()
    vendor = serializers.PrimaryKeyRelatedField(queryset=VendorV2.objects.all())
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
        fields = [
            "id",
            "vehicle",
            "user",
            "score",
            "content",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        """
        Ensure that the user has rented the vehicle before submitting a review.
        """
        user = data.get("user")  # Get the user submitting the review
        vehicle = data.get("vehicle")  # Get the vehicle being reviewed

        # Check if the user has rented the vehicle and the rental status is 'CONFIRMED'
        rental_exists = VehicleRental.objects.filter(
            user=user, vehicle=vehicle
        ).exists()

        if not rental_exists:
            raise serializers.ValidationError(
                "You can only leave a review for a vehicle you have rented."
            )

        return data


class VehicleAvailabilityRequestSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField(required=False, allow_null=True)
    end_time = serializers.DateTimeField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=VehicleType.choices, required=False, allow_blank = True)

    def to_internal_value(self, data):
        # Handle the empty string case for DateTimeField fields
        if 'start_time' in data and data['start_time'] == "":
            data['start_time'] = None
        if 'end_time' in data and data['end_time'] == "":
            data['end_time'] = None
        return super().to_internal_value(data)

    def validate_start_time(self, value):
        if value == "":
            return None  # Convert empty string to None
        return value

    def validate_end_time(self, value):
        if value == "":
            return None  # Convert empty string to None
        return value