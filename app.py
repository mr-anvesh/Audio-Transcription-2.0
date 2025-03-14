import streamlit as st
import whisper
import tempfile
import os
import moviepy.editor as mp
import datetime
import pysrt
import webvtt
from pathlib import Path
import subprocess

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def extract_audio_from_video(video_path):
    """Extract audio from video file"""
    if not check_ffmpeg():
        raise RuntimeError(
            "FFmpeg is not installed. Please check the README for installation instructions. "
            "If you're using Streamlit Cloud, make sure packages.txt contains 'ffmpeg'."
        )
    
    with st.spinner("Extracting audio from video..."):
        try:
            video = mp.VideoFileClip(video_path)
            audio_path = video_path + ".wav"
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            video.close()
            return audio_path
        except Exception as e:
            raise RuntimeError(f"Error extracting audio: {str(e)}")

def create_subtitle_timestamps(segments):
    """Create subtitles with proper timestamps"""
    subs = []
    for i, segment in enumerate(segments, 1):
        start = datetime.timedelta(seconds=segment['start'])
        end = datetime.timedelta(seconds=segment['end'])
        text = segment['text'].strip()
        subs.append({
            'index': i,
            'start': str(start).replace('.', ',')[:11],
            'end': str(end).replace('.', ',')[:11],
            'text': text
        })
    return subs

def generate_srt_content(subtitles):
    """Generate SRT format content"""
    srt_content = ""
    for sub in subtitles:
        srt_content += f"{sub['index']}\n"
        srt_content += f"{sub['start']} --> {sub['end']}\n"
        srt_content += f"{sub['text']}\n\n"
    return srt_content

def generate_vtt_content(subtitles):
    """Generate VTT format content"""
    vtt_content = "WEBVTT\n\n"
    for sub in subtitles:
        vtt_content += f"{sub['start']} --> {sub['end']}\n"
        vtt_content += f"{sub['text']}\n\n"
    return vtt_content

# Set page configuration
st.set_page_config(
    page_title="Audio/Video Transcription with Whisper",
    page_icon="🎙️",
    layout="wide"
)

# Title and description
st.title("🎙️ Audio/Video Transcription with Whisper")
st.markdown("""
This application transcribes audio/video files into text and generates subtitles in multiple formats.
Upload a file and select the Whisper model you want to use for transcription.
""")

# Check FFmpeg availability
if not check_ffmpeg():
    st.warning("""
    ⚠️ FFmpeg is not installed. Video file processing will not work.
    
    Please check the [README](https://github.com/yourusername/audio-transcription-whisper#prerequisites) for installation instructions.
    If you're using Streamlit Cloud, please ensure `packages.txt` contains `ffmpeg`.
    """)

# Available Whisper models
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]

# Sidebar for model selection
with st.sidebar:
    st.header("Model Configuration")
    selected_model = st.selectbox(
        "Select Whisper Model",
        WHISPER_MODELS,
        help="Choose the Whisper model to use for transcription. Larger models are more accurate but slower."
    )
    
    st.markdown("""
    ### Model Information
    - **tiny**: Fastest, least accurate
    - **base**: Fast, reasonable accuracy
    - **small**: Good balance of speed and accuracy
    - **medium**: More accurate, slower
    - **large**: Most accurate, slowest
    """)

# File upload - now supporting more formats
file = st.file_uploader(
    "Upload an audio/video file",
    type=["wav", "mp3", "m4a", "ogg", "mp4", "avi", "mkv", "mov"]
)

if file is not None:
    # Center the transcribe button using columns
    left_col, center_col, right_col = st.columns([3,1,3])
    with center_col:
        transcribe_button = st.button("Transcribe", type="primary", use_container_width=True)
    
    if transcribe_button:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            # Handle video files
            if tmp_file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                if not check_ffmpeg():
                    st.error("Cannot process video files without FFmpeg. Please upload an audio file instead.")
                    st.stop()
                audio_path = extract_audio_from_video(tmp_file_path)
                process_path = audio_path
            else:
                process_path = tmp_file_path

            with st.spinner(f"Loading {selected_model} model..."):
                model = whisper.load_model(selected_model)

            with st.spinner("Transcribing..."):
                # Perform transcription with word-level timestamps
                result = model.transcribe(process_path, word_timestamps=True)
                
                # Create subtitles with timestamps
                subtitles = create_subtitle_timestamps(result["segments"])
                
                # Display results
                st.success("Transcription completed!")
                
                # Create tabs for different views
                transcript_tab, subtitles_tab, edit_tab = st.tabs(["Full Transcript", "Subtitles View", "Edit Subtitles"])
                
                with transcript_tab:
                    st.subheader("Full Transcript:")
                    st.write(result["text"])
                    
                    # Download full transcript
                    st.download_button(
                        label="Download Full Transcript",
                        data=result["text"],
                        file_name="transcript.txt",
                        mime="text/plain"
                    )
                
                with subtitles_tab:
                    st.subheader("Subtitles:")
                    # Display subtitles with timestamps
                    for sub in subtitles:
                        st.markdown(f"**[{sub['start']} --> {sub['end']}]**  \n{sub['text']}")
                    
                    # Generate different subtitle formats
                    srt_content = generate_srt_content(subtitles)
                    vtt_content = generate_vtt_content(subtitles)
                    
                    # Download buttons for different formats
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download SRT",
                            data=srt_content,
                            file_name="subtitles.srt",
                            mime="text/plain"
                        )
                    with col2:
                        st.download_button(
                            label="Download VTT",
                            data=vtt_content,
                            file_name="subtitles.vtt",
                            mime="text/plain"
                        )
                
                with edit_tab:
                    st.subheader("Edit Subtitles:")
                    st.markdown("Edit the subtitles below. Each subtitle should be in the format: `[start] --> [end]` followed by the text.")
                    
                    # Create a text area with the current subtitles for editing
                    edited_subtitles = st.text_area(
                        "Edit subtitles",
                        value=srt_content,
                        height=400
                    )
                    
                    # Download edited subtitles
                    if st.button("Update Subtitles"):
                        st.download_button(
                            label="Download Edited SRT",
                            data=edited_subtitles,
                            file_name="edited_subtitles.srt",
                            mime="text/plain"
                        )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if "FFmpeg" in str(e):
                st.info("💡 For video files, FFmpeg is required. Please check the installation instructions in the README.")
        
        finally:
            # Clean up temporary files
            os.unlink(tmp_file_path)
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.unlink(audio_path)
    else:
        st.info("Press the Transcribe button when you're ready to start the transcription.")
else:
    st.info("Please upload an audio or video file to begin transcription.")
