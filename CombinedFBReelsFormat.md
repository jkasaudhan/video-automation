To combine `clip1.mp4` (1080x1920) and `clip2.mp4` (with different dimensions) into a single 1080x1920 video using **MoviePy v2.0**, you can follow the steps below. This script ensures that `clip2.mp4` is resized to fit within the 1080x1920 frame while maintaining its aspect ratio.


```python
from moviepy import VideoFileClip, CompositeVideoClip
from moviepy.video.fx import Resize
from pathlib import Path

def combine_videos(main_video_path: str, overlay_video_path: str, output_path: str):
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

    # Create a composite video with the overlay on top of the main video
    final_clip = CompositeVideoClip([main_clip, positioned_overlay], size=(main_width, main_height))

    # Export the final video
    final_clip.write_videofile(output_path, codec="libx264", fps=main_clip.fps)

    # Close clips
    main_clip.close()
    overlay_clip.close()
    resized_overlay.close()
    final_clip.close()

if __name__ == "__main__":
    main_video = "clip1.mp4"
    overlay_video = "clip2.mp4"
    output_video = "combined_video.mp4"

    # Ensure input files exist
    if not Path(main_video).exists():
        raise FileNotFoundError(f"Main video {main_video} not found!")
    if not Path(overlay_video).exists():
        raise FileNotFoundError(f"Overlay video {overlay_video} not found!")

    combine_videos(main_video, overlay_video, output_video)
    print(f"Processed video saved as {output_video}")
```


**Explanation:**

1. **Loading Videos:** The script loads `clip1.mp4` as the main background video and `clip2.mp4` as the overlay.

2. **Calculating Scale Factor:** It computes the scale factor required to fit the overlay video within the main video's dimensions while preserving the overlay's aspect ratio.

3. **Resizing Overlay:** The overlay video is resized using the calculated scale factor.

4. **Positioning Overlay:** The resized overlay is centered over the main video.

5. **Compositing Videos:** Both videos are combined into a single composite video with the specified output dimensions.

6. **Exporting Final Video:** The composite video is exported using the H.264 codec.

This approach ensures that `clip2.mp4` fits within the 1080x1920 frame without distortion, maintaining its original aspect ratio. 
