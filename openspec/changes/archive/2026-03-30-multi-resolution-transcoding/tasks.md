## 1. Domain Layer: Metadata-Driven Transcoding

- [x] 1.1 Update `FFmpegTranscoder` in `app/domain/transcoder.py` to add a `transcode_multiple_video_renditions` method that accepts a list of rich rendition configurations (width, height, CRF, preset, etc.).
- [x] 1.2 Implement the generation of a dynamic single-pass FFmpeg command using `filter_complex` with `split` and `scale` filters, fully driven by input configurations without hardcoded defaults.
- [x] 1.3 Ensure each video output mapping in the FFmpeg command correctly applies the specific video parameters (bitrate, preset, CRF) provided in the metadata.

## 2. Orchestration Layer: Clean Metadata Parsing

- [x] 2.1 Refactor `VideoTranscodingTask.transcode_video_renditions` in `app/tasks/transcoding.py` to correctly parse the nested `settings.outputs` structure (e.g., `out['video']['width']`, `out['video']['height']`, `out['video']['preset']`).
- [x] 2.2 Completely remove the hardcoded 640 and 360 default values from the loop in `transcode_video_renditions`.
- [x] 2.3 Map these parsed parameters into a structured configuration list for the new multi-output transcoder method.

## 3. Packaging and Verification

- [x] 3.1 Verify that `ShakaPackager` correctly organizes the shared audio track and multiple metadata-driven video-only renditions into the final CMAF package.
- [x] 3.2 Add a basic integration test or a manual verification script (e.g., `verify_transcoder.py`) to confirm that any set of resolutions/bitrates from the metadata is correctly processed.
