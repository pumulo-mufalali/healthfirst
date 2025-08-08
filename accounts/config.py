from datetime import time
from django.conf import settings


class DashboardConfig:
    """Configuration for dashboard settings and display options."""
    
    # Dashboard card configurations
    CARD_CONFIGS = {
        'patients': {
            'title': 'Total Patients',
            'icon': 'fas fa-users',
            'color': 'primary',
            'description': 'Registered patients in the system'
        },
        'appointments': {
            'title': 'Today\'s Appointments',
            'icon': 'fas fa-calendar-check',
            'color': 'success',
            'description': 'Scheduled appointments for today'
        },
        'records': {
            'title': 'Medical Records',
            'icon': 'fas fa-file-medical',
            'color': 'info',
            'description': 'Total medical records created'
        },
        'revenue': {
            'title': 'Monthly Revenue',
            'icon': 'fas fa-dollar-sign',
            'color': 'warning',
            'description': 'Estimated monthly revenue'
        }
    }
    
    # Chart configurations
    CHART_CONFIGS = {
        'appointment_status': {
            'type': 'doughnut',
            'colors': ['#28a745', '#ffc107', '#dc3545', '#6c757d'],
            'labels': ['Completed', 'Pending', 'Cancelled', 'No Show']
        },
        'patient_growth': {
            'type': 'line',
            'color': '#007bff',
            'fill': True
        },
        'doctor_workload': {
            'type': 'bar',
            'color': '#17a2b8'
        }
    }
    
    # Time periods for analytics
    TIME_PERIODS = {
        'today': 'Today',
        'week': 'This Week',
        'month': 'This Month',
        'quarter': 'This Quarter',
        'year': 'This Year'
    }


class AppointmentConfig:
    """Configuration for appointment-related settings."""
    
    # Appointment status options
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    ]
    
    # Status colors for UI
    STATUS_COLORS = {
        'pending': 'warning',
        'confirmed': 'info',
        'completed': 'success',
        'cancelled': 'danger',
        'no_show': 'secondary'
    }
    
    # Appointment time slots
    TIME_SLOTS = [
        (time(9, 0), '09:00 AM'),
        (time(9, 30), '09:30 AM'),
        (time(10, 0), '10:00 AM'),
        (time(10, 30), '10:30 AM'),
        (time(11, 0), '11:00 AM'),
        (time(11, 30), '11:30 AM'),
        (time(14, 0), '02:00 PM'),
        (time(14, 30), '02:30 PM'),
        (time(15, 0), '03:00 PM'),
        (time(15, 30), '03:30 PM'),
        (time(16, 0), '04:00 PM'),
        (time(16, 30), '04:30 PM'),
    ]
    
    # Appointment duration (in minutes)
    DEFAULT_DURATION = 30
    
    # Maximum appointments per day per doctor
    MAX_APPOINTMENTS_PER_DAY = 20
    
    # Reminder settings
    REMINDER_HOURS = [24, 2]  # Hours before appointment to send reminder


class PatientConfig:
    """Configuration for patient-related settings."""
    
    # Gender choices
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    # Age groups for analytics
    AGE_GROUPS = {
        '0-18': (0, 18),
        '19-30': (19, 30),
        '31-50': (31, 50),
        '51+': (51, 120)
    }
    
    # Required fields for patient registration
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'date_of_birth',
        'gender'
    ]
    
    # Optional fields
    OPTIONAL_FIELDS = [
        'address',
        'emergency_contact',
        'medical_history',
        'allergies'
    ]


class DoctorConfig:
    """Configuration for doctor-related settings."""
    
    # Specialization choices
    SPECIALIZATIONS = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
        ('urology', 'Urology'),
        ('general', 'General Medicine')
    ]
    
    # Availability status
    AVAILABILITY_CHOICES = [
        (True, 'Available'),
        (False, 'Unavailable')
    ]
    
    # Working hours
    WORKING_HOURS = {
        'start': time(9, 0),  # 9:00 AM
        'end': time(17, 0),   # 5:00 PM
        'lunch_start': time(12, 0),  # 12:00 PM
        'lunch_end': time(13, 0),    # 1:00 PM
    }


