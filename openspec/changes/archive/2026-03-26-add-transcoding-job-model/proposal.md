# Proposal: Add TranscodingJob Model

## Context
The project currently lacks a structured way to track the state of transcoding jobs. We need a model to store the input URL, output path, storage/DRM configurations, and the current status of the job (e.g., Queued, Transcoding, Completed, Failed).

## Objective
Implement a `TranscodingJob` model to manage the lifecycle of media transcoding tasks and provide a basic Django Admin interface for monitoring and manual intervention.

## Proposed Solution
- Create a `TranscodingJob` model in `app/models/transcoding.py`.
- Use `PositiveIntegerField` for the status with choices.
- Use `JSONField` for `meta_data`, `storage_config`, and `drm_config`.
- Register the model in `app/admin/transcoding.py` with a basic admin interface.

## Alternatives Considered
- Using separate models for each stage of the job, which would be over-engineered for this stage.
- Using a simple database table without Django models, which would lose the benefits of ORM and the built-in admin interface.
