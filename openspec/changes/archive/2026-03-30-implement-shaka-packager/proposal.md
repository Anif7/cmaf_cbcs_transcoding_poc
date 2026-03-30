## Why

The transcoding pipeline currently lacks a unified packaging stage capable of generating encrypted CMAF segments with Multi-DRM support (Widevine and FairPlay). Implementing a `ShakaPackager` service in the domain layer will allow for standard-compliant, encrypted output that is compatible with modern streaming platforms while maintaining a clean, ABR-organized folder structure and shared audio rendition.

## What Changes

- Implement `ShakaPackager` class in `app/domain/packager.py`.
- Support Multi-DRM packaging (Widevine, FairPlay) using the `cbcs` protection scheme.
- Organize outputs into ABR subfolders (e.g., `360p/`, `720p/`, `audio/`).
- Utilize a shared audio track across all video renditions for efficiency.
- Generate unified manifest files (HLS Master Playlist and DASH MPD).
- Integrate the packaging stage into the existing `VideoTranscodingTask` pipeline.

## Capabilities

### New Capabilities
- `multi-drm-packaging`: Capability to package multiple video renditions and a shared audio track into encrypted CMAF segments with HLS/DASH manifest generation and Multi-DRM support.

### Modified Capabilities
<!-- No requirement changes to existing capabilities. -->

## Impact

- `app/domain/packager.py`: New domain service implementation.
- `app/tasks/transcoding.py`: Integration into the `package_transcoded_streams` step.
- System dependency on `packager` (Shaka Packager CLI).
