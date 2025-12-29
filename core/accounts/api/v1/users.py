from .serializers import UserSerializer,UserReadUpdateSerializer, ProfileSerializer
from accounts.models import User,Profile
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,RetrieveUpdateAPIView
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
        


class ProfileList(ListAPIView):
        serializer_class = ProfileSerializer
        queryset = Profile.objects.all()


class ProfileDetail(RetrieveUpdateAPIView):
        serializer_class = ProfileSerializer
        queryset = Profile.objects.all()
        lookup_field = "id"