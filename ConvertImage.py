#!/usr/bin/env python3
"""
HEIC to JPG Converter

This script converts HEIC/HEIF image files to JPG format.
Supports both individual files and batch conversion of directories.
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIF opener with PIL
pillow_heif.register_heif_opener()


def convert_heic_to_jpg(input_path, output_path=None, quality=95, keep_metadata=True):
    """
    Convert a single HEIC file to JPG format.
    
    Args:
        input_path: Path to the input HEIC file
        output_path: Path for the output JPG file (optional)
        quality: JPEG quality (1-100, default 95)
        keep_metadata: Whether to preserve metadata (default True)
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        input_path = Path(input_path)
        
        # Generate output path if not provided
        if output_path is None:
            output_path = input_path.with_suffix('.jpg')
        else:
            output_path = Path(output_path)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Open and convert the image
        with Image.open(input_path) as image:
            # Convert to RGB if necessary (HEIC can have different color modes)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save as JPEG with specified quality
            save_kwargs = {
                'format': 'JPEG',
                'quality': quality,
                'optimize': True
            }
            
            # Preserve metadata if requested
            if keep_metadata and hasattr(image, 'info'):
                save_kwargs['exif'] = image.info.get('exif', b'')
            
            image.save(output_path, **save_kwargs)
        
        print(f"✅ Converted: {input_path.name} -> {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to convert {input_path}: {e}")
        return False


def convert_directory(directory_path, output_directory=None, recursive=False, quality=95, keep_metadata=True):
    """
    Convert all HEIC files in a directory to JPG format.
    
    Args:
        directory_path: Path to the directory containing HEIC files
        output_directory: Output directory (default: creates 'converted' subdirectory)
        recursive: Whether to process subdirectories recursively
        quality: JPEG quality (1-100, default 95)
        keep_metadata: Whether to preserve metadata (default True)
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    directory_path = Path(directory_path)
    
    if not directory_path.exists():
        print(f"❌ Directory does not exist: {directory_path}")
        return 0, 0
    
    if not directory_path.is_dir():
        print(f"❌ Path is not a directory: {directory_path}")
        return 0, 0
    
    # Set up output directory
    if output_directory is None:
        output_directory = directory_path / "converted"
    else:
        output_directory = Path(output_directory)
    
    output_directory.mkdir(parents=True, exist_ok=True)
    
    # Find HEIC files
    pattern = "**/*.heic" if recursive else "*.heic"
    heic_files = list(directory_path.glob(pattern))
    
    # Also check for .HEIF extension
    heif_pattern = "**/*.heif" if recursive else "*.heif"
    heic_files.extend(directory_path.glob(heif_pattern))
    
    if not heic_files:
        print(f"📁 No HEIC/HEIF files found in {directory_path}")
        return 0, 0
    
    print(f"🔍 Found {len(heic_files)} HEIC/HEIF files to convert")
    
    successful = 0
    failed = 0
    
    for heic_file in heic_files:
        # Preserve directory structure in output
        if recursive:
            relative_path = heic_file.relative_to(directory_path)
            output_file = output_directory / relative_path.with_suffix('.jpg')
        else:
            output_file = output_directory / heic_file.with_suffix('.jpg').name
        
        if convert_heic_to_jpg(heic_file, output_file, quality, keep_metadata):
            successful += 1
        else:
            failed += 1
    
    print(f"\n📊 Conversion complete:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Output directory: {output_directory}")
    
    return successful, failed


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Convert HEIC/HEIF images to JPG format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ConvertImage.py photos/                    # Convert all HEIC files in photos/
  python ConvertImage.py photos/ --recursive        # Include subdirectories
  python ConvertImage.py photo.heic                 # Convert single file
  python ConvertImage.py photos/ --quality 85       # Lower quality, smaller files
  python ConvertImage.py photos/ --output converted/ # Custom output directory
        """
    )
    
    parser.add_argument(
        "input",
        help="Input HEIC file or directory containing HEIC files"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file or directory (default: creates 'converted' subdirectory for directories)"
    )
    
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Process subdirectories recursively"
    )
    
    parser.add_argument(
        "--quality", "-q",
        type=int,
        default=95,
        choices=range(1, 101),
        metavar="1-100",
        help="JPEG quality (1-100, default: 95)"
    )
    
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Don't preserve metadata in converted files"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ Input path does not exist: {input_path}")
        sys.exit(1)
    
    # Check if pillow-heif is properly installed
    try:
        # Test if HEIF support is available
        test_formats = Image.registered_extensions()
        if '.heic' not in test_formats and '.heif' not in test_formats:
            print("⚠️  Warning: HEIF support may not be properly registered")
    except Exception as e:
        print(f"⚠️  Warning: Issue with HEIF support: {e}")
    
    if input_path.is_file():
        # Convert single file
        if not input_path.suffix.lower() in ['.heic', '.heif']:
            print(f"❌ File is not a HEIC/HEIF file: {input_path}")
            sys.exit(1)
        
        output_file = args.output
        if output_file and Path(output_file).is_dir():
            output_file = Path(output_file) / input_path.with_suffix('.jpg').name
        
        success = convert_heic_to_jpg(
            input_path, 
            output_file, 
            args.quality, 
            not args.no_metadata
        )
        
        sys.exit(0 if success else 1)
    
    elif input_path.is_dir():
        # Convert directory
        successful, failed = convert_directory(
            input_path,
            args.output,
            args.recursive,
            args.quality,
            not args.no_metadata
        )
        
        sys.exit(0 if failed == 0 else 1)
    
    else:
        print(f"❌ Invalid input path: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
