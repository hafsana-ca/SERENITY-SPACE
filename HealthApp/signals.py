from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ProfileDB

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileDB.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Ensure that ProfileDB is being saved, not a 'profile' attribute that doesn't exist
    try:
        instance.profiledb.save()  # Use profiledb to match the model name (ProfileDB)
    except ProfileDB.DoesNotExist:
        # If profile doesn't exist, create a new one
        ProfileDB.objects.create(user=instance)
