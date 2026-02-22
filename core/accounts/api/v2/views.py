from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import UserV2, ProfileV2
from django.utils.translation import gettext_lazy as _
from .serializers import UserV2Serializer, VerifyOtpSerializer, LoginSerializer, ProfileV2Serializer
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateAPIView
from drf_yasg.utils import swagger_auto_schema
from notification.models import Otp
from ...utils import generate_jwt_tokens
import random
import string
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema



class RegisterView(CreateAPIView):
    queryset = UserV2.objects.all()
    serializer_class = UserV2Serializer
    @swagger_auto_schema(tags=["Accounts V2"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            user = serializer.save()
            return Response({"message": "OTP sent."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer, tags=["Accounts V2"])
    def post(self, request, *args, **kwargs):
        # Deserialize the request data using LoginSerializer
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            # Fetch the user by phone number
            try:
                user = UserV2.objects.get(phone_number=phone_number)
            except UserV2.DoesNotExist:
                return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            # Generate OTP for the user
            otp_code = ''.join(random.choices(string.digits, k=5))  # 5-digit OTP
            print(f"Generated OTP for {phone_number}: {otp_code}")
            
            # Create OTP instance
            try:
                otp = Otp.objects.create(
                    otp_status='in_progress',  # Initial status
                    otp_type='sms',  # Assuming OTP is sent via SMS
                    otp_function='login',  # For login process
                    input=phone_number,  # The phone number for which OTP is created
                    code=otp_code,
                    otp_time=timezone.now(),  # Set the current time
                    user=user  # Link the OTP with the user
                )
                print(f"OTP created for user {phone_number}")
            except Exception as e:
                print(f"Error creating OTP for {phone_number}: {e}")
                return Response({"error": "Error generating OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "OTP has been sent to your phone number."
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOtpView(APIView):
    @swagger_auto_schema(request_body=VerifyOtpSerializer, tags=["Accounts V2"])
    def post(self, request, *args, **kwargs):
        # Serialize the data
        serializer = VerifyOtpSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']  # Capture the OTP entered by the user

            try:
                # Retrieve the user based on the phone number
                user = UserV2.objects.get(phone_number=phone_number)
                print(f"User found: {user.phone_number}")  # Log user found

                # Retrieve the most recent OTP for the user
                otp_record = Otp.objects.filter(user=user).order_by('-otp_time').first()
                print(f"OTP record found: {otp_record}")  # Log OTP record

                if not otp_record:
                    return Response({"error": "No OTP found."}, status=status.HTTP_404_NOT_FOUND)

                # Validate the OTP
                if otp_record.code != otp:
                    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

                # If OTP function is register, mark the user as active
                if otp_record.otp_function == 'register':
                    user.is_active = True
                    user.save()
                    print(f"User {user.phone_number} is now active.")  # Log user activation

                    # Update the OTP status to 'verified'
                    otp_record.otp_status = 'verified'
                    otp_record.save()
                    print(f"OTP status updated to 'verified' for user {user.phone_number}")  # Log OTP status update

                    return Response({
                        "message": "OTP verified successfully, user is now active.",
                        "access_token": generate_jwt_tokens(user)["access_token"],  # Return the access token
                        "refresh_token": generate_jwt_tokens(user)["refresh_token"],  # Return the refresh token
                    }, status=status.HTTP_200_OK)

                # If OTP function is login, just return JWT token without changing is_active
                elif otp_record.otp_function == 'login':
                    print(f"Generating JWT token for login for {user.phone_number}")  # Log login flow
                    tokens = generate_jwt_tokens(user)
                    print(f"Generated tokens for login: {tokens}")  # Log generated tokens
                    return Response({
                        "message": "OTP verified successfully, here is your JWT.",
                        "access_token": tokens["access_token"],  # Return the access token
                        "refresh_token": tokens["refresh_token"],  # Return the refresh token
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({"error": "Invalid OTP function."}, status=status.HTTP_400_BAD_REQUEST)

            except UserV2.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")  # Log unexpected errors
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ProfileV2List(ListAPIView):
    serializer_class = ProfileV2Serializer
    queryset = ProfileV2.objects.all()

    @swagger_auto_schema(tags=["Accounts V2"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProfileV2Detail(RetrieveUpdateAPIView):
    serializer_class = ProfileV2Serializer
    queryset = ProfileV2.objects.all()
    lookup_field = "id"
    @swagger_auto_schema(tags=["Accounts V2"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Accounts V2"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Accounts V2"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)