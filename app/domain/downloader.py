import os
import requests

class MediaDownloader:
    def download(self, source_url: str, local_path: str) -> None:
        response = requests.get(source_url, stream=True)
        response.raise_for_status()
        
        self._save_to_file(response, local_path)

    def _save_to_file(self, response: requests.Response, local_path: str) -> None:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as media_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    media_file.write(chunk)
