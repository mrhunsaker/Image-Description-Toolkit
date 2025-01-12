import os
from PIL import Image
import pillow_heif  # Use pillow-heif for HEIC file handling

def convert_heic_to_jpg(directory_path):
    """
    Convert .heic files in the directory_path to .jpg files.
    """
    output_directory = os.path.join(directory_path, "converted")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".heic"):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".jpg")

            try:
                # Open .heic file using pillow-heif
                heif_image = pillow_heif.open_heif(input_path)

                # Convert to PIL image
                image = Image.frombytes(
                    heif_image.mode,
                    heif_image.size,
                    heif_image.data
                )

                # Save as .jpg
                image.save(output_path, "JPEG")
                print(f"Converted: {input_path} -> {output_path}")
            except Exception as e:
                print(f"Failed to convert {input_path}: {e}")

def main():
    directory_path = r"C:\users\kelly\playground\images"  # Same directory as the earlier script
    convert_heic_to_jpg(directory_path)

if __name__ == "__main__":
    main()
