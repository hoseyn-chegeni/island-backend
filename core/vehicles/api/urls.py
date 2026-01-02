from django.urls import path
from .v1.views import (
    VehicleList,
    VehicleDetail,
    VehicleImageDeleteAPIView,
    VehicleImageCreateAPIView,
    VehicleLocationDetailAPIView,
    VehicleLocationListCreateAPIView,
)


urlpatterns = [
    path("", VehicleList.as_view()),
    path("<int:id>/", VehicleDetail.as_view()),
    path("image/<int:id>/", VehicleImageDeleteAPIView.as_view()),
    path("images/add/", VehicleImageCreateAPIView.as_view()),
    path("location/", VehicleLocationListCreateAPIView.as_view()),
    path("location/<int:id>", VehicleLocationDetailAPIView.as_view()),
]
