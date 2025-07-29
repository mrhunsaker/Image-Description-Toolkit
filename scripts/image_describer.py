#!/usr/bin/env python3
"""
ImageDescriber - AI-Powered Image Analysis Tool

This script processes directories of image files using Ollama's vision models
to generate detailed descriptions and extract metadata. Features include:

- AI-powered image descriptions using various Ollama vision models
- EXIF metadata extraction (camera settings, GPS, timestamps)
- Configurable prompt styles for different analysis needs
- Memory optimization for processing large image collections
- Comprehensive text file output with metadata integration
- Support for multiple image formats (JPG, PNG, BMP, TIFF, WebP)

The tool outputs descriptions to text files with comprehensive metadata
including camera settings, GPS coordinates, timestamps, and AI-generated
descriptions using configurable prompt styles.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
import base64
import json
import gc
import time
from datetime import datetime

import ollama
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


# Configure basic logging (will be enhanced in main() if log-dir is provided)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_logging(log_dir: Optional[str] = None, verbose: bool = False) -> None:
    """
    Set up logging configuration for the image describer.

    Parameters
    ----------
    log_dir : str or None, optional
        Directory to write log files to. If None, only console logging is used.
    verbose : bool, optional
        If True, enables debug logging. Otherwise, info level.

    Returns
    -------
    None

    Notes
    -----
    Configures both console and file logging if log_dir is provided.
    """
    global logger

    # Clear existing handlers
    logger.handlers.clear()

    # Set logging level
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if log_dir is provided
    if log_dir:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_filename = log_path / f"image_describer_{timestamp}.log"

        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info(f"Image describer log file: {log_filename.absolute()}")


class ImageDescriber:
    """Class to handle image description using Ollama vision model"""

    def __init__(self, model_name: str = None, max_image_size: int = 1024,
                 enable_compression: bool = True, batch_delay: float = 2.0,
                 config_file: str = "image_describer_config.json", prompt_style: str = "detailed",
                 output_dir: str = None):
        """
        Initialize the ImageDescriber

        Args:
            model_name: Name of the Ollama vision model to use (overrides config if specified)
            max_image_size: Maximum image dimension (width or height) in pixels
            enable_compression: Whether to compress images before processing
            batch_delay: Delay between processing images to prevent memory buildup
            config_file: Path to the JSON configuration file
            prompt_style: Style of prompt to use (detailed, concise, artistic, technical)
            output_dir: Custom output directory (default: same as input directory)
        """
        # Load configuration first
        self.config = self.load_config(config_file)

        # Set model name - use parameter if provided, otherwise use config, otherwise default
        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = self.config.get('model_settings', {}).get('model', 'moondream')

        self.max_image_size = max_image_size
        self.enable_compression = enable_compression
        self.batch_delay = batch_delay
        self.prompt_style = prompt_style
        self.output_dir = output_dir  # Custom output directory

        # Set supported formats from config
        self.supported_formats = set(self.config.get('processing_options', {}).get('supported_formats',
                                                    ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']))

    def load_config(self, config_file: str) -> dict:
        """
        Load configuration from JSON file

        Args:
            config_file: Path to the JSON configuration file

        Returns:
            Dictionary with configuration settings
        """
        try:
            config_path = Path(config_file)
            if not config_path.is_absolute():
                # Look for config file in script directory
                script_dir = Path(__file__).parent
                config_path = script_dir / config_file

            if not config_path.exists():
                logger.warning(f"Config file not found: {config_path}")
                return self.get_default_config()

            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            logger.info(f"Loaded configuration from: {config_path}")
            return config

        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            logger.info("Using default configuration")
            return self.get_default_config()

    def get_default_config(self) -> dict:
        """
        Get default configuration if config file is not available

        Returns:
            Dictionary with default configuration settings
        """
        return {
            "model_settings": {
                "model": "moondream",
                "temperature": 0.1,
                "num_predict": 600,
                "top_k": 40,
                "top_p": 0.9
            },
            "prompt_template": "Describe this image in detail, including:\n- Main subjects/objects\n- Setting/environment\n- Key colors and lighting\n- Notable activities or composition\nKeep it comprehensive and informative for metadata.",
            "default_prompt_style": "detailed",
            "prompt_variations": {
              "detailed": "Describe this image in detail, including:\n- Main subjects/objects\n- Setting/environment\n- Key colors and lighting\n- Notable activities or composition\nKeep it comprehensive and informative for metadata.",
              "concise": "Describe this image concisely, including:\n- Main subjects/objects\n- Setting/environment\n- Key colors and lighting\n- Notable activities or composition.",
              "Narrative": "Provide a narrative description including objects, colors and detail. Avoid interpretation, just describe.",
              "artistic": "Analyze this image from an artistic perspective, describing:\n- Visual composition and framing\n- Color palette and lighting mood\n- Artistic style or technique\n- Emotional tone or atmosphere\n- Subject matter and symbolism",
              "technical": "Provide a technical analysis of this image:\n- Camera settings and photographic technique\n- Lighting conditions and quality\n- Composition and framing\n- Image quality and clarity\n- Technical strengths or weaknesses",
              "colorful": "Give me a rich, vivid description emphasizing colors, lighting, and visual atmosphere. Focus on the palette, color relationships, and how colors contribute to the mood and composition.",
              "poet_basic": "Describe the image in a way that is objective, clear, and useful for someone who cannot see it. Focus on:\n- Main objects and their relationships\n- Spatial layout and positioning\n- Key colors and lighting\n- Text or symbols present\n- Avoid interpretation, emotion, or speculation.",
              "poet_extended": "Provide a comprehensive, objective description following POET guidelines:\n- List all significant objects, people, and text\n- Describe spatial relationships and arrangement\n- Note colors, lighting, and visual style\n- Include any visible actions or interactions\n- Avoid personal opinions, emotional tone, or artistic interpretation.",
              "poet_contextual": "Describe the image with context for accessibility:\n- Identify main elements and their arrangement\n- Mention any visible text, labels, or symbols\n- Note colors, lighting, and style\n- If relevant, describe the setting or environment\n- Do not interpret, speculate, or add emotion.",
              "poet_structured": "Produce a structured description for accessibility:\n1. Overview of the image\n2. List of main objects and their positions\n3. Description of colors and lighting\n4. Any visible text or symbols\n5. Notable actions or interactions\nAvoid interpretation and keep language factual."
            },
            "output_format": {
                "include_timestamp": True,
                "include_model_info": True,
                "include_file_path": True,
                "include_metadata": True,
                "separator": "-"
            },
            "processing_options": {
                "default_max_image_size": 1024,
                "default_batch_delay": 2.0,
                "default_compression": True,
                "extract_metadata": True,
                "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
            }
        }

    def get_prompt(self) -> str:
        """
        Get the prompt based on the selected style

        Returns:
            Prompt string
        """
        prompt_variations = self.config.get('prompt_variations', {})

        if self.prompt_style in prompt_variations:
            return prompt_variations[self.prompt_style]
        else:
            # Fallback to default prompt_template
            return self.config.get('prompt_template',
                                 "Describe this image in detail, including the main subjects, setting, colors, and composition.")

    def get_model_settings(self) -> dict:
        """
        Get model settings from configuration (excluding model name)

        Returns:
            Dictionary with model settings for ollama API call
        """
        model_settings = self.config.get('model_settings', {
            "temperature": 0.1,
            "num_predict": 400
        })

        # Remove model name from settings as it's passed separately to ollama
        settings = model_settings.copy()
        settings.pop('model', None)

        return settings

    def is_supported_image(self, file_path: Path) -> bool:
        """
        Check if the file is a supported image format.

        Parameters
        ----------
        file_path : Path
            Path to the image file.

        Returns
        -------
        bool
            True if supported, False otherwise.
        """
        return file_path.suffix.lower() in self.supported_formats

    def optimize_image(self, image_path: Path) -> Optional[bytes]:
        """
        Optimize image for processing by resizing and compressing

        Args:
            image_path: Path to the image file

        Returns:
            Optimized image bytes or None if failed
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                # Resize if too large
                if self.enable_compression and (img.width > self.max_image_size or img.height > self.max_image_size):
                    img.thumbnail((self.max_image_size, self.max_image_size), Image.Resampling.LANCZOS)
                    logger.info(f"Resized image {image_path.name} to {img.width}x{img.height}")

                # Save to bytes with compression
                import io
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85, optimize=True)
                return buffer.getvalue()

        except Exception as e:
            logger.error(f"Error optimizing image {image_path}: {e}")
            return None

    def encode_image_to_base64(self, image_path: Path) -> str:
        """
        Encode image to base64 string with optimization

        Args:
            image_path: Path to the image file

        Returns:
            Base64 encoded string of the image
        """
        try:
            # Try optimized approach first
            if self.enable_compression:
                optimized_bytes = self.optimize_image(image_path)
                if optimized_bytes:
                    return base64.b64encode(optimized_bytes).decode('utf-8')

            # Fallback to original method
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            return None

    def get_image_description(self, image_path: Path) -> Optional[str]:
        """
        Get description of an image using Ollama vision model

        Args:
            image_path: Path to the image file

        Returns:
            Description string or None if failed
        """
        try:
            # Check if image is supported
            if not self.is_supported_image(image_path):
                logger.warning(f"Unsupported image format: {image_path}")
                return None

            # Encode image to base64
            image_base64 = self.encode_image_to_base64(image_path)
            if not image_base64:
                return None

            # Get prompt from configuration
            prompt = self.get_prompt()
            logger.debug(f"Using prompt: {repr(prompt)}")

            # Get model settings from configuration
            model_settings = self.get_model_settings()
            logger.debug(f"Using model settings: {model_settings}")

            # Call Ollama API with configured settings
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [image_base64]
                    }
                ],
                options=model_settings
            )

            logger.debug(f"Raw response: {response}")
            logger.debug(f"Response type: {type(response)}")
            logger.debug(f"Response keys: {response.keys() if hasattr(response, 'keys') else 'no keys'}")
            if 'message' in response:
                logger.debug(f"Message: {response['message']}")
                logger.debug(f"Message type: {type(response['message'])}")
                if hasattr(response['message'], 'content'):
                    logger.debug(f"Message content: {repr(response['message'].content)}")
                elif 'content' in response['message']:
                    logger.debug(f"Message content dict: {repr(response['message']['content'])}")

            description = response['message']['content'].strip()
            logger.info(f"Generated description for {image_path.name}")
            logger.debug(f"Description content: {repr(description)}")
            logger.debug(f"Description length: {len(description)}")
            logger.debug(f"Description bool: {bool(description)}")

            # Clean up memory
            del image_base64, response
            gc.collect()

            return description

        except Exception as e:
            logger.error(f"Error generating description for {image_path}: {e}")
            # Clean up memory on error
            gc.collect()
            return None

    def write_description_to_file(self, image_path: Path, description: str, output_file: Path, metadata: Dict[str, Any] = None, base_directory: Path = None) -> bool:
        """
        Write description to a text file

        Args:
            image_path: Path to the image file
            description: Description to write
            output_file: Path to the output text file
            metadata: Optional metadata dictionary to include
            base_directory: Base directory for calculating relative paths

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get output format settings
            output_format = self.config.get('output_format', {})
            separator_char = output_format.get('separator', '-')

            # Calculate relative path if base directory is provided
            if base_directory:
                try:
                    relative_path = image_path.relative_to(base_directory)
                    entry = f"File: {relative_path}\n"
                except ValueError:
                    # Fallback if relative path calculation fails
                    entry = f"File: {image_path.name}\n"
            else:
                entry = f"File: {image_path.name}\n"

            if output_format.get('include_file_path', True):
                entry += f"Path: {image_path}\n"

            # Add metadata if enabled and available
            if output_format.get('include_metadata', True) and metadata:
                metadata_str = self.format_metadata(metadata)
                if metadata_str:
                    entry += f"{metadata_str}\n"

            if output_format.get('include_model_info', True):
                entry += f"Model: {self.model_name}\n"
                entry += f"Prompt Style: {self.prompt_style}\n"

            entry += f"Description: {description}\n"

            if output_format.get('include_timestamp', True):
                entry += f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"

            entry += separator_char * 80 + "\n\n"

            # Append to the file
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(entry)

            logger.info(f"Successfully wrote description for {image_path.name} to {output_file.name}")
            return True

        except Exception as e:
            logger.error(f"Error writing description to file: {e}")
            return False

    def process_directory(self, directory_path: Path, recursive: bool = False,
                         max_files: Optional[int] = None) -> None:
        """
        Process all images in a directory with memory optimization

        Args:
            directory_path: Path to the directory containing images
            recursive: Whether to process subdirectories recursively
            max_files: Maximum number of files to process (for testing)
        """
        if not directory_path.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return

        if not directory_path.is_dir():
            logger.error(f"Path is not a directory: {directory_path}")
            return

        # Create output file path - use custom output dir or workflow structure
        if self.output_dir:
            # User specified custom output directory
            output_dir = Path(self.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / "image_descriptions.txt"
        else:
            # Use workflow output structure
            try:
                from workflow_utils import WorkflowConfig
                config = WorkflowConfig()
                output_dir = config.get_step_output_dir("image_description", create=True)
                output_file = output_dir / "image_descriptions.txt"
                logger.info(f"Using workflow output directory: {output_dir}")
            except ImportError:
                # Fallback to local directory if workflow_utils not available
                output_file = directory_path / "image_descriptions.txt"

        # Initialize the output file with a header
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Image Descriptions Generated by Ollama Vision Model\n")
                f.write("=" * 80 + "\n")
                f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Model used: {self.model_name}\n")
                f.write(f"Prompt style: {self.prompt_style}\n")
                f.write(f"Directory: {directory_path}\n")
                f.write(f"Runtime Configuration: Model='{self.model_name}', Prompt='{self.prompt_style}'\n")
                f.write(f"Config File Model Settings: {self.config.get('model_settings', {})}\n")
                f.write("=" * 80 + "\n\n")
            logger.info(f"Created output file: {output_file}")
        except Exception as e:
            logger.error(f"Error creating output file: {e}")
            return

        # Get all image files
        pattern = "**/*" if recursive else "*"
        image_files = []

        for file_path in directory_path.glob(pattern):
            if file_path.is_file() and self.is_supported_image(file_path):
                image_files.append(file_path)

        if not image_files:
            logger.info("No supported image files found in the directory")
            return

        # Limit files if specified
        if max_files and len(image_files) > max_files:
            image_files = image_files[:max_files]
            logger.info(f"Limited to first {max_files} files for processing")

        logger.info(f"Found {len(image_files)} image files to process")

        # Process each image with memory management
        success_count = 0
        overall_start_time = time.time()

        for i, image_path in enumerate(image_files, 1):
            # Log progress and start time for this image
            logger.info(f"Describing image {i} of {len(image_files)}: {image_path.name}")
            image_start_time = time.time()
            logger.info(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(image_start_time))}")

            # Extract metadata from image
            metadata = self.extract_metadata(image_path)
            if metadata:
                logger.debug(f"Extracted metadata for {image_path.name}: {metadata}")
            else:
                logger.debug(f"No metadata extracted for {image_path.name}")

            # Get description from Ollama
            description = self.get_image_description(image_path)

            # Log end time for this image
            image_end_time = time.time()
            processing_duration = image_end_time - image_start_time
            logger.info(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(image_end_time))}")
            logger.info(f"Processing duration: {processing_duration:.2f} seconds")

            if description:
                # Write description to file with metadata and base directory for relative paths
                if self.write_description_to_file(image_path, description, output_file, metadata, directory_path):
                    success_count += 1
                    # Log with relative path for better readability
                    try:
                        relative_path = image_path.relative_to(directory_path)
                        logger.info(f"Successfully processed: {relative_path}")
                    except ValueError:
                        logger.info(f"Successfully processed: {image_path.name}")
                else:
                    logger.error(f"Failed to write description for: {image_path.name}")
            else:
                logger.error(f"Failed to generate description for: {image_path.name}")

            # Memory management: add delay and force garbage collection
            if self.batch_delay > 0:
                time.sleep(self.batch_delay)
            gc.collect()

        # Log overall completion summary
        overall_end_time = time.time()
        total_duration = overall_end_time - overall_start_time
        logger.info(f"Processing complete. Successfully processed {success_count}/{len(image_files)} images")
        logger.info(f"Total processing time: {total_duration:.2f} seconds")
        logger.info(f"Average time per image: {total_duration/len(image_files):.2f} seconds")
        logger.info(f"Descriptions saved to: {output_file}")

    def extract_metadata(self, image_path: Path) -> Dict[str, Any]:
        """
        Extract EXIF metadata from an image file

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary containing extracted metadata
        """
        metadata = {}

        try:
            # Check if metadata extraction is enabled
            if not self.config.get('processing_options', {}).get('extract_metadata', False):
                return metadata

            with Image.open(image_path) as img:
                # Use getexif() instead of _getexif() (modern method)
                exif_data = img.getexif()

                if exif_data:
                    # Convert EXIF data to human-readable format
                    exif_dict = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_dict[tag] = value

                    # Extract all available metadata
                    datetime_info = self._extract_datetime(exif_dict)
                    if datetime_info:
                        metadata['datetime'] = datetime_info

                    location_info = self._extract_location(exif_dict)
                    if location_info:
                        metadata['location'] = location_info

                    camera_info = self._extract_camera_info(exif_dict)
                    if camera_info:
                        metadata['camera'] = camera_info

                    technical_info = self._extract_technical_info(exif_dict)
                    if technical_info:
                        metadata['technical'] = technical_info

        except Exception as e:
            logger.debug(f"Error extracting metadata from {image_path}: {e}")

        return metadata

    def _extract_datetime(self, exif_data: dict) -> Optional[str]:
        """Extract date and time from EXIF data"""
        try:
            # Try different datetime fields
            datetime_fields = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']

            for field in datetime_fields:
                if field in exif_data:
                    dt_str = exif_data[field]
                    if dt_str:
                        # Parse and format the datetime
                        try:
                            dt = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
                            return dt.strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            # Try alternative format
                            try:
                                dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                                return dt.strftime('%Y-%m-%d %H:%M:%S')
                            except ValueError:
                                logger.debug(f"Could not parse datetime format: {dt_str}")
                                continue
        except Exception as e:
            logger.debug(f"Error extracting datetime: {e}")

        return None

    def _extract_location(self, exif_data: dict) -> Optional[Dict[str, Any]]:
        """Extract GPS location from EXIF data"""
        try:
            gps_info = exif_data.get('GPSInfo')
            if not gps_info:
                return None

            # Convert GPS info to readable format
            gps_dict = {}
            for tag_id, value in gps_info.items():
                tag = GPSTAGS.get(tag_id, tag_id)
                gps_dict[tag] = value

            location = {}

            # Extract latitude
            if 'GPSLatitude' in gps_dict and 'GPSLatitudeRef' in gps_dict:
                lat = self._convert_gps_coordinate(gps_dict['GPSLatitude'])
                if gps_dict['GPSLatitudeRef'] == 'S':
                    lat = -lat
                location['latitude'] = lat

            # Extract longitude
            if 'GPSLongitude' in gps_dict and 'GPSLongitudeRef' in gps_dict:
                lon = self._convert_gps_coordinate(gps_dict['GPSLongitude'])
                if gps_dict['GPSLongitudeRef'] == 'W':
                    lon = -lon
                location['longitude'] = lon

            # Extract altitude
            if 'GPSAltitude' in gps_dict:
                altitude = float(gps_dict['GPSAltitude'])
                if 'GPSAltitudeRef' in gps_dict and gps_dict['GPSAltitudeRef'] == 1:
                    altitude = -altitude
                location['altitude'] = altitude

            return location if location else None

        except Exception as e:
            logger.debug(f"Error extracting location: {e}")

        return None

    def _extract_camera_info(self, exif_data: dict) -> Optional[Dict[str, str]]:
        """Extract camera information from EXIF data"""
        try:
            camera_info = {}

            # Camera make and model
            if 'Make' in exif_data:
                camera_info['make'] = exif_data['Make']
            if 'Model' in exif_data:
                camera_info['model'] = exif_data['Model']

            # Lens information
            if 'LensModel' in exif_data:
                camera_info['lens'] = exif_data['LensModel']

            return camera_info if camera_info else None

        except Exception as e:
            logger.debug(f"Error extracting camera info: {e}")

        return None

    def _extract_technical_info(self, exif_data: dict) -> Optional[Dict[str, Any]]:
        """Extract technical camera settings from EXIF data"""
        try:
            technical_info = {}

            # ISO
            if 'ISOSpeedRatings' in exif_data:
                technical_info['iso'] = exif_data['ISOSpeedRatings']
            elif 'ISO' in exif_data:
                technical_info['iso'] = exif_data['ISO']

            # Aperture
            if 'FNumber' in exif_data:
                f_number = exif_data['FNumber']
                if isinstance(f_number, tuple) and len(f_number) == 2:
                    f_value = f_number[0] / f_number[1]
                    technical_info['aperture'] = f"f/{f_value:.1f}"
                else:
                    technical_info['aperture'] = f"f/{f_number}"

            # Shutter speed
            if 'ExposureTime' in exif_data:
                exposure_time = exif_data['ExposureTime']
                if isinstance(exposure_time, tuple) and len(exposure_time) == 2:
                    if exposure_time[0] == 1:
                        technical_info['shutter_speed'] = f"1/{exposure_time[1]}s"
                    else:
                        technical_info['shutter_speed'] = f"{exposure_time[0]/exposure_time[1]}s"
                else:
                    technical_info['shutter_speed'] = f"{exposure_time}s"

            # Focal length
            if 'FocalLength' in exif_data:
                focal_length = exif_data['FocalLength']
                if isinstance(focal_length, tuple) and len(focal_length) == 2:
                    fl_value = focal_length[0] / focal_length[1]
                    technical_info['focal_length'] = f"{fl_value:.0f}mm"
                else:
                    technical_info['focal_length'] = f"{focal_length}mm"

            return technical_info if technical_info else None

        except Exception as e:
            logger.debug(f"Error extracting technical info: {e}")

        return None

    def _convert_gps_coordinate(self, coord_tuple) -> float:
        """Convert GPS coordinate from tuple format to decimal degrees"""
        try:
            degrees = float(coord_tuple[0])
            minutes = float(coord_tuple[1])
            seconds = float(coord_tuple[2])
            return degrees + (minutes / 60.0) + (seconds / 3600.0)
        except:
            return 0.0

    def format_metadata(self, metadata: Dict[str, Any]) -> str:
        """
        Format metadata for display in output file

        Args:
            metadata: Dictionary containing metadata

        Returns:
            Formatted metadata string
        """
        if not metadata:
            return ""

        lines = []

        # Format datetime
        if 'datetime' in metadata:
            lines.append(f"Photo Date: {metadata['datetime']}")

        # Format location
        if 'location' in metadata:
            location = metadata['location']
            location_parts = []

            if 'latitude' in location and 'longitude' in location:
                location_parts.append(f"GPS: {location['latitude']:.6f}, {location['longitude']:.6f}")

            if 'altitude' in location:
                location_parts.append(f"Altitude: {location['altitude']:.1f}m")

            if location_parts:
                lines.append("Location: " + ", ".join(location_parts))

        # Format camera info
        if 'camera' in metadata:
            camera = metadata['camera']
            camera_parts = []

            if 'make' in camera and 'model' in camera:
                camera_parts.append(f"{camera['make']} {camera['model']}")

            if 'lens' in camera:
                camera_parts.append(f"Lens: {camera['lens']}")

            if camera_parts:
                lines.append("Camera: " + ", ".join(camera_parts))

        # Format technical info
        if 'technical' in metadata:
            technical = metadata['technical']
            technical_parts = []

            for key, value in technical.items():
                technical_parts.append(f"{key.replace('_', ' ').title()}: {value}")

            if technical_parts:
                lines.append("Settings: " + ", ".join(technical_parts))

        return "\n".join(lines)

    # ...existing code...
def get_default_prompt_style(config_file: str = "image_describer_config.json") -> str:
    """
    Get the default prompt style from configuration file

    Args:
        config_file: Path to configuration file

    Returns:
        Default prompt style name
    """
    try:
        config_path = Path(config_file)
        if not config_path.is_absolute():
            script_dir = Path(__file__).parent
            config_path = script_dir / config_file

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            default_style = config.get('default_prompt_style', 'detailed')
            # Validate that the default style exists in prompt_variations
            available_styles = list(config.get('prompt_variations', {}).keys())
            if default_style in available_styles:
                return default_style
            else:
                logger.warning(f"Default prompt style '{default_style}' not found in prompt_variations. Using 'detailed'.")
                return 'detailed' if 'detailed' in available_styles else available_styles[0] if available_styles else 'detailed'
    except:
        pass

    return "detailed"


def get_available_prompt_styles(config_file: str = "image_describer_config.json") -> list:
    """
    Get available prompt styles from configuration file

    Args:
        config_file: Path to configuration file

    Returns:
        List of available prompt style names
    """
    try:
        config_path = Path(config_file)
        if not config_path.is_absolute():
            script_dir = Path(__file__).parent
            config_path = script_dir / config_file

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return list(config.get('prompt_variations', {}).keys())
    except:
        pass

    # Default fallback
    return ["detailed", "concise", "artistic", "technical"]


def main():
    """Main function to run the image description script"""

    # Get available prompt styles and default from config
    available_styles = get_available_prompt_styles()
    default_style = get_default_prompt_style()

    parser = argparse.ArgumentParser(
        description="Process images with Ollama vision model and save descriptions to a text file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available prompt styles: {', '.join(available_styles)}
Default prompt style: {default_style}

Examples:
  python {Path(__file__).name} exportedphotos
  python {Path(__file__).name} exportedphotos --prompt-style artistic --model llava:7b
  python {Path(__file__).name} exportedphotos --max-size 512 --max-files 5 --verbose
  python {Path(__file__).name} exportedphotos --model llava:13b --prompt-style technical
  python {Path(__file__).name} exportedphotos --no-metadata --model moondream

Configuration:
  Use config_helper.py to manage settings:
    python config_helper.py help    - Show configuration help
    python config_helper.py show    - Show current configuration
    python config_helper.py modify  - Interactive configuration editor
        """
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Directory containing images to process"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Ollama vision model to use (default: from image_describer_config.json)"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process subdirectories recursively"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024,
        help="Maximum image dimension for processing (default: 1024)"
    )
    parser.add_argument(
        "--no-compression",
        action="store_true",
        help="Disable image compression"
    )
    parser.add_argument(
        "--batch-delay",
        type=float,
        default=2.0,
        help="Delay between processing images in seconds (default: 2.0)"
    )
    parser.add_argument(
        "--max-files",
        type=int,
        help="Maximum number of files to process (for testing)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="image_describer_config.json",
        help="Path to JSON configuration file (default: image_describer_config.json)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for description file (default: workflow_output/descriptions/)"
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        help="Directory for log files (default: uses workflow output/logs)"
    )
    parser.add_argument(
        "--prompt-style",
        type=str,
        default=default_style,
        choices=available_styles,
        help=f"Style of prompt to use. Available: {', '.join(available_styles)} (default: {default_style})"
    )
    parser.add_argument(
        "--poet",
        action="store_true",
        help="Generate all poet prompt styles (poet_basic, poet_structured, poet_extended, poet_contextual) and output as a single JSON file with image metadata"
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Disable metadata extraction from image files"
    )

    args = parser.parse_args()

    # Set up logging with log directory and verbosity
    setup_logging(log_dir=args.log_dir, verbose=args.verbose)

    # Convert directory path to Path object
    directory_path = Path(args.directory)

    # Create ImageDescriber instance with memory optimization
    describer = ImageDescriber(
        model_name=args.model,
        max_image_size=args.max_size,
        enable_compression=not args.no_compression,
        batch_delay=args.batch_delay,
        config_file=args.config,
        prompt_style=args.prompt_style,
        output_dir=args.output_dir
    )

    # Override metadata extraction if disabled via command line
    if args.no_metadata:
        describer.config['processing_options']['extract_metadata'] = False

    # Poet mode: generate all poet prompt styles and output as JSON
    if args.poet:
        poet_styles = ["poet_basic", "poet_structured", "poet_extended", "poet_contextual"]
        output_dir = Path(args.output_dir) if args.output_dir else Path("workflow_output/descriptions/")
        output_dir.mkdir(parents=True, exist_ok=True)
        image_files = [f for f in directory_path.iterdir() if describer.is_supported_image(f)]
        for img_path in image_files:
            metadata = describer.extract_metadata(img_path) if describer.config['processing_options'].get('extract_metadata', True) else {}
            poet_descriptions = []
            for style in poet_styles:
                describer.prompt_style = style
                desc = describer.get_image_description(img_path)
                poet_descriptions.append({
                    "style": style,
                    "description": desc
                })
            out_json = {
                "file_path": str(img_path.resolve()),
                "metadata": metadata,
                "poet_descriptions": poet_descriptions
            }
            out_file = output_dir / f"{img_path.stem}_poet.json"
            with open(out_file, "w", encoding="utf-8") as jf:
                json.dump(out_json, jf, indent=2)
            print(f"Poet descriptions written to {out_file}")
        sys.exit(0)
        describer.config['output_format']['include_metadata'] = False

    # Check if Ollama is available
    try:
        ollama.list()
        logger.info("Ollama is available")
    except Exception as e:
        logger.error(f"Ollama is not available or not running: {e}")
        logger.error("Please make sure Ollama is installed and running")
        sys.exit(1)

    # Check if the specified model is available
    try:
        models = ollama.list()
        available_models = [model['name'] for model in models.get('models', [])]
        if describer.model_name not in available_models:
            logger.error(f"Model '{describer.model_name}' is not available")
            logger.error(f"Available models: {', '.join(available_models)}")
            logger.info(f"You can install the model with: ollama pull {describer.model_name}")
            sys.exit(1)
        else:
            logger.info(f"Using model: {describer.model_name}")
    except Exception as e:
        logger.warning(f"Could not check available models: {e}")

    # Process the directory
    try:
        describer.process_directory(directory_path, recursive=args.recursive,
                                   max_files=args.max_files)
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
