from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length = 255,unique = True)
    is_superuser = models.BooleanField(default =  False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self) -> str:
        return self.email