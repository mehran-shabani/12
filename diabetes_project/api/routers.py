from django.urls import path
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
from django.conf import settings


def health_check(request):
    """Basic health check endpoint"""
    return JsonResponse({
        "status": "healthy",
        "service": "diabetes-api"
    })


def readiness_check(request):
    """Readiness check - verifies all dependencies are ready"""
    checks = {
        "database": False,
        "redis": False,
        "overall": False
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = True
    except:
        pass
    
    # Check Redis
    try:
        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        checks["redis"] = True
    except:
        pass
    
    # Overall status
    checks["overall"] = all([checks["database"], checks["redis"]])
    
    status_code = 200 if checks["overall"] else 503
    
    return JsonResponse(checks, status=status_code)


urlpatterns = [
    path('health/', health_check),
    path('ready/', readiness_check),
]