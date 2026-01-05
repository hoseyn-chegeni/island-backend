from django.urls import path
from .v1.views import (
    VehicleList,
    VehicleDetail,
    VehicleImageDeleteAPIView,
    VehicleImageCreateAPIView,
    VehicleLocationDetailAPIView,
    VehicleLocationListCreateAPIView,
    VehicleBrandDetail,
    VehicleCategoryDetail,
    VehicleCategoryList,
    VehicleBrandList,
    VehicleReviewList,
    VehicleReviewDetail,
)


urlpatterns = [
    path("", VehicleList.as_view()),
    path("<int:id>/", VehicleDetail.as_view()),
    path("image/<int:id>/", VehicleImageDeleteAPIView.as_view()),
    path("images/add/", VehicleImageCreateAPIView.as_view()),
    path("location/", VehicleLocationListCreateAPIView.as_view()),
    path("location/<int:id>", VehicleLocationDetailAPIView.as_view()),
    path("brand/", VehicleBrandList.as_view()),
    path("brand/<int:id>/", VehicleBrandDetail.as_view()),
    path("category/", VehicleCategoryList.as_view()),
    path("category/<int:id>/", VehicleCategoryDetail.as_view()),
    path("reviews/", VehicleReviewList.as_view()),
    path("reviews/<int:id>/", VehicleReviewDetail.as_view()),
]
