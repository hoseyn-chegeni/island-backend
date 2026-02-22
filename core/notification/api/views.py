from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from ..models import ReserveRequest
from .serializers import ReserveRequestSerializer


class ReserveRequestListAPIView(ListCreateAPIView):
    queryset = ReserveRequest.objects.all()
    serializer_class = ReserveRequestSerializer


class ReserveRequestDetailAPIView(RetrieveUpdateAPIView):
    queryset = ReserveRequest.objects.all()
    serializer_class = ReserveRequestSerializer
    lookup_field = "id"  
    