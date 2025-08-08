from datetime import date, timedelta
from django.db.models import Count, Sum
from patients.models import Patient
from appointments.models import Appointment, MedicalRecord
from doctors.models import Doctor


class DashboardCalculator:
    """Utility class to calculate dashboard statistics and move logic from HTML to Python."""
    
    @staticmethod
    def get_dashboard_stats(user_type=None):
        """Calculate all dashboard statistics and return as a dictionary."""
        today = date.today()
        
        # Basic counts
        total_patients = Patient.objects.count()
        total_doctors = Doctor.objects.count()
        total_appointments = Appointment.objects.count()
        total_medical_records = MedicalRecord.objects.count()
        
        # Today's appointments
        todays_appointments = Appointment.objects.filter(date=today).count()
        
        # Weekly statistics
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        weekly_appointments = Appointment.objects.filter(
            date__range=[week_start, week_end]
        ).count()
        
        # Monthly statistics
        month_start = today.replace(day=1)
        monthly_appointments = Appointment.objects.filter(
            date__gte=month_start
        ).count()
        
        # Appointment status breakdown
        appointment_statuses = Appointment.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Recent appointments (last 7 days)
        recent_appointments = Appointment.objects.filter(
            date__gte=today - timedelta(days=7)
        ).order_by('-date')[:5]
        
        # Patient growth (new patients this month)
        new_patients_this_month = Patient.objects.filter(
            created_at__gte=month_start
        ).count()
        
        # Doctor availability
        available_doctors = Doctor.objects.filter(is_available=True).count()
        
        # Calculate revenue (placeholder - you can integrate with payment system)
        estimated_monthly_revenue = monthly_appointments * 100  # Placeholder calculation
        
        return {
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_appointments': total_appointments,
            'total_medical_records': total_medical_records,
            'todays_appointments': todays_appointments,
            'weekly_appointments': weekly_appointments,
            'monthly_appointments': monthly_appointments,
            'appointment_statuses': appointment_statuses,
            'recent_appointments': recent_appointments,
            'new_patients_this_month': new_patients_this_month,
            'available_doctors': available_doctors,
            'estimated_monthly_revenue': estimated_monthly_revenue,
            'user_type': user_type,
        }
    
    @staticmethod
    def get_patient_dashboard_stats(patient_id):
        """Calculate patient-specific dashboard statistics."""
        today = date.today()
        
        # Patient's appointments
        patient_appointments = Appointment.objects.filter(patient_id=patient_id)
        total_appointments = patient_appointments.count()
        upcoming_appointments = patient_appointments.filter(
            date__gte=today
        ).order_by('date')[:5]
        
        # Patient's medical records
        medical_records = MedicalRecord.objects.filter(patient_id=patient_id)
        total_records = medical_records.count()
        recent_records = medical_records.order_by('-created_at')[:3]
        
        # Prescriptions
        prescriptions = medical_records.filter(record_type='prescription')
        total_prescriptions = prescriptions.count()
        
        return {
            'total_appointments': total_appointments,
            'upcoming_appointments': upcoming_appointments,
            'total_medical_records': total_records,
            'recent_records': recent_records,
            'total_prescriptions': total_prescriptions,
        }
    
    @staticmethod
    def get_doctor_dashboard_stats(doctor_id):
        """Calculate doctor-specific dashboard statistics."""
        today = date.today()
        
        # Doctor's appointments
        doctor_appointments = Appointment.objects.filter(doctor_id=doctor_id)
        total_appointments = doctor_appointments.count()
        todays_appointments = doctor_appointments.filter(date=today).count()
        
        # Upcoming appointments
        upcoming_appointments = doctor_appointments.filter(
            date__gte=today
        ).order_by('date')[:10]
        
        # Patient count
        unique_patients = doctor_appointments.values('patient').distinct().count()
        
        # Medical records created by doctor
        medical_records = MedicalRecord.objects.filter(doctor_id=doctor_id)
        total_records = medical_records.count()
        
        return {
            'total_appointments': total_appointments,
            'todays_appointments': todays_appointments,
            'upcoming_appointments': upcoming_appointments,
            'unique_patients': unique_patients,
            'total_medical_records': total_records,
        }


class TemplateDataProcessor:
    """Process and format data for templates to reduce HTML complexity."""
    
    @staticmethod
    def format_appointment_data(appointments):
        """Format appointment data for template display."""
        formatted_appointments = []
        for appointment in appointments:
            formatted_appointments.append({
                'id': appointment.id,
                'patient_name': appointment.patient.get_full_name(),
                'doctor_name': appointment.doctor.get_full_name(),
                'date': appointment.date.strftime('%B %d, %Y'),
                'time': appointment.time.strftime('%I:%M %p'),
                'status': appointment.get_status_display(),
                'status_class': appointment.get_status_class(),
                'is_today': appointment.date == date.today(),
                'is_upcoming': appointment.date > date.today(),
            })
        return formatted_appointments
    
    @staticmethod
    def format_patient_data(patients):
        """Format patient data for template display."""
        formatted_patients = []
        for patient in patients:
            formatted_patients.append({
                'id': patient.id,
                'name': patient.get_full_name(),
                'email': patient.email,
                'phone': patient.phone,
                'age': patient.calculate_age(),
                'gender': patient.get_gender_display(),
                'last_visit': patient.get_last_appointment_date(),
                'total_appointments': patient.appointment_set.count(),
            })
        return formatted_patients
    
    @staticmethod
    def format_doctor_data(doctors):
        """Format doctor data for template display."""
        formatted_doctors = []
        for doctor in doctors:
            formatted_doctors.append({
                'id': doctor.id,
                'name': doctor.get_full_name(),
                'specialization': doctor.specialization,
                'email': doctor.email,
                'phone': doctor.phone,
                'is_available': doctor.is_available,
                'total_appointments': doctor.appointment_set.count(),
                'total_patients': doctor.appointment_set.values('patient').distinct().count(),
            })
        return formatted_doctors


class NotificationProcessor:
    """Handle notification logic to reduce HTML template complexity."""
    
    @staticmethod
    def get_system_notifications(user):
        """Get system notifications for the user."""
        notifications = []
        today = date.today()
        
        if user.user_type == 'doctor':
            # Doctor-specific notifications
            todays_appointments = Appointment.objects.filter(
                doctor=user.doctor,
                date=today
            ).count()
            
            if todays_appointments > 0:
                notifications.append({
                    'type': 'info',
                    'message': f'You have {todays_appointments} appointment(s) today.',
                    'icon': 'calendar-check'
                })
            
            pending_records = MedicalRecord.objects.filter(
                doctor=user.doctor,
                status='pending'
            ).count()
            
            if pending_records > 0:
                notifications.append({
                    'type': 'warning',
                    'message': f'You have {pending_records} pending medical record(s).',
                    'icon': 'file-medical'
                })
        
        elif user.user_type == 'patient':
            # Patient-specific notifications
            upcoming_appointments = Appointment.objects.filter(
                patient=user.patient,
                date__gte=today
            ).count()
            
            if upcoming_appointments > 0:
                notifications.append({
                    'type': 'info',
                    'message': f'You have {upcoming_appointments} upcoming appointment(s).',
                    'icon': 'calendar'
                })
        
        return notifications
