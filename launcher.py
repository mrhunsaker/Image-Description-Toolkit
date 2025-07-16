#!/usr/bin/env python3
"""
Simple Launcher for Image Description Toolkit GUI

This script provides a simple way to launch the GUI application
with proper error handling and user feedback.
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher function"""
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    gui_script = script_dir / "image_description_gui.py"
    
    # Check if the GUI script exists
    if not gui_script.exists():
        print("❌ Error: GUI script not found!")
        print(f"Expected location: {gui_script}")
        print("Please ensure all files are in the same directory.")
        input("Press Enter to exit...")
        return 1
    
    # Check if required modules are available
    try:
        print("🔍 Checking dependencies...")
        
        # Check PyQt6
        import PyQt6
        print("✅ PyQt6 found")
        
        # Check our modules
        from image_describer import ImageDescriber
        print("✅ Image describer module found")
        
        from html_converter import DescriptionsToHTML
        print("✅ HTML converter module found")
        
        from ConvertImage import convert_heic_to_jpg
        print("✅ HEIC converter module found")
        
        print("✅ All dependencies available!")
        print()
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print()
        print("Please install required dependencies:")
        print("  pip install -r gui_requirements.txt")
        print()
        print("Or run the setup script:")
        print("  run_gui.bat")
        input("Press Enter to exit...")
        return 1
    
    # Launch the GUI application
    try:
        print("🚀 Starting Image Description Toolkit GUI...")
        print()
        
        # Import and run the GUI
        from image_description_gui import main as gui_main
        return gui_main()
        
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        print()
        print("Please check the error message above and ensure:")
        print("1. Python 3.8+ is installed")
        print("2. All dependencies are installed")
        print("3. All files are in the same directory")
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
