from django.contrib import admin
from app.models import TranscodingJob
from app.tasks.transcoding import run_transcoding_pipeline

@admin.register(TranscodingJob)
class TranscodingJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'input_url', 'output_path')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['retry_jobs']

    @admin.action(description='Retry selected jobs')
    def retry_jobs(self, request, queryset):
        for job in queryset:
            job.status = TranscodingJob.Status.QUEUED
            job.save()
            run_transcoding_pipeline.delay(job.id)
        self.message_user(request, f"Successfully triggered retry for {queryset.count()} jobs.")
