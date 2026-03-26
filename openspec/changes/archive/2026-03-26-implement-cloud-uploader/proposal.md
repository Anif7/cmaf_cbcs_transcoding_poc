## Why

The transcoding system requires a reliable way to upload packaged final artifacts to cloud storage (e.g., S3/MinIO). Implementing a dedicated `CloudUploader` service that wraps `rclone` ensures that we can handle high-performance, resilient transfers using a battle-tested tool, while maintaining a clean domain interface.

## What Changes

- Implement `CloudUploader` in `app/domain/uploader.py`.
- Wrap `rclone` CLI to perform directory-to-remote synchronization/copying.
- Implement robust credential handling without modifying the global process environment.
- Add support for S3/MinIO providers with configurable endpoints and checksum disabling.
- Ensure the orchestration pipeline (e.g., `VideoTranscodingTask`) can call this service as part of the pipeline.

## Capabilities

### New Capabilities
- `cloud-upload`: Capability to sync local directories to remote cloud storage using Rclone with dynamic configurations.

### Modified Capabilities
<!-- No requirement changes to existing capabilities. -->

## Impact

- `app/domain/uploader.py`: New implementation.
- `app/tasks/transcoding.py`: Integration of the new uploader (replacing the TODO).
- Systems requiring `rclone` to be installed in the environment.
