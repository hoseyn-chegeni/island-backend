from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import UserV2
from django.utils.translation import gettext_lazy as _
from .serializers import UserV2Serializer, VerifyOtpSerializer
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
from notification.models import Otp
from ...utils import generate_jwt_tokens
class RegisterView(CreateAPIView):
    queryset = UserV2.objects.all()
    serializer_class = UserV2Serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            user = serializer.save()
            return Response({"message": "OTP sent."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOtpView(APIView):
    @swagger_auto_schema(request_body=VerifyOtpSerializer)
    def post(self, request, *args, **kwargs):
        # Serialize the data
        serializer = VerifyOtpSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            try:
                user = UserV2.objects.get(phone_number=phone_number)

                # Mark the user as active
                user.is_active = True
                user.save()

                # Update the OTP status from 'in_progress' to 'verified'
                otp_record = Otp.objects.filter(user=user).order_by('-otp_time').first()

                if otp_record:
                    otp_record.otp_status = 'verified'
                    otp_record.save()

                # Manually generate JWT access and refresh tokens for the user
                tokens = generate_jwt_tokens(user)

                return Response({
                    "message": "OTP verified successfully, user is now active.",
                    "access_token": tokens["access_token"],  # Return the access token
                    "refresh_token": tokens["refresh_token"],  # Return the refresh token
                }, status=status.HTTP_200_OK)

            except UserV2.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)