#!/usr/bin/env python3
"""
Quick validation test - single image, single model
"""
import json
import requests
import base64
from pathlib import Path

def quick_test():
    # Find test images
    test_files_dir = Path("../tests/test_files/images")
    if test_files_dir.exists():
        images = list(test_files_dir.glob("*.jpg")) + list(test_files_dir.glob("*.png"))
        if images:
            test_image = images[0]
            print(f"🧪 Quick Test: {test_image.name}")
            
            # Encode image
            with open(test_image, 'rb') as f:
                image_b64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Test API call
            payload = {
                "model": "moondream",
                "prompt": "Describe this image briefly.",
                "images": [image_b64],
                "stream": False
            }
            
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                description = result.get("response", "").strip()
                print(f"✅ Success: {description[:100]}...")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                return False
    
    print("❌ No test images found")
    return False

if __name__ == "__main__":
    success = quick_test()
    print(f"\nReady for Ultimate Prompt Madness: {'YES' if success else 'NO'}")