class NotificationConfig:
    """Configuration for notification settings."""
    
    # Notification types
    NOTIFICATION_TYPES = {
        'appointment_reminder': {
            'title': 'Appointment Reminder',
            'icon': 'calendar-check',
            'color': 'info'
        },
        'appointment_confirmation': {
            'title': 'Appointment Confirmed',
            'icon': 'check-circle',
            'color': 'success'
        },
        'appointment_cancellation': {
            'title': 'Appointment Cancelled',
            'icon': 'times-circle',
            'color': 'danger'
        },
        'new_medical_record': {
            'title': 'New Medical Record',
            'icon': 'file-medical',
            'color': 'primary'
        },
        'system_alert': {
            'title': 'System Alert',
            'icon': 'exclamation-triangle',
            'color': 'warning'
        }
    }
    
    # Notification delivery methods
    DELIVERY_METHODS = [
        'email',
        'sms',
        'in_app'
    ]
    
    # Notification priority levels
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]


class ReportConfig:
    """Configuration for report generation."""
    
    # Report types
    REPORT_TYPES = {
        'monthly_summary': {
            'title': 'Monthly Summary Report',
            'description': 'Comprehensive monthly statistics and analytics',
            'sections': ['appointments', 'patients', 'revenue', 'doctors']
        },
        'doctor_performance': {
            'title': 'Doctor Performance Report',
            'description': 'Individual doctor performance metrics',
            'sections': ['appointments', 'patients', 'completion_rate']
        },
        'patient_analytics': {
            'title': 'Patient Analytics Report',
            'description': 'Patient demographics and trends',
            'sections': ['demographics', 'growth', 'appointments']
        },
        'financial_report': {
            'title': 'Financial Report',
            'description': 'Revenue and financial metrics',
            'sections': ['revenue', 'expenses', 'profit']
        }
    }
    
    # Export formats
    EXPORT_FORMATS = [
        'pdf',
        'excel',
        'csv',
        'json'
    ]
    
    # Date range presets
    DATE_RANGES = {
        'today': 'Today',
        'yesterday': 'Yesterday',
        'last_7_days': 'Last 7 Days',
        'last_30_days': 'Last 30 Days',
        'this_month': 'This Month',
        'last_month': 'Last Month',
        'this_quarter': 'This Quarter',
        'this_year': 'This Year'
    }


class SecurityConfig:
    """Configuration for security settings."""
    
    # Password requirements
    PASSWORD_REQUIREMENTS = {
        'min_length': 8,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special_chars': True
    }
    
    # Session timeout (in minutes)
    SESSION_TIMEOUT = 30
    
    # Login attempt limits
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 15  # minutes
    
    # API rate limiting
    API_RATE_LIMIT = {
        'requests_per_minute': 60,
        'requests_per_hour': 1000
    }


class EmailConfig:
    """Configuration for email settings."""
    
    # Email templates
    EMAIL_TEMPLATES = {
        'appointment_confirmation': {
            'subject': 'Appointment Confirmation - HealthFirst',
            'template': 'emails/appointment_confirmation.html'
        },
        'appointment_reminder': {
            'subject': 'Appointment Reminder - HealthFirst',
            'template': 'emails/appointment_reminder.html'
        },
        'password_reset': {
            'subject': 'Password Reset Request - HealthFirst',
            'template': 'emails/password_reset.html'
        },
        'welcome': {
            'subject': 'Welcome to HealthFirst',
            'template': 'emails/welcome.html'
        }
    }
    
    # Email settings
    EMAIL_SETTINGS = {
        'from_email': 'noreply@healthfirst.com',
        'reply_to': 'support@healthfirst.com',
        'company_name': 'HealthFirst',
        'company_address': '123 Medical Center Dr, Healthcare City, HC 12345'
    }
