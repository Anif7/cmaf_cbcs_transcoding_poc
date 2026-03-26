## Context

Final transcoded and packaged artifacts need to be moved from the local workspace to cloud storage. Rclone's `copy` and `sync` commands are ideal for this, but we need an implementation that follows project rules (no process environment mutation, clean naming, SRP).

## Goals / Non-Goals

**Goals:**
- Wrap `rclone` CLI in a `CloudUploader` service.
- Support dynamic S3/MinIO configuration.
- Avoid mutation of `os.environ`.
- Provide clean, intent-revealing method names.

**Non-Goals:**
- Implement low-level S3 protocols (use Rclone).
- Handle multi-tenant Rclone configurations (use temporary, on-the-fly backends).

## Decisions

- **On-the-fly Rclone Backends**: Instead of managing a persistent `rclone.conf` file or modifying `os.environ`, we will use Rclone's `:s3:` backend syntax and pass configuration as command-line flags (e.g., `--s3-access-key-id`). This is cleaner and safer for concurrent execution.
- **Service Layer Placement**: `CloudUploader` resides in `app/domain/uploader.py` as an explicit CLI wrapper.
- **Naming Alignment**: Use `upload_directory` instead of generic `upload`.

## Risks / Trade-offs

- **[Risk] Rclone binary missing** → Mitigation: Ensure Rclone is part of the system requirements and verify its path if needed.
- **[Risk] Command line length limits** → Mitigation: S3 parameters are relatively short; for very complex configs, a temporary config file would be used, but flags are sufficient here.
