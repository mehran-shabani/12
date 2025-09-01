from django.contrib import admin
from .models import ClinicalReference


@admin.register(ClinicalReference)
class ClinicalReferenceAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'topic', 'created_at']
    list_filter = ['topic', 'source', 'created_at']
    search_fields = ['title', 'content', 'topic']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['topic', 'title']