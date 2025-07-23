#!/usr/bin/env python3
"""
Quick Prompt Discovery - Simplified version for immediate results
"""

import json
import os
import random
import time
from pathlib import Path
from typing import Dict, List
import requests
import base64
from datetime import datetime

def get_valid_images(source_dir: str, max_count: int = 50) -> List[str]:
    """Get valid JPG/JPEG images only (skip HEIC for now)"""
    print(f"🔍 Scanning for images in {source_dir}")
    
    valid_extensions = {'.jpg', '.jpeg', '.png'}
    images = []
    
    source_path = Path(source_dir)
    for ext in valid_extensions:
        found = list(source_path.rglob(f"*{ext}"))
        found.extend(list(source_path.rglob(f"*{ext.upper()}")))
        images.extend(found)
    
    # Convert to strings and filter
    valid_images = []
    for img in images:
        img_str = str(img)
        # Skip temp files and very small files
        try:
            if os.path.getsize(img_str) > 10000:  # At least 10KB
                valid_images.append(img_str)
        except:
            continue
            
    print(f"📸 Found {len(valid_images)} valid images")
    
    # Return random sample
    if len(valid_images) > max_count:
        return random.sample(valid_images, max_count)
    return valid_images

def test_prompt(image_path: str, prompt: str, model_settings: Dict) -> str:
    """Test a single prompt on an image"""
    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
        
        payload = {
            "model": "moondream",
            "prompt": prompt,
            "images": [img_base64],
            "stream": False,
            **model_settings
        }
        
        response = requests.post('http://localhost:11434/api/generate', json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', '').strip()
        
    except Exception as e:
        return f"Error: {str(e)}"

def run_quick_experiment():
    """Run a quick experiment with a few prompts"""
    print("🚀 Starting Quick Prompt Discovery Experiment")
    print("=" * 50)
    
    # Get test images
    test_images = get_valid_images("C:\\Users\\kelly\\GitHub\\iPhone", 10)
    if not test_images:
        print("❌ No valid images found")
        return
        
    print(f"🎯 Testing with {len(test_images)} images")
    
    # Define a few key prompts to test
    prompts = {
        "current_default": {
            "prompt": "Describe this image in detail, including main subjects/objects, setting/environment, key colors and lighting, and notable activities or composition. Keep it comprehensive and informative for metadata.",
            "settings": {"temperature": 0.1, "num_predict": 400, "top_k": 40, "top_p": 0.9}
        },
        "technical_quality": {
            "prompt": "Analyze the technical quality of this image objectively. Is the image sharp and in focus or blurry? Is the exposure correct (not too bright/dark)? Is the horizon or main subject level, or tilted? Are there visible camera shake or motion blur issues? What is the overall image clarity and detail quality? Provide factual technical observations only.",
            "settings": {"temperature": 0.1, "num_predict": 300, "top_k": 30, "top_p": 0.8}
        },
        "color_analysis": {
            "prompt": "Provide a rich, detailed analysis of all colors in this image. Describe dominant colors and their specific shades (not just 'blue' but 'deep navy blue', 'sky blue', etc.), color relationships and harmonies, how colors are distributed across the image, lighting color temperature (warm/cool), and color saturation levels. Focus entirely on the color palette and visual characteristics.",
            "settings": {"temperature": 0.3, "num_predict": 400, "top_k": 50, "top_p": 0.95}
        },
        "social_media": {
            "prompt": "Analyze this image for social media potential. Provide a brief, engaging description of what's shown, identify visual appeal factors (composition, colors, subject matter), evaluate shareability elements, estimate the 'wow factor' or visual impact on a scale of 1-10, and suggest what mood or vibe this would have for posting. Balance descriptive content with engagement assessment.",
            "settings": {"temperature": 0.4, "num_predict": 350, "top_k": 60, "top_p": 0.9}
        }
    }
    
    # Results storage
    results = {}
    
    # Test each prompt on each image
    for prompt_name, prompt_config in prompts.items():
        print(f"\n🧪 Testing prompt: {prompt_name}")
        prompt_results = []
        
        for i, img_path in enumerate(test_images):
            print(f"  📸 Image {i+1}/{len(test_images)}: {Path(img_path).name}")
            
            description = test_prompt(
                img_path,
                prompt_config["prompt"], 
                prompt_config["settings"]
            )
            
            result = {
                'image_path': img_path,
                'description': description,
                'word_count': len(description.split()),
                'char_count': len(description),
                'timestamp': datetime.now().isoformat()
            }
            
            prompt_results.append(result)
            time.sleep(1)  # Rate limiting
            
        results[prompt_name] = prompt_results
        
        # Show quick stats
        word_counts = [r['word_count'] for r in prompt_results if not r['description'].startswith('Error')]
        if word_counts:
            avg_words = sum(word_counts) / len(word_counts)
            print(f"  📊 Average words: {avg_words:.1f}")
    
    # Save results
    os.makedirs("prompt_experiments", exist_ok=True)
    with open("prompt_experiments/quick_experiment_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate simple report
    print("\n📋 QUICK EXPERIMENT RESULTS")
    print("=" * 40)
    
    for prompt_name, prompt_results in results.items():
        successful_results = [r for r in prompt_results if not r['description'].startswith('Error')]
        if successful_results:
            word_counts = [r['word_count'] for r in successful_results]
            avg_words = sum(word_counts) / len(word_counts)
            print(f"\n🎯 {prompt_name.upper()}")
            print(f"   Success rate: {len(successful_results)}/{len(prompt_results)}")
            print(f"   Average words: {avg_words:.1f}")
            
            # Show sample description
            if successful_results:
                sample = successful_results[0]['description'][:200]
                print(f"   Sample: {sample}{'...' if len(successful_results[0]['description']) > 200 else ''}")
    
    print(f"\n✅ Quick experiment complete! Results saved to prompt_experiments/quick_experiment_results.json")

if __name__ == "__main__":
    run_quick_experiment()
