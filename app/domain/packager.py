import os
import subprocess

class ShakaPackager:
    def package(self, stream_inputs: list, output_dir: str, drm_config: dict) -> None:
        os.makedirs(output_dir, exist_ok=True)
        self._validate_drm_config(drm_config)
        command = self._build_command(stream_inputs, output_dir, drm_config)
        self._execute_packager(command, output_dir)

    def _validate_drm_config(self, drm_config: dict) -> None:
        fairplay = drm_config.get('fairplay', {})
        widevine = drm_config.get('widevine', {})
        if not fairplay.get('key') or not (fairplay.get('content_id') or widevine.get('content_id')):
            raise ValueError("DRM configuration requires key and content_id")

    def _build_command(self, stream_inputs: list, output_dir: str, drm_config: dict) -> list:
        fairplay = drm_config.get('fairplay', {})
        widevine = drm_config.get('widevine', {})
        
        key = fairplay.get('key')
        key_id = fairplay.get('content_id') or widevine.get('content_id')
        iv = fairplay.get('iv',)
        key_uri = fairplay.get('uri')

        command = ['packager']
        
        # ── Audio stream ──────────────────────────────────────────────────────
        # Extract audio from the highest quality rendition (last in list)
        os.makedirs(os.path.join(output_dir, 'audio'), exist_ok=True)
        audio_input = stream_inputs[-1]['path']
        command.append(
            f"input={audio_input},"
            f"stream=audio,"
            f"init_segment=audio/audio_init.m4s,"
            f"segment_template=audio/audio_$Number$.m4s,"
            f"playlist_name=audio/audio.m3u8,"
            f"drm_label=default"
        )

        # ── Video renditions ──────────────────────────────────────────────────
        for stream in stream_inputs:
            path     = stream['path']
            res_name = stream['name']
            os.makedirs(os.path.join(output_dir, res_name), exist_ok=True)

            descriptor = (
                f"input={path},"
                f"stream=video,"
                f"init_segment={res_name}/video_init.m4s,"
                f"segment_template={res_name}/video_$Number$.m4s,"
                f"playlist_name={res_name}/video_v.m3u8,"
                f"drm_label=default"
            )
            command.append(descriptor)

        # ── Global packaging flags ────────────────────────────────────────────
        command.extend([
            '--enable_raw_key_encryption',
            f'--keys=label=default:key_id={key_id}:key={key}',
            '--protection_scheme', 'cbcs',
            '--protection_systems', 'Widevine,FairPlay',
            '--segment_duration', '2',
            '--clear_lead', '1',
            '--hls_master_playlist_output', 'video.m3u8',
            '--hls_playlist_type', 'VOD',
            '--mpd_output', 'video.mpd',
            '--default_language', 'en',
        ])
        
        if iv:
            command.extend(['--iv', iv])
        if key_uri:
            command.extend(['--hls_key_uri', key_uri])
            
        return command

    def _execute_packager(self, command: list, output_dir: str) -> None:
        process = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
        if process.returncode != 0:
            raise RuntimeError(f"Shaka Packager failed: {process.stderr}")
