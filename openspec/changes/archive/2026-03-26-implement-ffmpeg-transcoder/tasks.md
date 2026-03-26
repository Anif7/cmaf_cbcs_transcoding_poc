## 1. Implement FFmpegTranscoder Class

- [x] 1.1 Create `app/domain/transcoder.py` and implement the `FFmpegTranscoder` class.
- [x] 1.2 Implement the `transcode` method with parameters for dimensions and bitrate.
- [x] 1.3 Implement the `_execute_ffmpeg` helper method using `subprocess.run`.
- [x] 1.4 Ensure scaling logic uses `min(iw,width)` to avoid up-scaling.

## 2. Verification and Testing

- [x] 2.1 Verify that the transcoder can successfully generate a 720p output from a sample video.
- [x] 2.2 Check the output stream properties (fps, GOP) using `ffprobe` to ensure compliance with DRM requirements.
