import os
import shutil
import requests
import logging
from app.models import TranscodingJob
from .downloader import MediaDownloader
from .transcoder import FfmpegTranscoder
from .packager import ShakaPackager
from .uploader import CloudUploader

logger = logging.getLogger(__name__)

class TranscodingOrchestrator:
    def __init__(self, job: TranscodingJob):
        self.job = job
        self.downloader = MediaDownloader()
        self.transcoder = FfmpegTranscoder()
        self.packager = ShakaPackager()
        self.uploader = CloudUploader()

    def run_pipeline(self) -> None:
        logger.info(f"Starting pipeline for Job {self.job.id}")
        work_dir = f"/tmp/transcoding_{self.job.id}"
        os.makedirs(work_dir, exist_ok=True)
        
        try:
            source_file = self._download_step(work_dir)
            transcoded_streams = self._transcode_step(work_dir)
            self._package_step(work_dir, transcoded_streams)
            self._upload_step(work_dir)
            
            self._finalize_job(TranscodingJob.Status.COMPLETED)
            logger.info(f"Job {self.job.id} completed successfully.")
            self._send_webhook('completed')
            
        except Exception as pipeline_error:
            logger.error(f"Job {self.job.id} failed: {str(pipeline_error)}")
            self._handle_failure(pipeline_error)
            self._send_webhook('error')
            raise pipeline_error
        finally:
            self._cleanup_workspace(work_dir)

    def _download_step(self, work_dir: str) -> str:
        logger.info(f"[{self.job.id}] Downloading: {self.job.input_url}")
        self._update_status(TranscodingJob.Status.DOWNLOADING)
        source_file = os.path.join(work_dir, 'source_media')
        self.downloader.download(self.job.input_url, source_file)
        return source_file

    def _transcode_step(self, work_dir: str) -> list:
        self._update_status(TranscodingJob.Status.TRANSCODING)
        source_file = os.path.join(work_dir, 'source_media')
        
        outputs = self.job.meta_data.get('settings', {}).get('outputs', [])
        if not outputs:
            outputs = [{'height': 360, 'width': 640, 'name': '360p'}]
            
        transcoded_streams = []
        for out in outputs:
            name = out.get('name') or f"{out['height']}p"
            width = out.get('width', 640)
            height = out.get('height', 360)
            
            logger.info(f"[{self.job.id}] Transcoding to {name} ({width}x{height})...")
            out_file = os.path.join(work_dir, f"{name}.mp4")
            self.transcoder.transcode(source_file, out_file, width, height)
            transcoded_streams.append({'path': out_file, 'name': name})
            
        return transcoded_streams

    def _package_step(self, work_dir: str, transcoded_streams: list) -> None:
        logger.info(f"[{self.job.id}] Packaging unified ABR CMAF/CBCS...")
        self._update_status(TranscodingJob.Status.PACKAGING)
        packaged_dir = os.path.join(work_dir, 'packaged_output')
        self.packager.package(
            transcoded_streams, 
            packaged_dir, 
            self.job.drm_config
        )

    def _upload_step(self, work_dir: str) -> None:
        logger.info(f"[{self.job.id}] Uploading artifacts to: {self.job.output_path}")
        self._update_status(TranscodingJob.Status.UPLOADING)
        packaged_dir = os.path.join(work_dir, 'packaged_output')
        
        storage = self.job.storage_config.get('output', {})
        self.uploader.upload(
            packaged_dir, 
            self.job.output_path,
            access_key_id=storage.get('ACCESS_KEY_ID'),
            secret_key=storage.get('SECRET_KEY'),
            endpoint=storage.get('ENDPOINT')
        )

    def _update_status(self, current_status: int) -> None:
        self.job.status = current_status
        self.job.save()

    def _finalize_job(self, final_status: int) -> None:
        self.job.status = final_status
        self.job.save()

    def _send_webhook(self, event: str) -> None:
        if not self.job.webhook_url:
            return
        
        try:
            payload = {
                'id': self.job.id,
                'status': event,
                'meta_data': self.job.meta_data,
                'error_message': self.job.error_message if event == 'error' else None
            }
            requests.post(self.job.webhook_url, json=payload, timeout=5)
        except Exception:
            pass

    def _handle_failure(self, error: Exception) -> None:
        self.job.status = TranscodingJob.Status.FAILED
        self.job.error_message = str(error)
        self.job.save()

    def _cleanup_workspace(self, work_dir: str) -> None:
        shutil.rmtree(work_dir, ignore_errors=True)
