# tests/test_export.py
import pytest
from rest_framework.test import APIClient
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary
from django.utils import timezone
import uuid

@pytest.mark.django_db
def test_export_patient_complete_data(monkeypatch):
    """تست export کامل اطلاعات بیمار"""
    # Mock کردن Celery
    def mock_delay(*args, **kwargs):
        return None
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    # ایجاد بیمار
    patient = Patient.objects.create(
        full_name="علی احمدی",
        sex="male",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    # ایجاد encounter
    encounter = Encounter.objects.create(
        patient=patient,
        occurred_at=timezone.now(),
        subjective="خستگی و تشنگی",
        objective={"bp": "140/90"},
        assessment={"dx": "diabetes"},
        plan={"med": "metformin"}
    )
    
    # ایجاد lab
    lab = LabResult.objects.create(
        patient=patient,
        test_name="HbA1c",
        value=8.5,
        unit="%",
        taken_at=timezone.now()
    )
    
    # ایجاد medication
    med = MedicationOrder.objects.create(
        patient=patient,
        drug_name="Metformin",
        dosage="500mg",
        frequency="twice daily",
        start_date="2025-01-15"
    )
    
    # ایجاد AI summary دستی (چون Celery mock شده)
    ai_summary = AISummary.objects.create(
        patient=patient,
        resource_type="Encounter",
        resource_id=encounter.id,
        summary="بیمار علائم دیابت دارد و نیاز به درمان دارویی دارد"
    )
    
    # تست export API
    response = client.get(f'/api/export/patient/{patient.id}/')
    assert response.status_code == 200
    
    data = response.json()
    
    # بررسی محتویات export
    assert data['patient']['full_name'] == "علی احمدی"
    assert len(data['encounters']) == 1
    assert len(data['lab_results']) == 1
    assert len(data['medications']) == 1
    assert len(data['ai_summaries']) == 1
    assert len(data['versions']) >= 1  # حداقل Patient version
    
    # بررسی metadata
    assert 'export_metadata' in data
    assert data['export_metadata']['total_encounters'] == 1
    assert data['export_metadata']['total_labs'] == 1
    assert data['export_metadata']['total_medications'] == 1

@pytest.mark.django_db
def test_export_patient_not_found():
    """تست export برای بیمار غیرموجود"""
    client = APIClient()
    
    fake_id = str(uuid.uuid4())
    response = client.get(f'/api/export/patient/{fake_id}/')
    assert response.status_code == 404