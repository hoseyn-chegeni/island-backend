from django.urls import path
from .v1.users import Userlist,UserDetail,ProfileList,ProfileDetail

app_name = "api_v1"

urlpatterns = [
    path("users/",Userlist.as_view()),
    path("users/<int:id>/",UserDetail.as_view()),
    path("profiles/",ProfileList.as_view()),
    path("profiles/<int:id>/",ProfileDetail.as_view()),
] 