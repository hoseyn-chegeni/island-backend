from django.contrib import admin
from .models import User, Profile, Vendor

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Vendor)
