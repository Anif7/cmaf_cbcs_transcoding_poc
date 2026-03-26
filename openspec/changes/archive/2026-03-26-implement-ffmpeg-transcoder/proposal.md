# Proposal: Implement FFmpegTranscoder for Multi-Resolution Scaling

## Context
To support Adaptive Bitrate (ABR) streaming, we need to generate multiple resolutions of the source media. These output files must be meticulously prepared for further DRM packaging (using tools like Shaka Packager), which requires strict adherence to specific encoding parameters like fixed framerate and strict GOP intervals.

## Objective
Implement a `FFmpegTranscoder` in `app/domain/` that provides a clean interface for transcoding media files into various resolutions. The transcoder must ensure that all outputs are perfectly aligned for DRM packaging, specifically by enforcing a strict 2-second GOP and fixed 24fps.

## Proposed Solution
- Create a `FfmpegTranscoder` class in `app/domain/transcoder.py`.
- Implement a `transcode` method that takes input/output paths, dimensions, and bitrate.
- Use `ffmpeg` to handle the heavy lifting of scaling and encoding.
- Enforce strict parameters:
    - `-r 24`: Force 24fps.
    - `-g 48 -keyint_min 48`: Force a strict 2-second GOP (24 * 2 = 48).
    - `-sc_threshold 0`: Disable scene-cut detection to maintain GOP consistency.
    - `-f mp4 -movflags +faststart`: Prepare for standard VOD delivery.

## Alternatives Considered
- **Cloud Transcoding APIs (AWS Elemental MediaConvert, Google Transcoder API)**: These are powerful but introduce external dependencies and costs. A local `ffmpeg` based transcoder is more suitable for this POC.
- **Python libraries like `moviepy` or `ffmpeg-python`**: While these provide higher-level APIs, they often abstract away too much or introduce overhead. Calling `ffmpeg` via `subprocess` provides the most direct control over the specific parameters needed for DRM preparation.
