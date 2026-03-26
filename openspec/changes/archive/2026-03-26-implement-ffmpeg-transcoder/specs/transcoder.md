## ADDED Requirements

### Requirement: Multi-Resolution Video Scaling
The transcoder must be able to scale the input video into different dimensions (e.g., 720p, 1080p).

#### Scenario: Scaled 720p Output
- **WHEN** a 720p resolution is requested (1280x720)
- **THEN** the transcoder should output a video with precisely those dimensions (if original is larger)
- **AND** it should never scale up the video if the source is smaller than the target.
- **AND** it should use a 2 Mbps bitrate (`2M`)

### Requirement: Strict GOP and Framerate Alignment
The output must be strictly prepared for seamless ABR switching and DRM packaging.

#### Scenario: Fixed 24fps and 2s GOP
- **WHEN** any video is transcoded
- **THEN** the transcoder should force the framerate to exactly 24fps
- **AND** it should enforce strict GOP intervals of exactly 48 frames (2 seconds)
- **AND** it should disable scene-cut detection to maintain GOP intervals

### Requirement: Standard VOD Output Format
The resulting video should follow the standard VOD MP4 format.

#### Scenario: Progressive MP4 Output
- **WHEN** transcoding is complete
- **THEN** the final output should be an MP4 file with the `+faststart` flag for quick VOD playback
