from .serializers import UserSerializer,UserReadUpdateSerializer
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import LargeResultSetPagination


class Userlist(ListCreateAPIView):
        serializer_class = UserSerializer
        queryset = User.objects.all()
        filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
        filterset_fields = ["is_active",]
        search_fields = ["=username","email"]
        ordering_fields  =["date_joined"]
        pagination_class = LargeResultSetPagination



class UserDetail(RetrieveUpdateDestroyAPIView):
        serializer_class = UserReadUpdateSerializer
        queryset = User.objects.all()
        lookup_field = "id"
        
