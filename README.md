# multi-channel-video-analyze

> **Multi-channel Video Analysis: Object Detection and OCR for Video Processing with Audio Synchronization**  
> SukoJim ✉️  
> _GitHub 2024._

The `multi-channel-video-analyze` project leverages YOLOv9 for detecting Regions of Interest (ROI) in videos where code snippets appear, performs OCR to extract text from these regions, and synchronizes the extracted text with corresponding audio segments. This combined approach enables detailed indexing and analysis of code and related speech within video frames.

<p align="center" width="100%">
<a target="_blank"><img src="src/assets/wave.gif" alt="multi-channel-video-analyze" style="width: 80%; min-width: 200px; display: block; margin: auto;"></a>
</p>

<h5 align="center"> If you like our project, please give us a star ⭐ on GitHub for the latest updates.</h5>

## :fire: News
* **[2024.5.15]** 🎉  `multi-channel-video-analyze`.

## ✨ Features

- Utilizes YOLOv9 for object detection to identify and crop Regions of Interest (ROI) where code appears in video frames.
- Performs OCR on cropped regions to extract text using Tesseract.
- Integrates with speech-to-text models to synchronize extracted text with corresponding audio segments.
- Indexes extracted text and audio for efficient retrieval and analysis.

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- Tesseract OCR
- FFMPEG (for audio processing)
- CUDA-enabled GPU (optional, for faster processing with YOLOv9 and speech-to-text models)

### Python Dependencies

Install the required Python packages using pip:

```bash
pip install -m requirments.txt
```
