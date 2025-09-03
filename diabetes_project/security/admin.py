from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['method', 'path', 'status_code', 'user_ip', 'response_time_ms', 'created_at']
    list_filter = ['method', 'status_code', 'created_at']
    search_fields = ['path', 'user_ip']
    readonly_fields = ['id', 'created_at', 'request_body']
    ordering = ['-created_at']