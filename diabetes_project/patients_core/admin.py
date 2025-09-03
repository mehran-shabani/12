from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'national_id', 'sex', 'dob', 'created_at']
    list_filter = ['sex', 'created_at']
    search_fields = ['full_name', 'national_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']