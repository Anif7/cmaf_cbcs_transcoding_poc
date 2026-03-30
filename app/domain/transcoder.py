import subprocess
import logging

logger = logging.getLogger(__name__)

class FFmpegTranscoder:
    def transcode(self, input_path: str, output_path: str, width: int, height: int, video_bitrate: str = '2M'):
        command = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', f'scale=min(iw\,{width}):-2',
            '-c:v', 'libx264', '-profile:v', 'main', '-level:v', '3.1',
            '-r', '24',
            '-b:v', video_bitrate,
            '-g', '48', '-keyint_min', '48', '-sc_threshold', '0',
            '-c:a', 'aac', '-b:a', '128k',
            '-f', 'mp4', '-movflags', '+faststart',
            output_path
        ]
        self._execute_ffmpeg(command)

    def _execute_ffmpeg(self, command: list):
        logger.info(f"Executing FFmpeg: {' '.join(command)}")
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed with exit code {e.returncode}: {e.stderr}")
            raise
