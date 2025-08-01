from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Doctor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    SPECIALIZATION_CHOICES = (
        ('cardiology', 'Cardiology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('neurology', 'Neurology'),
        ('gynecology', 'Gynecology'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    hospital = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    education = models.TextField(help_text="Degrees and institutions", null=True, blank=True)
    certifications = models.TextField(blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average_rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True, blank=True,
    )
    available_for_telemedicine = models.BooleanField(default=False, null=True, blank=True)
    available_days = models.CharField(max_length=100, help_text="Comma-separated days (e.g., Mon,Tue,Wed)", null=True, blank=True)
    available_hours = models.CharField(max_length=100, help_text="e.g., 9:00 AM - 5:00 PM", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.last_name}"

    @property
    def age(self):
        if self.date_of_birth: 
            import datetime
            return int((datetime.date.today() - self.date_of_birth).days / 365.25)
        return None

class DoctorAvailability(models.Model):
    DAY_CHOICES = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'day')
        verbose_name_plural = 'Doctor Availabilities'

    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.get_day_display()} {self.start_time}-{self.end_time}"