## ADDED Requirements

### Requirement: Download Media with rclone
The `MediaDownloader` must be able to use `rclone` to download a media file from a source URL to a local destination path.

#### Scenario: Successful download from HTTPS
- **WHEN** a valid HTTPS source URL is provided
- **THEN** `rclone` should download the file to the specified local path
- **AND** the download should be marked as successful

### Requirement: Handle Download Failures
The `MediaDownloader` must handle various failure scenarios.

#### Scenario: Source file not found
- **WHEN** a non-existent source URL is provided
- **THEN** `rclone` will exit with a non-zero code
- **AND** the `MediaDownloader` should raise an error containing the source URL

#### Scenario: Authentication failure
- **WHEN** an S3 source URL is provided with invalid access keys
- **THEN** `rclone` will fail with an authentication error
- **AND** the `MediaDownloader` should capture this failure message and raise a corresponding error
