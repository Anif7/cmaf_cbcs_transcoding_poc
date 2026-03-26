## 1. Domain Service Implementation

- [x] 1.1 Create `app/domain/uploader.py`.
- [x] 1.2 Implement `CloudUploader` class with `upload_directory` method.
- [x] 1.3 Add helper method to generate Rclone command flags from credentials (avoiding `os.environ` modification).
- [x] 1.4 Implement error handling for Rclone process failures.

## 2. Pipeline Integration

- [x] 2.1 Update `app/tasks/transcoding.py` to import `CloudUploader`.
- [x] 2.2 Implement `upload_final_artifacts` method in `VideoTranscodingTask` using `CloudUploader`.
- [x] 2.3 Ensure the pipeline correctly passes storage parameters to the uploader.

## 3. Verification

- [x] 3.1 Verify directory-to-cloud synchronization with mock Rclone or local MinIO.
- [x] 3.2 Verify that the process environment remains untouched during execution.
