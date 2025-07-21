#!/usr/bin/env python3
"""
Ollama Debug Script

This script helps debug Ollama connection issues by testing different
ways to interact with the Ollama API.
"""

import sys
import json

def test_ollama_connection():
    """Test Ollama connection in detail"""
    
    print("Ollama Debug Script")
    print("=" * 40)
    
    # Test 1: Import ollama
    print("\n1. Testing ollama import...")
    try:
        import ollama
        print("✅ Successfully imported ollama")
    except ImportError as e:
        print(f"❌ Failed to import ollama: {e}")
        print("Install with: pip install ollama")
        return False
    
    # Test 2: Basic connection
    print("\n2. Testing basic connection...")
    try:
        # Try to get server info
        response = ollama.list()
        print(f"✅ Got response from Ollama")
        print(f"Response type: {type(response)}")
        print(f"Response content: {response}")
    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        print("Make sure Ollama is running with: ollama serve")
        return False
    
    # Test 3: Parse models
    print("\n3. Parsing models...")
    try:
        models_list = []
        
        # Handle different response formats
        if hasattr(response, 'models'):
            # New Ollama client returns an object with .models attribute
            models_list = response.models
            print(f"Found response.models with {len(models_list)} entries")
        elif isinstance(response, dict):
            models_list = response.get('models', [])
            print(f"Found 'models' key with {len(models_list)} entries")
        elif isinstance(response, list):
            models_list = response
            print(f"Response is a list with {len(models_list)} entries")
        else:
            # Try to get models attribute
            try:
                models_list = getattr(response, 'models', [])
                print(f"Found models attribute with {len(models_list)} entries")
            except AttributeError:
                print(f"❌ Unexpected response format: {type(response)}")
                print(f"Available attributes: {dir(response) if hasattr(response, '__dict__') else 'N/A'}")
                return False
        
        print(f"Models list: {models_list}")
        print(f"Models list type: {type(models_list)}")
        
        # Parse individual models
        available_models = []
        for i, model in enumerate(models_list):
            print(f"\nModel {i+1}:")
            print(f"  Type: {type(model)}")
            print(f"  Content: {model}")
            
            model_name = None
            
            # Handle different model object types
            if hasattr(model, 'name'):
                model_name = model.name
                print(f"  Found name attribute: {model_name}")
            elif hasattr(model, 'model'):
                model_name = model.model
                print(f"  Found model attribute: {model_name}")
            elif isinstance(model, dict):
                print(f"  Keys: {list(model.keys()) if hasattr(model, 'keys') else 'N/A'}")
                
                # Try different possible key names
                for key in ['name', 'model', 'id', 'title']:
                    if key in model:
                        model_name = model[key]
                        print(f"  Found name in '{key}': {model_name}")
                        break
                        
            elif isinstance(model, str):
                model_name = model
                print(f"  String model: {model}")
            else:
                print(f"  Unknown model type, trying attributes...")
                print(f"  Attributes: {dir(model) if hasattr(model, '__dict__') else 'N/A'}")
            
            if model_name:
                available_models.append(model_name)
            else:
                print(f"  ❌ No name found for this model")
        
        print(f"\n4. Final results:")
        print(f"Available models: {available_models}")
        
        if available_models:
            print(f"✅ Found {len(available_models)} models:")
            for model in available_models:
                print(f"   - {model}")
        else:
            print("⚠️  No models found")
            print("Install a vision model with: ollama pull moondream")
            
    except Exception as e:
        print(f"❌ Error parsing models: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Test specific model
    print("\n5. Testing specific model...")
    if available_models:
        test_model = available_models[0]
        print(f"Testing model: {test_model}")
        
        try:
            # Try to get model info
            print(f"Attempting to use model: {test_model}")
            # Don't actually call the model, just verify it exists
            print(f"✅ Model {test_model} appears to be available")
        except Exception as e:
            print(f"❌ Error with model {test_model}: {e}")
    
    print("\n" + "=" * 40)
    print("Debug complete!")
    return True

if __name__ == "__main__":
    success = test_ollama_connection()
    
    if not success:
        print("\nTroubleshooting steps:")
        print("1. Install Ollama: https://ollama.com")
        print("2. Start Ollama: ollama serve")
        print("3. Install a vision model: ollama pull moondream")
        print("4. Install Python package: pip install ollama")
    
    input("\nPress Enter to exit...")
