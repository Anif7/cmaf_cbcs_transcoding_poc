## Context
To enable transcoding, we first need to fetch source media files from HTTP or HTTPS URLs. We need a dedicated `MediaDownloader` that handles this reliably. By using `rclone`, we can handle these direct downloads efficiently.

## Goals / Non-Goals
**Goals:**
- Provide a consistent interface for downloading media files via `rclone` from HTTP/HTTPS URLs.
- Handle download errors and provide helpful logging.

**Non-Goals:**
- Implement any logic for checking if the downloaded file is valid.
- Support downloading files *without* using `rclone`.
- Handle complex storage backend configurations (S3, GCS, etc.) for now.

## Decisions
- **Class Structure**: Implement a `MediaDownloader` class in `app/domain/downloader.py`.
- **`rclone` command**:
    - Use `rclone copyurl` to download the source file from a URL to a specific target path.
    - Example: `rclone copyurl <URL> /local/path`
- **Error Handling**: Use `subprocess.run(..., check=True)` to capture and log any non-zero exit codes from `rclone`.

## Risks / Trade-offs
- **Dependency on `rclone` installation**: The host system must have `rclone` installed and available in the `PATH`.
- **Subprocess execution**: Managing external processes requires careful handling of timeouts and resource cleanup.
- **Config as env vars**: For security and simplicity, we'll prefer passing `rclone` configurations via environment variables during the download process.
