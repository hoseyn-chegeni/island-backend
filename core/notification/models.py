from django.db import models
from accounts.models import UserV2
from .choices import OtpFunction,OtpStatus, OtpTypes,ReserveRequestStatus
# Create your models here.





class Otp(models.Model):
    otp_status = models.CharField(max_length=20,choices=OtpStatus.choices,default=OtpStatus.IN_PROGRESS)
    otp_type = models.CharField(max_length=10,choices=OtpTypes.choices,default=OtpTypes.EMAIL)
    otp_function = models.CharField(max_length=20,choices=OtpFunction.choices,default=OtpFunction.REGISTER,null=True, blank=True)
    input = models.CharField(max_length=255, null=True, blank=True)  
    code = models.CharField(max_length=5)  
    otp_time = models.DateTimeField(auto_now_add=True)  
    user = models.ForeignKey(UserV2, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'OTP for {self.user} - Status: {self.otp_status}'
    
class ReserveRequest(models.Model):
    input = models.CharField(max_length=255, blank = True, null = True)
    status = models.CharField(max_length=20, choices=ReserveRequestStatus.choices, default=ReserveRequestStatus.IN_PROGRESS)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ReserveRequest {self.id} - Status: {self.status}"