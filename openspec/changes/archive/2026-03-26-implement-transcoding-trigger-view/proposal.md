## Why

The current system lacks a dedicated API endpoint to trigger transcoding jobs with rich payload parameters. Providing this view will enable external systems or frontends to initiate complex transcoding pipelines (Download -> Transcode -> Package -> Upload) asynchronously using Celery.

## What Changes

- Implement `TranscodingTriggerView` in `app/views/` to handle JSON payloads and initiate jobs.
- Define a class-based Celery task for the transcoding pipeline following SRP and clean code principles.
- Integrate existing `MediaDownloader` and `FfmpegTranscoder` domain logic.
- Add placeholders (`# TODO`) for Packaging and Uploading steps.
- Update `app/urls.py` to include the new view.

## Capabilities

### New Capabilities
- `transcoding-trigger`: API endpoint to accept transcoding job requests and start the orchestration pipeline.

### Modified Capabilities
<!-- No existing capabilities being modified at the spec level. -->

## Impact

- `app/views/`: New file or addition to existing views.
- `app/tasks/`: New module for class-based Celery tasks.
- `app/urls.py`: New route for triggering jobs.
- `app/models/transcoding.py`: Utilized for job state management.
