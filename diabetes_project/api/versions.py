from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from records_versioning.models import RecordVersion
from records_versioning.services import VersioningService


class VersionViewSet(viewsets.ViewSet):
    """ViewSet for handling version history"""
    
    def list(self, request, resource_type=None, resource_id=None):
        """Get version history for a specific resource"""
        versions = RecordVersion.objects.filter(
            resource_type=resource_type,
            resource_id=resource_id
        ).order_by('-version')
        
        data = []
        for version in versions:
            data.append({
                "id": str(version.id),
                "version": version.version,
                "snapshot": version.snapshot,
                "diff": version.diff,
                "changed_by_id": str(version.changed_by_id) if version.changed_by_id else None,
                "created_at": version.created_at
            })
        
        return Response({
            "resource_type": resource_type,
            "resource_id": resource_id,
            "versions": data,
            "total_versions": len(data)
        })
    
    @action(detail=False, methods=['post'])
    def revert(self, request):
        """Revert a resource to a specific version"""
        resource_type = request.data.get('resource_type')
        resource_id = request.data.get('resource_id')
        target_version = request.data.get('target_version')
        
        if not all([resource_type, resource_id, target_version]):
            return Response({
                "error": "Missing required fields: resource_type, resource_id, target_version"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = VersioningService()
            success = service.revert_to_version(resource_type, resource_id, target_version)
            
            if success:
                return Response({
                    "message": f"Successfully reverted {resource_type} {resource_id} to version {target_version}"
                })
            else:
                return Response({
                    "error": "Failed to revert to specified version"
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)