## Context

The project aim is to provide a robust transcoding service. Currently, models for `TranscodingJob` exist, but there is no external API to trigger them, and the orchestration logic needs to be implemented within a Celery task structure that follows clean code principles (SRP).

## Goals / Non-Goals

**Goals:**
- Implement a Django View for triggering jobs.
- Implement a class-based Celery task for orchestration.
- Ensure the pipeline steps (Download, Transcode, Package, Upload) are modular and follow SRP.
- Use existing domain logic for downloading and transcoding.
- Provide hooks for future implementation of packaging and uploading.

**Non-Goals:**
- Implement the actual logic for packaging and uploading in this change (placeholders only).
- Implement complex retry logic or advanced error recovery beyond basic status updates.

## Decisions

- **Class-Based Celery Task**: Instead of a simple function, we will use a class-based approach inheriting from `celery.Task` to encapsulate the pipeline state. This task acts as the orchestrator, calling domain services.
- **Model-Level Status Management**: Status transitions and helpers (`update_status`, `mark_as_completed`, `mark_as_failed`) are moved to the `TranscodingJob` model for centralized state management.
- **Domain Webhook Logic**: Webhook sending is extracted to `app/domain/webhook.py` as a standalone function `send_job_webhook(job)` to ensure SRP.
- **Refined Naming**: Task methods use intent-revealing names like `download_source_media` and `transcode_to_specified_formats` instead of generic step numbers.

## Risks / Trade-offs

- **[Risk] Long running tasks** → Mitigation: Celery handles background execution; ensure timeouts are considered in future iterations.
- **[Risk] Cleanup failure** → Mitigation: Use `finally` block to ensure workspace cleanup.
