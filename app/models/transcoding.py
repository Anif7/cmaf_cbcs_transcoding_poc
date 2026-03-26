from django.db import models
from model_utils.models import TimeStampedModel

class TranscodingJob(TimeStampedModel):
    class Status(models.IntegerChoices):
        QUEUED = 1, 'Queued'
        DOWNLOADING = 2, 'Downloading'
        TRANSCODING = 3, 'Transcoding'
        PACKAGING = 4, 'Packaging'
        UPLOADING = 5, 'Uploading'
        COMPLETED = 6, 'Completed'
        FAILED = 7, 'Failed'

    input_url = models.URLField(max_length=512)
    output_path = models.CharField(max_length=512)
    webhook_url = models.URLField(max_length=512, blank=True, null=True)
    storage_config = models.JSONField(default=dict)
    drm_config = models.JSONField(default=dict)
    meta_data = models.JSONField(default=dict)
    status = models.PositiveIntegerField(choices=Status.choices, default=Status.QUEUED)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Job {self.id} - {self.get_status_display()}"
