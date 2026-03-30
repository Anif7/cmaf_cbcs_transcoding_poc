import os
import subprocess
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ShakaPackager:
    def package(self, video_streams: List[Dict], audio_path: str, output_dir: str, drm_config: Dict) -> None:
        logger.info(f"Starting packaging with DRM config: {drm_config}")
        os.makedirs(output_dir, exist_ok=True)
        
        command = self._build_command(video_streams, audio_path, output_dir, drm_config)
        self._execute_packager(command, output_dir)

    def _get_drm_params(self, drm_config: Dict) -> Dict:
        fairplay = drm_config.get('fairplay', {})
        widevine = drm_config.get('widevine', {})
        
        return {
            'key': widevine.get('key') or fairplay.get('key'),
            'key_id': widevine.get('key_id'),
            'iv': fairplay.get('iv'),
            'uri': fairplay.get('uri')
        }

    def _build_command(self, video_streams: List[Dict], audio_path: str, output_dir: str, drm_config: Dict) -> List[str]:
        drm = self._get_drm_params(drm_config)
        key, key_id, iv, key_uri = drm['key'], drm['key_id'], drm['iv'], drm['uri']

        command = ['packager']
        
        # 🎧 AUDIO (single)
        audio_dir = os.path.join(output_dir, 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        command.append(
            f"input={audio_path},"
            f"stream=audio,"
            f"init_segment=audio/audio_init.mp4,"
            f"segment_template=audio/audio_$Number$.mp4,"
            f"playlist_name=audio/audio.m3u8,"
            f"hls_group_id=audio,"
            f"hls_name=ENGLISH,"
            f"drm_label=default"
        )

        # 🎥 VIDEO (multiple)
        for stream in video_streams:
            path = stream['path']
            name = stream['name']
            
            res_dir = os.path.join(output_dir, name)
            os.makedirs(res_dir, exist_ok=True)

            command.append(
                f"input={path},"
                f"stream=video,"
                f"init_segment={name}/video_init.mp4,"
                f"segment_template={name}/video_$Number$.mp4,"
                f"playlist_name={name}/video.m3u8,"
                f"drm_label=default"
            )

        # 🔐 DRM & Metadata
        command.extend([
            '--enable_raw_key_encryption',
            f'--keys=label=default:key_id={key_id}:key={key}',
            '--protection_scheme', 'cbcs',
            '--protection_systems', 'Widevine,FairPlay',
            '--segment_duration', '10',
            '--clear_lead', '0',
            '--hls_master_playlist_output', 'video.m3u8',
            '--hls_playlist_type', 'VOD',
            '--mpd_output', 'video.mpd',
            '--generate_static_live_mpd',
        ])
        
        if iv:
            command.extend(['--iv', iv])
        if key_uri:
            command.extend(['--hls_key_uri', key_uri])
            
        return command

    def _execute_packager(self, command: List[str], output_dir: str) -> None:
        logger.info(f"Executing Shaka Packager: {' '.join(command)}")
        result = subprocess.run(command, cwd=output_dir, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Shaka Packager failed: {result.stderr}")
            raise RuntimeError(f"Shaka Packager failed: {result.stderr}")
