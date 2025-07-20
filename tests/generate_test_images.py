#!/usr/bin/env python3
"""
Generate Test Images

Creates simple test images for testing the image description system.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_test_image(filename: str, size: tuple = (400, 300), color: str = "blue", text: str = "Test Image"):
    """Create a simple test image with text"""
    # Create image with solid color background
    img = Image.new('RGB', size, color=color)
    
    # Add text to the image
    draw = ImageDraw.Draw(img)
    
    # Try to use a larger font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Get text size and center it
    if font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    else:
        # Approximate text size for default font
        text_width = len(text) * 6
        text_height = 11
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill="white", font=font)
    
    return img

def generate_test_images(output_dir: Path):
    """Generate a variety of test images"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    test_images = [
        ("red_square.jpg", (300, 300), "red", "Red Square"),
        ("blue_landscape.jpg", (600, 400), "blue", "Blue Landscape"),
        ("green_circle.png", (400, 400), "green", "Green Circle"),
        ("yellow_banner.jpg", (800, 200), "yellow", "Yellow Banner"),
        ("purple_portrait.png", (300, 400), "purple", "Purple Portrait"),
    ]
    
    created_files = []
    
    for filename, size, color, text in test_images:
        img = create_test_image(filename, size, color, text)
        
        # For circle image, add a circle
        if "circle" in filename.lower():
            draw = ImageDraw.Draw(img)
            center_x, center_y = size[0] // 2, size[1] // 2
            radius = min(size) // 3
            draw.ellipse(
                [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                fill="darkgreen", outline="white", width=3
            )
        
        filepath = output_dir / filename
        img.save(filepath, quality=95)
        created_files.append(filepath)
        print(f"Created: {filepath}")
    
    return created_files

if __name__ == "__main__":
    # Generate test images
    script_dir = Path(__file__).parent
    test_images_dir = script_dir / "test_files" / "images"
    
    print("Generating test images...")
    files = generate_test_images(test_images_dir)
    print(f"\nGenerated {len(files)} test images in {test_images_dir}")
