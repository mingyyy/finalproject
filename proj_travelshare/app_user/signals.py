from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import ProfileTraveler,ProfileHost


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.type == '0':
            ProfileTraveler.objects.create(user=instance)
        elif instance.type == '1':
            ProfileHost.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.type == '0':
        instance.profile_traveler.save()
    elif instance.type == '1':
        instance.profile_host.save()
