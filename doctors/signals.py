from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_doctor_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update Doctor profile when User is created/updated
    """
    if instance.user_type == 'doctor':
        if created:
            Doctor.objects.create(user=instance)
        else:
            # Update existing profile if it exists
            if hasattr(instance, 'doctor_profile'):
                instance.doctor_profile.save()