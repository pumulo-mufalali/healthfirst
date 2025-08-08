import json
import csv
from datetime import date, datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.services import ReportGenerator, AnalyticsService
from accounts.utils import DashboardCalculator


class Command(BaseCommand):
    help = 'Generate various reports using Python logic'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['monthly', 'doctor', 'patient', 'financial'],
            default='monthly',
            help='Type of report to generate'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'csv', 'txt'],
            default='json',
            help='Output format'
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Output file path'
        )
        parser.add_argument(
            '--month',
            type=int,
            help='Month for monthly report (1-12)'
        )
        parser.add_argument(
            '--year',
            type=int,
            help='Year for monthly report'
        )
        parser.add_argument(
            '--doctor-id',
            type=int,
            help='Doctor ID for doctor report'
        )
    
    def handle(self, *args, **options):
        report_type = options['type']
        output_format = options['format']
        output_file = options['output']
        
        self.stdout.write(f"Generating {report_type} report in {output_format} format...")
        
        try:
            if report_type == 'monthly':
                report_data = self.generate_monthly_report(options)
            elif report_type == 'doctor':
                report_data = self.generate_doctor_report(options)
            elif report_type == 'patient':
                report_data = self.generate_patient_report(options)
            elif report_type == 'financial':
                report_data = self.generate_financial_report(options)
            else:
                self.stdout.write(self.style.ERROR(f"Unknown report type: {report_type}"))
                return
            
            # Format and output the report
            formatted_data = self.format_report(report_data, output_format)
            
            if output_file:
                self.save_to_file(formatted_data, output_file, output_format)
                self.stdout.write(f"Report saved to {output_file}")
            else:
                self.stdout.write(formatted_data)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error generating report: {str(e)}"))
    
    def generate_monthly_report(self, options):
        """Generate monthly report."""
        month = options.get('month') or date.today().month
        year = options.get('year') or date.today().year
        
        report_data = ReportGenerator.generate_monthly_report(month, year)
        
        # Add additional analytics
        analytics = AnalyticsService.get_appointment_analytics()
        patient_analytics = AnalyticsService.get_patient_analytics()
        doctor_analytics = AnalyticsService.get_doctor_analytics()
        
        return {
            'report_type': 'monthly',
            'period': f"{month}/{year}",
            'generated_at': datetime.now().isoformat(),
            'summary': report_data['summary'],
            'analytics': analytics,
            'patient_analytics': patient_analytics,
            'doctor_analytics': doctor_analytics,
        }
    
    def generate_doctor_report(self, options):
        """Generate doctor performance report."""
        doctor_id = options.get('doctor_id')
        if not doctor_id:
            self.stdout.write(self.style.ERROR("Doctor ID is required for doctor report"))
            return None
        
        report_data = ReportGenerator.generate_doctor_report(doctor_id)
        
        return {
            'report_type': 'doctor',
            'doctor_id': doctor_id,
            'generated_at': datetime.now().isoformat(),
            'data': report_data,
        }
    
    def generate_patient_report(self, options):
        """Generate patient analytics report."""
        patient_analytics = AnalyticsService.get_patient_analytics()
        
        return {
            'report_type': 'patient',
            'generated_at': datetime.now().isoformat(),
            'analytics': patient_analytics,
        }
    
    def generate_financial_report(self, options):
        """Generate financial report."""
        # Get appointment analytics for revenue calculation
        analytics = AnalyticsService.get_appointment_analytics()
        
        # Calculate revenue (placeholder - integrate with payment system)
        completed_appointments = analytics['completed_appointments']
        estimated_revenue = completed_appointments * 100  # Placeholder calculation
        
        return {
            'report_type': 'financial',
            'generated_at': datetime.now().isoformat(),
            'revenue': {
                'total_revenue': estimated_revenue,
                'completed_appointments': completed_appointments,
                'average_per_appointment': estimated_revenue / completed_appointments if completed_appointments > 0 else 0,
            },
            'analytics': analytics,
        }
    
    def format_report(self, data, format_type):
        """Format report data for output."""
        if format_type == 'json':
            return json.dumps(data, indent=2, default=str)
        elif format_type == 'csv':
            return self.convert_to_csv(data)
        elif format_type == 'txt':
            return self.convert_to_text(data)
        else:
            return str(data)
    
    def convert_to_csv(self, data):
        """Convert report data to CSV format."""
        if not data:
            return ""
        
        output = []
        
        if data.get('report_type') == 'monthly':
            # Summary section
            output.append("Monthly Report Summary")
            output.append("Period,Total Appointments,Completed,Cancelled,New Patients,Revenue")
            summary = data.get('summary', {})
            output.append(f"{summary.get('period', '')},{summary.get('total_appointments', 0)},{summary.get('completed_appointments', 0)},{summary.get('cancelled_appointments', 0)},{summary.get('new_patients', 0)},{summary.get('total_revenue', 0)}")
            
            # Analytics section
            output.append("\nAppointment Analytics")
            output.append("Date,Count")
            analytics = data.get('analytics', {})
            for daily_count in analytics.get('daily_counts', []):
                output.append(f"{daily_count.get('date', '')},{daily_count.get('count', 0)}")
        
        return '\n'.join(output)
    
    def convert_to_text(self, data):
        """Convert report data to text format."""
        if not data:
            return ""
        
        output = []
        
        if data.get('report_type') == 'monthly':
            output.append("=" * 50)
            output.append("MONTHLY REPORT")
            output.append("=" * 50)
            
            summary = data.get('summary', {})
            output.append(f"Period: {summary.get('period', '')}")
            output.append(f"Total Appointments: {summary.get('total_appointments', 0)}")
            output.append(f"Completed: {summary.get('completed_appointments', 0)}")
            output.append(f"Cancelled: {summary.get('cancelled_appointments', 0)}")
            output.append(f"New Patients: {summary.get('new_patients', 0)}")
            output.append(f"Revenue: ${summary.get('total_revenue', 0)}")
            
            output.append("\n" + "=" * 30)
            output.append("PATIENT ANALYTICS")
            output.append("=" * 30)
            
            patient_analytics = data.get('patient_analytics', {})
            output.append(f"Total Patients: {patient_analytics.get('total_patients', 0)}")
            output.append(f"New This Month: {patient_analytics.get('new_patients_this_month', 0)}")
            output.append(f"Growth Rate: {patient_analytics.get('growth_rate', 0):.1f}%")
        
        return '\n'.join(output)
    
    def save_to_file(self, data, file_path, format_type):
        """Save report data to file."""
        mode = 'w'
        if format_type == 'csv':
            mode = 'w'
        elif format_type == 'json':
            mode = 'w'
        else:
            mode = 'w'
        
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(data)
