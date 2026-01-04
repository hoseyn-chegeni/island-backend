from django.urls import path
from .v1.users import (
    Userlist,
    UserDetail,
    ProfileList,
    ProfileDetail,
    RegistrationAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
    VendorRegistrationAPIView,
    VendorListAPIView,
    VendorDetailAPIView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView
)



app_name = "api_v1"

urlpatterns = [
    path("users/", Userlist.as_view()),
    path("users/<int:id>/", UserDetail.as_view()),
    path("profiles/", ProfileList.as_view()),
    path("profiles/<int:id>/", ProfileDetail.as_view()),
    path("register/", RegistrationAPIView.as_view()),
    path("register/vendor/", VendorRegistrationAPIView.as_view()),
    path("login/", CustomTokenObtainPairView.as_view()),
    path("jwt/refresh/", CustomTokenRefreshView.as_view()),
    path("jwt/verify/", CustomTokenVerifyView.as_view()),
    path("password/change/", ChangePasswordAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("vendors/", VendorListAPIView.as_view()),
    path("vendors/<int:id>/", VendorDetailAPIView.as_view()),
]
