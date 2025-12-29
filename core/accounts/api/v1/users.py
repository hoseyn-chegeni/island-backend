from .serializers import UserSerializer,UserReadUpdateSerializer, ProfileSerializer
from accounts.models import User,Profile
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,RetrieveUpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import LargeResultSetPagination
from django.db.models.functions import Concat
from django.db.models import Value

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
        filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
        filterset_fields = ["gender",]
        search_fields = ["full_name","=national_id",]
        ordering_fields  =["created_date","updated_date","date_of_birth",]
        pagination_class = LargeResultSetPagination


        def get_queryset(self):
                return Profile.objects.annotate(
                full_name=Concat(
                        "first_name",
                        Value(" "),
                        "last_name",
                )
                )


class ProfileDetail(RetrieveUpdateAPIView):
        serializer_class = ProfileSerializer
        queryset = Profile.objects.all()
        lookup_field = "id"