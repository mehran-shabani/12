from django.contrib import admin
from .models import MedicationOrder


@admin.register(MedicationOrder)
class MedicationOrderAdmin(admin.ModelAdmin):
    list_display = ['patient', 'drug_name', 'dosage', 'frequency', 'is_active', 'start_date']
    list_filter = ['is_active', 'route', 'start_date']
    search_fields = ['patient__full_name', 'drug_name', 'drug_code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['patient']
    ordering = ['-start_date']