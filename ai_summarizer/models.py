# ai_summarizer/models.py
from django.db import models
import uuid

class AISummary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients_core.Patient', on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=32)  # 'Encounter', 'LabResult', 'MedicationOrder'
    resource_id = models.UUIDField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary of {self.resource_type} {self.resource_id}"