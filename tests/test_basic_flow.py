# tests/test_basic_flow.py
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
def test_patient_creation():
    """تست ساخت بیمار"""
    client = APIClient()
    
    patient_data = {
        "full_name": "علی احمدی",
        "sex": "male",
        "primary_doctor_id": str(uuid.uuid4())
    }
    
    response = client.post('/api/patients/', patient_data, format='json')
    assert response.status_code == 201
    assert response.data['full_name'] == "علی احمدی"

@pytest.mark.django_db
def test_encounter_creation_with_mock_celery(monkeypatch):
    """تست ساخت ویزیت با mock کردن Celery"""
    # Mock کردن Celery task
    def mock_delay(*args, **kwargs):
        return None
    
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    # ایجاد بیمار
    patient = Patient.objects.create(
        full_name="علی احمدی",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    encounter_data = {
        "patient": str(patient.id),
        "occurred_at": "2025-01-15T10:00:00Z",
        "subjective": "خستگی و تشنگی مفرط",
        "objective": {"bp": "140/90", "weight": "80kg"},
        "assessment": {"icd10": ["E11"]},
        "plan": {"medication": "Metformin"}
    }
    
    response = client.post('/api/encounters/', encounter_data, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_lab_creation_with_mock_celery(monkeypatch):
    """تست ساخت آزمایش"""
    # Mock کردن Celery task
    def mock_delay(*args, **kwargs):
        return None
    
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    patient = Patient.objects.create(
        full_name="علی احمدی",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    lab_data = {
        "patient": str(patient.id),
        "test_name": "HbA1c",
        "value": 8.5,
        "unit": "%",
        "reference_range": "4.0-6.0",
        "taken_at": "2025-01-15T09:00:00Z"
    }
    
    response = client.post('/api/labs/', lab_data, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_medication_creation_with_mock_celery(monkeypatch):
    """تست ساخت دارو"""
    # Mock کردن Celery task
    def mock_delay(*args, **kwargs):
        return None
    
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    patient = Patient.objects.create(
        full_name="علی احمدی",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    med_data = {
        "patient": str(patient.id),
        "drug_name": "Metformin",
        "dosage": "500mg",
        "frequency": "twice daily",
        "start_date": "2025-01-15"
    }
    
    response = client.post('/api/meds/', med_data, format='json')
    assert response.status_code == 201

@pytest.mark.django_db 
def test_patient_timeline(monkeypatch):
    """تست Timeline API"""
    # Mock کردن Celery task
    def mock_delay(*args, **kwargs):
        return None
    
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    patient = Patient.objects.create(
        full_name="علی احمدی",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    # ایجاد encounter
    Encounter.objects.create(
        patient=patient,
        occurred_at=timezone.now(),
        subjective="خستگی"
    )
    
    # ایجاد lab
    LabResult.objects.create(
        patient=patient,
        test_name="HbA1c",
        value=8.5,
        unit="%",
        taken_at=timezone.now()
    )
    
    # ایجاد medication
    MedicationOrder.objects.create(
        patient=patient,
        drug_name="Metformin",
        dosage="500mg",
        frequency="twice daily",
        start_date="2025-01-15"
    )
    
    response = client.get(f'/api/patients/{patient.id}/timeline/')
    assert response.status_code == 200
    
    data = response.json()
    assert data['patient']['full_name'] == "علی احمدی"
    assert len(data['encounters']) == 1
    assert len(data['labs']) == 1
    assert len(data['medications']) == 1