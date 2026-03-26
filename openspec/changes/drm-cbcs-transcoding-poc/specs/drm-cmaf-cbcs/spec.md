## Multi-DRM Transcoding POC Specification

### Requirement: api-trigger-interface
The system MUST provide a REST API endpoint that accepts transcoding requests with a payload aligned to the `Lumberjack` structure (`input_url`, `output_url`, `storage_parameters`, `drm_encryption`, and `meta_data`).

#### Scenario: trigger-job-with-rich-payload
- **WHEN** a valid POST request is received.
- **THEN** a new job record is created in the database.
- **AND** a Celery background task is queued to initiate the transcoding pipeline.

### Requirement: multi-resolution-abr
The system MUST support generating multiple resolutions (ABR) as specified in the `outputs` property of the request settings.

#### Scenario: abr-transcoding-and-packaging
- **WHEN** the `outputs` request contains multiple target resolutions (e.g., 360p, 720p).
- **THEN** FFmpeg MUST transcode the source into corresponding intermediate files.
- **AND** Shaka Packager MUST package these files into resolution-specific subfolders (e.g., `360p/`, `720p/`).
- **AND** The master manifests (`video.m3u8` and `video.mpd`) MUST reference all generated resolutions.

### Requirement: unified-cmaf-cbcs-packaging
The system MUST use Shaka Packager to fragment the MP4 into CMAF segments and apply `cbcs` encryption for both Widevine and FairPlay.

#### Scenario: multi-drm-single-output
- **WHEN** the media is packaged with `cbcs` scheme and `Widevine,FairPlay` protection systems.
- **THEN** a single set of numbered `.m4s` fragments and initialization segments (e.g., `video_init.m4s`, `video_1.m4s`) is generated per resolution.
- **AND** Both manifests point to the same segments with **0 clear lead** (all segments encrypted).

### Requirement: cloud-upload-orchestration
The system MUST upload the packaged directory to the specified cloud destination using `rclone`, handling S3/Minio credentials dynamically.

#### Scenario: upload-to-destination
- **WHEN** packaging completes.
- **THEN** local artifacts are uploaded to the remote path specified in the API request, with checksums disabled to accommodate S3-compatible providers.
