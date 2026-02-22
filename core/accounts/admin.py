from django.contrib import admin
from .models import User, Profile, Vendor,UserV2,ProfileV2

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Vendor)
admin.site.register(UserV2)
admin.site.register(ProfileV2)
