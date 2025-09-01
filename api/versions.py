# api/versions.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from records_versioning.models import RecordVersion
from records_versioning.services import VersioningService

class VersionViewSet(viewsets.ViewSet):
    """API برای مدیریت نسخه‌گذاری"""
    
    def list(self, request, resource_type=None, resource_id=None):
        """لیست تمام نسخه‌های یک آبجکت"""
        versions = VersioningService.get_versions(resource_type, resource_id)
        
        data = []
        for v in versions:
            data.append({
                'version': v.version,
                'snapshot': v.snapshot,
                'diff': v.diff,
                'created_at': v.created_at
            })
        
        return Response(data)
    
    @action(detail=False, methods=['post'])
    def revert(self, request):
        """بازگردانی به نسخه مشخص"""
        resource_type = request.data.get('resource_type')
        resource_id = request.data.get('resource_id')
        version_number = request.data.get('version')
        
        snapshot = VersioningService.revert_to_version(
            resource_type, resource_id, version_number
        )
        
        if snapshot:
            return Response({
                'message': f'Successfully reverted to version {version_number}',
                'snapshot': snapshot
            })
        else:
            return Response({
                'error': 'Version not found'
            }, status=status.HTTP_404_NOT_FOUND)