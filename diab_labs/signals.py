# diab_labs/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LabResult
from ai_summarizer.tasks import summarize_record

@receiver(post_save, sender=LabResult)
def trigger_lab_summary(sender, instance, created, **kwargs):
    if created:
        payload = {
            "test_name": instance.test_name,
            "value": instance.value,
            "unit": instance.unit,
            "reference_range": instance.reference_range,
            "taken_at": instance.taken_at.isoformat()
        }
        summarize_record.delay(
            str(instance.patient_id),
            "LabResult",
            str(instance.id),
            payload
        )