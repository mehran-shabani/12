import json
from django.db import transaction
from django.apps import apps
from .models import RecordVersion


class VersioningService:
    """Service for handling record versioning"""
    
    def create_version(self, resource_type, resource_id, snapshot, changed_by_id=None):
        """Create a new version for a resource"""
        # Get the latest version number
        latest = RecordVersion.objects.filter(
            resource_type=resource_type,
            resource_id=resource_id
        ).order_by('-version').first()
        
        next_version = 1 if not latest else latest.version + 1
        
        # Calculate diff if there's a previous version
        diff = None
        if latest:
            diff = self._calculate_diff(latest.snapshot, snapshot)
        
        # Create new version
        version = RecordVersion.objects.create(
            resource_type=resource_type,
            resource_id=resource_id,
            version=next_version,
            snapshot=snapshot,
            diff=diff,
            changed_by_id=changed_by_id
        )
        
        return version
    
    def _calculate_diff(self, old_snapshot, new_snapshot):
        """Calculate differences between two snapshots"""
        diff = {
            "added": {},
            "removed": {},
            "changed": {}
        }
        
        old_keys = set(old_snapshot.keys())
        new_keys = set(new_snapshot.keys())
        
        # Find added fields
        for key in new_keys - old_keys:
            diff["added"][key] = new_snapshot[key]
        
        # Find removed fields
        for key in old_keys - new_keys:
            diff["removed"][key] = old_snapshot[key]
        
        # Find changed fields
        for key in old_keys & new_keys:
            if old_snapshot[key] != new_snapshot[key]:
                diff["changed"][key] = {
                    "old": old_snapshot[key],
                    "new": new_snapshot[key]
                }
        
        return diff
    
    def get_model_snapshot(self, instance):
        """Create a snapshot of a model instance"""
        snapshot = {}
        
        # Get all fields
        for field in instance._meta.fields:
            value = getattr(instance, field.name)
            
            # Convert complex types to JSON-serializable format
            if hasattr(value, 'isoformat'):  # datetime
                value = value.isoformat()
            elif hasattr(value, '__dict__'):  # model instance
                value = str(value.pk) if hasattr(value, 'pk') else str(value)
            
            snapshot[field.name] = value
        
        return snapshot
    
    @transaction.atomic
    def revert_to_version(self, resource_type, resource_id, target_version):
        """Revert a resource to a specific version"""
        # Get the target version
        version = RecordVersion.objects.get(
            resource_type=resource_type,
            resource_id=resource_id,
            version=target_version
        )
        
        # Get the model class
        model_mapping = {
            'Patient': 'patients_core.Patient',
            'Encounter': 'diab_encounters.Encounter',
            'LabResult': 'diab_labs.LabResult',
            'MedicationOrder': 'diab_medications.MedicationOrder'
        }
        
        if resource_type not in model_mapping:
            raise ValueError(f"Unknown resource type: {resource_type}")
        
        app_label, model_name = model_mapping[resource_type].split('.')
        model_class = apps.get_model(app_label, model_name)
        
        # Get the instance
        instance = model_class.objects.get(pk=resource_id)
        
        # Apply the snapshot
        snapshot = version.snapshot
        for field_name, value in snapshot.items():
            if hasattr(instance, field_name) and field_name not in ['id', 'created_at', 'updated_at']:
                setattr(instance, field_name, value)
        
        # Save the instance
        instance.save()
        
        # Create a new version record for the revert
        self.create_version(resource_type, resource_id, snapshot)
        
        return True