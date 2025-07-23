#!/usr/bin/env python3
"""Quick test to check available models"""

import requests
import os

print("MULTI-MODEL SETUP CHECK")
print("=" * 30)

# Check Ollama
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"✅ Ollama running with {len(models)} models:")
        for model in models:
            print(f"   - {model['name']}")
    else:
        print("❌ Ollama not responding properly")
except Exception as e:
    print(f"❌ Ollama error: {e}")

# Check API keys
print(f"\nAPI Keys:")
print(f"OpenAI: {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
print(f"Anthropic: {'✅' if os.getenv('ANTHROPIC_API_KEY') else '❌'}")
print(f"Google: {'✅' if os.getenv('GOOGLE_API_KEY') else '❌'}")
