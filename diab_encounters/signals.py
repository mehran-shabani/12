# diab_encounters/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Encounter
from ai_summarizer.tasks import summarize_record

@receiver(post_save, sender=Encounter)
def trigger_encounter_summary(sender, instance, created, **kwargs):
    if created:
        payload = {
            "subjective": instance.subjective,
            "objective": instance.objective,
            "assessment": instance.assessment,
            "plan": instance.plan,
            "occurred_at": instance.occurred_at.isoformat()
        }
        summarize_record.delay(
            str(instance.patient_id),
            "Encounter",
            str(instance.id),
            payload
        )