from django.contrib import admin, messages
from ..models import TranscodingJob
from ..tasks import video_transcoding_task

@admin.register(TranscodingJob)
class TranscodingJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created', 'modified')
    list_filter = ('status', 'created')
    search_fields = ('id',)
    readonly_fields = ('created', 'modified')
    actions = ['retry_jobs']

    @admin.action(description="Retry selected transcoding jobs")
    def retry_jobs(self, request, queryset):
        for job in queryset:
            video_transcoding_task.delay(job.id)
        self.message_user(request, f"Retried {queryset.count()} jobs.", messages.SUCCESS)
