# tests/test_versioning.py
import pytest
from rest_framework.test import APIClient
from patients_core.models import Patient
from diab_encounters.models import Encounter
from records_versioning.models import RecordVersion
from records_versioning.services import VersioningService
from django.utils import timezone
import uuid

@pytest.mark.django_db
def test_patient_versioning(monkeypatch):
    """تست versioning برای Patient"""
    # Mock کردن Celery
    def mock_delay(*args, **kwargs):
        return None
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    # ایجاد بیمار
    patient = Patient.objects.create(
        full_name="علی احمدی",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    # بررسی ایجاد نسخه اول
    assert RecordVersion.objects.filter(
        resource_type='Patient',
        resource_id=patient.id,
        version=1
    ).exists()
    
    # ویرایش بیمار
    patient.full_name = "علی احمدی تغییر یافته"
    patient.save()
    
    # بررسی ایجاد نسخه دوم
    assert RecordVersion.objects.filter(
        resource_type='Patient',
        resource_id=patient.id,
        version=2
    ).exists()

@pytest.mark.django_db
def test_encounter_versioning(monkeypatch):
    """تست versioning برای Encounter"""
    # Mock کردن Celery
    def mock_delay(*args, **kwargs):
        return None
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    patient = Patient.objects.create(
        full_name="علی احمدی",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    encounter = Encounter.objects.create(
        patient=patient,
        occurred_at=timezone.now(),
        subjective="خستگی اولیه"
    )
    
    # بررسی نسخه اول
    assert RecordVersion.objects.filter(
        resource_type='Encounter',
        resource_id=encounter.id,
        version=1
    ).exists()
    
    # ویرایش encounter
    encounter.subjective = "خستگی تغییر یافته"
    encounter.save()
    
    # بررسی نسخه دوم
    version_2 = RecordVersion.objects.get(
        resource_type='Encounter',
        resource_id=encounter.id,
        version=2
    )
    
    # بررسی diff
    assert 'subjective' in version_2.diff
    assert version_2.diff['subjective']['old'] == "خستگی اولیه"
    assert version_2.diff['subjective']['new'] == "خستگی تغییر یافته"

@pytest.mark.django_db
def test_version_api_endpoints(monkeypatch):
    """تست API endpoints برای versioning"""
    # Mock کردن Celery
    def mock_delay(*args, **kwargs):
        return None
    monkeypatch.setattr("ai_summarizer.tasks.summarize_record.delay", mock_delay)
    
    client = APIClient()
    
    patient = Patient.objects.create(
        full_name="علی احمدی",
        primary_doctor_id=str(uuid.uuid4())
    )
    
    # ویرایش برای ایجاد نسخه دوم
    patient.full_name = "علی احمدی جدید"
    patient.save()
    
    # تست API گرفتن نسخه‌ها
    response = client.get(f'/api/versions/Patient/{patient.id}/')
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2  # دو نسخه
    assert data[0]['version'] == 2  # آخرین نسخه اول
    assert data[1]['version'] == 1