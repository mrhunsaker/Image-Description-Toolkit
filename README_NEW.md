# Image Description Toolkit

An AI-powered toolkit for generating descriptive text from images using local language models via Ollama. This toolkit provides both individual scripts for specific tasks and a unified workflow system for processing multiple images efficiently.

## 🌟 Features

- **AI-Powered Descriptions**: Generate natural language descriptions using local Ollama models
- **Flexible Workflow System**: Unified pipeline for processing multiple images
- **Image Format Conversion**: Convert between various image formats (including HEIC to JPG)
- **Video Frame Extraction**: Extract frames from videos for analysis
- **Batch Processing**: Handle multiple files efficiently
- **HTML Export**: Convert descriptions to formatted HTML galleries
- **Comprehensive Testing**: Automated test suite with 29+ test cases
- **Professional Project Structure**: Organized codebase with proper separation of concerns

## 📁 Project Structure

```
Image-Description-Toolkit/
├── docs/                      # Documentation
│   ├── BLOG_POST.md           # Project overview and use cases
│   ├── CONFIGURATION.md       # Configuration guide
│   ├── CONVERT_README.md      # Image conversion documentation
│   ├── HTML_README.md         # HTML export guide
│   ├── VideoREADME.md         # Video processing guide
│   └── WORKFLOW_README.md     # Workflow system documentation
├── tests/                     # Test suite and test files
│   ├── test_files/           # Test images and data
│   ├── comprehensive_test.py # Complete test suite (29 tests)
│   ├── generate_test_images.py # Test image generator
│   ├── run_tests.py         # Test runner
│   ├── demo_workflow.py     # Demo and testing
│   └── test_workflow.py     # Workflow testing
├── scripts/                   # Utility scripts
│   ├── convert_mkv_to_mp4.bat # Video conversion utility
│   ├── debug_ollama.py        # Ollama debugging tools
│   ├── descriptions_to_html.py # HTML export utility
│   └── html_converter.py      # HTML conversion tools
├── config/                    # Configuration files
│   ├── image_describer_config.json      # AI model settings
│   ├── video_frame_extractor_config.json # Video processing config
│   └── workflow_config.json             # Workflow system config
├── workflow.py               # Main workflow system
├── workflow_utils.py         # Workflow utilities
├── image_describer.py        # AI image description engine
├── ConvertImage.py           # Image format conversion
├── video_frame_extractor.py  # Video frame extraction
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Ollama** (for AI descriptions)
   ```bash
   # Download from https://ollama.ai/
   ollama pull llava:7b  # or your preferred vision model
   ```

3. **Run the Workflow System**
   ```bash
   python workflow.py path/to/your/images
   ```

4. **Or Use Individual Scripts**
   ```bash
   # Generate descriptions
   python image_describer.py path/to/images

   # Convert image formats
   python ConvertImage.py input.heic output.jpg

   # Extract video frames
   python video_frame_extractor.py video.mp4

   # Convert descriptions to HTML
   python scripts/descriptions_to_html.py descriptions/
   ```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Quick tests (no AI dependencies required)
cd tests
python run_tests.py

# Full test suite (requires Ollama)
python comprehensive_test.py --verbose

# Individual test categories
python comprehensive_test.py --individual  # Test individual scripts
python comprehensive_test.py --workflow    # Test workflow system
```

The test suite includes 29+ automated tests covering:
- ✅ **Dependency verification** - Check all required packages
- ✅ **Configuration validation** - Verify config files are valid
- ✅ **Individual script functionality** - Test each component independently
- ✅ **Workflow system integration** - End-to-end workflow testing
- ✅ **File handling and error cases** - Robust error handling validation
- ✅ **Output format validation** - Ensure proper output generation

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Configuration Guide](docs/CONFIGURATION.md)** - Setup and configuration options
- **[Workflow System](docs/WORKFLOW_README.md)** - Unified processing pipeline
- **[Video Processing](docs/VideoREADME.md)** - Video frame extraction guide
- **[HTML Export](docs/HTML_README.md)** - Converting descriptions to HTML
- **[Image Conversion](docs/CONVERT_README.md)** - Format conversion tools
- **[Blog Post](docs/BLOG_POST.md)** - Project overview and use cases

## 🛠️ Core Components

### Workflow System (`workflow.py`)
Unified pipeline that orchestrates the entire process:
- **Auto-discovery**: Finds image files automatically
- **Multi-stage processing**: Handles conversion, description, and export
- **Progress tracking**: Real-time progress monitoring
- **Error resilience**: Continues processing despite individual failures
- **Comprehensive reporting**: Detailed logs and summaries

### Image Describer (`image_describer.py`)
AI-powered image analysis using local Ollama models:
- **Multiple models**: Support for llava, moondream, llama3.2-vision, etc.
- **Custom prompts**: Configurable description prompts
- **Batch processing**: Efficient handling of multiple images
- **EXIF extraction**: Camera settings, GPS, timestamps
- **Memory optimization**: Smart memory management for large collections

