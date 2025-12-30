from django.urls import path
from .v1.views import VehicleList, VehicleDetail, VehicleImageDeleteAPIView, VehicleImageCreateAPIView


urlpatterns = [
    path("",VehicleList.as_view()),
    path("<int:id>/",VehicleDetail.as_view()),
    path("image/<int:id>/",VehicleImageDeleteAPIView.as_view()),
    path("images/add/", VehicleImageCreateAPIView.as_view(), name="vehicle-image-add"),    
]