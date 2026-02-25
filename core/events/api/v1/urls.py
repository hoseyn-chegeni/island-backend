from django.urls import path
from .views import EventTypeListCreateAPIView,EventTypeRetrieveUpdateDestroyAPIView,EventListCreateAPIView,EventRetrieveUpdateDestroyAPIView

urlpatterns = [
    # EventType URLs
    path('event-types/',EventTypeListCreateAPIView.as_view(),),
    path('event-types/<int:pk>/',EventTypeRetrieveUpdateDestroyAPIView.as_view(),),
    # Event URLs
    path('events/',EventListCreateAPIView.as_view(),),
    path('events/<int:pk>/',EventRetrieveUpdateDestroyAPIView.as_view(),),
]