# Comparative Analysis: Legacy Lumberjack vs. Unified CMAF CBCS

## 📌 Executive Summary
This document provides a detailed technical comparison between the legacy **Lumberjack** transcoding workflow and the new **Unified CMAF CBCS** pipeline. By transitioning to a unified encryption scheme and a single-container format (CMAF), we have achieved a **~60.1% reduction in storage requirements** and significant compute optimizations.

---

## 📊 Side-by-Side Comparison

| Feature | Legacy (Lumberjack) | Unified CMAF (New POC) | Impact |
| :--- | :--- | :--- | :--- |
| **Encryption Scheme** | **Dual**: CENC (Widevine) & CBCS (FairPlay) | **Unified**: CBCS for both | ⬇️ Simplified Key Mgmt |
| **Media Containers** | **Separate**: DASH & HLS fMP4 files | **Single**: CMAF fMP4 for both | ⬇️ 50% Fewer Media Files |
| **Audio Strategy** | **Redundant**: Per-resolution & Separate DASH/HLS files | **Shared**: Single high-quality AAC track | 📉 **~90% Redundancy Cut** |
| **DRM Packaging Workflow** | **Double**: Separate DASH (CENC) & HLS (CBCS) runs | **Single**: Unified HLS + DASH run | 📉 **50% Time Saving** |
| **Storage Footprint** | ~58.63 MB (Sample Case) | ~23.36 MB (Sample Case) | 📉 **60.1% Reduction** |

---

## 🔍 Deep Dive Analysis

### 1. Storage Efficiency & Cost
In the legacy Lumberjack flow, the system had to store two entirely different encrypted versions of the same content to satisfy both DRM systems:
-   **Widevine (CENC)** was required for Android/Desktop.
-   **FairPlay (CBCS)** was required for Apple devices.

**By the numbers (Sample Case):**
-   **Lumberjack Storage**: 58.63 MB
-   **Unified CMAF Storage**: 23.36 MB
-   **Net Savings**: 35.27 MB (**~60.1%**)

This translates directly to a **60% reduction in S3/Minio storage costs** and, more importantly, a **60% reduction in CDN egress costs**, as only one version of the segments needs to be cached and delivered.

### 2. Audio Optimization
Lumberjack historically generated audio files for *every* resolution and for *both* DASH and HLS manifests separately. Even if the audio data was identical, it was duplicated in storage:
-   **Old Approach**: 5 resolutions × 2 manifests = 10 sets of audio files.
-   **The New Approach**: Extract **one shared audio track**.
-   **Improvement**: Removes **90% of redundant audio data**, further lowering storage and origin egress.

### 3. Compute & Turnaround Time (Hetzner)
Transcoding on Hetzner servers involves significant compute time per resolution.
-   **Lumberjack**: Required two separate packaging **runs** after transcoding to generate the different encryption schemes.
-   **Unified CMAF**: Packaging is now a **single unified run**.
-   **Efficiency Gain**: **50% reduction in packaging cycle time**. Since we only generate one set of encrypted segments, the overall time a server instance needs to be active is significantly reduced, lowering the total compute cost per job.

---

## 💡 Conclusion
The transition from Lumberjack to the Unified CMAF CBCS pipeline is a major step forward in efficiency. By aligning with modern DRM standards (where both Widevine and FairPlay support CBCS), we have eliminated redundant media assets, halved our storage footprint, and streamlined our compute workflow.

> [!TIP]
> This unified approach also simplifies **CDN Purging** and **Cache invalidation**, as there is only one "Source of Truth" for the encrypted segments.

---
