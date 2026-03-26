import subprocess
from typing import Dict, List

class CloudUploader:
    def upload_directory(self, source_dir: str, destination_path: str, credentials: Dict[str, str]) -> None:
        target_path = self._get_target_path(destination_path)
        rclone_command = self._build_rclone_command(source_dir, target_path, credentials)
        
        self._execute_rclone(rclone_command)

    def _get_target_path(self, destination_path: str) -> str:
        if '://' in destination_path:
            return destination_path.split('://', 1)[1]
        return destination_path

    def _build_rclone_command(self, source_dir: str, target_path: str, credentials: Dict[str, str]) -> List[str]:
        command = [
            'rclone', 'copy', 
            source_dir, 
            f':s3:{target_path}',
            '--s3-provider', 'Minio',
            '--s3-access-key-id', credentials.get('access_key_id', ''),
            '--s3-secret-access-key', credentials.get('secret_key', ''),
            '--s3-endpoint', credentials.get('endpoint', ''),
            '--s3-disable-checksum'
        ]
        return command

    def _execute_rclone(self, command: List[str]) -> None:
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Cloud upload failed: {result.stderr}")
