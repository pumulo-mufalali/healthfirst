from datetime import date, timedelta
from django.db.models import Q, Count, Avg
from django.contrib.auth import get_user_model
from patients.models import Patient
from appointments.models import Appointment, MedicalRecord
from doctors.models import Doctor


class AnalyticsService:
    """Service class for handling analytics and reporting logic."""
    
    @staticmethod
    def get_appointment_analytics(start_date=None, end_date=None):
        """Calculate appointment analytics for reporting."""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        appointments = Appointment.objects.filter(
            date__range=[start_date, end_date]
        )
        
        # Daily appointment counts
        daily_counts = appointments.values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Status breakdown
        status_breakdown = appointments.values('status').annotate(
            count=Count('id')
        )
        
        # Doctor performance
        doctor_performance = appointments.values(
            'doctor__first_name', 'doctor__last_name'
        ).annotate(
            total_appointments=Count('id'),
            completed_appointments=Count('id', filter=Q(status='completed')),
            cancelled_appointments=Count('id', filter=Q(status='cancelled'))
        )
        
        # Patient demographics
        patient_demographics = appointments.values(
            'patient__gender'
        ).annotate(
            count=Count('id')
        )
        
        return {
            'daily_counts': daily_counts,
            'status_breakdown': status_breakdown,
            'doctor_performance': doctor_performance,
            'patient_demographics': patient_demographics,
            'total_appointments': appointments.count(),
            'completed_appointments': appointments.filter(status='completed').count(),
            'cancelled_appointments': appointments.filter(status='cancelled').count(),
        }
    
    @staticmethod
    def get_patient_analytics():
        """Calculate patient analytics and trends."""
        today = date.today()
        month_start = today.replace(day=1)
        
        # New patients this month
        new_patients = Patient.objects.filter(
            created_at__gte=month_start
        ).count()
        
        # Patient growth rate
        last_month_start = (month_start - timedelta(days=1)).replace(day=1)
        last_month_patients = Patient.objects.filter(
            created_at__gte=last_month_start,
            created_at__lt=month_start
        ).count()
        
        growth_rate = 0
        if last_month_patients > 0:
            growth_rate = ((new_patients - last_month_patients) / last_month_patients) * 100
        
        # Patient age distribution
        age_distribution = Patient.objects.extra(
            select={'age': 'EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))'}
        ).values('age').annotate(count=Count('id'))
        
        # Gender distribution
        gender_distribution = Patient.objects.values('gender').annotate(
            count=Count('id')
        )
        
        return {
            'new_patients_this_month': new_patients,
            'growth_rate': growth_rate,
            'age_distribution': age_distribution,
            'gender_distribution': gender_distribution,
            'total_patients': Patient.objects.count(),
        }
    
    @staticmethod
    def get_doctor_analytics():
        """Calculate doctor performance analytics."""
        # Doctor workload
        doctor_workload = Doctor.objects.annotate(
            total_appointments=Count('appointment'),
            completed_appointments=Count('appointment', filter=Q(appointment__status='completed')),
            pending_appointments=Count('appointment', filter=Q(appointment__status='pending')),
        )
        
        # Average appointments per doctor
        avg_appointments = doctor_workload.aggregate(
            avg_appointments=Avg('total_appointments')
        )['avg_appointments'] or 0
        
        # Most active doctors
        most_active_doctors = doctor_workload.order_by('-total_appointments')[:5]
        
        # Specialization distribution
        specialization_distribution = Doctor.objects.values('specialization').annotate(
            count=Count('id')
        )
        
        return {
            'doctor_workload': doctor_workload,
            'avg_appointments_per_doctor': avg_appointments,
            'most_active_doctors': most_active_doctors,
            'specialization_distribution': specialization_distribution,
            'total_doctors': Doctor.objects.count(),
            'available_doctors': Doctor.objects.filter(is_available=True).count(),
        }


class ReportGenerator:
    """Generate various reports using Python logic instead of HTML templates."""
    
    @staticmethod
    def generate_monthly_report(month=None, year=None):
        """Generate comprehensive monthly report."""
        if not month:
            month = date.today().month
        if not year:
            year = date.today().year
        
        report_date = date(year, month, 1)
        next_month = (report_date + timedelta(days=32)).replace(day=1)
        
        # Get analytics for the month
        analytics = AnalyticsService.get_appointment_analytics(report_date, next_month - timedelta(days=1))
        patient_analytics = AnalyticsService.get_patient_analytics()
        doctor_analytics = AnalyticsService.get_doctor_analytics()
        
        # Calculate revenue (placeholder)
        revenue = analytics['completed_appointments'] * 100
        
        # Generate report summary
        report_summary = {
            'period': f"{report_date.strftime('%B %Y')}",
            'total_appointments': analytics['total_appointments'],
            'completed_appointments': analytics['completed_appointments'],
            'cancelled_appointments': analytics['cancelled_appointments'],
            'new_patients': patient_analytics['new_patients_this_month'],
            'total_revenue': revenue,
            'completion_rate': (analytics['completed_appointments'] / analytics['total_appointments'] * 100) if analytics['total_appointments'] > 0 else 0,
        }
        
        return {
            'summary': report_summary,
            'analytics': analytics,
            'patient_analytics': patient_analytics,
            'doctor_analytics': doctor_analytics,
        }
    
    @staticmethod
    def generate_doctor_report(doctor_id, start_date=None, end_date=None):
        """Generate doctor-specific performance report."""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        doctor = Doctor.objects.get(id=doctor_id)
        appointments = Appointment.objects.filter(
            doctor=doctor,
            date__range=[start_date, end_date]
        )
        
        # Doctor's appointment statistics
        appointment_stats = {
            'total': appointments.count(),
            'completed': appointments.filter(status='completed').count(),
            'cancelled': appointments.filter(status='cancelled').count(),
            'pending': appointments.filter(status='pending').count(),
        }
        
        # Patient count
        unique_patients = appointments.values('patient').distinct().count()
        
        # Medical records created
        medical_records = MedicalRecord.objects.filter(
            doctor=doctor,
            created_at__range=[start_date, end_date]
        ).count()
        
        # Calculate completion rate
        completion_rate = 0
        if appointment_stats['total'] > 0:
            completion_rate = (appointment_stats['completed'] / appointment_stats['total']) * 100
        
        return {
            'doctor': doctor,
            'period': f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}",
            'appointment_stats': appointment_stats,
            'unique_patients': unique_patients,
            'medical_records': medical_records,
            'completion_rate': completion_rate,
        }


class DataExportService:
    """Handle data export functionality using Python."""
    
    @staticmethod
    def export_appointments_to_dict(start_date=None, end_date=None):
        """Export appointment data to dictionary format."""
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        appointments = Appointment.objects.filter(
            date__range=[start_date, end_date]
        ).select_related('patient', 'doctor')
        
        export_data = []
        for appointment in appointments:
            export_data.append({
                'id': appointment.id,
                'patient_name': appointment.patient.get_full_name(),
                'doctor_name': appointment.doctor.get_full_name(),
                'date': appointment.date.strftime('%Y-%m-%d'),
                'time': appointment.time.strftime('%H:%M'),
                'status': appointment.get_status_display(),
                'notes': appointment.notes or '',
                'created_at': appointment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return export_data
    
    @staticmethod
    def export_patients_to_dict():
        """Export patient data to dictionary format."""
        patients = Patient.objects.all()
        
        export_data = []
        for patient in patients:
            export_data.append({
                'id': patient.id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'email': patient.email,
                'phone': patient.phone,
                'gender': patient.get_gender_display(),
                'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),
                'address': patient.address or '',
                'created_at': patient.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return export_data
