from django.db import models
import uuid


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(null=True, blank=True)
    user_ip = models.GenericIPAddressField()
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    status_code = models.IntegerField()
    request_body = models.JSONField(null=True, blank=True)
    response_time_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.method} {self.path} - {self.status_code}"