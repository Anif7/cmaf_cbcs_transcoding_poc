import subprocess
import logging
from app.utils import convert_to_ffmpeg_bitrate

logger = logging.getLogger(__name__)


class FFmpegTranscoder:
    def extract_audio(self, input_path: str, output_path: str):
        command = [
            'ffmpeg', '-y', '-i', input_path,
            '-vn', '-c:a', 'aac', '-b:a', '128k',
            '-ac', '2', '-ar', '48000',
            output_path
        ]
        self._execute_ffmpeg(command)

    def transcode_video_variants(self, input_path: str, video_variants: list):
        if not video_variants:
            return

        logger.info(f"Generating single-pass transcoding command for {len(video_variants)} variants")
        command = ['ffmpeg', '-y', '-i', input_path]
        command.extend(['-filter_complex', create_filter_complex(video_variants)])

        for index, variant in enumerate(video_variants):
            command.extend(build_variant_output_arguments(index, variant))

        self._execute_ffmpeg(command)

    def _execute_ffmpeg(self, command: list):
        logger.info(f"Executing FFmpeg: {' '.join(command)}")
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed with exit code {e.returncode}: {e.stderr}")
            raise


def create_filter_complex(video_variants: list) -> str:
    split_outputs = "".join([f"[v{i}]" for i in range(len(video_variants))])
    filter_parts = [f"[0:v]split={len(video_variants)}{split_outputs}"]
    
    for index, variant in enumerate(video_variants):
        filter_parts.append(f"[v{index}]scale=min(iw\,{variant['width']}):-2[v{index}out]")
        
    return ';'.join(filter_parts)

def build_variant_output_arguments(index: int, variant: dict) -> list:
    video_config = variant.get('video', {})
    arguments = [
        '-map', f"[v{index}out]",
        '-c:v', 'libx264', '-profile:v', 'main', '-level:v', '3.1',
        '-r', str(video_config.get('fps', 24)),
        '-g', '48', '-keyint_min', '48', '-sc_threshold', '0',
        '-preset', video_config.get('preset', 'faster')
    ]

    if 'crf' in video_config:
        arguments.extend(['-crf', str(video_config['crf'])])

    arguments.extend(get_bitrate_arguments(video_config))
    arguments.extend(['-an', '-f', 'mp4', '-movflags', '+faststart', variant['path']])
    
    return arguments

def get_bitrate_arguments(video_config: dict) -> list:
    arguments = []
    if 'max_video_bitrate' in video_config:
        bitrate = convert_to_ffmpeg_bitrate(video_config['max_video_bitrate'])
        arguments.extend(['-b:v', bitrate])
        if 'bitrate_buffer_size' in video_config:
            buffer_size = convert_to_ffmpeg_bitrate(video_config['bitrate_buffer_size'])
            arguments.extend(['-maxrate', bitrate, '-bufsize', buffer_size])
    return arguments