#!/usr/bin/env python3
"""
Run Complete Test Suite

This script sets up test files and runs the comprehensive test suite.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the complete test setup and execution"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print("🧪 Image Description Toolkit - Complete Test Suite")
    print("=" * 60)
    
    # Step 1: Generate test images
    print("\n1️⃣ Generating test images...")
    try:
        result = subprocess.run([sys.executable, "generate_test_images.py"], 
                              cwd=script_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Test images generated successfully")
        else:
            print(f"⚠️ Warning: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Warning: Could not generate test images: {e}")
    
    # Step 2: Run comprehensive tests
    print("\n2️⃣ Running comprehensive tests...")
    
    # Determine test mode based on available dependencies
    try:
        import ollama
        import cv2
        print("📋 Full mode: All dependencies available")
        cmd = [sys.executable, "comprehensive_test.py", "--verbose"]
    except ImportError:
        print("📋 Quick mode: Some dependencies missing")
        cmd = [sys.executable, "comprehensive_test.py", "--quick", "--verbose"]
    
    # Run tests from the tests directory
    try:
        result = subprocess.run(cmd, cwd=script_dir)
        return result.returncode
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
