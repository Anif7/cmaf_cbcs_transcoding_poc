## Context

The current `VideoTranscodingTask` logic has hardcoded default values for width (640) and height (360) and does not correctly parse the nested `settings.outputs` JSON structure provided by users. This prevents the system from being truly data-driven and flexible. We need to refactor this in a "clean code" manner to support any number of resolutions and specific encoding settings like CRF and presets.

## Goals / Non-Goals

**Goals:**
- Completely remove hardcoded 640x360 defaults.
- Implement a robust metadata parser for the `settings.outputs` list, supporting nested `video` and `audio` configurations.
- Use this rich metadata to drive single-pass multi-resolution video transcoding.

**Non-Goals:**
- Hardcoding additional "commonly used" resolutions as secondary defaults.
- Implementing complex validation logic for resolutions (this should be handled at the API level or by FFmpeg).

## Decisions

### 1. Nested Metadata Traversal
The orchestrator will now explicitly look into the `video` and `audio` sub-objects of each output rendition.
- **Rationale**: This matches the professional-grade metadata structure (e.g., `out['video']['width']`, `out['video']['crf']`).
- **Implementation**: `VideoTranscodingTask.transcode_video_renditions` will map these values into a list of rendition configurations before passing them to the transcoder.

### 2. Single-Pass Execution for Video Renditions
We will continue with the decision to use a single FFmpeg pass for all video-only renditions, now driven by these dynamic parameters.
- **Rationale**: Optimization remains critical as we scale to more resolutions (e.g., 360p, 480p, 720p, 1080p).
- **Implementation**: The FFmpeg command generator in `FFmpegTranscoder` will dynamically build the `filter_complex` string based on the provided list of renditions.

### 3. Removal of Default Values
If a required parameter (like width/height) is missing from an rendition's metadata, the task should log a warning or use the source values (aspect ratio preserving) rather than hardcoded 640x360.
- **Rationale**: Ensures the system behaves as expected based *only* on user input.

## Risks / Trade-offs

- **Invalid Metadata** → If the user sends corrupted or logically impossible metadata (e.g., width=0), FFmpeg will fail. *Mitigation*: Proper error handling and logging of the FFmpeg output to provide meaningful feedback to the user.
- **Command Generation Complexity** → As we add more per-rendition parameters (preset, CRF), the dynamic FFmpeg command string becomes more complex. *Mitigation*: Use a structured command builder pattern.
