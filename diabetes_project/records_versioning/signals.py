from django.db.models.signals import post_save
from django.dispatch import receiver
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from .services import VersioningService


# Define which models should be versioned
VERSIONED_MODELS = [Patient, Encounter, LabResult, MedicationOrder]


def create_version_for_model(sender, instance, created, **kwargs):
    """Create a version record when a model is saved"""
    if created:
        # Skip versioning for new records
        return
    
    service = VersioningService()
    resource_type = sender.__name__
    resource_id = str(instance.pk)
    
    # Create snapshot
    snapshot = service.get_model_snapshot(instance)
    
    # Create version
    service.create_version(resource_type, resource_id, snapshot)


# Connect signals for all versioned models
for model in VERSIONED_MODELS:
    post_save.connect(create_version_for_model, sender=model)