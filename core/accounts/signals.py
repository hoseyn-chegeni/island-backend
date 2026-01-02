from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Vendor


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_vendor(sender, instance, created, **kwargs):
    if created and instance.is_vendor == True:
        Vendor.objects.create(user=instance)
