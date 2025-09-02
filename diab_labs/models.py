# diab_labs/models.py
from django.db import models
import uuid

class LabResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients_core.Patient', on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=120)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    reference_range = models.CharField(max_length=50, blank=True)
    taken_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-taken_at']
        indexes = [
            models.Index(fields=['patient', 'taken_at']),
            models.Index(fields=['test_name', 'taken_at']),
        ]

    def __str__(self):
        return f"{self.test_name}: {self.value} {self.unit}"