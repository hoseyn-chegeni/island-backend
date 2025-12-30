from django.urls import path
from .v1.views import VehicleList, VehicleDetail


urlpatterns = [
    path("",VehicleList.as_view()),
    path("/<int:id>/",VehicleDetail.as_view()),

]