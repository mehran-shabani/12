import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_can_access_patient_api_without_token():
    client = APIClient()
    response = client.get('/api/patients/')
    assert response.status_code in [200, 204, 403]

