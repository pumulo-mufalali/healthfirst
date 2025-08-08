#!/usr/bin/env python3
"""
Python Enhancement Demo for HealthFirst Project

This script demonstrates how we've increased Python usage and reduced HTML complexity
by moving business logic from templates to Python modules.
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthfirst.settings')
django.setup()

from accounts.utils import DashboardCalculator, TemplateDataProcessor, NotificationProcessor
from accounts.services import AnalyticsService, ReportGenerator, DataExportService
from accounts.config import DashboardConfig, AppointmentConfig, PatientConfig
from accounts.validators import PasswordValidator, EmailValidator, PhoneValidator


def demonstrate_dashboard_calculations():
    """Demonstrate dashboard calculations moved from HTML to Python."""
    print("=" * 60)
    print("DASHBOARD CALCULATIONS (Python Logic)")
    print("=" * 60)
    
    # Get dashboard statistics using Python utilities
    stats = DashboardCalculator.get_dashboard_stats('admin')
    
    print(f"Total Patients: {stats['total_patients']}")
    print(f"Total Doctors: {stats['total_doctors']}")
    print(f"Today's Appointments: {stats['todays_appointments']}")
    print(f"Weekly Appointments: {stats['weekly_appointments']}")
    print(f"Monthly Appointments: {stats['monthly_appointments']}")
    print(f"Estimated Revenue: ${stats['estimated_monthly_revenue']}")
    print(f"New Patients This Month: {stats['new_patients_this_month']}")
    print(f"Available Doctors: {stats['available_doctors']}")
    
    # Show appointment status breakdown
    print("\nAppointment Status Breakdown:")
    for status in stats['appointment_statuses']:
        print(f"  {status['status']}: {status['count']}")


def demonstrate_analytics_service():
    """Demonstrate analytics service functionality."""
    print("\n" + "=" * 60)
    print("ANALYTICS SERVICE (Python Business Logic)")
    print("=" * 60)
    
    # Get appointment analytics
    appointment_analytics = AnalyticsService.get_appointment_analytics()
    
    print(f"Total Appointments: {appointment_analytics['total_appointments']}")
    print(f"Completed Appointments: {appointment_analytics['completed_appointments']}")
    print(f"Cancelled Appointments: {appointment_analytics['cancelled_appointments']}")
    
    # Get patient analytics
    patient_analytics = AnalyticsService.get_patient_analytics()
    
    print(f"\nPatient Analytics:")
    print(f"Total Patients: {patient_analytics['total_patients']}")
    print(f"New Patients This Month: {patient_analytics['new_patients_this_month']}")
    print(f"Growth Rate: {patient_analytics['growth_rate']:.1f}%")
    
    # Get doctor analytics
    doctor_analytics = AnalyticsService.get_doctor_analytics()
    
    print(f"\nDoctor Analytics:")
    print(f"Total Doctors: {doctor_analytics['total_doctors']}")
    print(f"Available Doctors: {doctor_analytics['available_doctors']}")
    print(f"Average Appointments per Doctor: {doctor_analytics['avg_appointments_per_doctor']:.1f}")


def demonstrate_report_generation():
    """Demonstrate report generation using Python."""
    print("\n" + "=" * 60)
    print("REPORT GENERATION (Python Logic)")
    print("=" * 60)
    
    # Generate monthly report
    monthly_report = ReportGenerator.generate_monthly_report()
    
    print("Monthly Report Summary:")
    summary = monthly_report['summary']
    print(f"Period: {summary['period']}")
    print(f"Total Appointments: {summary['total_appointments']}")
    print(f"Completed: {summary['completed_appointments']}")
    print(f"Cancelled: {summary['cancelled_appointments']}")
    print(f"New Patients: {summary['new_patients']}")
    print(f"Total Revenue: ${summary['total_revenue']}")
    print(f"Completion Rate: {summary['completion_rate']:.1f}%")


def demonstrate_data_processing():
    """Demonstrate data processing utilities."""
    print("\n" + "=" * 60)
    print("DATA PROCESSING (Python Utilities)")
    print("=" * 60)
    
    # Show configuration options
    print("Dashboard Card Configurations:")
    for card_type, config in DashboardConfig.CARD_CONFIGS.items():
        print(f"  {card_type}: {config['title']} ({config['color']})")
    
    print("\nAppointment Status Colors:")
    for status, color in AppointmentConfig.STATUS_COLORS.items():
        print(f"  {status}: {color}")
    
    print("\nPatient Gender Choices:")
    for code, label in PatientConfig.GENDER_CHOICES:
        print(f"  {code}: {label}")


def demonstrate_validation():
    """Demonstrate validation utilities."""
    print("\n" + "=" * 60)
    print("VALIDATION UTILITIES (Python Logic)")
    print("=" * 60)
    
    # Test password validation
    test_passwords = [
        "weak",
        "Strong123!",
        "no_uppercase123!",
        "NO_LOWERCASE123!",
        "NoNumbers!",
        "NoSpecial123"
    ]
    
    print("Password Validation Tests:")
    for password in test_passwords:
        errors = PasswordValidator.validate_password_strength(password)
        status = "✓ Valid" if not errors else "✗ Invalid"
        print(f"  '{password}': {status}")
        if errors:
            for error in errors:
                print(f"    - {error}")
    
    # Test email validation
    test_emails = [
        "valid@example.com",
        "invalid-email",
        "no@domain",
        "spaces @example.com"
    ]
    
    print("\nEmail Validation Tests:")
    for email in test_emails:
        errors = EmailValidator.validate_email_format(email)
        status = "✓ Valid" if not errors else "✗ Invalid"
        print(f"  '{email}': {status}")
        if errors:
            for error in errors:
                print(f"    - {error}")
    
    # Test phone validation
    test_phones = [
        "1234567890",
        "123-456-7890",
        "(123) 456-7890",
        "123",
        "1234567890123456"
    ]
    
    print("\nPhone Validation Tests:")
    for phone in test_phones:
        errors = PhoneValidator.validate_phone_format(phone)
        status = "✓ Valid" if not errors else "✗ Invalid"
        print(f"  '{phone}': {status}")
        if errors:
            for error in errors:
                print(f"    - {error}")


def demonstrate_data_export():
    """Demonstrate data export functionality."""
    print("\n" + "=" * 60)
    print("DATA EXPORT (Python Processing)")
    print("=" * 60)
    
    # Export appointment data
    appointment_data = DataExportService.export_appointments_to_dict()
    
    print(f"Exported {len(appointment_data)} appointments")
    if appointment_data:
        print("Sample appointment data:")
        sample = appointment_data[0]
        for key, value in sample.items():
            print(f"  {key}: {value}")
    
    # Export patient data
    patient_data = DataExportService.export_patients_to_dict()
    
    print(f"\nExported {len(patient_data)} patients")
    if patient_data:
        print("Sample patient data:")
        sample = patient_data[0]
        for key, value in sample.items():
            print(f"  {key}: {value}")


def show_python_enhancement_summary():
    """Show summary of Python enhancements."""
    print("\n" + "=" * 60)
    print("PYTHON ENHANCEMENT SUMMARY")
    print("=" * 60)
    
    enhancements = [
        "✅ DashboardCalculator - Moved dashboard logic from HTML to Python",
        "✅ AnalyticsService - Centralized analytics calculations",
        "✅ ReportGenerator - Python-based report generation",
        "✅ TemplateDataProcessor - Data formatting utilities",
        "✅ NotificationProcessor - Notification logic in Python",
        "✅ DataExportService - Export functionality in Python",
        "✅ Configuration classes - Centralized settings",
        "✅ Validation utilities - Form validation in Python",
        "✅ API handlers - Data processing endpoints",
        "✅ Management commands - Report generation scripts"
    ]
    
    for enhancement in enhancements:
        print(enhancement)
    
    print("\nBenefits:")
    benefits = [
        "🔹 Reduced HTML template complexity",
        "🔹 Improved code maintainability",
        "🔹 Better separation of concerns",
        "🔹 Enhanced testability",
        "🔹 Centralized business logic",
        "🔹 Reusable Python utilities",
        "🔹 API-driven data processing",
        "🔹 Configuration-driven approach"
    ]
    
    for benefit in benefits:
        print(benefit)


def main():
    """Main demonstration function."""
    print("HealthFirst Python Enhancement Demonstration")
    print("=" * 60)
    print("This script demonstrates how we've increased Python usage")
    print("and reduced HTML template complexity in the project.\n")
    
    try:
        demonstrate_dashboard_calculations()
        demonstrate_analytics_service()
        demonstrate_report_generation()
        demonstrate_data_processing()
        demonstrate_validation()
        demonstrate_data_export()
        show_python_enhancement_summary()
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("The project now has significantly more Python code")
        print("and reduced HTML template complexity.")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
