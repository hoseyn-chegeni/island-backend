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
from rest_framework.response import Response
from datetime import datetime
from rentals.models import VehicleAvailability
from django.db.models import Q


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
    ordering_fields = ["created_at", "price_per_day"]  # Add price_per_day to the ordering fields
    pagination_class = LargeResultSetPagination

    @swagger_auto_schema(
        tags=["Vehicles"],
        manual_parameters=[
            openapi.Parameter(
                'start_time', openapi.IN_QUERY, description="Start time for the availability range",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
            ),
            openapi.Parameter(
                'end_time', openapi.IN_QUERY, description="End time for the availability range",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME
            ),
            openapi.Parameter(
                'type', openapi.IN_QUERY, description="Vehicle type",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_top', openapi.IN_QUERY, description="Filter vehicles that are marked as 'top'",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'brand', openapi.IN_QUERY, description="Filter by vehicle brand",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'color', openapi.IN_QUERY, description="Filter by vehicle color",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status', openapi.IN_QUERY, description="Filter by vehicle status",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Filter by category",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        vehicle_type = request.query_params.get('type', None)
        is_top = request.query_params.get('is_top', None)
        brand = request.query_params.get('brand', None)
        color = request.query_params.get('color', None)
        status = request.query_params.get('status', None)
        category = request.query_params.get('category', None)

        # Start with the base queryset
        available_vehicles = Vehicle.objects.all()

        # Apply filters for type, is_top, brand, color, status, and category
        if vehicle_type:
            available_vehicles = available_vehicles.filter(type=vehicle_type)

        # Convert 'is_top' from string to boolean (if passed as a string)
        if is_top is not None:
            is_top = is_top.lower() == 'true'
            available_vehicles = available_vehicles.filter(is_top=is_top)

        if brand:
            available_vehicles = available_vehicles.filter(brand__name=brand)
        if color:
            available_vehicles = available_vehicles.filter(color=color)
        if status:
            available_vehicles = available_vehicles.filter(status=status)
        if category:
            available_vehicles = available_vehicles.filter(category__name=category)

        # If both start_time and end_time are provided, filter vehicles by availability dates
        if start_time and end_time:
            try:
                start_time = datetime.fromisoformat(start_time)  # Converts to datetime
                end_time = datetime.fromisoformat(end_time)  # Converts to datetime
            except ValueError:
                # Raise a valid 400 error if the datetime is invalid
                return Response({"error": "Invalid date format. Use ISO format."}, status=status.HTTP_400_BAD_REQUEST)

            # Exclude vehicles with unavailable dates in the given time range
            available_vehicles = available_vehicles.exclude(
                vehicleavailability__date__gte=start_time.date(),
                vehicleavailability__date__lte=end_time.date()
            ).distinct()

        # Perform search if 'search' term is provided
        search_term = request.query_params.get('search', None)
        if search_term:
            available_vehicles = available_vehicles.filter(
                Q(brand__name__icontains=search_term) |
                Q(model__icontains=search_term) |
                Q(plate_number__icontains=search_term)
            )

        # Handle ordering based on query params
        ordering = request.query_params.get('ordering', None)
        if ordering:
            available_vehicles = available_vehicles.order_by(ordering)

        # Return the filtered vehicles
        serializer = self.get_serializer(available_vehicles, many=True)
        return Response(serializer.data)


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
            start_time = serializer.validated_data.get("start_time", None)
            end_time = serializer.validated_data.get("end_time", None)
            vehicle_type = request.data.get(
                "type", ""
            )  # Get vehicle type from request data, default to empty string

            # Build the query to filter available vehicles
            available_vehicles = Vehicle.objects.exclude(
                id__in=VehicleAvailability.objects.filter(
                    date__range=[
                        start_time.date() if start_time else None,
                        end_time.date() if end_time else None,
                    ]
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
