#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Model Ultimate Prompt Madness Discovery Engine - CORRECTED VERSION

This script extends the Ultimate Prompt Madness framework to test prompts against
multiple AI models simultaneously, enabling cross-model performance comparison
and optimization discovery.

FIXED:
- Uses workflow_output timestamped directories (like workflow.py)
- Proper logging structure
- Safety limits and loop controls
"""

import json
import os
import sys
import time
import logging
import base64
import random
import requests
import statistics
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime
from PIL import Image
import pillow_heif
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Register HEIF opener with PIL
pillow_heif.register_heif_opener()

def setup_logging(output_dir, script_name):
    """Setup logging to workflow_output directory"""
    log_file = output_dir / f'{script_name}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ],
        force=True
    )
    return logging.getLogger(script_name)

@dataclass
class ModelConfig:
    """Configuration for a specific AI model"""
    name: str
    type: str  # 'ollama', 'openai', 'anthropic', 'google', 'custom'
    endpoint: str
    api_key: Optional[str] = None
    model_id: str = ""
    supports_images: bool = True
    max_tokens: int = 1000
    timeout: int = 120
    rate_limit_delay: float = 0.5
    custom_headers: Dict[str, str] = None

class MultiModelPromptMadness:
    def __init__(self, config_path="multi_model_prompt_madness_config.json"):
        """Initialize the multi-model prompt discovery engine"""
        self.config_path = config_path
        self.config = self.load_config()
        
        # Create timestamped output directory in project root (like workflow.py)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("../workflow_output") / f"multi_model_prompt_madness_{timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = setup_logging(self.output_dir, "multi_model_prompt_madness")
        
        # Initialize model configurations
        self.models = self.initialize_models()
        
        # HEIC conversion setup
        self.temp_converted_dir = self.output_dir / "temp_converted"
        self.temp_converted_dir.mkdir(exist_ok=True)
        
        # Statistics tracking per model
        self.stats = {
            "total_experiments": 0,
            "successful_experiments": 0,
            "failed_experiments": 0,
            "unique_prompts_tested": 0,
            "total_descriptions_generated": 0,
            "start_time": time.time(),
            "model_stats": {}
        }
        
        # Initialize model stats
        for model_name in self.config["experiment_config"]["models_to_test"]:
            self.stats["model_stats"][model_name] = {
                "experiments": 0,
                "successes": 0,
                "failures": 0,
                "avg_response_time": 0,
                "total_response_time": 0
            }
        
        self.logger.info(f"🚀 Multi-Model Prompt Madness initialized")
        self.logger.info(f"📁 Output directory: {self.output_dir}")
        self.logger.info(f"🤖 Models configured: {list(self.stats['model_stats'].keys())}")

    def load_config(self):
        """Load the experimental configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load config: {e}")
            sys.exit(1)

    def initialize_models(self):
        """Initialize model configurations"""
        models = {}
        
        # Add Ollama models
        for model_name in self.config["experiment_config"]["models_to_test"]:
            if model_name in ["moondream", "llava", "bakllava"]:
                models[model_name] = ModelConfig(
                    name=model_name,
                    type="ollama",
                    endpoint="http://localhost:11434/api/generate",
                    model_id=model_name
                )
        
        return models

    def discover_all_images(self):
        """Discover ALL available images (same as ultimate_prompt_madness)"""
        self.logger.info("Discovering ALL available images (JPG, PNG, etc. - excluding HEIC)...")
        
        iphone_dir = Path("C:/Users/kelly/GitHub/iPhone")
        if not iphone_dir.exists():
            self.logger.error(f"iPhone directory not found: {iphone_dir}")
            return []
        
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp', '*.gif']
        
        all_images = []
        for ext in extensions:
            all_images.extend(iphone_dir.rglob(ext))
            all_images.extend(iphone_dir.rglob(ext.upper()))
        
        unique_images = list(set(str(img) for img in all_images))
        
        self.logger.info(f"Discovered {len(unique_images)} supported images!")
        
        # Save discovered images
        discovery_file = self.output_dir / "multi_model_discovered_images.json"
        with open(discovery_file, 'w', encoding='utf-8') as f:
            json.dump({"discovered_images": unique_images}, f, indent=2)
        
        return unique_images

    def image_to_base64(self, image_path):
        """Convert image to base64 for API"""
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Failed to encode image {image_path}: {e}")
            return None

    async def get_model_description(self, model_config: ModelConfig, image_path: str, prompt: str, model_settings: dict):
        """Get description from a specific model"""
        start_time = time.time()
        
        try:
            if model_config.type == "ollama":
                return await self.get_ollama_description(model_config, image_path, prompt, model_settings)
            # Add other model types here (OpenAI, Anthropic, etc.)
            else:
                self.logger.warning(f"Model type {model_config.type} not implemented yet")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get description from {model_config.name}: {e}")
            return None
        finally:
            response_time = time.time() - start_time
            model_stats = self.stats["model_stats"][model_config.name]
            model_stats["total_response_time"] += response_time
            model_stats["experiments"] += 1
            if model_stats["experiments"] > 0:
                model_stats["avg_response_time"] = model_stats["total_response_time"] / model_stats["experiments"]

    async def get_ollama_description(self, model_config: ModelConfig, image_path: str, prompt: str, model_settings: dict):
        """Get description from Ollama model"""
        image_b64 = self.image_to_base64(image_path)
        if not image_b64:
            return None
        
        payload = {
            "model": model_config.model_id,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
            **model_settings
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=model_config.timeout)) as session:
            try:
                async with session.post(model_config.endpoint, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        description = result.get("response", "").strip()
                        
                        if description:
                            return {
                                "model": model_config.name,
                                "image_path": str(image_path),
                                "description": description,
                                "timestamp": datetime.now().isoformat(),
                                "metrics": self.calculate_metrics(description)
                            }
                    else:
                        self.logger.error(f"Ollama API error {response.status} for {model_config.name}")
                        
            except asyncio.TimeoutError:
                self.logger.error(f"Timeout for {model_config.name} on {Path(image_path).name}")
            except Exception as e:
                self.logger.error(f"Error with {model_config.name}: {e}")
        
        return None

    def calculate_metrics(self, description):
        """Calculate metrics for a description (same as ultimate_prompt_madness)"""
        words = description.split()
        unique_words = set(words)
        
        return {
            "word_count": len(words),
            "unique_word_count": len(unique_words),
            "character_count": len(description),
            "sentence_count": description.count('.') + description.count('!') + description.count('?'),
            "lexical_diversity": len(unique_words) / len(words) if words else 0,
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0
        }

    async def run_multi_model_experiment(self):
        """Run the multi-model experiment with FIXED loop control"""
        self.logger.info("LAUNCHING MULTI-MODEL PROMPT MADNESS EXPERIMENT!")
        self.logger.info("=" * 60)
        
        # Discover images with safety limits
        all_images = self.discover_all_images()
        if not all_images:
            self.logger.error("No images found!")
            return
        
        # SAFETY LIMITS
        max_safe_images = 100  # Smaller for multi-model testing
        max_images_per_prompt = 20
        
        if len(all_images) > max_safe_images:
            test_images = random.sample(all_images, max_safe_images)
            self.logger.info(f"SAFETY LIMIT: Using {len(test_images)} of {len(all_images)} images")
        else:
            test_images = all_images
        
        # Get experimental prompts
        experimental_prompts = self.config.get("experimental_prompts", {})
        total_prompts = len(experimental_prompts)
        
        self.logger.info(f"Testing {total_prompts} prompts across {len(self.models)} models")
        
        # Process each prompt
        completed_prompts = 0
        for prompt_id, prompt_config in experimental_prompts.items():
            completed_prompts += 1
            self.logger.info(f"PROMPT {completed_prompts}/{total_prompts}: {prompt_id}")
            
            # Limit images per prompt
            prompt_test_images = test_images[:max_images_per_prompt]
            
            # Test across all models
            all_results = {}
            for model_name, model_config in self.models.items():
                self.logger.info(f"  Testing model: {model_name}")
                model_results = []
                
                for i, image_path in enumerate(prompt_test_images, 1):
                    if i % 10 == 0:
                        self.logger.info(f"    Image {i}/{len(prompt_test_images)}")
                    
                    # Get description from this model
                    result = await self.get_model_description(
                        model_config, image_path, prompt_config["prompt"], prompt_config["model_settings"]
                    )
                    
                    if result:
                        result.update({
                            "prompt_name": prompt_id,
                            "prompt_text": prompt_config["prompt"]
                        })
                        model_results.append(result)
                        self.stats["successful_experiments"] += 1
                        self.stats["model_stats"][model_name]["successes"] += 1
                    else:
                        self.stats["failed_experiments"] += 1
                        self.stats["model_stats"][model_name]["failures"] += 1
                    
                    self.stats["total_experiments"] += 1
                    
                    # Rate limiting
                    await asyncio.sleep(model_config.rate_limit_delay)
                
                all_results[model_name] = model_results
                self.logger.info(f"  ✅ {model_name}: {len(model_results)} descriptions")
            
            # Save results for this prompt
            if any(all_results.values()):
                results_file = self.output_dir / f"{prompt_id}_multi_model_results.json"
                with open(results_file, 'w', encoding='utf-8') as f:
                    json.dump({prompt_id: all_results}, f, indent=2, ensure_ascii=False)
                
                total_descriptions = sum(len(results) for results in all_results.values())
                self.logger.info(f"COMPLETED: {prompt_id} - {total_descriptions} total descriptions")
                self.stats["total_descriptions_generated"] += total_descriptions
            
            # Progress update
            self.logger.info(f"PROGRESS: {completed_prompts}/{total_prompts} prompts completed")
        
        self.logger.info("MULTI-MODEL EXPERIMENT COMPLETE!")
        self.print_final_statistics()

    def print_final_statistics(self):
        """Print final statistics"""
        elapsed_time = time.time() - self.stats["start_time"]
        
        self.logger.info("=" * 60)
        self.logger.info("MULTI-MODEL PROMPT MADNESS COMPLETE!")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Experiments: {self.stats['total_experiments']}")
        self.logger.info(f"✅ Successful: {self.stats['successful_experiments']}")
        self.logger.info(f"❌ Failed: {self.stats['failed_experiments']}")
        self.logger.info(f"Total Descriptions: {self.stats['total_descriptions_generated']}")
        self.logger.info(f"⏱️ Total Time: {elapsed_time:.1f} seconds")
        
        self.logger.info("\n📊 MODEL PERFORMANCE:")
        for model_name, stats in self.stats["model_stats"].items():
            success_rate = (stats["successes"] / stats["experiments"] * 100) if stats["experiments"] > 0 else 0
            self.logger.info(f"  {model_name}: {success_rate:.1f}% success, {stats['avg_response_time']:.2f}s avg")
        
        self.logger.info(f"📁 Results Directory: {self.output_dir}")


async def main():
    """Main entry point"""
    print("Multi-Model Prompt Madness Discovery Engine Starting...")
    
    try:
        experiment = MultiModelPromptMadness()
        await experiment.run_multi_model_experiment()
    except KeyboardInterrupt:
        print("🛑 Experiment interrupted by user")
    except Exception as e:
        print(f"💥 Experiment failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
