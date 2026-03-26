# Multi-DRM Transcoding POC Task List

## 1. Infrastructure (Django-Celery-Redis)
- [x] 1.1 Setup `TranscodingJob` database model (status using `PositiveIntegerField` and `IntegerChoices`).
- [x] 1.2 Setup `app/domain/`, `app/tasks/`, `app/views/`, and `app/admin/` directories.
- [x] 1.3 Configure `Celery` in `app/celery.py` and `app/settings.py`.
- [x] 1.4 Create `requirements.txt` and `setup.sh` for easy deployment.
- [x] 1.5 Register `TranscodingJobAdmin` with a custom **Retry** action.

## 2. Domain Layer Implementation (Clean Code)
- [x] 2.1 Refactor code to follow Single Responsibility Principle (SRP) and consistent abstraction levels.
- [x] 2.2 Align metadata mapping with the `Lumberjack` payload structure.
- [x] 2.3 **MediaDownloader**: Implement remote source ingestion.
- [x] 2.4 **FfmpegTranscoder**: Support for multi-resolution H.264/AAC transcoding.
- [x] 2.5 **ShakaPackager**: Implement CBCS unified fragmentation with segment templates.
- [x] 2.6 **CloudUploader**: Dynamic Rclone bucket configuration with credentials.

## 3. High-Fidelity Playback Optimizations
- [x] 3.1 Fix `hls_master_playlist_output` for wide compatibility.
- [x] 3.2 Add `drm_label=default` for robust key mapping.
- [x] 3.3 Ensure **VOD** playlist type and static MPD generation to prevent buffering.
- [x] 3.4 Disable `clear_lead` to ensure 100% of segments are encrypted.
- [ ] 3.5 Implement **ABR (Adaptive Bitrate)** support with folder-based partitioning.

## 4. Final Verification
- [ ] 4.1 Perform an end-to-end ABR test run (360p and 720p).
- [ ] 4.2 Verify manifest integrity for both Widevine (DASH) and FairPlay (HLS).
