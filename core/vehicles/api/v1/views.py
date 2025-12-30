from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import VehicleSerializer
from vehicles.models import Vehicle 


class VehicleList(ListCreateAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()


class VehicleDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    lookup_field = "id"
