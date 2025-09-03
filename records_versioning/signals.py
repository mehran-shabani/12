# records_versioning/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from .services import VersioningService

@receiver(post_save, sender=Patient)
def version_patient(sender, instance, **kwargs):
    VersioningService.create_version(instance)

@receiver(post_save, sender=Encounter)
def version_encounter(sender, instance, **kwargs):
    VersioningService.create_version(instance)

@receiver(post_save, sender=LabResult)
def version_lab_result(sender, instance, **kwargs):
    VersioningService.create_version(instance)

@receiver(post_save, sender=MedicationOrder)
def version_medication_order(sender, instance, **kwargs):
    VersioningService.create_version(instance)