### Image Converter (`ConvertImage.py`)
Format conversion utilities with advanced features:
- **Wide format support**: JPEG, PNG, WebP, BMP, TIFF, HEIC/HEIF
- **Quality controls**: Configurable compression and quality settings
- **Metadata preservation**: Maintains EXIF data during conversion
- **Batch operations**: Convert entire directories efficiently

### Video Frame Extractor (`video_frame_extractor.py`)
Extract frames from videos for image analysis:
- **Flexible intervals**: Time-based or frame-based extraction
- **Quality options**: Configurable output resolution and format
- **Multiple formats**: Supports most common video formats
- **Organized output**: Systematic frame numbering and organization

### HTML Gallery Generator (`scripts/descriptions_to_html.py`)
Convert descriptions to beautiful web galleries:
- **Responsive design**: Mobile-friendly layouts
- **Accessibility compliant**: WCAG 2.1 standards
- **Interactive features**: Lightbox, filtering, search
- **Custom styling**: Configurable themes and layouts

## ⚙️ Configuration

Each component has dedicated configuration in the `config/` directory:

- **`workflow_config.json`** - Workflow system settings and processing options
- **`image_describer_config.json`** - AI model selection, prompts, and parameters
- **`video_frame_extractor_config.json`** - Video processing settings and output options

Configuration files use JSON format with comprehensive validation and documentation.

## 🔧 Advanced Usage

### Custom AI Models
```bash
# Install and configure custom Ollama models
ollama pull bakllava:latest
ollama pull moondream:latest

# Update config/image_describer_config.json to use your preferred model
```

### Batch Processing
```bash
# Process entire directory trees
python workflow.py /path/to/images --recursive

# Process with custom configuration
python workflow.py /path/to/images --config custom_config.json

# Process videos and extract frames first
python video_frame_extractor.py /path/to/videos
python workflow.py /path/to/extracted/frames
```

### Integration Examples
```python
# Use components programmatically
from workflow_utils import WorkflowManager
from image_describer import ImageDescriber

# Setup workflow
manager = WorkflowManager('config/workflow_config.json')
results = manager.process_directory('/path/to/images')

# Direct API usage
describer = ImageDescriber('config/image_describer_config.json')
description = describer.describe_image('/path/to/image.jpg')
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Install development dependencies**: `pip install -r requirements.txt`
4. **Run the test suite**: `cd tests && python run_tests.py`
5. **Make your changes**
6. **Ensure all tests pass**: Test suite must show 29/29 tests passing
7. **Update documentation** if needed
8. **Submit a pull request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for new features
- Ensure backward compatibility
- Test with multiple Python versions (3.8+)

## 📋 Requirements

### System Requirements
- **Python 3.8+** - Core runtime environment
- **Ollama** - For AI-powered image descriptions
- **ffmpeg** - For video processing (optional, for video frame extraction)

### Python Dependencies
See `requirements.txt` for the complete list. Key dependencies include:
- `ollama>=0.3.0` - Ollama Python client
- `Pillow>=10.0.0` - Image processing
- `opencv-python>=4.8.0` - Video processing
- `numpy>=1.24.0` - Numerical operations

### Optional Dependencies
- **Nvidia GPU drivers** - For faster AI processing
- **CUDA toolkit** - GPU acceleration (if available)

## 🎯 Use Cases

### Content Creation
- **Website Alt-Text**: Generate accessible descriptions for web images
- **Social Media**: Create engaging captions for posts
- **Documentation**: Catalog and describe image collections
- **SEO Optimization**: Generate keyword-rich image descriptions

### Accessibility
- **Screen Readers**: Provide detailed descriptions for visually impaired users
- **WCAG Compliance**: Meet accessibility standards for web content
- **Educational Content**: Describe diagrams, charts, and visual materials

### Research & Analysis
- **Dataset Analysis**: Process large collections of research images
- **Content Classification**: Categorize images based on descriptions
- **Quality Assessment**: Evaluate image content systematically
- **Metadata Enhancement**: Enrich existing image databases

### Media Processing
- **Video Analysis**: Extract and analyze key frames from videos
- **Format Migration**: Convert legacy image formats to modern standards
- **Batch Processing**: Handle large media libraries efficiently
- **Archive Management**: Organize and describe historical image collections

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team** - For providing excellent local AI model infrastructure
- **Python Community** - For the robust ecosystem of image processing libraries
- **Contributors** - Everyone who has helped improve this toolkit

## 📞 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Check the `docs/` directory for detailed guides
- **Testing**: Run `cd tests && python run_tests.py` to verify your setup
- **Community**: Join discussions in GitHub Discussions

---

**Ready to get started?** Run `cd tests && python run_tests.py` to verify your setup, then try `python workflow.py --help` to see all available options!
