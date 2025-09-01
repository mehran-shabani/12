from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LabResult
from ai_summarizer.tasks import summarize_record


@receiver(post_save, sender=LabResult)
def trigger_lab_summary(sender, instance, created, **kwargs):
    """
    Trigger AI summary generation when a new lab result is created
    """
    if created:
        payload = {
            "test_name": instance.test_name,
            "test_code": instance.test_code,
            "value": instance.value,
            "unit": instance.unit,
            "reference_range": instance.reference_range,
            "is_abnormal": instance.is_abnormal,
            "taken_at": str(instance.taken_at)
        }
        
        # Queue the task
        summarize_record.delay(
            str(instance.patient_id),
            "LabResult",
            str(instance.id),
            payload
        )