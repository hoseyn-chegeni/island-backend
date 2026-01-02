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
)
from vehicles.models import Vehicle, VehicleImage, VehicleLocation, Category, Brand
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.utils import LargeResultSetPagination
from rest_framework.parsers import MultiPartParser, FormParser


class VehicleList(ListCreateAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
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


class VehicleDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    lookup_field = "id"


class VehicleImageDeleteAPIView(DestroyAPIView):
    queryset = VehicleImage.objects.all()
    lookup_field = "id"


class VehicleImageCreateAPIView(CreateAPIView):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageAddSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.validated_data.get("vehicle")
        serializer.save()


class VehicleLocationListCreateAPIView(CreateAPIView):
    queryset = VehicleLocation.objects.all()
    serializer_class = VehicleLocationSerializer


class VehicleLocationDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleLocation.objects.all()
    serializer_class = VehicleLocationSerializer
    lookup_field = "id"


class VehicleBrandList(ListCreateAPIView):
    serializer_class = VehicleBrandSerializer
    queryset = Brand.objects.all()


class VehicleBrandDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleBrandSerializer
    queryset = Brand.objects.all()
    lookup_field = "id"


class VehicleCategoryList(ListCreateAPIView):
    serializer_class = VehicleCategorySerializer
    queryset = Category.objects.all()


class VehicleCategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleCategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"
