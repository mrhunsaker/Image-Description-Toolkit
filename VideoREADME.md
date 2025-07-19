# HBConvert - Video Processing Tools

A collection of tools for video processing: HandBrake batch conversion and intelligent frame extraction.

## Tools Included

### 1. HandBrake Batch Converter (`convert_mkv_to_mp4.bat`)
Batch convert MKV files to MP4 using HandBrake CLI while preserving all audio, video, and subtitle tracks.

### 2. Video Frame Extractor (`video_frame_extractor.py`)
A Python tool for extracting frames from video files with configurable options including intelligent scene change detection.

## Video Frame Extractor

### Features

- **Two Extraction Modes:**
  - **Time Interval**: Extract frames at regular intervals (e.g., every 5 seconds)
  - **Scene Change Detection**: Intelligently extract frames when significant visual changes occur
- **Recursive Directory Processing**: Process entire folder structures automatically
- **Configurable Settings**: All options controlled via JSON configuration file
- **Multiple Video Formats**: Supports MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V
- **Flexible Output Options**: Simple flat structure or preserve directory hierarchy
- **Image Quality Control**: Adjustable JPEG compression (1-100)
- **Frame Resizing**: Optional resize frames to save space
- **Progress Logging**: Detailed progress reporting and timing information
- **Smart Skip Logic**: Skip processing if output already exists (configurable)
- **Command Line Overrides**: Override config settings via command line arguments

### Installation

#### Prerequisites
- Python 3.7 or higher
- OpenCV and NumPy libraries

#### Quick Setup
1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Manual Installation
```bash
pip install opencv-python numpy
```

### Usage

#### Basic Usage
Extract frames from a single video:
```bash
python video_frame_extractor.py video.mp4
```

Process all videos in a directory recursively:
```bash
python video_frame_extractor.py "C:\Videos"
```

#### Command Line Options

**Time Interval Override:**
```bash
# Extract every 2 seconds (overrides config)
python video_frame_extractor.py --time 2.0 "C:\Videos"
```

**Scene Change Override:**
```bash
# Use scene detection with 25% threshold (overrides config)
python video_frame_extractor.py --scene 25.0 "C:\Videos"
```

**Custom Config File:**
```bash
python video_frame_extractor.py "C:\Videos" -c my_config.json
```

### Configuration

The tool uses a JSON configuration file (`frame_extractor_config.json`) that will be automatically created on first run. You can customize all extraction behavior by editing this file.

#### Configuration Options

| Setting | Description | Default | Example |
|---------|-------------|---------|---------|
| `extraction_mode` | Extraction method | `"time_interval"` | `"scene_change"` |
| `time_interval_seconds` | Seconds between extractions | `5.0` | `10.0` |
| `scene_change_threshold` | Sensitivity for scene detection (%) | `30.0` | `25.0` |
| `min_scene_duration_seconds` | Minimum time between scene extractions | `1.0` | `2.0` |
| `output_directory` | Where to save extracted frames | `"extracted_frames"` | `"thumbnails"` |
| `preserve_directory_structure` | Keep original folder layout | `true` | `false` |
| `image_quality` | JPEG quality (1-100) | `95` | `80` |
| `resize_width` | Resize frame width (pixels) | `null` | `1920` |
| `resize_height` | Resize frame height (pixels) | `null` | `1080` |
| `frame_prefix` | Filename prefix for extracted frames | `"frame"` | `"thumb"` |
| `start_time_seconds` | Start extraction at time | `0` | `30` |
| `end_time_seconds` | Stop extraction at time | `null` | `300` |
| `max_frames_per_video` | Limit frames per video | `null` | `50` |
| `skip_existing` | Skip if output directory has files | `true` | `false` |
| `log_progress` | Show detailed progress | `true` | `false` |

### Sample Configuration

```json
{
    "extraction_mode": "scene_change",
    "scene_change_threshold": 25.0,
    "min_scene_duration_seconds": 2.0,
    "output_directory": "thumbnails",
    "preserve_directory_structure": true,
    "image_quality": 90,
    "resize_width": 1280,
    "resize_height": 720,
    "frame_prefix": "scene",
    "max_frames_per_video": 20,
    "skip_existing": true,
    "log_progress": true
}
```

## Extraction Modes

### Time Interval Mode
Extracts frames at regular time intervals. Perfect for:
- Creating consistent thumbnails
- Time-lapse creation
- Regular sampling of video content

**Example**: Extract a frame every 10 seconds
```json
{
    "extraction_mode": "time_interval",
    "time_interval_seconds": 10.0
}
```

### Scene Change Detection Mode
Intelligently detects when video content changes significantly. Perfect for:
- Capturing key moments
- Identifying scene transitions
- Content analysis and summarization

**How it works**: Compares consecutive frames and extracts when a threshold percentage of pixels change significantly.

**Example**: Extract frames when 25% of the image changes, with minimum 2 seconds between extractions
```json
{
    "extraction_mode": "scene_change",
    "scene_change_threshold": 25.0,
    "min_scene_duration_seconds": 2.0
}
```

