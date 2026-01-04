from django.urls import path
from .v1.views import (
    VehicleRentalDetailAPIView,
    VehicleRentalListCreateAPIView,
    MyRentHistoryAPIView,
)


urlpatterns = [
    path("vehicles/", VehicleRentalListCreateAPIView.as_view()),
    path("vehicles/<int:id>/", VehicleRentalDetailAPIView.as_view()),
    path("my-rent-history/", MyRentHistoryAPIView.as_view()),
]
