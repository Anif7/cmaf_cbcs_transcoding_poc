## Context

Current DRM workflows often generate two separate sets of media segments: one using CENC (AES-CTR) for Widevine and another using CBCS (AES-CBC) for FairPlay. This POC demonstrates a unified pipeline using CMAF and CBCS, triggered via a structured API and managed by database models within a Django-based framework.

## Goals / Non-Goals

**Goals:**
-   **API-First Orchestration**: Receive jobs through a REST API including source URLs, destination metadata, and DRM keys (aligned with Lumberjack payload).
-   **Multi-Resolution ABR (Adaptive Bitrate)**: Support for generating multiple resolutions (e.g., 360p, 720p) in a single job.
-   **Structured State Management**: Track job statuses and configuration in database models with a Retry functionality in the Admin.
-   **Clean Architecture & SRP**: Rigid adherence to Clean Code principles, isolating concerns into `app/models`, `app/views`, `app/tasks`, and `app/domain`.
-   **Unified CMAF/CBCS Delivery**: Single set of segments for both ecosystems with no "clear lead" (all segments encrypted).

**Non-Goals:**
-   **Production Scalability**: Limited concurrency focus for POC.
-   **Frontend UI**: Focused strictly on Backend-to-Backend (B2B) functionality.

## Decisions

-   **Framework**: Django with Celery and Redis.
-   **Unified Packaging (Shaka Packager)**:
    -   **Encryption**: `cbcs` scheme with shared Key ID and Key.
    -   **Segment Template**: Numbered segments (`video_$Number$.m4s`) and init segments.
    -   **Static manifests**: Explicitly set as VOD to prevent "live" buffering issues.
    -   **Organized Storage**: Segments sorted into resolution-specific subfolders (e.g., `360p/`).
-   **Orchestration**:
    -   **Domain Layer** (`app/domain/`): CLI wrappers for FFmpeg, Shaka, and Rclone with strict SRP.
    -   **Models Layer** (`app/models/`): Tracks job metadata and status.
-   **Tooling Integration**: `subprocess` with environment-based credential injection (Rclone).

## System Dependencies

To successfully run this POC, the following system-level tools MUST be pre-installed and available in the system's `PATH`:
1.  **FFmpeg**: For ABR transcoding.
2.  **Shaka Packager**: For multi-DRM fragmentation.
3.  **Rclone**: For cloud delivery.
4.  **Redis**: Required for Celery.

## Setup & Deployment

A `setup.sh` script is provided to automate the initial configuration:
- Creates a Python virtual environment.
- Installs dependencies from `requirements.txt`.
- Initializes the SQLite database and runs migrations.
- Disables Python bytecode (`.pyc`) generation during setup.

To run the full pipeline, ensure Redis is running, start a Celery worker (`celery -A app worker`), and trigger jobs via the REST API endpoint.

## Monitoring & Debugging

-   **Django Admin**: Located at `/admin/` with custom **Retry** action support.
-   **Logging**: Structured logging in orchestrator and tasks layers (viewable in Celery logs).
