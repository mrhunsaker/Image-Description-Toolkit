# Image Description Toolkit - Windows GUI Application

A comprehensive Windows GUI application for AI-powered image analysis, built with PyQt6 and full accessibility support.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
1. **Run the setup script**:
   - Double-click `run_gui.bat` (for Command Prompt)
   - Or right-click `run_gui.ps1` → "Run with PowerShell"

### Option 2: Manual Setup
1. **Install dependencies**:
   ```bash
   pip install -r gui_requirements.txt
   ```

2. **Run the GUI**:
   ```bash
   python image_description_gui.py
   ```

## 📋 Prerequisites

- **Python 3.8+** - Download from [python.org](https://python.org)
- **Ollama** - Download from [ollama.com](https://ollama.com)
- **Vision Model** - Install with: `ollama pull moondream`

## 🖥️ GUI Features

### Main Tabs

#### 1. **Image Processing**
- **Folder Selection**: Browse and select folders containing images
- **Recursive Processing**: Process subdirectories automatically
- **AI Model Selection**: Choose from moondream, llama3.2-vision, llava, etc.
- **Description Styles**: detailed, concise, artistic, technical, colorful
- **Real-time Progress**: Progress bars and status updates
- **Batch Processing**: Handle multiple images efficiently

#### 2. **HEIC Conversion**
- **Batch HEIC to JPG**: Convert Apple HEIC files to JPG
- **Quality Control**: Adjustable JPEG quality (1-100)
- **Folder Processing**: Convert entire folders at once
- **Progress Tracking**: Real-time conversion progress

#### 3. **HTML Gallery**
- **Web Gallery Generation**: Create beautiful HTML galleries
- **Metadata Options**: Include or exclude full metadata
- **Live Preview**: Preview generated HTML in browser
- **Responsive Design**: Works on desktop and mobile

#### 4. **Settings**
- **Model Information**: View available AI models
- **Processing Options**: Configure image size, batch delays
- **Persistent Settings**: Automatically saves your preferences

### 🎯 Accessibility Features

This application is designed for **full accessibility** with:

- **Screen Reader Support**: Compatible with NVDA, JAWS, Windows Narrator
- **Keyboard Navigation**: All functions accessible via keyboard
- **High Contrast Support**: Works with Windows high contrast modes
- **Focus Management**: Logical tab order and focus indicators
- **Accessible Descriptions**: All controls properly labeled

### ⌨️ Keyboard Shortcuts

- **Ctrl+O**: Open folder
- **Ctrl+P**: Start processing
- **Escape**: Stop processing
- **F1**: Show help
- **Ctrl+Q**: Exit application

## 🔧 Technical Details

### Architecture
- **Frontend**: PyQt6 with accessibility APIs
- **Backend**: Your existing Python modules (unchanged)
- **Threading**: Background processing to prevent UI freezing
- **Settings**: Persistent configuration storage

### File Structure
```
Image-Description-Toolkit/
├── image_description_gui.py    # Main GUI application
├── html_converter.py           # HTML conversion wrapper
├── gui_requirements.txt        # GUI dependencies
├── run_gui.bat                 # Windows batch setup
├── run_gui.ps1                 # PowerShell setup
├── GUI_README.md              # This file
├── image_describer.py         # Original image processing (unchanged)
├── descriptions_to_html.py    # Original HTML converter (unchanged)
├── ConvertImage.py            # Original HEIC converter (unchanged)
├── config.json                # Configuration file (unchanged)
└── requirements.txt           # Original dependencies (unchanged)
```

## 🛠️ Usage Guide

### Processing Images

1. **Select Images**:
   - Click "Browse..." to select a folder
   - Check "Process subdirectories recursively" if needed

2. **Configure Processing**:
   - Choose AI model (moondream recommended)
   - Select description style
   - Review settings in Settings tab

3. **Start Processing**:
   - Click "Start Processing"
   - Monitor progress in real-time
   - View results in the results panel

### Converting HEIC Files

1. **Select Input Folder**: Folder containing HEIC files
2. **Select Output Folder**: Where JPG files will be saved
3. **Adjust Quality**: Use slider to set JPEG quality (95 recommended)
4. **Start Conversion**: Click "Start Conversion"

### Generating HTML Gallery

1. **Select Description File**: Choose the `image_descriptions.txt` file
2. **Choose Output Location**: Where to save the HTML gallery
3. **Configure Options**: Include full metadata if desired
4. **Generate**: Click "Generate HTML Gallery"
5. **Preview**: Click "Preview HTML" to view in browser

## 🔍 Troubleshooting

### Common Issues

**"Python is not installed"**
- Install Python 3.8+ from [python.org](https://python.org)
- Ensure Python is added to PATH during installation

**"Ollama is not running"**
- Start Ollama application
- Install a vision model: `ollama pull moondream`
- Verify Ollama is accessible at `http://localhost:11434`

**"Ollama error: 'name'" or similar model errors**
- Run `python debug_ollama.py` to diagnose the issue
- Ensure Ollama is running: `ollama serve`
- Check installed models: `ollama list`
- Install a vision model: `ollama pull moondream`

**"Unexpected response format from Ollama: <class 'ollama._types.ListResponse'>"**
- This indicates a version mismatch in the Ollama Python client
- Update the Ollama package: `pip install --upgrade ollama`
- Or downgrade if needed: `pip install ollama==0.1.7`
- Run `python debug_ollama.py` to test the connection

**"Failed to install dependencies"**
- Check internet connection
- Try: `pip install --upgrade pip`
- Run as administrator if needed

**"No supported image files found"**
- Ensure folder contains JPG, PNG, BMP, TIFF, or WebP files
- Check file extensions are standard

### Debug Tools

**Quick Test Everything**
- Run `quick_test.bat` for automated testing
- Run `python test_gui.py` for detailed diagnostics

**Ollama-Specific Issues**
- Run `python debug_ollama.py` for detailed Ollama debugging
- Check console output for detailed error messages

### Getting Help

- **In-app Help**: Press F1 or use Help menu
- **Error Messages**: Check the results panels for detailed error information
- **Logs**: Console output shows detailed processing information

## 🎨 Customization

### Themes
The GUI automatically adapts to your Windows theme (light/dark mode).

### Settings
All settings are automatically saved and restored:
- Window size and position
- Selected model and prompt style
- Processing options
- File paths

### Model Configuration
Edit `config.json` to:
- Add new prompt styles
- Configure model parameters
- Adjust processing options

## 🔒 Privacy & Security

- **Local Processing**: All AI processing happens locally via Ollama
- **No Data Transmission**: Images never leave your computer
- **Secure Storage**: Settings stored in Windows standard locations
- **No Telemetry**: No usage data collected or transmitted

## 📦 Dependencies

### Core GUI Dependencies
- `PyQt6>=6.6.0` - Modern Qt6 GUI framework
- `qtawesome>=1.3.0` - Icon library
- `darkdetect>=0.8.0` - Dark theme detection

### Image Processing Dependencies
- `ollama>=0.3.0` - Ollama API client
- `pillow>=10.0.0` - Image processing
- `requests>=2.31.0` - HTTP requests
- `pillow-heif>=0.13.0` - HEIC support

## 🤝 Integration with Existing Scripts

The GUI application **does not modify** your existing Python scripts:

- `image_describer.py` - Used as-is for image processing
- `descriptions_to_html.py` - Used as-is for HTML generation  
- `ConvertImage.py` - Used as-is for HEIC conversion
- `config.json` - Used as-is for configuration

You can continue using the command-line scripts alongside the GUI application.

## 📋 System Requirements

- **OS**: Windows 10/11 (64-bit recommended)
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for models and processing
- **Display**: 1024x768 minimum resolution

## 📝 License

This GUI application follows the same license as the original Image Description Toolkit.

## 🙏 Acknowledgments

Built with:
- **PyQt6** - Cross-platform GUI framework
- **Your existing codebase** - Excellent foundation for AI image processing
- **Ollama** - Local AI model serving
- **Accessibility standards** - WCAG 2.1 compliance
