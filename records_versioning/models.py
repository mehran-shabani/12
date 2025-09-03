# records_versioning/models.py
from django.db import models
import uuid
import json

class RecordVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_type = models.CharField(max_length=48)  # 'Patient', 'Encounter', 'LabResult', 'MedicationOrder'
    resource_id = models.UUIDField()
    version = models.PositiveIntegerField()
    snapshot = models.JSONField()  # کامل snapshot از آبجکت
    diff = models.JSONField(null=True, blank=True)  # تفاوت با نسخه قبل
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['resource_type', 'resource_id', 'version']
        ordering = ['-version']

    def __str__(self):
        return f"{self.resource_type} {self.resource_id} v{self.version}"