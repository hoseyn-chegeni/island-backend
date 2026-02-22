from django.urls import path
from .views import RegisterView,VerifyOtpView,LoginView, ProfileV2Detail, ProfileV2List, VendorV2RegisterView


app_name = "api_v2"

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("vendor/register/", VendorV2RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
    path("profile/", ProfileV2List.as_view()),
    path("profile/<int:id>/", ProfileV2Detail.as_view()),
]
