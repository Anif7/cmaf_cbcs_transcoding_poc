import os
import shutil
import logging
from celery import shared_task, Task
from app.models.transcoding import TranscodingJob
from app.domain.downloader import MediaDownloader
from app.domain.transcoder import FfmpegTranscoder
from app.domain.webhook import send_job_webhook

logger = logging.getLogger(__name__)

class VideoTranscodingTask(Task):
    name = 'app.tasks.transcoding.video_transcoding_task'

    def run(self, job_id, *args, **kwargs):
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
        source_file = self.download_source_media(job, work_dir)
        transcoded_streams = self.transcode_to_specified_formats(job, work_dir, source_file)
        self.package_transcoded_streams(job, work_dir, transcoded_streams)
        self.upload_final_artifacts(job, work_dir)
        
        job.mark_as_completed()
        send_job_webhook(job)

    def download_source_media(self, job, work_dir):
        job.update_status(TranscodingJob.Status.DOWNLOADING)
        source_file = os.path.join(work_dir, 'source_media')
        MediaDownloader().download(job.input_url, source_file)
        return source_file

    def transcode_to_specified_formats(self, job, work_dir, source_file):
        job.update_status(TranscodingJob.Status.TRANSCODING)
        
        outputs = job.meta_data.get('settings', {}).get('outputs', [])
        if not outputs:
            outputs = [{'height': 360, 'width': 640, 'name': '360p'}]
            
        transcoded_streams = []
        transcoder = FfmpegTranscoder()
        for out in outputs:
            name = out.get('name') or f"{out['height']}p"
            width = out.get('width', 640)
            height = out.get('height', 360)
            
            out_file = os.path.join(work_dir, f"{name}.mp4")
            transcoder.transcode(source_file, out_file, width, height)
            transcoded_streams.append({'path': out_file, 'name': name})
            
        return transcoded_streams

    def package_transcoded_streams(self, job, work_dir, transcoded_streams):
        # TODO: Implement packaging unified ABR CMAF/CBCS
        job.update_status(TranscodingJob.Status.PACKAGING)

    def upload_final_artifacts(self, job, work_dir):
        # TODO: Implement uploading artifacts to cloud storage
        job.update_status(TranscodingJob.Status.UPLOADING)

    def cleanup_workspace(self, work_dir):
        shutil.rmtree(work_dir, ignore_errors=True)

video_transcoding_task = shared_task(bind=True, base=VideoTranscodingTask)(lambda self, *args, **kwargs: self.run(*args, **kwargs))
