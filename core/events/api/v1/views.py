from rest_framework import generics
from ...models import EventType, Event
from .serializers import EventTypeSerializer, EventSerializer

# EventType List and Create API
class EventTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer

    def perform_create(self, serializer):
        serializer.save()

# Event List and Create API
class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save()

# EventType Retrieve, Update and Delete API
class EventTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer

# Event Retrieve, Update and Delete API
class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer