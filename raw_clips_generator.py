import os
from typing import List, Dict
from moviepy import VideoFileClip
import json

def split_video(
    main_video_path: str,
    clips_config: List[Dict[str, str]],
    output_folder: str
) -> None:
    """
    Split a main video into smaller clips based on provided configurations.

    Args:
    main_video_path (str): Path to the main video file.
    clips_config (List[Dict[str, str]]): List of clip configurations.
    output_folder (str): Destination folder for output clips.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load the main video
    with VideoFileClip(main_video_path) as video:
        for clip_config in clips_config:
            start_time = float(clip_config['start_time'])
            end_time = float(clip_config['end_time'])
            clip_name = clip_config['name']

            # Extract the subclip
            subclip = video.subclipped(start_time, end_time)

            # Generate output path
            output_path = os.path.join(output_folder, f"{clip_name}.mp4")

            # Write the subclip to file
            subclip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            print(f"Clip '{clip_name}' created successfully.")

# Function to read JSON config file
def load_config(file_path):
    """Loads configuration from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
        return None
    
# Example usage
# if __name__ == "__main__":
#    main_video = "./vid_automation/clips/original.mov"
#    output_folder = "./vid_automation/clips"
#    config = load_config('./vid_automation/video1/config.json')
#    clips_config = config.get('clips_config')

#    split_video(config.get("main_video_path"), clips_config, config.get('output_folder'))

