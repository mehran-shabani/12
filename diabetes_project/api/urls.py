from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PatientViewSet, EncounterViewSet


router = SimpleRouter()
router.register(r'patients', PatientViewSet)
router.register(r'encounters', EncounterViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]

