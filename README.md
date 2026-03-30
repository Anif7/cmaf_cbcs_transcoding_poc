# CMAF CBCS Transcoding & Multi-DRM Pipeline (POC)

## 🚀 Overview
This repository contains a **Proof-of-Concept (POC)** for a high-performance video transcoding and packaging pipeline. The primary objective of this POC is to demonstrate **Unified CMAF Delivery** using the `cbcs` encryption scheme for both **Apple FairPlay** and **Google Widevine**.

### The Problem: Legacy Multi-DRM
Traditionally, supporting both Widevine (Android/Chrome) and FairPlay (Apple) required:
- **CENC (AES-CTR)** encryption for Widevine (DASH).
- **CBCS (AES-CBC)** encryption for FairPlay (HLS).
- **Redundant Storage**: Two complete sets of encrypted media files (doubling storage costs).
- **Increased Packaging Costs**: Separate packaging workflows for HLS and DASH.

### The Solution: Unified CMAF CBCS
This POC leverages the industry convergence around `cbcs` (AES-CBC) and CMAF:
- ✅ **Single Set of Media Files**: One set of `cbcs` encrypted segments is shared by both HLS and DASH manifests.
- ✅ **50% Storage Savings**: Eliminates redundant `cenc` files, halving storage and egress costs.
- ✅ **Simplified Delivery**: A unified packaging process generates both DASH and HLS manifests pointing to the same disk location.
- ✅ **Native Device Support**: Modern Widevine implementations (Android/Web) and FairPlay (iOS/macOS) now both support `cbcs`.

> [!NOTE]
> For a detailed technical breakdown and performance metrics (storage, compute, cost) comparing this new approach to the legacy Lumberjack workflow, see our **[Comparative Analysis](COMPARISON.md)**.

---

## 🛠 Features
- **Modern Packaging**: CMAF-based unified delivery for HLS and DASH.
- **Unified DRM Signaling**: Integrated Widevine and FairPlay protection within a single workflow.
- **Asynchronous Processing**: Scalable task orchestration using **Celery** and **Redis**.
- **Efficient Transcoding**: Single-pass multi-variant generation using **FFmpeg**.
- **Cloud-Native Storage**: Automated artifact uploads to S3-compatible storage (Minio) via **Rclone**.
- **Real-time Observability**: Webhook notifications for job status updates (Downloding, Transcoding, Packaging, Uploading, Completed).

---

## 🏗 Architecture & Workflow

The `VideoTranscodingTask` orchestrates the following automated pipeline:

1.  **Ingestion**: Source media is fetched from the provided `input_url`.
2.  **Audio Extraction**: A shared audio track (AAC) is extracted to prevent redundant encoding across video variants.
3.  **Video Transcoding**: FFmpeg scales and encodes the source into multiple resolutions (e.g., 360p, 720p, 1080p) using `libx264`.
4.  **CMAF Packaging & Encryption**: **Shaka Packager** creates:
    -   Common `cbcs` encrypted segments.
    -   HLS Master Playlist (`video.m3u8`).
    -   DASH Manifest (`video.mpd`).
5.  **Artifact Delivery**: **Rclone** synchronizes the final segments and manifests to the specified cloud storage.
6.  **Webhook Notification**: The system notifies the management layer of job completion or failure.

---

## 💻 Tech Stack
- **Backend**: Python 3.12, Django 5.x
- **Task Queue**: Celery, Redis
- **Media Engines**: 
  - **FFmpeg**: Video encoding and audio extraction.
  - **Shaka Packager**: Unified CMAF packaging and Multi-DRM signaling.
- **Storage Utility**: Rclone (S3 integration)

---

## 🏁 Getting Started

### Prerequisites
Ensure the following binaries are installed and available in your `PATH`:
- `ffmpeg`
- `packager` (Shaka Packager)
- `rclone`

### Installation
1. Clone the repository and navigate to the project root.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python manage.py migrate
   ```
4. Start the Celery worker:
   ```bash
   celery -A app worker -l info
   ```

---

## 🔌 API Usage

### Trigger a Transcoding Job
**Endpoint**: `POST /api/v1/transcode/trigger/`

**Sample Request Body**:
```json
{
  "input_url": "https://example.com/source.mp4",
  "output_url": "s3://my-bucket/vod/my-content/",
  "webhook_url": "https://callback.com/jobs/",
  "storage_parameters": {
    "output": {
      "ENDPOINT": "http://minio:9000",
      "ACCESS_KEY_ID": "admin",
      "SECRET_KEY": "password"
    }
  },
  "drm_encryption": {
    "widevine": {
      "key_id": "YOUR_KEY_ID",
      "key": "YOUR_WIDEVINE_KEY"
    },
    "fairplay": {
      "key": "YOUR_FAIRPLAY_KEY",
      "iv": "YOUR_IV",
      "uri": "skd://YOUR_KEY_ID"
    }
  },
  "settings": {
    "outputs": [
      {
        "name": "720p",
        "video": { "width": 1280, "height": 720, "max_video_bitrate": "2500k" }
      },
      {
        "name": "1080p",
        "video": { "width": 1920, "height": 1080, "max_video_bitrate": "5000k" }
      }
    ]
  }
}
```

---

## 📈 Roadmap
- [ ] Support for **CENC** (CTR) fallback for legacy devices.
- [ ] Dynamic bitrate ladder generation based on source analysis.
- [ ] Multi-lingual audio track support.
- [ ] Multi-CDN manifest generation.

---
