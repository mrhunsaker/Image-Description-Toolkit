#!/usr/bin/env python3
"""
Test script to verify GUI functionality

This script performs basic checks before launching the GUI to ensure
all components are working correctly.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import PyQt6
        print("✅ PyQt6 imported successfully")
    except ImportError as e:
        print(f"❌ PyQt6 import failed: {e}")
        return False
    
    try:
        from image_describer import ImageDescriber
        print("✅ ImageDescriber imported successfully")
    except ImportError as e:
        print(f"❌ ImageDescriber import failed: {e}")
        return False
        
    try:
        from html_converter import DescriptionsToHTML
        print("✅ HTML converter imported successfully")
    except ImportError as e:
        print(f"❌ HTML converter import failed: {e}")
        return False
        
    try:
        from ConvertImage import convert_heic_to_jpg
        print("✅ HEIC converter imported successfully")
    except ImportError as e:
        print(f"❌ HEIC converter import failed: {e}")
        return False
        
    return True

def test_ollama():
    """Test Ollama connection"""
    print("\nTesting Ollama connection...")
    
    try:
        import ollama
        
        # Test basic connection
        print("Attempting to connect to Ollama...")
        response = ollama.list()
        
        print(f"Raw Ollama response: {response}")
        print(f"Response type: {type(response)}")
        
        # Parse response safely
        if hasattr(response, 'models'):
            # New Ollama client returns an object with .models attribute
            models_list = response.models
        elif isinstance(response, dict):
            models_list = response.get('models', [])
        elif isinstance(response, list):
            models_list = response
        else:
            # Try to get models attribute
            try:
                models_list = getattr(response, 'models', [])
            except AttributeError:
                print(f"❌ Unexpected response format: {type(response)}")
                return False
        
        print(f"Models list: {models_list}")
        
        # Extract model names
        available_models = []
        for model in models_list:
            model_name = None
            
            # Handle different model object types
            if hasattr(model, 'name'):
                model_name = model.name
            elif hasattr(model, 'model'):
                model_name = model.model
            elif isinstance(model, dict):
                model_name = model.get('name') or model.get('model') or model.get('id')
            elif isinstance(model, str):
                model_name = model
            
            if model_name:
                available_models.append(model_name)
                print(f"Found model: {model_name}")
        
        if available_models:
            print(f"✅ Ollama is running with {len(available_models)} models:")
            for model in available_models:
                print(f"   - {model}")
        else:
            print("⚠️  Ollama is running but no models are installed")
            print("   Install a vision model with: ollama pull moondream")
            
        return True
        
    except ImportError:
        print("❌ Ollama Python package not installed")
        print("   Install with: pip install ollama")
        return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("   Please ensure Ollama is installed and running")
        print("   Try: ollama serve")
        return False

def test_config():
    """Test configuration file"""
    print("\nTesting configuration...")
    
    config_path = Path("config.json")
    if config_path.exists():
        try:
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            print("✅ Configuration file loaded successfully")
            
            # Check for required sections
            if 'model_settings' in config:
                print("✅ Model settings found")
            if 'prompt_variations' in config:
                print("✅ Prompt variations found")
                
            return True
            
        except Exception as e:
            print(f"❌ Configuration file error: {e}")
            return False
    else:
        print("⚠️  Configuration file not found, will use defaults")
        return True

def main():
    """Main test function"""
    print("Image Description Toolkit - GUI Test\n")
    
    success = True
    
    # Test imports
    success &= test_imports()
    
    # Test Ollama
    success &= test_ollama()
    
    # Test config
    success &= test_config()
    
    print("\n" + "="*50)
    
    if success:
        print("✅ All tests passed! GUI should work correctly.")
        
        # Ask if user wants to launch GUI
        try:
            launch = input("\nLaunch GUI now? (y/N): ").strip().lower()
            if launch == 'y':
                print("Launching GUI...")
                from image_description_gui import main as gui_main
                return gui_main()
        except KeyboardInterrupt:
            print("\nExiting...")
            return 0
    else:
        print("❌ Some tests failed. Please fix the issues before running the GUI.")
        print("\nCommon solutions:")
        print("1. Install dependencies: pip install -r gui_requirements.txt")
        print("2. Install Ollama: https://ollama.com")
        print("3. Install a vision model: ollama pull moondream")
        
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
