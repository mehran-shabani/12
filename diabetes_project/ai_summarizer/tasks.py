import os
import json
from celery import shared_task
import openai
from django.utils import timezone
from ai_summarizer.models import AISummary
from patients_core.models import Patient

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


@shared_task(bind=True, max_retries=3)
def summarize_record(self, patient_id, resource_type, resource_id, payload):
    """
    Generate AI summary for a medical record
    """
    try:
        # Build prompt based on resource type
        if resource_type == "Encounter":
            prompt = f"""لطفا این ویزیت پزشکی را خلاصه کن:
            
            Subjective: {payload.get('subjective', '')}
            Objective: {json.dumps(payload.get('objective', {}), ensure_ascii=False)}
            Assessment: {json.dumps(payload.get('assessment', {}), ensure_ascii=False)}
            Plan: {json.dumps(payload.get('plan', {}), ensure_ascii=False)}
            
            خلاصه را به صورت کوتاه و مفید برای پزشک بنویس."""
            
        elif resource_type == "LabResult":
            prompt = f"""لطفا این نتیجه آزمایش را تحلیل کن:
            
            Test: {payload.get('test_name', '')}
            Value: {payload.get('value', '')} {payload.get('unit', '')}
            Reference Range: {payload.get('reference_range', '')}
            Abnormal: {'Yes' if payload.get('is_abnormal') else 'No'}
            
            تحلیل مختصر و نکات مهم را بنویس."""
            
        elif resource_type == "MedicationOrder":
            prompt = f"""لطفا این دستور دارویی را خلاصه کن:
            
            Drug: {payload.get('drug_name', '')}
            Dosage: {payload.get('dosage', '')}
            Frequency: {payload.get('frequency', '')}
            Route: {payload.get('route', '')}
            Duration: {payload.get('start_date', '')} to {payload.get('end_date', 'ongoing')}
            
            نکات مهم و تداخلات احتمالی را ذکر کن."""
        else:
            prompt = f"خلاصه این {resource_type}: {json.dumps(payload, ensure_ascii=False)}"
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "تو یک دستیار پزشکی هستی که در خلاصه‌سازی اطلاعات پزشکی تخصص داری."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        
        summary_text = response['choices'][0]['message']['content'].strip()
        
        # Save summary to database
        AISummary.objects.create(
            patient_id=patient_id,
            resource_type=resource_type,
            resource_id=resource_id,
            summary=summary_text
        )
        
        return f"Summary created for {resource_type} {resource_id}"
        
    except Exception as e:
        # Retry the task with exponential backoff
        print(f"Error in summarize_record: {str(e)}")
        raise self.retry(exc=e, countdown=10 * (self.request.retries + 1))


@shared_task
def cleanup_old_summaries():
    """
    Cleanup summaries older than 6 months
    """
    from datetime import timedelta
    cutoff_date = timezone.now() - timedelta(days=180)
    
    deleted_count = AISummary.objects.filter(created_at__lt=cutoff_date).delete()[0]
    
    return f"Deleted {deleted_count} old summaries"