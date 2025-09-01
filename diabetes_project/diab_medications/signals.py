from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MedicationOrder
from ai_summarizer.tasks import summarize_record


@receiver(post_save, sender=MedicationOrder)
def trigger_medication_summary(sender, instance, created, **kwargs):
    """
    Trigger AI summary generation when a new medication order is created
    """
    if created:
        payload = {
            "drug_name": instance.drug_name,
            "drug_code": instance.drug_code,
            "dosage": instance.dosage,
            "frequency": instance.frequency,
            "route": instance.route,
            "start_date": str(instance.start_date),
            "end_date": str(instance.end_date) if instance.end_date else None,
            "is_active": instance.is_active,
            "prescriber_id": str(instance.prescriber_id)
        }
        
        # Queue the task
        summarize_record.delay(
            str(instance.patient_id),
            "MedicationOrder",
            str(instance.id),
            payload
        )