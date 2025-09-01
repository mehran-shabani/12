import pytest
from datetime import date, datetime
from patients_core.models import Patient
from diab_encounters.models import Encounter
from diab_labs.models import LabResult
from diab_medications.models import MedicationOrder
from ai_summarizer.models import AISummary


@pytest.mark.django_db
class TestPatientModel:
    def test_create_patient(self):
        patient = Patient.objects.create(
            full_name="Test Patient",
            dob=date(1980, 1, 1),
            sex="male",
            national_id="1234567890",
            primary_doctor_id="00000000-0000-0000-0000-000000000001"
        )
        
        assert patient.id is not None
        assert patient.full_name == "Test Patient"
        assert str(patient) == "Test Patient"


@pytest.mark.django_db
class TestEncounterModel:
    def test_create_encounter(self):
        patient = Patient.objects.create(
            full_name="Test Patient",
            primary_doctor_id="00000000-0000-0000-0000-000000000001"
        )
        
        encounter = Encounter.objects.create(
            patient=patient,
            occurred_at=datetime.now(),
            subjective="Patient reports fatigue",
            objective={"bp": "120/80", "hr": 72},
            assessment={"diagnosis": "Type 2 Diabetes"},
            plan={"medication": "Metformin 500mg"}
        )
        
        assert encounter.id is not None
        assert encounter.patient == patient
        assert "fatigue" in encounter.subjective


@pytest.mark.django_db
class TestLabResultModel:
    def test_create_lab_result(self):
        patient = Patient.objects.create(
            full_name="Test Patient",
            primary_doctor_id="00000000-0000-0000-0000-000000000001"
        )
        
        lab = LabResult.objects.create(
            patient=patient,
            test_name="HbA1c",
            test_code="HBA1C",
            value="7.5",
            unit="%",
            reference_range="<5.7",
            is_abnormal=True,
            taken_at=datetime.now()
        )
        
        assert lab.id is not None
        assert lab.is_abnormal is True
        assert lab.test_name == "HbA1c"


@pytest.mark.django_db
class TestMedicationOrderModel:
    def test_create_medication_order(self):
        patient = Patient.objects.create(
            full_name="Test Patient",
            primary_doctor_id="00000000-0000-0000-0000-000000000001"
        )
        
        med = MedicationOrder.objects.create(
            patient=patient,
            drug_name="Metformin",
            drug_code="MET500",
            dosage="500mg",
            frequency="Twice daily",
            route="oral",
            start_date=date.today(),
            is_active=True,
            prescriber_id="00000000-0000-0000-0000-000000000001"
        )
        
        assert med.id is not None
        assert med.is_active is True
        assert med.drug_name == "Metformin"