# diab_medications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MedicationOrder
from ai_summarizer.tasks import summarize_record

@receiver(post_save, sender=MedicationOrder)
def trigger_med_summary(sender, instance, created, **kwargs):
    if created:
        payload = {
            "drug_name": instance.drug_name,
            "dosage": instance.dosage,
            "frequency": instance.frequency,
            "start_date": instance.start_date.isoformat() if hasattr(instance.start_date, 'isoformat') else str(instance.start_date),
            "end_date": instance.end_date.isoformat() if instance.end_date and hasattr(instance.end_date, 'isoformat') else str(instance.end_date) if instance.end_date else None,
            "notes": instance.notes
        }
        summarize_record.delay(
            str(instance.patient_id),
            "MedicationOrder",
            str(instance.id),
            payload
        )