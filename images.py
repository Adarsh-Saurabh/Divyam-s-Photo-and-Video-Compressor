# Register HEIF support BEFORE importing PIL
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_SUPPORT = True
except ImportError:
    HEIF_SUPPORT = False
    print("⚠️ Warning: 'pillow-heif' not installed. HEIC files will be skipped.")
    print("   Run: pip install pillow-heif")

from PIL import Image
from pathlib import Path

def compress_images_fixed_height(input_folder, output_folder, target_height=1500, quality=85):
    """
    Resize images to fixed height (e.g., 1500px), preserve aspect ratio & metadata.
    Supports HEIC if pillow-heif is installed.
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported formats (Pillow + HEIF)
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff', '.bmp', '.heic', '.heif'}

    for file in input_path.iterdir():
        if file.suffix.lower() not in image_extensions:
            continue

        print(f"🖼️ Processing: {file.name}")
        try:
            with Image.open(file) as img:
                w, h = img.size

                # Skip if already <= target height (optional: change if you always want 1500px)
                if h <= target_height:
                    new_img = img.copy()
                else:
                    # Resize to fixed height, proportional width
                    scale = target_height / h
                    new_w = int(w * scale)
                    new_h = target_height
                    # Ensure even dimensions (safe for codecs)
                    new_w = new_w if new_w % 2 == 0 else new_w + 1
                    new_img = img.resize((new_w, new_h), Image.LANCZOS)

                # Preserve EXIF (for JPEG/HEIC/TIFF)
                exif_data = None
                if file.suffix.lower() in {'.jpg', '.jpeg', '.heic', '.heif', '.tiff'}:
                    exif_data = img.info.get("exif")

                # Determine output format
                suffix = file.suffix.lower()
                output_file = output_path / file.name

                save_kwargs = {}
                if suffix in {'.jpg', '.jpeg'}:
                    save_kwargs = {"format": "JPEG", "quality": quality, "optimize": True}
                    if exif_data:
                        save_kwargs["exif"] = exif_data
                elif suffix in {'.heic', '.heif'}:
                    # Save as HEIC (requires pillow-heif)
                    save_kwargs = {"format": "HEIF", "quality": quality}
                    if exif_data:
                        save_kwargs["exif"] = exif_data
                elif suffix == '.png':
                    save_kwargs = {"format": "PNG", "optimize": True}
                elif suffix == '.webp':
                    save_kwargs = {"format": "WEBP", "quality": quality, "method": 6}
                else:
                    save_kwargs = {"format": new_img.format or "TIFF"}

                new_img.save(output_file, **save_kwargs)
                print(f"✅ Saved: {output_file.name}")

        except Exception as e:
            print(f"❌ Failed: {file.name} – {e}")

# === Usage ===
if __name__ == "__main__":
    INPUT_FOLDER = ""      # 👈 Change to your folder
    OUTPUT_FOLDER = "resized_1500px"

    compress_images_fixed_height(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        target_height=1500,
        quality=85  # For HEIC/JPEG/WebP
    )