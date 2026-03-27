## 1. Domain Service Implementation

- [x] 1.1 Create `app/domain/packager.py`.
- [x] 1.2 Implement `ShakaPackager` class with `package` method.
- [x] 1.3 Add DRM configuration validation.
- [x] 1.4 Implement `_build_command` to generate the complex Shaka Packager CLI string.
- [x] 1.5 Implement directory organization (ABR subfolders).
- [x] 1.6 Implement error handling for packager process failures.

## 2. Pipeline Integration

- [x] 2.1 Update `app/tasks/transcoding.py` to import `ShakaPackager`.
- [x] 2.2 Implement `package_transcoded_streams` method in `VideoTranscodingTask` using `ShakaPackager`.
- [x] 2.3 Ensure the pipeline correctly passes DRM configuration and stream metadata.

## 3. Verification

- [ ] 3.1 Verify manifest generation (HLS/DASH) with sample renditions.
- [ ] 3.2 Verify `cbcs` encryption flags in the generated artifacts.
- [ ] 3.3 Verify subfolder organization and shared audio track reference.
