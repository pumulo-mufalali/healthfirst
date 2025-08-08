import json
from datetime import date, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import AnalyticsService, ReportGenerator, DataExportService
from .utils import DashboardCalculator, TemplateDataProcessor


class APIResponseHandler:
    """Handle API responses and data formatting."""
    
    @staticmethod
    def success_response(data, message="Success"):
        """Return a standardized success response."""
        return JsonResponse({
            'status': 'success',
            'message': message,
            'data': data
        })
    
    @staticmethod
    def error_response(message, status_code=400):
        """Return a standardized error response."""
        return JsonResponse({
            'status': 'error',
            'message': message
        }, status=status_code)


@csrf_exempt
@require_http_methods(["GET"])
def dashboard_stats_api(request):
    """API endpoint for dashboard statistics."""
    try:
        user_type = request.GET.get('user_type', 'admin')
        stats = DashboardCalculator.get_dashboard_stats(user_type)
        
        # Format data for API response
        formatted_stats = {
            'summary': {
                'total_patients': stats['total_patients'],
                'total_doctors': stats['total_doctors'],
                'total_appointments': stats['total_appointments'],
                'todays_appointments': stats['todays_appointments'],
                'weekly_appointments': stats['weekly_appointments'],
                'monthly_appointments': stats['monthly_appointments'],
                'estimated_revenue': stats['estimated_monthly_revenue'],
            },
            'charts': {
                'appointment_statuses': list(stats['appointment_statuses']),
                'recent_appointments': TemplateDataProcessor.format_appointment_data(
                    stats['recent_appointments']
                ),
            },
            'metrics': {
                'new_patients_this_month': stats['new_patients_this_month'],
                'available_doctors': stats['available_doctors'],
            }
        }
        
        return APIResponseHandler.success_response(formatted_stats)
    
    except Exception as e:
        return APIResponseHandler.error_response(str(e))


@csrf_exempt
@require_http_methods(["GET"])
def analytics_api(request):
    """API endpoint for analytics data."""
    try:
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = date.fromisoformat(start_date_str)
        if end_date_str:
            end_date = date.fromisoformat(end_date_str)
        
        # Get appointment analytics
        appointment_analytics = AnalyticsService.get_appointment_analytics(start_date, end_date)
        
        # Get patient analytics
        patient_analytics = AnalyticsService.get_patient_analytics()
        
        # Get doctor analytics
        doctor_analytics = AnalyticsService.get_doctor_analytics()
        
        analytics_data = {
            'appointments': appointment_analytics,
            'patients': patient_analytics,
            'doctors': doctor_analytics,
        }
        
        return APIResponseHandler.success_response(analytics_data)
    
    except Exception as e:
        return APIResponseHandler.error_response(str(e))


@csrf_exempt
@require_http_methods(["GET"])
def report_api(request):
    """API endpoint for generating reports."""
    try:
        report_type = request.GET.get('type', 'monthly')
        
        if report_type == 'monthly':
            month = int(request.GET.get('month', date.today().month))
            year = int(request.GET.get('year', date.today().year))
            report_data = ReportGenerator.generate_monthly_report(month, year)
        
        elif report_type == 'doctor':
            doctor_id = int(request.GET.get('doctor_id'))
            start_date_str = request.GET.get('start_date')
            end_date_str = request.GET.get('end_date')
            
            start_date = None
            end_date = None
            
            if start_date_str:
                start_date = date.fromisoformat(start_date_str)
            if end_date_str:
                end_date = date.fromisoformat(end_date_str)
            
            report_data = ReportGenerator.generate_doctor_report(doctor_id, start_date, end_date)
        
        else:
            return APIResponseHandler.error_response("Invalid report type")
        
        return APIResponseHandler.success_response(report_data)
    
    except Exception as e:
        return APIResponseHandler.error_response(str(e))


