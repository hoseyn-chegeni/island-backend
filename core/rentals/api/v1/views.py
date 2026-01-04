from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import VehicleRentalSerializer
from ...models import VehicleRental
from rest_framework.permissions import IsAdminUser
from core.utils import IsOwnerOrAdmin

class VehicleRentalListCreateAPIView(ListCreateAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer
    permission_classes = [IsAdminUser,]

class VehicleRentalDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer
    lookup_field = "id"
    permission_classes = [IsOwnerOrAdmin,]
