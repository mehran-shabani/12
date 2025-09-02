import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestHealthEndpoints:
    def test_health_check(self):
        client = APIClient()
        response = client.get('/health/')
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'diabetes-api'
    
    def test_readiness_check_success(self, mocker):
        # Mock Redis connection where it's used
        mocker.patch('api.routers.redis.from_url').return_value.ping.return_value = True
        
        client = APIClient()
        response = client.get('/ready/')
        
        assert response.status_code == 200
        data = response.json()
        assert data['database'] is True
        assert data['redis'] is True
        assert data['overall'] is True