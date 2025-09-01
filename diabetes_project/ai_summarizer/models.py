from django.db import models
import uuid


class AISummary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients_core.Patient', on_delete=models.CASCADE, related_name='ai_summaries')
    resource_type = models.CharField(max_length=32)  # e.g. 'Encounter', 'LabResult', 'MedicationOrder'
    resource_id = models.UUIDField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_summaries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Summary of {self.resource_type} {self.resource_id}"