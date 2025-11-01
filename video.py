import subprocess
from pathlib import Path

def compress_videos_hevc_720p(input_folder, output_folder, quality_preset='p4', bitrate='1.5M'):
    """
    Compress videos to 720p using HEVC (H.265) via NVIDIA NVENC.
    
    Args:
        input_folder (str): Input directory with videos.
        output_folder (str): Output directory for compressed videos.
        quality_preset (str): NVENC preset (p1=fastest, p7=best quality). p4 is balanced.
        bitrate (str): Target video bitrate (e.g., '1.2M', '1.5M', '2M').
                      HEVC typically needs ~30–50% less bitrate than H.264 for same quality.
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    video_extensions = {'.mp4', '.mkv', '.mov', '.avi', '.webm', '.flv', '.wmv'}

    for file in input_path.iterdir():
        if file.suffix.lower() not in video_extensions:
            continue

        output_file = output_path / file.name
        print(f"🚀 Compressing (HEVC GPU): {file.name} ...")

        cmd = [
            'ffmpeg',
            '-hwaccel', 'cuda',               # Enable GPU decoding
            '-i', str(file),
            '-vf', 'scale=-2:720',            # Scale to 720p, preserve aspect ratio
            '-c:v', 'hevc_nvenc',
            '-preset', quality_preset,
            '-b:v', bitrate,
            '-maxrate', bitrate,
            '-bufsize', '3M',
            '-profile:v', 'main',             # Main profile for broad HEVC support
            '-c:a', 'aac',
            '-b:a', '128k',
            '-map_metadata', '0',             # Preserve all metadata
            '-y',
            str(output_file)
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"✅ Done: {file.name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {file.name} – {e}")

# === Usage ===
if __name__ == "__main__":
    INPUT_FOLDER = ""        # 👈 Change to your source folder
    OUTPUT_FOLDER = "compressed_720p_hevc"

    # Recommended for 720p HEVC on RTX 3050:
    # - Bitrate: 1.2M–1.8M (1.5M is a sweet spot)
    # - Preset: p4 (balanced), p5 (slightly better compression)
    compress_videos_hevc_720p(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        quality_preset='p5',
        bitrate='2M'
    )