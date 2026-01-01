from django.urls import path
from .v1.views import CheckVehicleAvailabilityAPIView, VehicleRentalDetailAPIView,VehicleRentalListCreateAPIView


urlpatterns = [
    path('vehicles/check-availability/', CheckVehicleAvailabilityAPIView.as_view(),),
    path("vehicles/",VehicleRentalListCreateAPIView.as_view()),
    path('vehicles/<int:id>/', VehicleRentalDetailAPIView.as_view())
]