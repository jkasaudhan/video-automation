import os
import time
import streamlit as st
from typing import List, Set
from raw_clips_generator import load_config, split_video
import sys
from io import StringIO
from streamlit_output_capturer import StreamlitOutputCapturer

# Constants
VIDEO_ROOT = "videos"
FINAL_DIR = "final"
CONFIG_FILE = "config.json"

def initialize_session() -> None:
    """Initialize session state variables"""
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "videos_available" not in st.session_state:
        st.session_state.videos_available = False

def get_video_directories() -> Set[str]:
    """Get available video directories with validation"""
    try:
        return {d for d in os.listdir(VIDEO_ROOT) if os.path.isdir(os.path.join(VIDEO_ROOT, d))}
    except FileNotFoundError:
        st.error(f"Video directory not found: {VIDEO_ROOT}")
        return set()

def render_sidebar() -> str:
    """Render sidebar controls and return selected folder"""
    with st.sidebar:
        st.header("⚙️ Video Processing Settings")
        selected_folder = st.selectbox(
            label="📁 Select Video Folder",
            options=sorted(get_video_directories()),
            help="Select folder containing source videos and configuration"
        )
        
        st.caption(f"""
        **Folder Requirements:**
        - Must contain {CONFIG_FILE} with clip configurations
        - Should include source video for clip generation
        - Output will be saved in {FINAL_DIR} subdirectory
        """)

        st.divider()
        if st.button("🎬 Generate Raw Clips"):
            st.session_state.processing = True
            st.session_state.selected_folder = selected_folder
        
        if st.button("🎬 Show Raw Clips"):
            st.session_state.processing = False
            st.session_state.videos_available = True
            st.session_state.selected_folder = selected_folder
               

        if st.button("🔄 Resize & Mix Videos", on_click=process_start):
            pass
        if st.button("📤 Upload to YouTube", on_click=process_start):
            pass
        if st.button("📱 Upload to Facebook", on_click=process_start):
            pass

        st.divider()
        st.markdown('<div style="text-align: center">Project By Nepali Roots</div>', 
                   unsafe_allow_html=True)
    
    return selected_folder

def process_start() -> None:
    """Handle processing initialization"""
    st.session_state.processing = True
    st.session_state.videos_available = False

def display_videos(videos_dir) -> None:
    """Display processed videos in main content area"""
    st.header("🎥 Processed Videos")
    final_path = os.path.join(videos_dir)
    
    if not os.path.exists(final_path):
        st.warning("No processed videos found")
        return

    video_files = [f for f in os.listdir(final_path) if f.endswith((".mp4", ".mov"))]
    if not video_files:
        st.info("No videos available in final directory")
        return

    cols = st.columns(2)
    for idx, video_file in enumerate(video_files):
        with cols[idx % 2]:
            st.video(os.path.join(final_path, video_file))
            st.caption(video_file)

def generate_raw_clips(selected_folder, log_placeholder, spinner_placeholder):
    """Process videos with real-time logging"""
    config = load_config(f"./{VIDEO_ROOT}/{selected_folder}/config.json")
    output_folder = config.get('output_folder')
    
    output_capturer = StreamlitOutputCapturer(log_placeholder)
    
    try:
        sys.stdout = output_capturer
        with st.spinner("Processing videos...", show_time=True):
            split_video(
                config.get("main_video_path"),
                config.get("clips_config"),
                output_folder
            )
        st.success("✅ Clip generation completed!")
        st.session_state.videos_available = True
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout
        st.session_state.processing = False

def main() -> None:
    """Main application layout"""
    st.set_page_config(
        page_title="Video Automation Studio",
        page_icon="🎞️",
        layout="wide"
    )
    initialize_session()
    
    st.title("🎬 Video Automation Studio")
    selected_folder = render_sidebar()

    # Main content area
    main_container = st.container()
    
    with main_container:
        if st.session_state.processing:
            log_placeholder = st.empty()
            spinner_placeholder = st.empty()
            generate_raw_clips(st.session_state.selected_folder, log_placeholder, spinner_placeholder)
        elif st.session_state.videos_available:
            display_videos(os.path.join(VIDEO_ROOT, selected_folder, "raw_clips"))
        else:
            st.info("👋 Select a folder and start processing to see results")

if __name__ == "__main__":
    main()
