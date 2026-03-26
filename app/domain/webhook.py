import logging
import requests
from app.models.transcoding import TranscodingJob

logger = logging.getLogger(__name__)

def send_job_webhook(job: TranscodingJob):
    if not job.webhook_url:
        return
    
    try:
        payload = {
            'id': job.id,
            'status': job.get_status_display().lower(),
            'meta_data': job.meta_data,
            'error_message': job.error_message if job.status == TranscodingJob.Status.FAILED else None
        }
        requests.post(job.webhook_url, json=payload, timeout=5)
    except Exception as e:
        logger.warning(f"Failed to send webhook for Job {job.id}: {str(e)}")
