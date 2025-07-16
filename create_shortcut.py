#!/usr/bin/env python3
"""
Desktop Shortcut Creator for Image Description Toolkit

This script creates a desktop shortcut for the GUI application
with the appropriate icon and working directory.
"""

import os
import sys
import winshell
from pathlib import Path
from win32com.client import Dispatch

def create_desktop_shortcut():
    """Create a desktop shortcut for the GUI application"""
    
    # Get the current directory (where the script is located)
    script_dir = Path(__file__).parent.absolute()
    
    # Get the desktop path
    desktop = winshell.desktop()
    
    # Create shortcut path
    shortcut_path = os.path.join(desktop, "Image Description Toolkit.lnk")
    
    # Get Python executable path
    python_exe = sys.executable
    
    # Target script path
    target_script = script_dir / "image_description_gui.py"
    
    # Create the shortcut
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    
    # Set shortcut properties
    shortcut.Targetpath = python_exe
    shortcut.Arguments = f'"{target_script}"'
    shortcut.WorkingDirectory = str(script_dir)
    shortcut.WindowStyle = 1  # Normal window
    shortcut.Description = "Image Description Toolkit - AI-powered image analysis"
    
    # Save the shortcut
    shortcut.save()
    
    print(f"✅ Desktop shortcut created: {shortcut_path}")
    return True

def main():
    """Main function"""
    print("Creating desktop shortcut for Image Description Toolkit...")
    print()
    
    try:
        success = create_desktop_shortcut()
        if success:
            print("✅ Desktop shortcut created successfully!")
            print("You can now double-click the shortcut on your desktop to start the application.")
        else:
            print("❌ Failed to create desktop shortcut")
            return 1
            
    except ImportError as e:
        print("❌ Error: Required Windows modules not available")
        print("Please install with: pip install pywin32 winshell")
        return 1
        
    except Exception as e:
        print(f"❌ Error creating desktop shortcut: {e}")
        return 1
    
    print()
    input("Press Enter to exit...")
    return 0

if __name__ == "__main__":
    sys.exit(main())
