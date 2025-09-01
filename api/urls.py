# api/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PatientViewSet, EncounterViewSet, LabResultViewSet, MedicationOrderViewSet
from .versions import VersionViewSet
from .views_export import export_patient

router = SimpleRouter()
router.register(r'patients', PatientViewSet)
router.register(r'encounters', EncounterViewSet)
router.register(r'labs', LabResultViewSet)
router.register(r'meds', MedicationOrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/versions/<str:resource_type>/<uuid:resource_id>/', VersionViewSet.as_view({'get': 'list'})),
    path('api/versions/revert/', VersionViewSet.as_view({'post': 'revert'})),
    path('api/export/patient/<uuid:pk>/', export_patient, name='export_patient'),
]