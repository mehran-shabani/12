# patients_core/models.py
from django.db import models
import uuid

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=120)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    primary_doctor_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name