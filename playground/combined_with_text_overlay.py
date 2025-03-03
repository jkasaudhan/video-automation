from moviepy import VideoFileClip, CompositeVideoClip, TextClip, ColorClip
from moviepy.video.fx import Resize
from pathlib import Path

def add_text_overlay(main_video_path: str, overlay_video_path: str, output_path: str, text: str):
    # Load the main video (assumed to be 1080x1920)
    main_clip = VideoFileClip(main_video_path)
    main_width, main_height = main_clip.size

    # Load the overlay video
    overlay_clip = VideoFileClip(overlay_video_path)
    overlay_width, overlay_height = overlay_clip.size

    # Calculate scaling factor to fit overlay within main video
    scale_factor = min(main_width / overlay_width, main_height / overlay_height)

    # Resize overlay while maintaining aspect ratio
    resized_overlay = overlay_clip.with_effects([Resize(scale_factor)])

    # Position the resized overlay at the center of the main video
    positioned_overlay = resized_overlay.with_position(("center", "center"))

    # Define text properties
    fontsize = 50
    text_color = 'white'
    font_path = font_path = "./vid_automation/Arial.ttf"  # Ensure this font is available on your system
    stroke_color = 'black'
    stroke_width = 2

    # Create the text clip
    text_clip = TextClip(
        text=text,
        font_size=fontsize,
        color=text_color,
        font=font_path,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        size=(int(main_width * 0.8), None),  # 80% of the main video width
        method='caption'
    )

    # Calculate text position (10% below the top)
    text_y_position = main_height * 0.15

    # Create a background for the text with padding
    padding = 10  # Padding in pixels
    text_background = ColorClip(
        size=(text_clip.w + 2 * padding, text_clip.h + 2 * padding),
        color=(0, 0, 0)  # Black background
    ).with_opacity(0.6)  # Semi-transparent background

    # Position the text on the background
    text_with_background = CompositeVideoClip(
        [text_background, text_clip.with_position((padding, padding))],
        size=text_background.size
    )

    # Position the text_with_background on the main video
    text_with_background = text_with_background.with_position(
        ('center', text_y_position)
    ).with_duration(main_clip.duration)

    # Create a composite video with the overlay and text
    final_clip = CompositeVideoClip(
        [main_clip, positioned_overlay, text_with_background],
        size=(main_width, main_height)
    )

    # Export the final video
    final_clip.write_videofile(output_path, codec="libx264", fps=main_clip.fps,  audio_codec="aac", preset="ultrafast")

    # Close clips
    main_clip.close()
    overlay_clip.close()
    resized_overlay.close()
    text_clip.close()
    text_background.close()
    text_with_background.close()
    final_clip.close()

if __name__ == "__main__":
    main_video = "./vid_automation/clips/start.mp4"
    overlay_video = "./vid_automation/clips/clip2.mp4"
    output_video = "./vid_automation/clips/combined_video_with_text.mp4"
    overlay_text = "How to start a company in Germany????"

    # Ensure input files exist
    if not Path(main_video).exists():
        raise FileNotFoundError(f"Main video {main_video} not found!")
    if not Path(overlay_video).exists():
        raise FileNotFoundError(f"Overlay video {overlay_video} not found!")

    add_text_overlay(main_video, overlay_video, output_video, overlay_text)
    print(f"Processed video saved as {output_video}")
