from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import UserV2
from django.utils.translation import gettext_lazy as _
from .serializers import UserV2Serializer, VerifyOtpSerializer
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
from notification.models import Otp

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
            # After validation, we get the phone number and update the user
            phone_number = serializer.validated_data['phone_number']
            user = UserV2.objects.get(phone_number=phone_number)
            
            # Mark the user as active after OTP validation
            user.is_active = True
            user.save()

            # Update the OTP status from 'in_progress' to 'verified'
            otp_record = Otp.objects.filter(user=user).order_by('-otp_time').first()
            if otp_record:
                otp_record.otp_status = 'verified'  # Change status to 'verified'
                otp_record.save()

            return Response({"message": "OTP verified successfully, user is now active."}, status=status.HTTP_200_OK)

        # If serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)