from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Vendor, UserV2, ProfileV2, VendorV2
import random
import string
from django.utils import timezone
from notification.models import Otp


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_vendor(sender, instance, created, **kwargs):
    if created and instance.is_vendor == True:
        Vendor.objects.create(user=instance)


@receiver(post_save, sender=UserV2)
def create_otp_for_new_user(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.phone_number}")
        otp_code = "".join(random.choices(string.digits, k=5))
        print(f"Generated OTP for {instance.phone_number}: {otp_code}")

        try:
            Otp.objects.create(
                otp_status="in_progress",
                otp_type="sms",
                otp_function="register",
                input=instance.phone_number,
                code=otp_code,
                otp_time=timezone.now(),
                user=instance,
            )
        except Exception as e:
            print(f"Error creating OTP for {instance.phone_number}: {e}")


@receiver(post_save, sender=UserV2)
def save_profile(sender, instance, created, **kwargs):
    if created:
        ProfileV2.objects.create(user=instance)


@receiver(post_save, sender=UserV2)
def save_vendor(sender, instance, created, **kwargs):
    if created and instance.is_vendor == True:
        VendorV2.objects.create(user=instance)
