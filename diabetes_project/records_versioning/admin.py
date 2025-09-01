from django.contrib import admin
from .models import RecordVersion


@admin.register(RecordVersion)
class RecordVersionAdmin(admin.ModelAdmin):
    list_display = ['resource_type', 'resource_id', 'version', 'created_at']
    list_filter = ['resource_type', 'created_at']
    search_fields = ['resource_id']
    readonly_fields = ['id', 'created_at', 'snapshot', 'diff']
    ordering = ['-created_at']