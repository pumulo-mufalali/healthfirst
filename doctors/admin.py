from django.contrib import admin
from .models import Doctor, DoctorAvailability
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Doctor Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (DoctorInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'hospital')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')
    list_filter = ('specialization', 'gender', 'available_for_telemedicine')
    raw_id_fields = ('user',)

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'start_time', 'end_time', 'is_available')
    list_filter = ('day', 'is_available')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)