from .serializers import UserSerializer,UserReadUpdateSerializer
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

class Userlist(ListCreateAPIView):
        serializer_class = UserSerializer
        queryset = User.objects.all()

class UserDetail(RetrieveUpdateDestroyAPIView):
        serializer_class = UserReadUpdateSerializer
        queryset = User.objects.all()
        lookup_field = "id"
