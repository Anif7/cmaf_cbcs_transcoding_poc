from django.contrib import admin
from ..models import TranscodingJob

@admin.register(TranscodingJob)
class TranscodingJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'input_url', 'status', 'created', 'modified')
    list_filter = ('status', 'created')
    search_fields = ('input_url', 'id')
    readonly_fields = ('created', 'modified')
