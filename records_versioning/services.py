# records_versioning/services.py
from django.core import serializers
from django.forms.models import model_to_dict
from .models import RecordVersion
import json

class VersioningService:
    @staticmethod
    def create_version(instance):
        """ایجاد نسخه جدید از یک آبجکت"""
        resource_type = instance.__class__.__name__
        resource_id = instance.id
        
        # گرفتن آخرین نسخه
        last_version = RecordVersion.objects.filter(
            resource_type=resource_type,
            resource_id=resource_id
        ).first()
        
        next_version = (last_version.version + 1) if last_version else 1
        
        # تبدیل آبجکت به dictionary
        snapshot = model_to_dict(instance)
        
        # تبدیل UUID و datetime به string برای JSON serialization
        for key, value in snapshot.items():
            if hasattr(value, 'isoformat'):
                snapshot[key] = value.isoformat()
            elif hasattr(value, '__str__') and 'UUID' in str(type(value)):
                snapshot[key] = str(value)
        
        # محاسبه diff در صورت وجود نسخه قبل
        diff = None
        if last_version:
            diff = VersioningService._calculate_diff(last_version.snapshot, snapshot)
        
        # ایجاد نسخه جدید
        version = RecordVersion.objects.create(
            resource_type=resource_type,
            resource_id=resource_id,
            version=next_version,
            snapshot=snapshot,
            diff=diff
        )
        
        return version
    
    @staticmethod
    def _calculate_diff(old_data, new_data):
        """محاسبه تفاوت بین دو نسخه"""
        diff = {}
        
        # تغییرات
        for key, new_value in new_data.items():
            old_value = old_data.get(key)
            if old_value != new_value:
                diff[key] = {
                    'old': old_value,
                    'new': new_value
                }
        
        # فیلدهای حذف شده
        for key in old_data:
            if key not in new_data:
                diff[key] = {
                    'old': old_data[key],
                    'new': None
                }
        
        return diff
    
    @staticmethod
    def get_versions(resource_type, resource_id):
        """گرفتن تمام نسخه‌های یک آبجکت"""
        return RecordVersion.objects.filter(
            resource_type=resource_type,
            resource_id=resource_id
        ).order_by('-version')
    
    @staticmethod
    def revert_to_version(resource_type, resource_id, version_number):
        """بازگردانی به نسخه مشخص"""
        try:
            version = RecordVersion.objects.get(
                resource_type=resource_type,
                resource_id=resource_id,
                version=version_number
            )
            return version.snapshot
        except RecordVersion.DoesNotExist:
            return None