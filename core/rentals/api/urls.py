from django.urls import path
from .v1.views import CheckVehicleAvailabilityAPIView


urlpatterns = [
    path('vehicles/check-availability/', CheckVehicleAvailabilityAPIView.as_view(), ),
]