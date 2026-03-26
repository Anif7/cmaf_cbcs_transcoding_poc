## Context
The transcoding phase is critical for multi-bitrate ABR delivery. Each output variant must be perfectly aligned to ensure that the final packaged DASH/HLS manifests are seamless. This requires a specialized `FfmpegTranscoder` that enforces strict encoding parameters.

## Goals / Non-Goals
**Goals:**
- Provide a robust interface for scaling and encoding media files.
- Enforce strict 2-second GOP and fixed 24fps for stable DRM packaging.
- Ensure efficient subprocess execution and error handling.
- Maintain clean code by following SRP and minimizing comments/docstrings.

**Non-Goals:**
- Support live transcoding (this is for VOD only).
- Support advanced video filtering beyond simple scaling.
- Directly handle packaging formats like HLS/DASH (this is handled by the packager).

## Decisions
- **Class Implementation**: `FFmpegTranscoder` in `app/domain/transcoder.py`.
- **Primary Method**: `transcode(input_path, output_path, width, height, video_bitrate='2M')`.
- **Encoding Parameters**:
    - **Video Codec**: `libx264` with `main` profile and `3.1` level for broad compatibility.
    - **Scaling**: Use `scale='min(iw,width):-2'`. This ensures we only scale down or preserve dimensions, never scale up. This is also for ABR variant consistency.
    - **Frame Rate**: Strictly forced to `24` fps using `-r 24`.
    - **GOP Alignment**: 
        - `-g 48`: (24 fps * 2 seconds = 48 frames).
        - `-keyint_min 48`: Ensure IDR frames only occur every 2 seconds.
        - `-sc_threshold 0`: Disable scene-cut detection to prevent GOP drifts.
    - **Audio**: `aac` at `128k`.
    - **Container**: `mp4` with `+faststart` for quick VOD playback.
- **Refactoring Strategy**:
    - Extract command construction into a separate helper if needed for better readability.
    - Use `logging` instead of simple `print` or `subprocess.run` defaults.

## Risks / Trade-offs
- **CPU Intensity**: Software encoding with `libx264` is CPU intensive. Scaling might be slow for higher resolutions depending on the host machine.
- **Fixed Parameters**: Forcing 24fps and 2s GOP is great for stability but might not be optimal for all source media (e.g., high-motion sports might prefer 60fps).
