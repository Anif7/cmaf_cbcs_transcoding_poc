import subprocess
import logging

logger = logging.getLogger(__name__)

class DownloadError(Exception):
    pass

class MediaDownloader:
    def download(self, source_url: str, destination_path: str):
        command = [
            "rclone",
            "copyurl",
            source_url,
            destination_path,
        ]

        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"rclone failed: {e.stderr}")
            raise DownloadError(f"rclone failed with exit code {e.returncode}") from e
        except FileNotFoundError:
            raise DownloadError("rclone command not found.")
