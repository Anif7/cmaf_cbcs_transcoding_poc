import logging
from celery import shared_task
from app.models import TranscodingJob
from app.domain.orchestrator import TranscodingOrchestrator

logger = logging.getLogger(__name__)

@shared_task
def run_transcoding_pipeline(job_id):
    logger.info(f"Task received for Job {job_id}")
    try:
        transcoding_job = TranscodingJob.objects.get(id=job_id)
        orchestrator = TranscodingOrchestrator(transcoding_job)
        orchestrator.run_pipeline()
    except Exception as e:
        logger.error(f"Task failed for Job {job_id}: {str(e)}")
        pass
