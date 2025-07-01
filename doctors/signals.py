from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()

@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'doctor':
        print('PROFILE CREATEDDDDDDDDDDDDD')
        Doctor.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_doctor_profile(sender, instance, **kwargs):
    if hasattr(instance, 'doctor_profile'):
        instance.doctor_profile.save()