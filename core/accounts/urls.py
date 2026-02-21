from django.urls import path, include


urlpatterns = [
    path("api/v1/", include("accounts.api.urls")),   
    path("api/v2/", include("accounts.api.v2.urls")),  
]
