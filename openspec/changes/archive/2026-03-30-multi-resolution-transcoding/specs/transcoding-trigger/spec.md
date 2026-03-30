## MODIFIED Requirements

### Requirement: Transcoding Trigger API Endpoint
The system SHALL provide a POST API endpoint `/api/v1/transcode/trigger/` that accepts a JSON payload to initiate a transcoding job, supporting complex multi-resolution output configurations.

#### Scenario: Successful multi-resolution job creation
- **WHEN** a valid JSON payload with `input_url`, `output_url`, `settings.outputs`, `storage_parameters`, and `drm_encryption` is POSTed
- **THEN** the system SHALL create a `TranscodingJob` record with `QUEUED` status
- **THEN** the system SHALL return a 201 Created response with the job ID and status
- **THEN** the system SHALL trigger a Celery task to process the job with all rendition settings included

#### Scenario: Invalid payload
- **WHEN** an invalid JSON payload is POSTed
- **THEN** the system SHALL return a 400 Bad Request response with an error message
