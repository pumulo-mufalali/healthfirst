import re
from datetime import date, datetime, time
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .config import SecurityConfig, AppointmentConfig, PatientConfig


class PasswordValidator:
    """Custom password validator to ensure strong passwords."""
    
    @staticmethod
    def validate_password_strength(password):
        """Validate password strength according to security config."""
        errors = []
        
        if len(password) < SecurityConfig.PASSWORD_REQUIREMENTS['min_length']:
            errors.append(f"Password must be at least {SecurityConfig.PASSWORD_REQUIREMENTS['min_length']} characters long.")
        
        if SecurityConfig.PASSWORD_REQUIREMENTS['require_uppercase'] and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")
        
        if SecurityConfig.PASSWORD_REQUIREMENTS['require_lowercase'] and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter.")
        
        if SecurityConfig.PASSWORD_REQUIREMENTS['require_numbers'] and not re.search(r'\d', password):
            errors.append("Password must contain at least one number.")
        
        if SecurityConfig.PASSWORD_REQUIREMENTS['require_special_chars'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character.")
        
        return errors
    
    @staticmethod
    def validate_password_confirmation(password, confirm_password):
        """Validate that password confirmation matches."""
        if password != confirm_password:
            return ["Passwords do not match."]
        return []


class EmailValidator:
    """Email validation utilities."""
    
    @staticmethod
    def validate_email_format(email):
        """Validate email format using regex."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return ["Please enter a valid email address."]
        return []
    
    @staticmethod
    def validate_email_domain(email):
        """Validate email domain (basic check)."""
        domain = email.split('@')[1] if '@' in email else ''
        
        # Basic domain validation
        if not domain or len(domain) < 3:
            return ["Please enter a valid email domain."]
        
        return []


class PhoneValidator:
    """Phone number validation utilities."""
    
    @staticmethod
    def validate_phone_format(phone):
        """Validate phone number format."""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it's a valid length (7-15 digits)
        if len(digits_only) < 7 or len(digits_only) > 15:
            return ["Please enter a valid phone number (7-15 digits)."]
        
        return []
    
    @staticmethod
    def format_phone_number(phone):
        """Format phone number for display."""
        digits_only = re.sub(r'\D', '', phone)
        
        if len(digits_only) == 10:
            return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
        elif len(digits_only) == 11 and digits_only[0] == '1':
            return f"+1 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"
        else:
            return phone


class DateValidator:
    """Date validation utilities."""
    
    @staticmethod
    def validate_date_of_birth(date_of_birth):
        """Validate date of birth."""
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        
        if age < 0:
            return ["Date of birth cannot be in the future."]
        elif age > 120:
            return ["Please enter a valid date of birth."]
        
        return []
    
    @staticmethod
    def validate_appointment_date(appointment_date):
        """Validate appointment date."""
        today = date.today()
        
        if appointment_date < today:
            return ["Appointment date cannot be in the past."]
        
        # Check if appointment is not too far in the future (e.g., 1 year)
        max_future_date = today.replace(year=today.year + 1)
        if appointment_date > max_future_date:
            return ["Appointment date cannot be more than 1 year in the future."]
        
        return []
    
    @staticmethod
    def validate_appointment_time(appointment_time, appointment_date):
        """Validate appointment time."""
        today = date.today()
        
        # If appointment is today, check if time is not in the past
        if appointment_date == today:
            current_time = datetime.now().time()
            if appointment_time < current_time:
                return ["Appointment time cannot be in the past for today's appointments."]
        
        # Check if time is within working hours
        working_start = AppointmentConfig.WORKING_HOURS['start']
        working_end = AppointmentConfig.WORKING_HOURS['end']
        
        if appointment_time < working_start or appointment_time > working_end:
            return ["Appointment time must be within working hours (9:00 AM - 5:00 PM)."]
        
        return []


class NameValidator:
    """Name validation utilities."""
    
    @staticmethod
    def validate_name_format(name):
        """Validate name format."""
        if not name or len(name.strip()) < 2:
            return ["Name must be at least 2 characters long."]
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r'^[a-zA-Z\s\'-]+$', name):
            return ["Name can only contain letters, spaces, hyphens, and apostrophes."]
        
        return []
    
    @staticmethod
    def validate_full_name(first_name, last_name):
        """Validate full name combination."""
        errors = []
        
        # Check if names are different
        if first_name.lower() == last_name.lower():
            errors.append("First name and last name should be different.")
        
        # Check for reasonable length
        if len(first_name) > 50 or len(last_name) > 50:
            errors.append("Name is too long (maximum 50 characters).")
        
        return errors


class AppointmentValidator:
    """Appointment-specific validation utilities."""
    
    @staticmethod
    def validate_appointment_availability(doctor, appointment_date, appointment_time, appointment_id=None):
        """Validate appointment availability."""
        from appointments.models import Appointment
        
        # Check if doctor is available
        if not doctor.is_available:
            return ["Selected doctor is not available for appointments."]
        
        # Check for existing appointments at the same time
        conflicting_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=appointment_date,
            time=appointment_time,
            status__in=['pending', 'confirmed']
        )
        
        if appointment_id:
            conflicting_appointments = conflicting_appointments.exclude(id=appointment_id)
        
        if conflicting_appointments.exists():
            return ["This time slot is already booked for the selected doctor."]
        
        # Check daily appointment limit
        daily_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=appointment_date,
            status__in=['pending', 'confirmed']
        )
        
        if appointment_id:
            daily_appointments = daily_appointments.exclude(id=appointment_id)
        
        if daily_appointments.count() >= AppointmentConfig.MAX_APPOINTMENTS_PER_DAY:
            return ["Doctor has reached maximum appointments for this day."]
        
        return []
    
    @staticmethod
    def validate_appointment_duration(start_time, end_time):
        """Validate appointment duration."""
        if end_time <= start_time:
            return ["End time must be after start time."]
        
        # Calculate duration in minutes
        duration = (end_time.hour - start_time.hour) * 60 + (end_time.minute - start_time.minute)
        
        if duration < 15:
            return ["Appointment duration must be at least 15 minutes."]
        
        if duration > 120:
            return ["Appointment duration cannot exceed 2 hours."]
        
        return []


class PatientValidator:
    """Patient-specific validation utilities."""
    
    @staticmethod
    def validate_patient_data(data):
        """Validate patient registration data."""
        errors = []
        
        # Check required fields
        for field in PatientConfig.REQUIRED_FIELDS:
            if not data.get(field):
                errors.append(f"{field.replace('_', ' ').title()} is required.")
        
        # Validate email
        if data.get('email'):
            errors.extend(EmailValidator.validate_email_format(data['email']))
        
        # Validate phone
        if data.get('phone'):
            errors.extend(PhoneValidator.validate_phone_format(data['phone']))
        
        # Validate names
        if data.get('first_name'):
            errors.extend(NameValidator.validate_name_format(data['first_name']))
        
        if data.get('last_name'):
            errors.extend(NameValidator.validate_name_format(data['last_name']))
        
        # Validate date of birth
        if data.get('date_of_birth'):
            try:
                dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                errors.extend(DateValidator.validate_date_of_birth(dob))
            except ValueError:
                errors.append("Please enter a valid date of birth.")
        
        # Validate gender
        if data.get('gender') and data['gender'] not in [choice[0] for choice in PatientConfig.GENDER_CHOICES]:
            errors.append("Please select a valid gender.")
        
        return errors


class DoctorValidator:
    """Doctor-specific validation utilities."""
    
    @staticmethod
    def validate_doctor_data(data):
        """Validate doctor registration data."""
        errors = []
        
        # Validate names
        if data.get('first_name'):
            errors.extend(NameValidator.validate_name_format(data['first_name']))
        
        if data.get('last_name'):
            errors.extend(NameValidator.validate_name_format(data['last_name']))
        
        # Validate email
        if data.get('email'):
            errors.extend(EmailValidator.validate_email_format(data['email']))
        
        # Validate phone
        if data.get('phone'):
            errors.extend(PhoneValidator.validate_phone_format(data['phone']))
        
        # Validate specialization
        if data.get('specialization'):
            valid_specializations = [choice[0] for choice in DoctorConfig.SPECIALIZATIONS]
            if data['specialization'] not in valid_specializations:
                errors.append("Please select a valid specialization.")
        
        return errors


class FormValidator:
    """General form validation utilities."""
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """Validate that all required fields are present."""
        errors = []
        
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field.replace('_', ' ').title()} is required.")
        
        return errors
    
    @staticmethod
    def validate_field_length(value, field_name, max_length):
        """Validate field length."""
        if value and len(value) > max_length:
            return [f"{field_name.replace('_', ' ').title()} is too long (maximum {max_length} characters)."]
        return []
    
    @staticmethod
    def validate_unique_field(model, field_name, value, exclude_id=None):
        """Validate unique field values."""
        filter_kwargs = {field_name: value}
        if exclude_id:
            filter_kwargs['id__ne'] = exclude_id
        
        if model.objects.filter(**filter_kwargs).exists():
            return [f"{field_name.replace('_', ' ').title()} already exists."]
        
        return []
