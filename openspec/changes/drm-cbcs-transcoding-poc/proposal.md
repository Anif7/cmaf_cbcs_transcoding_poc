## Why

Traditional DRM workflows often require separate media sets for different platforms: CENC (AES-CTR) for Widevine/PlayReady and CBCS (AES-CBC) for FairPlay. This redundancy increases storage costs and fragments CDN cache, leading to lower cache efficiency.

By adopting the CMAF (Common Media Application Format) with the `cbcs` encryption scheme, we can generate a single set of encrypted `.m4s` segments that are natively compatible with both Widevine and FairPlay. This POC aims to demonstrate this "single-file" approach, showing how it reduces storage footprint and improves playback performance globally.

## What Changes

We will introduce a structured Python-based Proof of Concept application (Django-based) that automates the DRM transcoding pipeline via an API-triggered workflow. This will include:
1.  **API Integration**: An endpoint to receive transcoding details (source URL, destination path, bucket keys, DRM keys) from an external project.
2.  **Database Models**: To track transcoding progress, store keys, and manage configuration.
3.  **Celery Tasks**: Background processing for long-running transcoding and packaging jobs.
4.  **Domain-Driven Orchestration**: Decoupled domain logic for media acquisition, transcoding (H.264/AAC), unified packaging (CMAF/CBCS), and cloud-upload.
5.  **Structured Architecture**: Organized into `app/models`, `app/views`, `app/tasks` and `app/domain` for better separation of concerns.

## Capabilities

### New Capabilities
- `drm-cmaf-cbcs`: A structured, API-triggered pipeline for unified DRM transcoding (Widevine + FairPlay) using CMAF and CBCS encryption, integrated with DB state management.

### Modified Capabilities
- (None)

## Impact

-   **New Tools**: A Python script/orchestrator using standard CLI tools (`ffmpeg`, `packager`, `rclone`).
-   **Infrastructure**: Requires `ffmpeg`, `shaka-packager`, and `rclone` in the environment.
-   **Security**: Uses static keys for the POC, with future extensions for key server integration.
