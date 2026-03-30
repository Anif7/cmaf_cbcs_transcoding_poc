## Why

The current implementation of `VideoTranscodingTask` relies on hardcoded default values for resolution (Width=640, Height=360) and does not correctly parse the detailed configuration provided in the `settings.outputs` metadata. This prevents the system from supporting custom resolutions, bitrates, and presets. We need to refactor the task logic to properly parse the nested video/audio metadata and remove these defaults in a clean, maintainable way.

## What Changes

- **Metadata Parsing Logic**: Refactor `VideoTranscodingTask.transcode_video_renditions` to correctly navigate the `settings.outputs` structure (e.g., `out['video']['width']`) and avoid hardcoded defaults.
- **FFmpeg Integration**: Update `FFmpegTranscoder` to receive these rich parameters (CRF, bitrate, preset, etc.) and apply them to the encoding process.
- **Efficiency Optimization**: Combine this clean metadata parsing with a single-pass video transcoding execution (using `filter_complex`) to decode the source only once for all renditions.

## Capabilities

### New Capabilities
- `dynamic-multi-resolution-transcoding`: Ability to transcode a source media into any number of resolutions and bitrates based purely on the provided job metadata, without reliance on internal defaults.

### Modified Capabilities
- `transcoding-trigger`: Ensure the API accepts the full nested `settings.outputs` JSON structure.

## Impact

- `app/tasks/transcoding.py`: Complete refactoring of `transcode_video_renditions` and `execute_pipeline` to handle the new metadata format.
- `app/domain/transcoder.py`: Update the transcoding method to accept and apply the full range of encoding parameters.
