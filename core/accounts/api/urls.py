from django.urls import path
from .v1.users import Userlist,UserDetail,ProfileList,ProfileDetail, RegistrationAPIView, ChangePasswordAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView



app_name = "api_v1"

urlpatterns = [
    path("users/",Userlist.as_view()),
    path("users/<int:id>/",UserDetail.as_view()),
    path("profiles/",ProfileList.as_view()),
    path("profiles/<int:id>/",ProfileDetail.as_view()),
    path("register/", RegistrationAPIView.as_view()),
    path('login/',TokenObtainPairView.as_view()),
    path('jwt/refresh/',TokenRefreshView.as_view()),
    path('jwt/verify/',TokenVerifyView.as_view()),
    path('password/change/', ChangePasswordAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
] 