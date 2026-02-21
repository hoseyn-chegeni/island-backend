from django.urls import path
from .views import RegisterView,VerifyOtpView,LoginView


app_name = "api_v2"

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
]
