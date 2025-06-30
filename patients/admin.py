from django.contrib import admin
from .models import Patient
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Patient Profile'
    fk_name = 'user'

@admin.display(description='Age')
def age_display(self, obj):
    return obj.age if obj.age is not None else "N/A"

class CustomUserAdmin(UserAdmin):
    inlines = (PatientInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'blood_group')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    list_filter = ('gender', 'blood_group')
    raw_id_fields = ('user',)

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)