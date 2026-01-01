from django.urls import path, include


urlpatterns = [
    path("",include("rentals.api.urls"))
]