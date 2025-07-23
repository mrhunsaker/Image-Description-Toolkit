#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate Prompt Madness Discovery Engine - CORRECTED VERSION

This script unleashes maximum AI creativity on prompt discovery using ALL available images,
extreme parameter variations, and wild experimental prompt combinations.

FIXED:
- Uses workflow_output timestamped directories (like workflow.py)
- Proper logging structure
- Loop control fixes to prevent runaway experiments
- Safety limits for large-scale experiments
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
from pathlib import Path
from datetime import datetime
from PIL import Image
import pillow_heif

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

class UltimatePromptMadness:
    def __init__(self, config_path="ultimate_prompt_madness_config.json"):
        """Initialize the ultimate prompt discovery engine"""
        self.config_path = config_path
        self.config = self.load_config()
        
        # Create timestamped output directory in project root (like workflow.py)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path("../workflow_output") / f"ultimate_prompt_madness_{timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = setup_logging(self.output_dir, "ultimate_prompt_madness")
        
        # HEIC conversion setup
        self.temp_converted_dir = self.output_dir / "temp_converted"
        self.temp_converted_dir.mkdir(exist_ok=True)
        
        # Statistics tracking
        self.stats = {
            "total_experiments": 0,
            "successful_experiments": 0,
            "failed_experiments": 0,
            "heic_conversions": 0,
            "unique_prompts_tested": 0,
            "total_descriptions_generated": 0,
            "start_time": time.time()
        }
        
        self.logger.info(f"🚀 Ultimate Prompt Madness initialized")
        self.logger.info(f"📁 Output directory: {self.output_dir}")

    def load_config(self):
        """Load the experimental configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load config: {e}")
            sys.exit(1)

    def discover_all_images(self):
        """Discover ALL available images from the iPhone directory (excluding HEIC/video formats)"""
        self.logger.info("Discovering ALL available images (JPG, PNG, etc. - excluding HEIC)...")
        
        iphone_dir = Path("C:/Users/kelly/GitHub/iPhone")
        if not iphone_dir.exists():
            self.logger.error(f"iPhone directory not found: {iphone_dir}")
            return []
        
        # Image extensions to search for (excluding HEIC and video formats)
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp', '*.gif']
        
        all_images = []
        for ext in extensions:
            all_images.extend(iphone_dir.rglob(ext))
            all_images.extend(iphone_dir.rglob(ext.upper()))
        
        # Remove duplicates and convert to strings
        unique_images = list(set(str(img) for img in all_images))
        
        self.logger.info(f"Discovered {len(unique_images)} supported images (excluding HEIC)!")
        
        # Save discovered images for reproducibility
        discovery_file = self.output_dir / "ultimate_discovered_images.json"
        with open(discovery_file, 'w', encoding='utf-8') as f:
            json.dump({"discovered_images": unique_images}, f, indent=2)
        
        return unique_images

    def image_to_base64(self, image_path):
        """Convert image to base64 for API (no HEIC conversion needed)"""
        try:
            with open(image_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Failed to encode image {image_path}: {e}")
            return None

    def get_ollama_description(self, image_path, prompt, model_settings):
        """Get description from Ollama API with enhanced error handling"""
        try:
            image_b64 = self.image_to_base64(image_path)
            if not image_b64:
                self.logger.error(f"Failed to encode image: {image_path}")
                return None
            
            payload = {
                "model": "moondream",
                "prompt": prompt,
                "images": [image_b64],
                "stream": False,
                **model_settings
            }
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                description = result.get("response", "").strip()
                
                if description:
                    metrics = self.calculate_metrics(description)
                    return {
                        "image_path": str(image_path),
                        "description": description,
                        "timestamp": datetime.now().isoformat(),
                        "metrics": metrics
                    }
                else:
                    self.logger.warning(f"Empty description returned for {image_path}")
            else:
                self.logger.error(f"❌ Ollama API error {response.status_code}: {response.text}")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to get description for {image_path}: {e}")
        
        return None

    def calculate_metrics(self, description):
        """Calculate comprehensive metrics for a description"""
        words = description.split()
        unique_words = set(words)
        
        return {
            "word_count": len(words),
            "unique_word_count": len(unique_words),
            "character_count": len(description),
            "sentence_count": description.count('.') + description.count('!') + description.count('?'),
            "lexical_diversity": len(unique_words) / len(words) if words else 0,
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "creativity_score": self.calculate_creativity_score(description),
            "technical_depth": self.calculate_technical_depth(description),
            "emotional_resonance": self.calculate_emotional_resonance(description)
        }

    def calculate_creativity_score(self, description):
        """Calculate a creativity score based on vocabulary variety and imagery"""
        creative_words = [
            'vivid', 'striking', 'ethereal', 'luminous', 'transcendent', 'mesmerizing',
            'captivating', 'enigmatic', 'surreal', 'haunting', 'breathtaking', 'mystical'
        ]
        score = sum(1 for word in creative_words if word.lower() in description.lower())
        return min(score / 5.0, 1.0)

    def calculate_technical_depth(self, description):
        """Calculate technical depth score"""
        technical_terms = [
            'exposure', 'aperture', 'focus', 'depth of field', 'bokeh', 'composition',
            'lighting', 'shadows', 'highlights', 'contrast', 'saturation', 'hue'
        ]
        score = sum(1 for term in technical_terms if term.lower() in description.lower())
        return min(score / 8.0, 1.0)

    def calculate_emotional_resonance(self, description):
        """Calculate emotional resonance score"""
        emotional_words = [
            'peaceful', 'serene', 'joyful', 'melancholy', 'dramatic', 'intense',
            'calm', 'energetic', 'warm', 'cool', 'inviting', 'mysterious'
        ]
        score = sum(1 for word in emotional_words if word.lower() in description.lower())
        return min(score / 6.0, 1.0)

    def generate_creative_prompt_mutations(self, base_prompt, mutation_type="creative"):
        """Generate creative mutations of prompts"""
        mutations = []
        
        if mutation_type == "creative":
            prefixes = [
                "Imagine you are a time traveler from 2087 analyzing this ancient image:",
                "Analyzing as if this image contains hidden messages from the future:",
            ]
            
            suffixes = [
                "Write your analysis as if it will be read by beings who have never seen images.",
                "Explain what this image teaches about the nature of consciousness and reality."
            ]
            
            for prefix in prefixes:
                for suffix in suffixes:
                    mutations.append(f"{prefix}\n\n{base_prompt}\n\n{suffix}")
        
        return mutations

    def test_prompt_with_chaos(self, image_path, prompt_name, prompt_config):
        """Test a prompt with chaos mode enhancements"""
        results = []
        base_prompt = prompt_config["prompt"]
        model_settings = prompt_config["model_settings"].copy()
        
        # Chaos mode: Random parameter injection
        if self.config.get("experimental_settings", {}).get("chaos_mode", {}).get("enabled", False):
            if self.config["experimental_settings"]["chaos_mode"].get("random_parameter_injection", False):
                # Randomly modify parameters within ranges
                model_settings["temperature"] = random.choice([0.01, 0.1, 0.2, 0.3, 0.4, 0.5])
                model_settings["top_k"] = random.choice([20, 40, 60, 80, 100])
                model_settings["top_p"] = random.choice([0.7, 0.8, 0.9, 0.95, 0.99])
            
            # Creative prompt mutations
            if self.config["experimental_settings"]["chaos_mode"].get("creative_prompt_mutations", False):
                prompt_mutations = self.generate_creative_prompt_mutations(base_prompt, "creative")
                
                # Test original + 2 random mutations (limited for safety)
                prompts_to_test = [base_prompt] + random.sample(prompt_mutations, min(2, len(prompt_mutations)))
            else:
                prompts_to_test = [base_prompt]
        else:
            prompts_to_test = [base_prompt]
        
        # Test each prompt variation
        for i, prompt in enumerate(prompts_to_test):
            variation_name = f"{prompt_name}_variation_{i}" if i > 0 else prompt_name
            result = self.get_ollama_description(image_path, prompt, model_settings)
            
            if result:
                result.update({
                    "prompt_name": variation_name,
                    "prompt_text": prompt,
                    "model_settings": model_settings,
                    "chaos_mode": i > 0,
                    "mutation_type": "base" if i == 0 else "chaos_mutation"
                })
                results.append(result)
        
        return results

    def run_ultimate_experiment(self):
        """Run the ultimate prompt madness experiment with FIXED loop control"""
        self.logger.info("LAUNCHING ULTIMATE PROMPT MADNESS EXPERIMENT!")
        self.logger.info("=" * 60)
        
        # Discover all images
        all_images = self.discover_all_images()
        if not all_images:
            self.logger.error("No images found!")
            return
        
        # SAFETY LIMITS: Prevent runaway experiments
        max_safe_images = 500
        max_images_per_prompt = 100
        
        if len(all_images) > max_safe_images:
            test_images = random.sample(all_images, max_safe_images)
            self.logger.info(f"SAFETY LIMIT: Using {len(test_images)} of {len(all_images)} images")
        else:
            test_images = all_images
            self.logger.info(f"Using ALL {len(test_images)} discovered images!")
        
        # Save test images list
        test_images_file = self.output_dir / "ultimate_test_images.json"
        with open(test_images_file, 'w', encoding='utf-8') as f:
            json.dump({"test_images": test_images}, f, indent=2)
        
        # Get experimental prompts only (simpler for now)
        experimental_prompts = self.config.get("experimental_prompts", {})
        
        # FIXED: Process ALL prompts, not just one
        total_prompts = len(experimental_prompts)
        completed_prompts = 0
        
        self.logger.info(f"Testing {total_prompts} unique prompt variations!")
        self.stats["unique_prompts_tested"] = total_prompts
        
        # FIXED: Explicit loop with proper advancement
        for prompt_id, prompt_config in experimental_prompts.items():
            completed_prompts += 1
            self.logger.info(f"STARTING PROMPT {completed_prompts}/{total_prompts}: {prompt_id}")
            
            # Limit images per prompt to prevent runaway
            prompt_test_images = test_images[:max_images_per_prompt]
            
            results = []
            for i, image_path in enumerate(prompt_test_images, 1):
                if i % 25 == 0:
                    self.logger.info(f"  Processing image {i}/{len(prompt_test_images)}: {Path(image_path).name}")
                
                self.stats["total_experiments"] += 1
                
                # Test with chaos mode
                image_results = self.test_prompt_with_chaos(image_path, prompt_id, prompt_config)
                
                if image_results:
                    results.extend(image_results)
                    self.stats["successful_experiments"] += len(image_results)
                    self.stats["total_descriptions_generated"] += len(image_results)
                else:
                    self.stats["failed_experiments"] += 1
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
            
            # Save results for this prompt
            if results:
                results_file = self.output_dir / f"{prompt_id}_results.json"
                with open(results_file, 'w', encoding='utf-8') as f:
                    json.dump({prompt_id: results}, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"COMPLETED PROMPT {completed_prompts}/{total_prompts}: {prompt_id} - {len(results)} descriptions generated")
            else:
                self.logger.warning(f"No results for {prompt_id}")
            
            # FIXED: Force progress update and ensure loop advancement
            self.logger.info(f"PROGRESS: {completed_prompts}/{total_prompts} prompts completed ({(completed_prompts/total_prompts)*100:.1f}%)")
            
            # SAFETY: Break if we've processed all prompts
            if completed_prompts >= total_prompts:
                self.logger.info("All prompts completed - experiment finished!")
                break
        
        self.logger.info("ULTIMATE PROMPT MADNESS EXPERIMENT COMPLETE!")
        self.print_final_statistics()

    def print_final_statistics(self):
        """Print final experiment statistics"""
        elapsed_time = time.time() - self.stats["start_time"]
        
        self.logger.info("=" * 60)
        self.logger.info("ULTIMATE PROMPT MADNESS COMPLETE!")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Experiments: {self.stats['total_experiments']}")
        self.logger.info(f"✅ Successful: {self.stats['successful_experiments']}")
        self.logger.info(f"❌ Failed: {self.stats['failed_experiments']}")
        self.logger.info(f"Unique Prompts: {self.stats['unique_prompts_tested']}")
        self.logger.info(f"Total Descriptions: {self.stats['total_descriptions_generated']}")
        self.logger.info(f"⏱️ Total Time: {elapsed_time:.1f} seconds")
        self.logger.info(f"📁 Results Directory: {self.output_dir}")
        self.logger.info("=" * 60)


def main():
    """Main entry point"""
    print("Ultimate Prompt Madness Discovery Engine Starting...")
    
    try:
        experiment = UltimatePromptMadness()
        experiment.run_ultimate_experiment()
    except KeyboardInterrupt:
        print("🛑 Experiment interrupted by user")
    except Exception as e:
        print(f"💥 Experiment failed: {e}")
        raise

if __name__ == "__main__":
    main()
