from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import VehicleRentalSerializer
from ...models import VehicleRental
from rest_framework.permissions import IsAuthenticated
from core.utils import IsOwnerOrAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response


class VehicleRentalListCreateAPIView(ListCreateAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer
    permission_classes = [IsAuthenticated,]

class VehicleRentalDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VehicleRental.objects.all()
    serializer_class = VehicleRentalSerializer
    lookup_field = "id"
    permission_classes = [IsOwnerOrAdmin,]




class MyRentHistoryAPIView(ListAPIView):
    serializer_class = VehicleRentalSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):

        user_id = self.request.user.id  # Get the user id from the JWT
        return VehicleRental.objects.filter(user_id=user_id)  # Filter rentals by user_id

    def list(self, request, *args, **kwargs):
        """
        Custom list method to handle the response format.
        """
        rentals = self.get_queryset()
        serializer = self.get_serializer(rentals, many=True)
        return Response(serializer.data)