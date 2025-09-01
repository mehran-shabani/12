# diab_medications/models.py
from django.db import models
import uuid

class MedicationOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients_core.Patient', on_delete=models.CASCADE, related_name='medication_orders')
    drug_name = models.CharField(max_length=120)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.drug_name} ({self.dosage}) for {self.patient.full_name}"