# Workflow System - Image Description Toolkit

The Image Description Toolkit now includes a comprehensive workflow system that can orchestrate the entire pipeline from videos/images to final HTML reports, while maintaining full backward compatibility with all existing scripts.

## 🚀 Quick Start

### Run Complete Workflow
```bash
# Process all media types through complete pipeline
python workflow.py media_folder

# Custom output directory
python workflow.py media_folder --output-dir results

# Specific steps only
python workflow.py photos --steps describe,html
```

### Individual Scripts (Now Use Workflow Output Structure by Default)
```bash
# All scripts now output to organized workflow directories by default
python image_describer.py photos         # → workflow_output/descriptions/image_descriptions.txt
python video_frame_extractor.py videos   # → workflow_output/extracted_frames/
python ConvertImage.py heic_photos       # → workflow_output/converted_images/
python descriptions_to_html.py image_descriptions.txt # → workflow_output/html_reports/image_descriptions.html
```

## 🗃️ Workflow Steps

The workflow system supports four main steps that can be run individually or in any combination:

| Step      | Description                      | Input           | Output                  |
|-----------|----------------------------------|-----------------|-------------------------|
| **video** | Extract frames from videos       | Video files     | JPG frames              |
| **convert** | Convert HEIC/HEIF to JPG       | HEIC/HEIF files | JPG files               |
| **describe** | AI-powered image descriptions | Image files     | Text descriptions       |
| **html** | Generate HTML reports             | Description files | HTML reports           |

All outputs are organized in the `workflow_output/` directory by default.

## 🗂️ Directory Structure

The workflow creates an organized output structure:

```
workflow_output/
├── extracted_frames/     # Video frames (from video step)
├── converted_images/     # HEIC→JPG conversions (from convert step)
├── descriptions/         # AI descriptions (from describe step)
├── html_reports/         # HTML reports (from html step)
└── logs/                # Workflow logs
```

## ⚙️ Configuration

### Workflow Configuration (`workflow_config.json`)

```json
{
  "workflow": {
    "base_output_dir": "workflow_output",
    "preserve_structure": true,
    "steps": {
      "video_extraction": {
        "enabled": true,
        "output_subdir": "extracted_frames"
      },
      "image_conversion": {
        "enabled": true,
        "output_subdir": "converted_images",
        "quality": 95
      },
      "image_description": {
        "enabled": true,
        "output_subdir": "descriptions",
        "model": "moondream",
        "prompt_style": "detailed"
      },
      "html_generation": {
        "enabled": true,
        "output_subdir": "html_reports",
        "include_details": false
      }
    }
  }
}
```

### Individual Script Configs
- `image_describer_config.json` - Image description settings (see CONFIGURATION.md)
- `video_frame_extractor_config.json` - Video extraction settings

All scripts now use the workflow output structure by default. No legacy flags or config options are required.

## 📖 Usage Examples

### Complete Media Processing
```bash
# Process mixed media folder with all steps
python workflow.py mixed_media_folder

# Custom configuration and output
python workflow.py media --output-dir analysis --config my_workflow.json
```

### Partial Workflows
```bash
# Only video processing and description
python workflow.py videos --steps video,describe

# Only image description and HTML generation
python workflow.py photos --steps describe,html

# Only HEIC conversion
python workflow.py heic_photos --steps convert
```

### Advanced Options
```bash
# Override AI model
python workflow.py photos --steps describe,html --model llava:7b

# Override prompt style
python workflow.py photos --steps describe --prompt-style artistic

# Verbose logging
python workflow.py media --verbose

# Dry run (show what would be done)
python workflow.py media --dry-run
```

### Individual Script Usage (Now Always Uses Workflow Output Structure)
```bash
python image_describer.py photos
python video_frame_extractor.py videos
python ConvertImage.py heic_photos
python descriptions_to_html.py image_descriptions.txt
# All outputs go to workflow_output/ subdirectories by default.
```

## 🔧 Backward Compatibility

**All existing scripts work unchanged!** The workflow system is purely additive:

- ✅ All command-line arguments preserved
- ✅ All configuration files work as before
- ✅ All output formats unchanged
- ✅ All existing workflows continue to work

### Enhanced Individual Scripts

Some scripts now support additional workflow-friendly options:

#### `image_describer.py` Enhancements
```bash
# New: Custom output directory
python image_describer.py photos --output-dir descriptions/

# All existing options still work
python image_describer.py photos --model llava:7b --prompt-style artistic
```

## 🔗 Integration Examples

### Video → Descriptions → HTML
```bash
# Automated pipeline
python workflow.py video_folder --steps video,describe,html

# Or step by step (equivalent)
python video_frame_extractor.py video_folder
python image_describer.py extracted_frames
python descriptions_to_html.py extracted_frames/image_descriptions.txt
```

### HEIC Conversion → Descriptions
```bash
# Automated pipeline
python workflow.py heic_photos --steps convert,describe

# Or step by step (equivalent)
python ConvertImage.py heic_photos --output converted/
python image_describer.py converted/
```

## 📊 Workflow Output

### Console Output
```
WORKFLOW SUMMARY
============================================================
Input directory: /path/to/media
Output directory: /path/to/workflow_output
Overall success: ✅ YES
Steps completed: video, convert, describe, html

Detailed results saved in workflow log file.
```

### Log Files
- Timestamped log files: `workflow_YYYYMMDD_HHMMSS.log`
- Detailed step-by-step execution logs
- Error reporting and debugging information

## 🛠️ Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

**Ollama connection issues:**
```bash
# Test Ollama connectivity
python debug_ollama.py

# Ensure Ollama is running
ollama serve
```

**Workflow step failures:**
- Check individual script functionality first
- Review workflow log files for detailed error information
- Use `--verbose` flag for additional debugging output

### Individual Script Testing
```bash
# Test each component independently
python video_frame_extractor.py test_video.mp4
python ConvertImage.py test_image.heic
python image_describer.py test_photos/
python descriptions_to_html.py image_descriptions.txt
# All outputs will be in workflow_output/ subdirectories.
```

## 🔄 Migration from Individual Scripts

### If you currently use:
```bash
# Old workflow (manual steps)
python video_frame_extractor.py videos/
python ConvertImage.py heic_photos/ --output converted/
python image_describer.py extracted_frames/
python image_describer.py converted/
python descriptions_to_html.py extracted_frames/image_descriptions.txt
python descriptions_to_html.py converted/image_descriptions.txt
```

### You can now use:
```bash
# New workflow (automated)
python workflow.py videos/ --steps video,describe,html
python workflow.py heic_photos/ --steps convert,describe,html
```

## 🗂️ File Organization

The workflow system automatically organizes outputs:

- **Preserves input structure** when `preserve_structure: true`
- **Separates processing steps** into logical directories
- **Consolidates related outputs** (descriptions, HTML reports)
- **Maintains traceability** through detailed logging

Example output structure:
```
workflow_output/
├── extracted_frames/
├── converted_images/
├── descriptions/
├── html_reports/
└── logs/
```

This makes it easy to:
- Track processing steps
- Debug issues
- Reprocess specific steps
- Share organized results

The workflow system provides a powerful, automated approach while maintaining the flexibility of individual script usage.
