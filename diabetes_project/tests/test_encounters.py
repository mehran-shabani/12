import pytest
from patients_core.models import Patient
from diab_encounters.models import Encounter
from django.utils import timezone


@pytest.mark.django_db
def test_create_encounter():
    patient = Patient.objects.create(
        full_name="Test Patient",
        primary_doctor_id="00000000-0000-0000-0000-000000000111"
    )

    encounter = Encounter.objects.create(
        patient=patient,
        occurred_at=timezone.now(),
        subjective="خستگی",
        objective={"bp": "130/80"},
        assessment={"dx": "diabetes"},
        plan={"drug": "metformin"}
    )

    assert encounter.id is not None
    assert encounter.patient == patient

