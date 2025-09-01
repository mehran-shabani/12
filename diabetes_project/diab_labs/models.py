from django.db import models
import uuid


class LabResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients_core.Patient', on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=100)
    test_code = models.CharField(max_length=20, blank=True)
    value = models.CharField(max_length=50)
    unit = models.CharField(max_length=20, blank=True)
    reference_range = models.CharField(max_length=50, blank=True)
    is_abnormal = models.BooleanField(default=False)
    taken_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lab_results'
        ordering = ['-taken_at']

    def __str__(self):
        return f"{self.test_name} for {self.patient.full_name}"