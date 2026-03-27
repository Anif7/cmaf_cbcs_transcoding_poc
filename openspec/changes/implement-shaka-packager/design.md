## Context

The transcoding pipeline produces multiple MP4 renditions that need to be packaged for secure, adaptive streaming. Shaka Packager is the industry standard for generating unified CMAF outputs with Multi-DRM support.

## Goals / Non-Goals

**Goals:**
- Implement a `ShakaPackager` domain service.
- Generate encrypted CMAF segments with the `cbcs` scheme.
- Support Widevine and FairPlay concurrently.
- Optimize storage by using a shared audio track for all video renditions.
- Produce HLS and DASH manifests.

**Non-Goals:**
- Support server-side license generation (client-side raw keys only).
- Implement legacy HLS (TS) segments (Modern CMAF only).

## Decisions

- **CLI-based Execution**: Use `subprocess` to trigger the `packager` binary.
- **Raw Key Encryption**: Use `--enable_raw_key_encryption` for maximum control over key delivery.
- **Subfolder Pattern**: Each video rendition gets its own init and segment templates in named subfolders (e.g., `init_segment=<res>/video_init.m4s`) to ensure a clean delivery structure.
- **Audio Extraction**: Audio will be extracted once from the highest-quality rendition to serve all video streams, reducing total packaged size.

## Risks / Trade-offs

- **[Risk] Widevine/FairPlay key mismatch** → Mitigation: Enforce strict validation of DRM configuration before execution.
- **[Risk] Subfolder permissions** → Mitigation: Ensure the orchestrator handles directory creation before passing to the packager.
