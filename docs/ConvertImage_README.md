# HEIC to JPG Converter

A Python script to convert HEIC/HEIF image files to JPG format. Now fully integrated with the workflow system for organized output and batch processing. Supports both individual files and batch conversion of directories with various quality and metadata options.

## Features

- ✅ Convert single HEIC/HEIF files to JPG
- 🗂️ Batch convert entire directories
- 🔄 Recursive directory processing
- 🎨 Adjustable JPEG quality (1-100)
- 📊 Metadata preservation option
- 📈 Progress tracking and statistics
- 🛡️ Robust error handling
- 🎯 Cross-platform support
- 🗃️ Workflow integration: outputs organized in `workflow_output/converted_images/` by default

## Requirements

- Python 3.7+
- PIL (Pillow)
- pillow-heif

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```
This single requirements file covers all toolkit features.

Or install manually:
```bash
pip install pillow pillow-heif
```

## Usage

### Command Line Interface

```bash
python ConvertImage.py <input> [options]
```
Outputs are organized in `workflow_output/converted_images/` by default.

### Basic Examples

```bash
# Convert a single HEIC file
python ConvertImage.py photo.heic

# Convert all HEIC files in a directory
python ConvertImage.py photos/

# Convert with custom output directory
python ConvertImage.py photos/ --output converted/

# Convert with lower quality (smaller files)
python ConvertImage.py photos/ --quality 85

# Process subdirectories recursively
python ConvertImage.py photos/ --recursive

# Convert without preserving metadata
python ConvertImage.py photos/ --no-metadata

# Output to workflow structure (default)
python ConvertImage.py photos/
# → workflow_output/converted_images/
```

### Advanced Examples

```bash
# High quality conversion with recursive processing
python ConvertImage.py photos/ --quality 95 --recursive --output jpg_converted/

# Batch convert with custom quality and no metadata
python ConvertImage.py input_folder/ --quality 80 --no-metadata --output output_folder/

# Convert single file to specific output location
python ConvertImage.py important_photo.heic --output family_photos/converted_photo.jpg

# Use with workflow system
python workflow.py media_folder --steps convert
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file or directory | `workflow_output/converted_images/` |
| `--recursive` | `-r` | Process subdirectories recursively | False |
| `--quality` | `-q` | JPEG quality (1-100) | 95 |
| `--no-metadata` | | Don't preserve metadata | False (metadata preserved) |
| `--verbose` | | Enable verbose logging | False |

## File Structure

### Single File Conversion
```
Input:  photo.heic
Output: workflow_output/converted_images/photo.jpg
```

### Directory Conversion
```
Input Directory:
  photos/
    ├── img1.heic
    ├── img2.heic
    └── subfolder/
        └── img3.heic

Output (default):
  workflow_output/
    └── converted_images/
        ├── img1.jpg
        ├── img2.jpg
        └── subfolder/  (if --recursive)
            └── img3.jpg
```

## Quality Settings

| Quality | File Size | Use Case |
|---------|-----------|----------|
| 95-100 | Large | Professional/archival |
| 85-94 | Medium | General use |
| 70-84 | Small | Web/sharing |
| 50-69 | Very Small | Thumbnails |

## Error Handling

The script includes comprehensive error handling for:
- Missing input files/directories
- Invalid HEIC/HEIF files
- Permission errors
- Disk space issues
- Corrupted files
- Workflow output directory creation issues

## Metadata Preservation

By default, the script preserves EXIF metadata from the original HEIC files. This includes:
- Camera settings
- GPS coordinates
- Timestamps
- Camera model information

Use `--no-metadata` to exclude metadata for smaller file sizes.

Metadata is preserved in all output files unless explicitly disabled.

## Supported Formats

### Input Formats
- `.heic` (HEIC format)
- `.heif` (HEIF format)

### Output Format
- `.jpg` (JPEG format)

All output files are placed in the workflow output directory by default.

## Performance Tips

1. **Quality vs Size**: Use quality 85-90 for good balance
2. **Batch Processing**: Process directories rather than individual files
3. **Recursive Processing**: Use `--recursive` for deep directory structures
4. **Output Organization**: Use workflow system for automatic organization

## Troubleshooting

### Common Issues

**"HEIF support may not be properly registered"**
- Ensure `pillow-heif` is installed: `pip install pillow-heif`
- Try reinstalling: `pip uninstall pillow-heif && pip install pillow-heif`

**"No HEIC/HEIF files found"**
- Check file extensions (case-sensitive on some systems)
- Verify files are actually HEIC/HEIF format
- Use `--recursive` for subdirectories

**Permission Errors**
- Ensure read access to input files
- Ensure write access to output directory (workflow_output/converted_images/)
- Run with appropriate permissions

**Memory Issues with Large Files**
- Process files individually rather than in large batches
- Use lower quality settings for very large images
- Ensure sufficient disk space

## Output Examples

```
🔍 Found 3 HEIC/HEIF files to convert
✅ Converted: IMG_001.heic -> workflow_output/converted_images/IMG_001.jpg
✅ Converted: IMG_002.heic -> workflow_output/converted_images/IMG_002.jpg
✅ Converted: IMG_003.heic -> workflow_output/converted_images/IMG_003.jpg

📊 Conversion complete:
   ✅ Successful: 3
   ❌ Failed: 0
   🗂️ Output directory: workflow_output/converted_images/
```

## License

This script is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or improvements to enhance the script's functionality.

---

For full workflow documentation and integration examples, see `WORKFLOW_README.md`.
