from django.urls import path
from .v1.views import (
    VehicleRentalDetailAPIView,
    VehicleRentalListCreateAPIView,
)


urlpatterns = [

    path("vehicles/", VehicleRentalListCreateAPIView.as_view()),
    path("vehicles/<int:id>/", VehicleRentalDetailAPIView.as_view()),
]
