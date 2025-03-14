# Audio/Video Transcription using Whisper

This application provides a web interface for transcribing audio and video files using OpenAI's Whisper model. It features a user-friendly interface built with Streamlit that allows users to select different Whisper models, upload files for transcription, and generate subtitles in multiple formats.

## ⚠️ Important: FFmpeg Requirement

This application requires FFmpeg for processing video files. Audio files can be processed without FFmpeg.

### Local Installation
Install FFmpeg based on your operating system:

- **Windows**:
  ```bash
  # Using Chocolatey
  choco install ffmpeg

  # Or download the FFmpeg build from https://www.gyan.dev/ffmpeg/builds/ 
  # and add it to your system PATH
  ```
- **macOS**:
  ```bash
  brew install ffmpeg
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

### Streamlit Cloud Deployment
If deploying to Streamlit Cloud:
1. Create a file named `packages.txt` in your repository root
2. Add the following content:
   ```
   ffmpeg
   ```
This will ensure FFmpeg is installed in the Streamlit Cloud environment.

## Features

- Support for multiple audio/video formats:
  - Audio: WAV, MP3, M4A, OGG
  - Video: MP4, AVI, MKV, MOV (requires FFmpeg)
- Automatic audio extraction from video files
- Choice of different Whisper models (tiny, base, small, medium, large)
- Real-time transcription with progress indicators
- Multiple output formats:
  - Full transcript (TXT)
  - Subtitles (SRT, VTT)
- Interactive subtitle editor
- User-friendly interface with model information
- Timestamp-accurate subtitles

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd audio-transcription-whisper
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Ensure FFmpeg is installed (see FFmpeg Requirement section above)

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Select your preferred Whisper model from the sidebar

4. Upload an audio or video file using the file uploader
   - For video files, ensure FFmpeg is installed
   - Audio files can be processed without FFmpeg

5. Wait for the transcription to complete

6. Use the different tabs to:
   - View the full transcript
   - View and download subtitles in different formats
   - Edit subtitles before downloading

## Model Information

- **tiny**: Fastest but least accurate model
- **base**: Good balance of speed and accuracy for simple transcriptions
- **small**: Better accuracy than base, still relatively fast
- **medium**: High accuracy, slower processing
- **large**: Most accurate, slowest processing

## Requirements

- Python 3.7+
- FFmpeg (for video processing)
- Python packages (installed via requirements.txt):
  - streamlit
  - openai-whisper
  - torch
  - torchaudio
  - numpy
  - moviepy
  - pysrt
  - webvtt-py
  - ffmpeg-python

## Note

- The first time you use a specific model, it will be downloaded automatically. Larger models require more time to download and more system resources to run.
- Video processing requires FFmpeg and additional time for audio extraction before transcription begins.
- For best results with video files, ensure they have clear audio tracks.
- When deploying to Streamlit Cloud, ensure you have included the `packages.txt` file with FFmpeg. 