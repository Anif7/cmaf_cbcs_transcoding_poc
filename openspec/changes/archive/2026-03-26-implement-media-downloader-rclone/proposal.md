# Proposal: Implement MediaDownloader using rclone

## Context
To process video transcoding jobs, we need to download source media files from HTTP or HTTPS URLs. Implementing a robust and efficient media retrieval system is essential for the stability and performance of our transcoding pipeline.

## Objective
The goal is to implement a `MediaDownloader` in `app/domain/downloader.py` that leverages the `rclone` command-line tool. This will provide a reliable way to download input media files from HTTP/HTTPS URLs, benefiting from `rclone`'s efficient data transfer capabilities.

## Proposed Solution
- Create a `MediaDownloader` class in `app/domain/downloader.py`.
- The downloader will use the `subprocess` module to execute `rclone copyto` or `rclone copy` commands.
- It will support configuring storage backends through JSON configurations (likely passed from the `TranscodingJob`).
- The downloader will handle transient failures and provide logging for the download process.

## Alternatives Considered
- **Native SDKs (boto3, google-cloud-storage)**: This would require writing specific code for each provider we want to support, increasing complexity. `rclone`'s unified interface simplifies this significantly.
- **`requests` for all downloads**: While suitable for some HTTP endpoints, `requests` is less efficient for large files and lacks built-in support for cloud storage protocols.
