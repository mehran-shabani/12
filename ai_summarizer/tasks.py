# ai_summarizer/tasks.py
import os
import json
from celery import shared_task
import openai
from django.utils import timezone
from ai_summarizer.models import AISummary

@shared_task(bind=True, max_retries=3)
def summarize_record(self, patient_id, resource_type, resource_id, payload):
    try:
        # تنظیم OpenAI client
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"لطفا این {resource_type} را خلاصه کن:\n{json.dumps(payload, ensure_ascii=False)}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "تو یک پزشک متخصص هستی که باید اطلاعات بالینی را خلاصه کنی."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )
        
        summary_text = response.choices[0].message.content

        AISummary.objects.create(
            patient_id=patient_id,
            resource_type=resource_type,
            resource_id=resource_id,
            summary=summary_text,
            created_at=timezone.now()
        )
        
        return f"Summary created for {resource_type} {resource_id}"
        
    except Exception as e:
        print(f"Error in summarize_record: {e}")
        raise self.retry(exc=e, countdown=10)