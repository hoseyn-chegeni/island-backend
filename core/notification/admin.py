from django.contrib import admin
from .models import Otp, ReserveRequest

# Register your models here.
admin.site.register(Otp)
admin.site.register(ReserveRequest)
