from django.db import models
import uuid


class ClinicalReference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=120)
    topic = models.CharField(max_length=80)
    tags = models.JSONField(default=list, blank=True)
    content = models.TextField()
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clinical_references'
        ordering = ['topic', 'title']

    def __str__(self):
        return f"{self.title} - {self.source}"