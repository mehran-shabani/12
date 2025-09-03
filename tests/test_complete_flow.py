# tests/test_complete_flow.py
import pytest
from rest_framework.test import APIClient
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary
from records_versioning.models import RecordVersion
from django.utils import timezone
import uuid
import json

@pytest.mark.django_db
def test_complete_diabetes_flow(monkeypatch):
    """تست کامل flow از ایجاد بیمار تا AI Summary"""
    
    # Mock کردن Celery task مستقیماً
    def mock_delay(*args, **kwargs):
        # شبیه‌سازی اجرای task
        patient_id, resource_type, resource_id, payload = args
        AISummary.objects.create(
            patient_id=patient_id,
            resource_type=resource_type,
            resource_id=resource_id,
            summary=f"خلاصه AI برای {resource_type}: {json.dumps(payload, ensure_ascii=False)[:100]}..."
        )
        return None
    
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    # 1️⃣ ایجاد بیمار
    patient_data = {
        "full_name": "علی احمدی",
        "sex": "male",
        "dob": "1980-05-15",
        "national_id": "1234567890",
        "primary_doctor_id": str(uuid.uuid4())
    }
    
    response = client.post('/api/patients/', patient_data, format='json')
    assert response.status_code == 201
    patient_id = response.data['id']
    
    # 2️⃣ ایجاد encounter
    encounter_data = {
        "patient": patient_id,
        "occurred_at": "2025-01-15T10:00:00Z",
        "subjective": "خستگی مفرط، تشنگی زیاد، کاهش وزن",
        "objective": {
            "vital_signs": {"bp": "140/90", "weight": "75kg", "height": "175cm"},
            "physical_exam": "alert, oriented"
        },
        "assessment": {
            "primary_diagnosis": "Type 2 Diabetes Mellitus",
            "icd10": ["E11.9"],
            "severity": "moderate"
        },
        "plan": {
            "medications": ["Metformin 500mg BID"],
            "lifestyle": ["diet modification", "exercise"],
            "follow_up": "2 weeks"
        }
    }
    
    response = client.post('/api/encounters/', encounter_data, format='json')
    assert response.status_code == 201
    encounter_id = response.data['id']
    
    # 3️⃣ ایجاد lab results
    lab_data = {
        "patient": patient_id,
        "test_name": "HbA1c",
        "value": 8.5,
        "unit": "%",
        "reference_range": "4.0-6.0",
        "taken_at": "2025-01-15T08:00:00Z"
    }
    
    response = client.post('/api/labs/', lab_data, format='json')
    assert response.status_code == 201
    lab_id = response.data['id']
    
    # 4️⃣ ایجاد medication order
    med_data = {
        "patient": patient_id,
        "drug_name": "Metformin",
        "dosage": "500mg",
        "frequency": "twice daily",
        "start_date": "2025-01-15",
        "notes": "با غذا مصرف شود"
    }
    
    response = client.post('/api/meds/', med_data, format='json')
    assert response.status_code == 201
    med_id = response.data['id']
    
    # 5️⃣ بررسی Timeline API
    response = client.get(f'/api/patients/{patient_id}/timeline/')
    assert response.status_code == 200
    
    timeline_data = response.json()
    assert timeline_data['patient']['full_name'] == "علی احمدی"
    assert len(timeline_data['encounters']) == 1
    assert len(timeline_data['labs']) == 1
    assert len(timeline_data['medications']) == 1
    
    # 6️⃣ بررسی Export API
    response = client.get(f'/api/export/patient/{patient_id}/')
    assert response.status_code == 200
    
    export_data = response.json()
    assert export_data['patient']['full_name'] == "علی احمدی"
    assert export_data['export_metadata']['total_encounters'] == 1
    assert export_data['export_metadata']['total_labs'] == 1
    assert export_data['export_metadata']['total_medications'] == 1
    
    # 7️⃣ بررسی Versioning API
    response = client.get(f'/api/versions/Patient/{patient_id}/')
    assert response.status_code == 200
    
    versions_data = response.json()
    assert len(versions_data) >= 1
    
    # 8️⃣ تست manual AI Summary (چون Celery mock شده)
    ai_summary = AISummary.objects.create(
        patient_id=patient_id,
        resource_type="Encounter",
        resource_id=encounter_id,
        summary="بیمار مبتلا به دیابت نوع 2 با کنترل نامناسب قند خون. نیاز به شروع متفورمین و تغییرات سبک زندگی دارد."
    )
    
    # 9️⃣ بررسی نهایی Timeline با AI Summary
    response = client.get(f'/api/patients/{patient_id}/timeline/')
    timeline_final = response.json()
    
    # باید حداقل 4 summary داشته باشیم: Encounter + Lab + Med + Manual
    assert len(timeline_final['ai_summaries']) >= 4
    
    # بررسی وجود summaryهای مختلف
    summary_types = [s['resource_type'] for s in timeline_final['ai_summaries']]
    assert 'Encounter' in summary_types
    assert 'LabResult' in summary_types
    assert 'MedicationOrder' in summary_types

@pytest.mark.django_db
def test_api_endpoints_accessibility():
    """تست دسترسی به تمام endpoint ها بدون توکن"""
    client = APIClient()
    
    # تست endpoint های اصلی
    endpoints = [
        '/api/patients/',
        '/api/encounters/',
        '/api/labs/',
        '/api/meds/',
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        # باید 200 یا 404 باشه، نه 401 (unauthorized)
        assert response.status_code in [200, 404]

@pytest.mark.django_db
def test_full_crud_operations(monkeypatch):
    """تست عملیات CRUD کامل"""
    # Mock Celery
    def mock_delay(*args, **kwargs):
        return None
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    # CREATE
    patient_data = {
        "full_name": "احمد رضایی",
        "sex": "male",
        "primary_doctor_id": str(uuid.uuid4())
    }
    response = client.post('/api/patients/', patient_data, format='json')
    assert response.status_code == 201
    patient_id = response.data['id']
    
    # READ
    response = client.get(f'/api/patients/{patient_id}/')
    assert response.status_code == 200
    assert response.data['full_name'] == "احمد رضایی"
    
    # UPDATE
    update_data = {"full_name": "احمد رضایی تغییر یافته"}
    response = client.patch(f'/api/patients/{patient_id}/', update_data, format='json')
    assert response.status_code == 200
    assert response.data['full_name'] == "احمد رضایی تغییر یافته"
    
    # بررسی versioning بعد از update
    versions = RecordVersion.objects.filter(
        resource_type='Patient',
        resource_id=patient_id
    )
    assert versions.count() == 2  # نسخه اولیه + نسخه ویرایش شده
    
    # DELETE
    response = client.delete(f'/api/patients/{patient_id}/')
    assert response.status_code == 204