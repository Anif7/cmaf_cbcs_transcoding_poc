import os
import shutil
import logging
from celery import shared_task, Task
from app.models.transcoding import TranscodingJob
from app.domain.downloader import MediaDownloader
from app.domain.transcoder import FFmpegTranscoder
from app.domain.webhook import send_job_webhook
from app.domain.uploader import CloudUploader
from app.domain.packager import ShakaPackager

logger = logging.getLogger(__name__)

class VideoTranscodingTask(Task):
    name = 'app.tasks.transcoding.video_transcoding_task'

    def run(self, job_id, *args, **kwargs):
        logger.info(f"Starting VideoTranscodingTask for Job {job_id}")
        try:
            job = TranscodingJob.objects.get(id=job_id)
        except TranscodingJob.DoesNotExist:
            logger.error(f"Job {job_id} not found.")
            return

        work_dir = f"/tmp/transcoding_{job.id}"
        os.makedirs(work_dir, exist_ok=True)
        
        try:
            self.execute_pipeline(job, work_dir)
        except Exception as e:
            logger.error(f"Task failed for Job {job.id}: {str(e)}")
            job.mark_as_failed(str(e))
            send_job_webhook(job)
        finally:
            self.cleanup_workspace(work_dir)

    def execute_pipeline(self, job, work_dir):
        logger.info(f"Step 1/4: Downloading source media for Job {job.id}")
        source_file = self.download_source_media(job, work_dir)
        
        logger.info(f"Step 1.5: Extracting shared audio track")
        audio_path = os.path.join(work_dir, "audio_track.mp4")
        FFmpegTranscoder().extract_audio(source_file, audio_path)
        
        logger.info(f"Step 2/4: Transcoding video variants")
        video_variants = self.transcode_video_variants(job, work_dir, source_file)
        
        logger.info(f"Step 3/4: Packaging Job {job.id}")
        self.package_content(job, work_dir, video_variants, audio_path)
        
        logger.info(f"Step 4/4: Uploading Job {job.id} to cloud storage")
        self.upload_final_artifacts(job, work_dir)
        
        job.mark_as_completed()
        logger.info(f"Successfully completed Job {job.id}")
        send_job_webhook(job)

    def download_source_media(self, job, work_dir):
        job.update_status(TranscodingJob.Status.DOWNLOADING)
        source_file = os.path.join(work_dir, 'source_media')
        MediaDownloader().download(job.input_url, source_file)
        return source_file

    def transcode_video_variants(self, job, work_dir, source_file):
        job.update_status(TranscodingJob.Status.TRANSCODING)
        video_variants = self._extract_video_parameters(job, work_dir)
        
        logger.info(f"Triggering single-pass transcoding for {len(video_variants)} variants")
        FFmpegTranscoder().transcode_video_variants(source_file, video_variants)
        return video_variants

    def _extract_video_parameters(self, job: TranscodingJob, work_dir: str) -> list:
        outputs = job.meta_data.get('settings', {}).get('outputs')
        if not outputs:
            logger.warning("No outputs found in metadata. Using fallback 360p.")
            outputs = [{'video': {'width': 640, 'height': 360}, 'name': '360p'}]
            
        return [self._format_variant_config(output, work_dir) for output in outputs]

    def _format_variant_config(self, output: dict, work_dir: str) -> dict:
        video_config = output.get('video', {})
        name = output['name']
        return {
            'path': os.path.join(work_dir, f"{name}.mp4"),
            'name': name,
            'width': video_config.get('width'),
            'height': video_config.get('height'),
            'video': video_config
        }

    def package_content(self, job, work_dir, video_variants, audio_path):
        job.update_status(TranscodingJob.Status.PACKAGING)
        output_dir = os.path.join(work_dir, 'packaged')
        ShakaPackager().package(video_variants, audio_path, output_dir, job.drm_config)

    def upload_final_artifacts(self, job, work_dir):
        job.update_status(TranscodingJob.Status.UPLOADING)
        destination = job.output_path
        storage_config = job.storage_config.get('output', {})
        logger.info(f"Uploading artifacts to: {destination}")
        CloudUploader().upload_directory(
            source_dir=os.path.join(work_dir, 'packaged'),
            destination_path=destination,
            credentials=storage_config
        )

    def cleanup_workspace(self, work_dir):
        logger.info(f"Cleaning up workspace: {work_dir}")
        shutil.rmtree(work_dir, ignore_errors=True)

@shared_task(bind=True, base=VideoTranscodingTask)
def video_transcoding_task(self, *args, **kwargs):
    return VideoTranscodingTask.run(self, *args, **kwargs)
