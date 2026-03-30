# Capability: Multi-DRM Packaging

## Purpose
This capability enables secure, industry-standard content protection for video-on-demand assets using Common Media Application Format (CMAF) and Multi-DRM encryption (Widevine and FairPlay).

## Requirements

### Requirement: Multi-DRM CMAF Packaging
The system SHALL package transcoded media into encrypted CMAF segments using the `cbcs` protection scheme for both Widevine and FairPlay DRM.

#### Scenario: Successful Multi-DRM package
- **WHEN** multiple video renditions, a source for audio, and valid DRM credentials (key, key_id, iv, uri) are provided
- **THEN** the system SHALL generate encrypted `.mp4` segments and a Master HLS Playlist and DASH MPD
- **THEN** the system SHALL use raw key encryption with Widevine and FairPlay protection systems enabled

### Requirement: Unified ABR Organization
The system SHALL organize packaged artifacts into a clean, resolution-based subfolder structure with a shared audio track.

#### Scenario: Subfolder organization verify
- **WHEN** packaging is complete
- **THEN** the system SHALL have created a separate folder for each video rendition (e.g., `360p/`, `720p/`) and a single `audio/` folder
- **THEN** the Master Playlist SHALL reference the unique audio rendition across all video variants
