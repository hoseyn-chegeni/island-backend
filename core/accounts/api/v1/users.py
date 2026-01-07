from .serializers import (
    UserSerializer,
    UserReadUpdateSerializer,
    ProfileSerializer,
    RegistrationSerializer,
    PasswordChangeSerializer,
    LogoutSerializer,
    VendorRegistrationSerializer,
    VendorSerializer,
)
from accounts.models import User, Profile, Vendor
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from core.utils import LargeResultSetPagination
from django.db.models.functions import Concat
from django.db.models import Value
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.choices import VendorStatus, VendorType
from core.utils import IsOwnerOrAdmin, CustomUserRateThrottle, CustomAnonRateThrottle
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


class Userlist(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active"]
    search_fields = ["=username", "email"]
    ordering_fields = ["date_joined"]
    pagination_class = LargeResultSetPagination
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(
        tags=["Users"],
        manual_parameters=[
            openapi.Parameter(
                "is_active",
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ordering",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["date_joined", "-date_joined"],
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserReadUpdateSerializer
    queryset = User.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Users"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProfileList(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]
    filterset_fields = [
        "gender",
    ]
    search_fields = [
        "full_name",
        "=national_id",
    ]
    ordering_fields = [
        "created_date",
        "updated_date",
        "date_of_birth",
    ]
    pagination_class = LargeResultSetPagination

    def get_queryset(self):
        return Profile.objects.annotate(
            full_name=Concat(
                "first_name",
                Value(" "),
                "last_name",
            )
        )

    @swagger_auto_schema(tags=["Profiles"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProfileDetail(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Profiles"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Profiles"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Profiles"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# TODO: Switch to phone number and OTP registration
class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Register"])
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            data = {
                "user": {"id": user.id, "email": user.email},
                "access": access,
                "refresh": str(refresh),
            }

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    model = User
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            # optional: keep user logged in after password change
            update_session_auth_hash(request, user)
            return Response(
                {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )


class VendorRegistrationAPIView(generics.GenericAPIView):
    serializer_class = VendorRegistrationSerializer
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Register"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_vendor": user.is_vendor,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class VendorListAPIView(ListAPIView):
    queryset = Vendor.objects.select_related("user")
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type", "status"]
    search_fields = ["name", "=user__email"]
    ordering_fields = ["created_at"]
    pagination_class = LargeResultSetPagination
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(
        tags=["Vendors"],
        manual_parameters=[
            openapi.Parameter(
                name="type",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=[choice.value for choice in VendorType],
            ),
            openapi.Parameter(
                name="status",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=[choice.value for choice in VendorStatus],
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="ordering",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=["created_at", "-created_at"],
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class VendorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.select_related("user")
    serializer_class = VendorSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Vendors"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vendors"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vendors"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Vendors"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]


class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]


class CustomTokenVerifyView(TokenVerifyView):
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]
