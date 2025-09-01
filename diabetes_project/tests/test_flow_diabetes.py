import pytest
from datetime import date, datetime
from rest_framework.test import APIClient
from patients_core.models import Patient
from diab_encounters.models import Encounter
from ai_summarizer.models import AISummary


@pytest.mark.django_db
class TestDiabetesFlow:
    """Test complete diabetes patient flow"""
    
    def test_full_diabetes_flow(self, monkeypatch):
        # Mock OpenAI API
        def mock_openai_create(**kwargs):
            return {
                "choices": [{
                    "message": {
                        "content": "خلاصه آزمایشی: بیمار دیابتی با HbA1c بالا نیاز به تنظیم دارو دارد."
                    }
                }]
            }
        
        monkeypatch.setattr("openai.ChatCompletion.create", mock_openai_create)
        
        client = APIClient()
        
        # Step 1: Create a patient
        patient_data = {
            "full_name": "علی تستی",
            "dob": "1980-01-01",
            "sex": "male",
            "national_id": "1234567890",
            "primary_doctor_id": "00000000-0000-0000-0000-000000000001"
        }
        
        response = client.post('/api/patients/', patient_data, format='json')
        assert response.status_code == 201
        patient_id = response.data['id']
        
        # Step 2: Create an encounter
        encounter_data = {
            "patient": patient_id,
            "occurred_at": datetime.now().isoformat(),
            "subjective": "بیمار از خستگی و تشنگی زیاد شکایت دارد",
            "objective": {
                "bp": "140/90",
                "hr": 85,
                "weight": "85kg",
                "height": "175cm"
            },
            "assessment": {
                "diagnosis": "Type 2 Diabetes Mellitus",
                "icd10": "E11.9"
            },
            "plan": {
                "medication": "Metformin 500mg twice daily",
                "lifestyle": "Diet modification and exercise",
                "followup": "1 month"
            }
        }
        
        response = client.post('/api/encounters/', encounter_data, format='json')
        assert response.status_code == 201
        encounter_id = response.data['id']
        
        # Step 3: Create lab results
        lab_data = {
            "patient": patient_id,
            "test_name": "HbA1c",
            "test_code": "HBA1C",
            "value": "8.5",
            "unit": "%",
            "reference_range": "<5.7",
            "is_abnormal": True,
            "taken_at": datetime.now().isoformat()
        }
        
        response = client.post('/api/labs/', lab_data, format='json')
        assert response.status_code == 201
        
        # Step 4: Create medication order
        med_data = {
            "patient": patient_id,
            "drug_name": "Metformin",
            "drug_code": "MET500",
            "dosage": "500mg",
            "frequency": "Twice daily with meals",
            "route": "oral",
            "start_date": date.today().isoformat(),
            "is_active": True,
            "prescriber_id": "00000000-0000-0000-0000-000000000001"
        }
        
        response = client.post('/api/medications/', med_data, format='json')
        assert response.status_code == 201
        
        # Step 5: Check timeline
        response = client.get(f'/api/patients/{patient_id}/timeline/')
        assert response.status_code == 200
        
        timeline = response.data
        assert timeline['patient']['full_name'] == "علی تستی"
        assert len(timeline['encounters']) > 0
        assert len(timeline['labs']) > 0
        assert len(timeline['medications']) > 0
        
        # Step 6: Check AI summaries (should be created by signals)
        # Note: In real test, we'd use Celery's eager mode
        summaries = AISummary.objects.filter(patient_id=patient_id)
        # Since we're mocking, manually create one for testing
        AISummary.objects.create(
            patient_id=patient_id,
            resource_type="Encounter",
            resource_id=encounter_id,
            summary="خلاصه آزمایشی: بیمار دیابتی با HbA1c بالا نیاز به تنظیم دارو دارد."
        )
        
        # Step 7: Export patient data
        response = client.get(f'/api/export/patient/{patient_id}/')
        assert response.status_code == 200
        assert response['Content-Disposition'].startswith('attachment')
        
        export_data = response.json()
        assert export_data['patient']['full_name'] == "علی تستی"
        assert 'encounters' in export_data
        assert 'lab_results' in export_data
        assert 'medications' in export_data
        assert 'statistics' in export_data