import os
import subprocess

class CloudUploader:
    def upload(self, source_dir: str, destination_url: str, **credentials) -> None:
        env = self._get_rclone_environment(credentials)
        target = self._get_target_path(destination_url)
        self._execute_rclone(source_dir, target, env)

    def _get_rclone_environment(self, credentials: dict) -> dict:
        env = os.environ.copy()
        env.update({
            'RCLONE_CONFIG_TEMP_TYPE': 's3',
            'RCLONE_CONFIG_TEMP_PROVIDER': 'Minio',
            'RCLONE_CONFIG_TEMP_ACCESS_KEY_ID': credentials.get('access_key_id'),
            'RCLONE_CONFIG_TEMP_SECRET_ACCESS_KEY': credentials.get('secret_key'),
            'RCLONE_CONFIG_TEMP_ENDPOINT': credentials.get('endpoint'),
            'RCLONE_CONFIG_TEMP_DISABLE_CHECKSUM': 'true',
            'RCLONE_S3_DISABLE_CHECKSUM': 'true'
        })
        return env

    def _get_target_path(self, destination_url: str) -> str:
        return destination_url.split('://', 1)[1] if '://' in destination_url else destination_url

    def _execute_rclone(self, source_dir: str, target: str, env: dict) -> None:
        # Using sync/copy with --s3-disable-checksum to avoid hash calculation issues with Minio/S3
        command = ['rclone', 'copy', source_dir, f'temp:{target}', '--s3-disable-checksum']
        process = subprocess.run(command, env=env, capture_output=True, text=True)
        if process.returncode != 0:
            raise RuntimeError(f"Rclone upload failed: {process.stderr}")
