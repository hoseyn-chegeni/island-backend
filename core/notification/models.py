from django.db import models
from accounts.models import User
import uuid
from .choices import OtpFunction,OtpStatus, OtpTypes
# Create your models here.





class Otp(models.Model):
    otp_status = models.CharField(max_length=20,choices=OtpStatus.choices,default=OtpStatus.IN_PROGRESS)
    otp_type = models.CharField(max_length=10,choices=OtpTypes.choices,default=OtpTypes.EMAIL)
    otp_function = models.CharField(max_length=20,choices=OtpFunction.choices,default=OtpFunction.REGISTER,null=True, blank=True)
    input = models.CharField(max_length=255, null=True, blank=True)  # For phone number or email
    code = models.CharField(max_length=6)  # OTP code, adjust length as needed
    otp_time = models.DateTimeField(auto_now_add=True)  # The time when OTP was generated
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming User model is used for user information

    def __str__(self):
        return f'OTP for {self.user} - Status: {self.otp_status}'