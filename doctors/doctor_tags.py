from django import template
from django import template
from django.contrib.auth import get_user_model
from .models import Doctor, Specialization


register = template.Library()
User = get_user_model()

@register.filter
def is_admin_or_staff(user):
    return user.is_authenticated and (user.user_type in ['admin', 'staff'] or user.is_superuser)

register = template.Library()
User = get_user_model()

@register.filter
def is_admin_or_staff(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.user_type in ['admin', 'staff'] or user.is_superuser)

@register.filter
def is_doctor(user):
    """Check if user is a doctor"""
    return user.is_authenticated and user.user_type == 'doctor'


@register.filter
def doctor_rating_stars(rating):
    """Convert numeric rating to star icons"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return {
        'full': range(full_stars),
        'half': range(half_star),
        'empty': range(empty_stars)
    }

@register.filter
def doctor_availability_status(doctor):
    """Check if doctor is currently available"""
    from datetime import datetime, time
    now = datetime.now()
    current_day = now.strftime('%a')
    current_time = now.time()
    
    availability = doctor.availabilities.filter(
        day=current_day,
        start_time__lte=current_time,
        end_time__gte=current_time,
        is_available=True
    ).exists()
    
    return "Available" if availability else "Not Available"

@register.simple_tag
def doctor_contact_info(doctor):
    """Format doctor's contact information"""
    return f"{doctor.user.phone} | {doctor.user.email}"

@register.filter
def years_experience_display(years):
    """Format years of experience display"""
    if years == 1:
        return "1 year"
    return f"{years} years"