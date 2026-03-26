## 1. Implement MediaDownloader Class

- [x] 1.1 Create `app/domain/downloader.py` and implement the `MediaDownloader` class.
- [x] 1.2 Implement the `download` method to execute the `rclone copyurl` command using `subprocess.run`.
- [x] 1.3 Add logic to handle direct URL downloads with `rclone`.
- [x] 1.4 Implement robust error handling to capture and raise specific exceptions for common `rclone` failures.

## 2. Testing and Verification

- [x] 2.1 Verify that the `MediaDownloader` can successfully download a file from a public URL.
- [x] 2.2 Manually test with a sample S3 configuration (if possible) or mock the `subprocess` call to verify environment variable handling.
