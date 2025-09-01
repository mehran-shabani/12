from django.contrib import admin
from .models import LabResult


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['patient', 'test_name', 'value', 'unit', 'is_abnormal', 'taken_at']
    list_filter = ['is_abnormal', 'test_name', 'taken_at']
    search_fields = ['patient__full_name', 'test_name', 'test_code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['patient']
    ordering = ['-taken_at']