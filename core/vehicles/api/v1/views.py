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
)
from vehicles.models import (
    Vehicle,
    VehicleImage,
    VehicleLocation,
    Category,
    Brand,
    VehicleReview,
)
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


class VehicleList(ListCreateAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]
    filterset_fields = [
        "vendor__user__email",
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