@csrf_exempt
@require_http_methods(["GET"])
def export_api(request):
    """API endpoint for data export."""
    try:
        export_type = request.GET.get('type', 'appointments')
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = date.fromisoformat(start_date_str)
        if end_date_str:
            end_date = date.fromisoformat(end_date_str)
        
        if export_type == 'appointments':
            export_data = DataExportService.export_appointments_to_dict(start_date, end_date)
        elif export_type == 'patients':
            export_data = DataExportService.export_patients_to_dict()
        else:
            return APIResponseHandler.error_response("Invalid export type")
        
        return APIResponseHandler.success_response(export_data)
    
    except Exception as e:
        return APIResponseHandler.error_response(str(e))


class DataProcessor:
    """Process and transform data for different use cases."""
    
    @staticmethod
    def process_appointment_data(appointments):
        """Process appointment data for different views."""
        processed_data = {
            'summary': {
                'total': len(appointments),
                'today': len([a for a in appointments if a.date == date.today()]),
                'upcoming': len([a for a in appointments if a.date > date.today()]),
                'completed': len([a for a in appointments if a.status == 'completed']),
                'cancelled': len([a for a in appointments if a.status == 'cancelled']),
            },
            'by_date': {},
            'by_doctor': {},
            'by_status': {},
        }
        
        for appointment in appointments:
            # Group by date
            date_key = appointment.date.strftime('%Y-%m-%d')
            if date_key not in processed_data['by_date']:
                processed_data['by_date'][date_key] = []
            processed_data['by_date'][date_key].append(appointment)
            
            # Group by doctor
            doctor_key = appointment.doctor.get_full_name()
            if doctor_key not in processed_data['by_doctor']:
                processed_data['by_doctor'][doctor_key] = []
            processed_data['by_doctor'][doctor_key].append(appointment)
            
            # Group by status
            status_key = appointment.get_status_display()
            if status_key not in processed_data['by_status']:
                processed_data['by_status'][status_key] = []
            processed_data['by_status'][status_key].append(appointment)
        
        return processed_data
    
    @staticmethod
    def process_patient_data(patients):
        """Process patient data for different views."""
        processed_data = {
            'summary': {
                'total': len(patients),
                'male': len([p for p in patients if p.gender == 'M']),
                'female': len([p for p in patients if p.gender == 'F']),
                'new_this_month': len([p for p in patients if p.created_at.month == date.today().month]),
            },
            'by_age_group': {
                '0-18': [],
                '19-30': [],
                '31-50': [],
                '51+': [],
            },
            'by_gender': {
                'Male': [],
                'Female': [],
            },
        }
        
        for patient in patients:
            # Group by age
            age = patient.calculate_age()
            if age <= 18:
                processed_data['by_age_group']['0-18'].append(patient)
            elif age <= 30:
                processed_data['by_age_group']['19-30'].append(patient)
            elif age <= 50:
                processed_data['by_age_group']['31-50'].append(patient)
            else:
                processed_data['by_age_group']['51+'].append(patient)
            
            # Group by gender
            gender_key = patient.get_gender_display()
            processed_data['by_gender'][gender_key].append(patient)
        
        return processed_data
    
    @staticmethod
    def process_doctor_data(doctors):
        """Process doctor data for different views."""
        processed_data = {
            'summary': {
                'total': len(doctors),
                'available': len([d for d in doctors if d.is_available]),
                'unavailable': len([d for d in doctors if not d.is_available]),
            },
            'by_specialization': {},
            'by_availability': {
                'Available': [],
                'Unavailable': [],
            },
        }
        
        for doctor in doctors:
            # Group by specialization
            spec_key = doctor.specialization
            if spec_key not in processed_data['by_specialization']:
                processed_data['by_specialization'][spec_key] = []
            processed_data['by_specialization'][spec_key].append(doctor)
            
            # Group by availability
            availability_key = 'Available' if doctor.is_available else 'Unavailable'
            processed_data['by_availability'][availability_key].append(doctor)
        
        return processed_data
