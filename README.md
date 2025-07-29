# Image Description Toolkit

An AI-powered toolkit for generating descriptive text from images using local language models via Ollama. The toolkit now features a unified workflow system that orchestrates the entire pipeline from video frame extraction through HTML report generation, making it simple to process large collections of media files.

## 🚀 Features

- Unified workflow system for end-to-end processing
- AI-powered image descriptions using Ollama models (moondream, llava, llama3.2-vision, etc.)
- Video frame extraction and HEIC to JPG conversion
- Batch and recursive processing for directories
- Comprehensive metadata extraction and HTML report generation
- Robust error handling and professional logging
- Simplified configuration and output structure

## 🛠️ System Requirements

- **Ollama** (for vision model inference): Must be installed and running
- **Python 3.8+**
- All dependencies are installed via a single `requirements.txt`

## 📁 Project Structure

```
Image-Description-Toolkit/
├── workflow.py                # Main workflow orchestrator
├── comprehensive_test.py      # Comprehensive model testing and comparison
├── scripts/                   # Core processing scripts
│   ├── workflow.py
│   ├── video_frame_extractor.py
│   ├── ConvertImage.py
│   ├── image_describer.py
│   ├── descriptions_to_html.py
│   ├── workflow_utils.py
│   ├── workflow_config.json
│   ├── image_describer_config.json
│   └── video_frame_extractor_config.json
├── docs/                      # Documentation
├── tests/                     # Test suite and test files
├── TESTING_GUIDE.md           # Comprehensive testing documentation
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Ollama and a vision model
ollama pull llava:7b  # or moondream, llama3.2-vision, etc.

# 3. Process your media files (videos + images)
python workflow.py path/to/your/media

# 4. Find results in the organized output directory
# -> workflow_output/YYYYMMDD_HHMMSS/
```

## 🦋 Comprehensive Testing

Before processing large collections, use the comprehensive testing system to find the optimal AI model for your needs:

```bash
python comprehensive_test.py path/to/sample/images
```

Generates:
- Interactive HTML report
- CSV data for analysis
- Performance statistics
- Failure analysis

See `TESTING_GUIDE.md` for details.

## 🛠️ Workflow Steps

The workflow system supports:
1. **video**: Extract frames from videos
2. **convert**: Convert HEIC to JPG
3. **describe**: AI-powered image descriptions
4. **html**: Generate HTML reports

Run all steps or any combination:

```bash
python workflow.py media_folder --steps video,describe,html
```

## ⚙️ Configuration

All configuration files are in `scripts/`:
- `workflow_config.json`: Workflow settings
- `image_describer_config.json`: AI model and prompt settings
- `video_frame_extractor_config.json`: Video extraction settings

## 📄 Individual Script Usage

You can use scripts directly for fine-grained control:

```bash
python video_frame_extractor.py path/to/videos
python ConvertImage.py path/to/heic/files --output converted/
python image_describer.py path/to/images --model llava:7b
python descriptions_to_html.py descriptions.txt report.html
```

All scripts now use the organized workflow output structure by default.

## 🦋 Testing

Run the test suite:

```bash
cd tests
python run_tests.py
```

Or test individual components:

```bash
python test_workflow.py
```

## 🤝 Contributing

- Fork the repository
- Create a feature branch
- Install dependencies
- Run tests
- Submit a pull request

See the docs for guidelines.

## 📞 Support & Documentation

- Documentation: `docs/` directory
- Issues: [GitHub Issues](https://github.com/kellylford/Image-Description-Toolkit/issues)
- Discussions: [GitHub Discussions](https://github.com/kellylford/Image-Description-Toolkit/discussions)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Ready to get started?**

```bash
pip install -r requirements.txt
ollama pull llava:7b
python workflow.py path/to/your/media/files
```

The workflow system will handle the rest automatically!