## Output Structure

### With Directory Structure Preserved
```
extracted_frames/
├── Movies/
│   ├── Action/
│   │   └── movie1/
│   │       ├── frame_00.05s.jpg
│   │       ├── frame_00.10s.jpg
│   │       └── ...
│   └── Comedy/
│       └── movie2/
│           ├── frame_00.05s.jpg
│           └── ...
```

### Flattened Structure
```
extracted_frames/
├── movie1/
│   ├── frame_00.05s.jpg
│   ├── frame_00.10s.jpg
│   └── ...
├── movie2/
│   ├── frame_00.05s.jpg
│   └── ...
```

## Examples

### Extract Thumbnails for Video Library
```json
{
    "extraction_mode": "time_interval",
    "time_interval_seconds": 60.0,
    "output_directory": "video_thumbnails",
    "resize_width": 320,
    "resize_height": 180,
    "image_quality": 85,
    "max_frames_per_video": 5
}
```

### Scene Analysis for Content Review
```json
{
    "extraction_mode": "scene_change",
    "scene_change_threshold": 20.0,
    "min_scene_duration_seconds": 3.0,
    "output_directory": "scene_analysis",
    "preserve_directory_structure": true,
    "frame_prefix": "scene"
}
```

### High-Quality Stills Every 30 Seconds
```json
{
    "extraction_mode": "time_interval",
    "time_interval_seconds": 30.0,
    "image_quality": 100,
    "output_directory": "high_quality_stills"
}
```

### Command Line Examples

```bash
# Extract frames every 2 seconds from a single video
python video_frame_extractor.py movie.mp4 --time 2

# Use scene detection with 15% threshold on entire directory
python video_frame_extractor.py C:\Videos --scene 15

# Extract frames every 30 seconds with custom config
python video_frame_extractor.py videos/ -c thumbnails.json --time 30

# Use sensitive scene detection (10% threshold)
python video_frame_extractor.py documentary.mkv --scene 10

# Quick thumbnail extraction (every 60 seconds)
python video_frame_extractor.py C:\Movies --time 60
```
```

## HandBrake Batch Converter

### Features
- **Batch Processing**: Convert all MKV files in a directory and subdirectories
- **Format Preservation**: Keeps all audio tracks, video streams, and subtitle tracks intact
- **Multiple Presets**: Choose from Fast 1080p30, High Profile, or Universal presets
- **Progress Logging**: Detailed conversion logs with timestamps
- **Error Handling**: Continues processing even if individual files fail

### Prerequisites
- HandBrake CLI (`HandBrakeCLI.exe`) must be installed and in your system PATH
- Download from: https://handbrake.fr/downloads.php

### Usage

1. **Run the batch file:**
   ```cmd
   convert_mkv_to_mp4.bat
   ```

2. **Follow the prompts:**
   - Enter the directory path containing MKV files
   - Choose conversion preset (1=Fast, 2=High Profile, 3=Universal)
   - Conversion will begin automatically

3. **Monitor progress:**
   - Real-time progress shown in console
   - Detailed logs saved to `handbrake_conversion_log.txt`

### Example Output Structure
```
Original: C:\Videos\movie.mkv
Converted: C:\Videos\movie.mp4
```

## Combined Workflow

You can use both tools together for a complete video processing workflow:

1. **Convert videos**: Use HandBrake batch converter to convert MKV → MP4
2. **Extract frames**: Use the frame extractor to create thumbnails or analyze content

## Troubleshooting

### HandBrake Issues

**Error: "HandBrakeCLI is not recognized"**
- Install HandBrake CLI and add to system PATH
- Or place `HandBrakeCLI.exe` in the same directory as the batch file

**Error: "Access denied" or file locked**
- Close any media players that might have the video files open
- Run command prompt as administrator

### Frame Extractor Issues

**Error: "Import cv2 could not be resolved"**
- Install OpenCV: `pip install opencv-python`

**Error: "Could not open video"**
- Check video file format is supported
- Verify file path is correct
- Ensure video file is not corrupted

**No frames extracted**
- Check video duration vs. `time_interval_seconds`
- Verify `start_time_seconds` and `end_time_seconds` settings
- For scene change mode, try lowering `scene_change_threshold`

**Out of memory errors**
- Reduce `resize_width` and `resize_height`
- Lower `image_quality`
- Process videos individually instead of batch processing

### Performance Tips

- Use scene change mode for videos with distinct scenes
- Use time interval mode for consistent sampling
- Resize frames to reduce output file sizes
- Adjust `image_quality` based on your needs (80-95 is usually sufficient)
- Use `max_frames_per_video` to limit output for very long videos

## Supported Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MKV (.mkv)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)
- M4V (.m4v)

## Requirements

- Python 3.7+
- OpenCV Python (opencv-python>=4.8.0)
- NumPy (numpy>=1.24.0)

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.
