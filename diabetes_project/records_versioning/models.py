from django.db import models
import uuid


class RecordVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource_type = models.CharField(max_length=48)
    resource_id = models.UUIDField()
    version = models.PositiveIntegerField()
    snapshot = models.JSONField()
    diff = models.JSONField(null=True, blank=True)
    changed_by_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'record_versions'
        ordering = ['-version']
        unique_together = ['resource_type', 'resource_id', 'version']

    def __str__(self):
        return f"{self.resource_type} {self.resource_id} v{self.version}"