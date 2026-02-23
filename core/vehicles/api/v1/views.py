from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from .serializers import (
    VehicleSerializer,
    VehicleImageAddSerializer,
    VehicleLocationSerializer,
    VehicleBrandSerializer,
    VehicleCategorySerializer,
    VehicleReviewSerializer,
    VehicleAvailabilityRequestSerializer,
)
from vehicles.models import (
    Vehicle,
    VehicleImage,
    VehicleLocation,
    Category,
    Brand,
    VehicleReview,
)
from rentals.models import VehicleAvailability
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.utils import (
    LargeResultSetPagination,
    CustomUserRateThrottle,
    CustomAnonRateThrottle,
)
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status


class VehicleList(ListCreateAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]
    filterset_fields = [
        "vendor__user__phone_number",
        "type",
        "brand",
        "color",
        "status",
        "category",
        "is_top",
    ]
    search_fields = ["brand", "model", "=plate_number"]
    ordering_fields = ["created_at"]
    pagination_class = LargeResultSetPagination

    @swagger_auto_schema(tags=["Vehicles"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicles"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VehicleDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    lookup_field = "id"
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicles"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicles"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicles"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicles"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class VehicleImageDeleteAPIView(DestroyAPIView):
    queryset = VehicleImage.objects.all()
    lookup_field = "id"
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Images"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class VehicleImageCreateAPIView(CreateAPIView):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageAddSerializer
    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Images"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data.get("vehicle")
        serializer.save()


class VehicleLocationListCreateAPIView(CreateAPIView):
    queryset = VehicleLocation.objects.all()
    serializer_class = VehicleLocationSerializer
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Locations"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VehicleLocationDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleLocation.objects.all()
    serializer_class = VehicleLocationSerializer
    lookup_field = "id"
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Locations"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Locations"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Locations"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Locations"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class VehicleBrandList(ListCreateAPIView):
    serializer_class = VehicleBrandSerializer
    queryset = Brand.objects.all()
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Brands"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Brands"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VehicleBrandDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleBrandSerializer
    queryset = Brand.objects.all()
    lookup_field = "id"
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Brands"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Brands"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Brands"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Brands"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class VehicleCategoryList(ListCreateAPIView):
    serializer_class = VehicleCategorySerializer
    queryset = Category.objects.all()
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Categories"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Categories"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VehicleCategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleCategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vehicle-Categories"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Categories"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Categories"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Categories"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class VehicleReviewList(ListCreateAPIView):
    serializer_class = VehicleReviewSerializer
    queryset = VehicleReview.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["vehicle"]
    ordering_fields = ["score"]
    pagination_class = LargeResultSetPagination

    @swagger_auto_schema(
        tags=["Vehicle-Reviews"],
        manual_parameters=[
            openapi.Parameter(
                "vehicle_id",  # Filter parameter for vehicle ID
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Filter reviews by vehicle ID",
            ),
            openapi.Parameter(
                "ordering",  # Ordering parameter for score
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["score", "-score"],  # Possible ordering options
                description="Order reviews by score (ascending or descending)",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Reviews"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VehicleReviewDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleReviewSerializer
    queryset = VehicleReview.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(tags=["Vehicle-Reviews"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Reviews"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Reviews"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vehicle-Reviews"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class VehicleAvailabilityView(APIView):
    @swagger_auto_schema(
        request_body=VehicleAvailabilityRequestSerializer, tags=["Vehicles"]
    )
    def post(self, request, *args, **kwargs):
        # Deserialize the input data
        serializer = VehicleAvailabilityRequestSerializer(data=request.data)

        if serializer.is_valid():
            start_time = serializer.validated_data["start_time"]
            end_time = serializer.validated_data["end_time"]
            vehicle_type = request.data.get("type", "")  # Get vehicle type from request data, default to empty string

            # Build the query to filter available vehicles
            available_vehicles = Vehicle.objects.exclude(
                id__in=VehicleAvailability.objects.filter(
                    date__range=[start_time.date(), end_time.date()]
                ).values_list("vehicle", flat=True)
            )

            # If vehicle type is not empty, filter by the type
            if vehicle_type:
                available_vehicles = available_vehicles.filter(type=vehicle_type)

            # If no available vehicles found, return a 404 error
            if not available_vehicles:
                return Response(
                    {"message": "No vehicles are available during this time range."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Serialize the list of available vehicles
            vehicle_serializer = VehicleSerializer(available_vehicles, many=True)

            return Response(vehicle_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)