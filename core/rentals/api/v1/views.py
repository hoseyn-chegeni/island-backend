from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import VehicleRentalSerializer
from ...models import VehicleRental


class VehicleRentalListCreateAPIView(ListCreateAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer


class VehicleRentalDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer
    lookup_field = "id"
