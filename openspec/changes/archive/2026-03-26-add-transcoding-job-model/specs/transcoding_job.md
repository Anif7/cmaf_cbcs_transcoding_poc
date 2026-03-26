## ADDED Requirements

### Requirement: Create TranscodingJob
A `TranscodingJob` can be created with an input URL, output path, and relevant configurations.

#### Scenario: New Job Initialization
- **WHEN** a new `TranscodingJob` is created
- **THEN** its default status should be `Queued` (1)
- **AND** `meta_data`, `storage_config`, and `drm_config` should default to empty JSON objects

### Requirement: Track Job Status
The `TranscodingJob` tracks the progress through multiple stages.

#### Scenario: Updating Status to Transcoding
- **WHEN** a job moves from `Downloading` to `Transcoding`
- **THEN** the status field should reflect the update
- **AND** the `updated_at` timestamp should be updated automatically

### Requirement: Manage Job Errors
Jobs that fail should store an error message.

#### Scenario: Job Failure
- **WHEN** a job is marked as `Failed` (7)
- **THEN** it should store the failure reason in `error_message`
