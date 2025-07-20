#!/usr/bin/env python3
"""
Workflow System Test

This script tests the workflow system components to ensure everything is working correctly.
Run this after installing dependencies to verify the system is properly set up.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from workflow_utils import WorkflowConfig, WorkflowLogger, FileDiscovery
        print("✅ Workflow utilities import successful")
    except ImportError as e:
        print(f"❌ Workflow utilities import failed: {e}")
        return False
    
    try:
        import ollama
        print("✅ Ollama import successful")
    except ImportError as e:
        print(f"❌ Ollama import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL import successful")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV import successful")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    return True

def test_workflow_config():
    """Test workflow configuration loading"""
    print("\nTesting workflow configuration...")
    
    try:
        from workflow_utils import WorkflowConfig
        config = WorkflowConfig()
        
        print(f"✅ Config loaded successfully")
        print(f"   Base output dir: {config.base_output_dir}")
        print(f"   Video step enabled: {config.is_step_enabled('video_extraction')}")
        print(f"   Image patterns: {config.get_file_patterns('images')}")
        
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_file_discovery():
    """Test file discovery functionality"""
    print("\nTesting file discovery...")
    
    try:
        from workflow_utils import WorkflowConfig, FileDiscovery
        config = WorkflowConfig()
        discovery = FileDiscovery(config)
        
        # Test with current directory
        current_dir = Path(".")
        categories = discovery.categorize_files(current_dir, recursive=False)
        
        print(f"✅ File discovery successful")
        print(f"   Python files found: {len([f for f in current_dir.glob('*.py')])}")
        print(f"   Image patterns supported: {len(config.get_file_patterns('images'))}")
        
        return True
    except Exception as e:
        print(f"❌ File discovery test failed: {e}")
        return False

def test_workflow_script():
    """Test that the workflow script can be executed"""
    print("\nTesting workflow script...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "workflow.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Workflow Steps:" in result.stdout:
            print("✅ Workflow script executable and help works")
            return True
        else:
            print(f"❌ Workflow script help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Workflow script test failed: {e}")
        return False

def test_individual_scripts():
    """Test that individual scripts still work"""
    print("\nTesting individual script compatibility...")
    
    scripts_to_test = [
        ("image_describer.py", "Process images with Ollama"),
        ("video_frame_extractor.py", "Extract frames from video"),
        ("ConvertImage.py", "Convert HEIC"),
        ("descriptions_to_html.py", "Convert image descriptions")
    ]
    
    all_passed = True
    
    for script, expected_text in scripts_to_test:
        try:
            import subprocess
            result = subprocess.run([sys.executable, script, "--help"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and expected_text.lower() in result.stdout.lower():
                print(f"✅ {script} works correctly")
            else:
                print(f"❌ {script} help failed")
                all_passed = False
        except Exception as e:
            print(f"❌ {script} test failed: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("Image Description Toolkit - Workflow System Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_workflow_config,
        test_file_discovery,
        test_workflow_script,
        test_individual_scripts
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! The workflow system is ready to use.")
        print("\nNext steps:")
        print("1. Ensure Ollama is running: ollama serve")
        print("2. Install a vision model: ollama pull moondream")
        print("3. Try the workflow: python workflow.py --help")
        print("4. See WORKFLOW_README.md for complete documentation")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Install Ollama: https://ollama.com/")
        print("- Check Python version (3.8+ required)")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
