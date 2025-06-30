from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Patient

User = get_user_model()

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'patient':
        Patient.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    if hasattr(instance, 'patient_profile'):
        instance.patient_profile.save()