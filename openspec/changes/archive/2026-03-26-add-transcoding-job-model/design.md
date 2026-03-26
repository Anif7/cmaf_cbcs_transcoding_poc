## Context
The application needs to handle transcoding jobs triggered by APIs. Currently, these jobs are handled without a persistent state store, making it harder to monitor or retry them. 

## Goals / Non-Goals
**Goals:**
- Implement a `TranscodingJob` model to track media processing tasks.
- Provide a clear status lifecycle for each job.
- Store relevant configurations (storage, DRM, meta-data) for each job.
- Register the model in the Django admin interface for visibility.

**Non-Goals:**
- Implement the actual transcoding logic (this model is only for tracking).
- Set up complex background worker integrations (this model only provides the storage layer).

## Decisions
- **Inheritance**: Inherit from `model_utils.models.TimeStampedModel` to provide automatic `created` and `modified` timestamps.
- **Model Fields**: 
    - `input_url`: URL of the source media file.
    - `output_path`: Destination path for the transcoded media.
    - `webhook_url`: Optional callback URL for job completion.
    - `storage_config`: Store destination S3/GCS credentials and bucket details.
    - `drm_config`: Store DRM keys, provider, and encryption settings.
    - `meta_data`: Store arbitrary job metadata as a JSON object.
    - `status`: Use `IntegerChoices` for efficient indexing and clear logic.
    - `error_message`: Store failure details for troubleshooting.

- **Admin Interface**: 
    - Display `id`, `input_url`, `status`, `created`, and `modified` in the list view.
    - Provide filters for `status` and search for `input_url` and `id`.

## Risks / Trade-offs
- **JSONField Stability**: Using `JSONField` for configurations allows flexibility but loses the benefit of schema enforcement at the DB level.
- **Single Model for All Tasks**: As the project grows, we might need separate models for different task types, but `TranscodingJob` is sufficient for current requirements.
