from .serializers import UserSerializer,UserReadUpdateSerializer, ProfileSerializer, RegistrationSerializer,PasswordChangeSerializer,LogoutSerializer
from accounts.models import User,Profile
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListAPIView,RetrieveUpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import LargeResultSetPagination
from django.db.models.functions import Concat
from django.db.models import Value
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash




class Userlist(ListAPIView):
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


# TODO: Switch to phone number and OTP registration
class RegistrationAPIView(generics.GenericAPIView):
        serializer_class = RegistrationSerializer
        def post(self,request,*args,**kwargs):
                serializer = RegistrationSerializer(data=request.data)
                if serializer.is_valid():
                        user = serializer.save()
                        refresh = RefreshToken.for_user(user)
                        access = str(refresh.access_token)
                        data = {
                                'user': {
                                'id': user.id,
                                'email': user.email
                                },
                                'access': access,
                                'refresh': str(refresh)
                        }

                        return Response(data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            # optional: keep user logged in after password change
            update_session_auth_hash(request, user)
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        
