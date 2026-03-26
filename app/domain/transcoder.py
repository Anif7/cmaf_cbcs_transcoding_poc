import subprocess

class FfmpegTranscoder:
    def transcode(self, input_path: str, output_path: str, width: int, height: int, video_bitrate: str = '2M') -> None:
        command = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', f'scale={width}:{height}',
            '-c:v', 'libx264', '-profile:v', 'main', '-level:v', '3.1',
            '-r', '24', # Force 24fps for stable segment calculation
            '-b:v', video_bitrate,
            '-g', '48', '-keyint_min', '48', '-sc_threshold', '0', # Strict 2s GOP
            '-c:a', 'aac', '-b:a', '128k',
            '-f', 'mp4', '-movflags', '+faststart', # Standard VOD MP4
            output_path
        ]
        self._execute_ffmpeg(command)

    def _execute_ffmpeg(self, command: list) -> None:
        subprocess.run(command, check=True, capture_output=True, text=True)
