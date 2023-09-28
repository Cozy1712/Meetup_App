from .models import myUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        myUser.objects.create(name=instance)
  

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() 