from django.urls import path
from .views import ReserveRequestListAPIView, ReserveRequestDetailAPIView

urlpatterns = [
    path("reserve-requests/", ReserveRequestListAPIView.as_view()),
    path("reserve-requests/<int:id>/", ReserveRequestDetailAPIView.as_view()),
]
