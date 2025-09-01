from django.db import models
import uuid


class Encounter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('patients_core.Patient', on_delete=models.CASCADE, related_name='encounters')
    occurred_at = models.DateTimeField()
    subjective = models.TextField(blank=True)
    objective = models.JSONField(default=dict, blank=True)
    assessment = models.JSONField(default=dict, blank=True)
    plan = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'encounters'
        ordering = ['-occurred_at']

    def __str__(self):
        return f"Encounter {self.id} for {self.patient.full_name}"