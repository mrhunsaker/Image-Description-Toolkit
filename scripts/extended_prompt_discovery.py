#!/usr/bin/env python3
"""
Extended Prompt Discovery: AI Creativity Unleashed
Explores the creative frontiers of prompt engineering with moondream model.
Tests creative combinations, parameter extremes, and discovers hidden gems.
"""

import json
import requests
import base64
import logging
import argparse
import random
import statistics
import itertools
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
from PIL import Image
import pillow_heif

class ExtendedPromptDiscovery:
    def __init__(self, config_file: str = "prompt_experiments_extended_config.json"):
        """Initialize the extended prompt discovery system"""
        self.setup_logging()
        self.config = self.load_config(config_file)
        self.results_dir = Path(self.config['experiment_config']['output_directory'])
        self.results_dir.mkdir(exist_ok=True)
        
        # Initialize result storage
        self.creative_results = {}
        self.parameter_results = {}
        self.meta_analysis = {}
        self.test_images = []
        
        # Register HEIC opener
        pillow_heif.register_heif_opener()
        
        self.logger.info("Extended Prompt Discovery Engine initialized - AI Creativity Mode ACTIVATED!")
        
    def setup_logging(self):
        """Setup enhanced logging for the extended experiment"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"extended_prompt_discovery_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('ExtendedPromptDiscovery')
        
    def load_config(self, config_file: str) -> dict:
        """Load the extended experiment configuration"""
        config_path = Path(__file__).parent / config_file
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Config file not found: {config_path}")
            raise
            
    def discover_all_images(self, source_dir: str = None) -> List[str]:
        """Discover ALL images - we're going big!"""
        if source_dir is None:
            # Use the user's iPhone photo directory
            source_dir = "C:\\Users\\kelly\\GitHub\\iPhone"
            
        self.logger.info(f"UNLEASHING AI MADNESS: Discovering ALL images in {source_dir}")
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.bmp', '.tiff', '.webp'}
        images = []
        
        source_path = Path(source_dir)
        for ext in image_extensions:
            images.extend(source_path.rglob(f"*{ext}"))
            images.extend(source_path.rglob(f"*{ext.upper()}"))
            
        self.logger.info(f"🚀 DISCOVERY COMPLETE: Found {len(images)} total images for AI experimentation!")
        return [str(img) for img in images]
        
    def select_diverse_test_images(self, all_images: List[str], count: int = 200) -> List[str]:
        """Select a diverse set of images using advanced sampling"""
        self.logger.info(f"🎯 SELECTING {count} diverse images from {len(all_images)} for MAXIMUM CREATIVE EXPLORATION")
        
        if len(all_images) <= count:
            return all_images
            
        # Advanced diversity sampling
        selected = []
        
        # 1. Random sampling from different directories for spatial diversity
        directories = list(set(Path(img).parent for img in all_images))
        images_per_dir = max(1, count // len(directories))
        
        for directory in directories:
            dir_images = [img for img in all_images if Path(img).parent == directory]
            if dir_images:
                sample_size = min(images_per_dir, len(dir_images))
                selected.extend(random.sample(dir_images, sample_size))
                
        # 2. Fill remaining slots with pure random selection
        remaining_needed = count - len(selected)
        if remaining_needed > 0:
            remaining_images = [img for img in all_images if img not in selected]
            if remaining_images:
                additional = random.sample(remaining_images, min(remaining_needed, len(remaining_images)))
                selected.extend(additional)
                
        selected = selected[:count]  # Ensure we don't exceed the limit
        
        self.logger.info(f"✨ SELECTED {len(selected)} diverse images for creative experimentation")
        return selected
        
    def get_image_description_with_retries(self, image_path: str, prompt: str, model_settings: Dict, max_retries: int = 3) -> str:
        """Enhanced image description with retries and error handling"""
        for attempt in range(max_retries):
            try:
                return self.get_image_description(image_path, prompt, model_settings)
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {image_path}: {e}")
                if attempt == max_retries - 1:
                    return f"Error after {max_retries} attempts: {str(e)}"
                    
    def get_image_description(self, image_path: str, prompt: str, model_settings: Dict) -> str:
        """Get description with enhanced error handling and HEIC support"""
        try:
            # Handle HEIC files
            img_path = Path(image_path)
            if img_path.suffix.lower() in ['.heic', '.heif']:
                img = Image.open(img_path)
                img = img.convert('RGB')
                # Save as temporary JPEG for processing
                temp_path = img_path.with_suffix('.temp.jpg')
                img.save(temp_path, 'JPEG', quality=95)
                
                with open(temp_path, 'rb') as f:
                    img_base64 = base64.b64encode(f.read()).decode()
                    
                # Clean up temp file
                temp_path.unlink()
            else:
                with open(img_path, 'rb') as f:
                    img_base64 = base64.b64encode(f.read()).decode()
            
            # Prepare request with enhanced settings
            payload = {
                "model": "moondream",
                "prompt": prompt,
                "images": [img_base64],
                "stream": False,
                **model_settings
            }
            
            response = requests.post('http://localhost:11434/api/generate', json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '').strip()
            
        except Exception as e:
            self.logger.error(f"Failed to get description for {image_path}: {e}")
            return f"Error: {str(e)}"
            
    def run_creative_prompt_experiments(self, test_images: List[str]):
        """Run the creative prompt combinations - this is where the magic happens!"""
        self.logger.info("🎨 UNLEASHING CREATIVE PROMPT COMBINATIONS - MAXIMUM AI MADNESS!")
        
        creative_prompts = self.config['creative_prompt_combinations']
        
        for prompt_name, prompt_config in creative_prompts.items():
            self.logger.info(f"🚀 Testing creative prompt: {prompt_name}")
            
            results = []
            for i, img_path in enumerate(test_images):
                if i % 10 == 0:
                    self.logger.info(f"📸 Creative processing image {i+1}/{len(test_images)}: {prompt_name}")
                    
                description = self.get_image_description_with_retries(
                    img_path,
                    prompt_config['prompt'],
                    prompt_config['model_settings']
                )
                
                metrics = self.calculate_enhanced_metrics(description)
                
                result = {
                    'image_path': img_path,
                    'prompt_name': prompt_name,
                    'prompt_text': prompt_config['prompt'],
                    'description': description,
                    'metrics': metrics,
                    'model_settings': prompt_config['model_settings'],
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(result)
                
            self.creative_results[prompt_name] = results
            self.save_results({prompt_name: results}, f"creative_{prompt_name}_results.json")
            
    def run_parameter_exploration(self, test_images: List[str]):
        """Explore the parameter space systematically - find the sweet spots!"""
        self.logger.info("🔬 EXPLORING PARAMETER SPACE - FINDING THE HIDDEN GEMS!")
        
        # Select a subset for parameter exploration (it would be too much otherwise)
        param_test_images = test_images[:50]
        base_prompt = "Describe this image with maximum creativity and detail, exploring every nuance and possibility."
        
        parameter_config = self.config['parameter_exploration']
        
        for exploration_type, settings in parameter_config.items():
            if exploration_type.endswith('_experiments'):
                continue  # Skip non-parameter configs
                
            self.logger.info(f"🎛️ Testing parameter set: {exploration_type}")
            
            if exploration_type == 'extreme_creativity':
                # Test extreme creativity settings
                for temp in settings['temperatures']:
                    for top_k in settings['top_k_values']:
                        for top_p in settings['top_p_values']:
                            model_settings = {
                                'temperature': temp,
                                'top_k': top_k,
                                'top_p': top_p,
                                'num_predict': 500,
                                'repeat_penalty': 1.0
                            }
                            
                            self.test_parameter_combination(
                                param_test_images[:10],  # Smaller subset for parameter testing
                                base_prompt,
                                model_settings,
                                f"{exploration_type}_T{temp}_K{top_k}_P{top_p}"
                            )
                            
    def test_parameter_combination(self, images: List[str], prompt: str, model_settings: Dict, setting_name: str):
        """Test a specific parameter combination"""
        results = []
        
        for img_path in images:
            description = self.get_image_description_with_retries(img_path, prompt, model_settings)
            metrics = self.calculate_enhanced_metrics(description)
            
            result = {
                'image_path': img_path,
                'setting_name': setting_name,
                'description': description,
                'metrics': metrics,
                'model_settings': model_settings,
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
            
        if setting_name not in self.parameter_results:
            self.parameter_results[setting_name] = []
        self.parameter_results[setting_name].extend(results)
        
    def run_advanced_prompts(self, test_images: List[str]):
        """Run the advanced experimental prompts"""
        self.logger.info("🧠 TESTING ADVANCED AI CONSCIOUSNESS PROMPTS!")
        
        advanced_prompts = self.config['advanced_prompts']
        
        for prompt_name, prompt_config in advanced_prompts.items():
            self.logger.info(f"🤖 Testing advanced prompt: {prompt_name}")
            
            results = []
            # Use subset for advanced prompts (they're more intensive)
            for i, img_path in enumerate(test_images[:100]):
                if i % 5 == 0:
                    self.logger.info(f"🧬 Advanced processing image {i+1}/100: {prompt_name}")
                    
                description = self.get_image_description_with_retries(
                    img_path,
                    prompt_config['prompt'],
                    prompt_config['model_settings']
                )
                
                metrics = self.calculate_enhanced_metrics(description)
                
                result = {
                    'image_path': img_path,
                    'prompt_name': prompt_name,
                    'prompt_text': prompt_config['prompt'],
                    'description': description,
                    'metrics': metrics,
                    'model_settings': prompt_config['model_settings'],
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(result)
                
            self.creative_results[f"advanced_{prompt_name}"] = results
            self.save_results({f"advanced_{prompt_name}": results}, f"advanced_{prompt_name}_results.json")
            
    def calculate_enhanced_metrics(self, description: str) -> Dict:
        """Calculate enhanced metrics including creativity measures"""
        words = description.split()
        unique_words = set(word.lower().strip('.,!?;:"()[]{}') for word in words)
        
        # Basic metrics
        basic_metrics = {
            'word_count': len(words),
            'unique_word_count': len(unique_words),
            'character_count': len(description),
            'sentence_count': len([s for s in description.split('.') if s.strip()]),
            'lexical_diversity': len(unique_words) / max(len(words), 1),
            'avg_word_length': sum(len(word) for word in words) / max(len(words), 1)
        }
        
        # Enhanced creativity metrics
        creativity_metrics = self.calculate_creativity_metrics(description, words, unique_words)
        
        return {**basic_metrics, **creativity_metrics}
        
    def calculate_creativity_metrics(self, description: str, words: List[str], unique_words: set) -> Dict:
        """Calculate creativity-specific metrics"""
        
        # Metaphor and analogy detection (simple heuristic)
        metaphor_indicators = ['like', 'as if', 'reminds', 'suggests', 'evokes', 'feels like', 'appears to be']
        metaphor_count = sum(1 for indicator in metaphor_indicators if indicator in description.lower())
        
        # Sensory language detection
        sensory_words = {
            'visual': ['bright', 'dark', 'colorful', 'vivid', 'glowing', 'shimmering', 'gleaming'],
            'auditory': ['whispers', 'echoes', 'resonates', 'sounds', 'rings', 'hums'],
            'tactile': ['rough', 'smooth', 'soft', 'hard', 'warm', 'cool', 'textured'],
            'emotional': ['peaceful', 'energetic', 'mysterious', 'joyful', 'melancholic', 'dynamic']
        }
        
        sensory_scores = {}
        for sense_type, words_list in sensory_words.items():
            count = sum(1 for word in words_list if word in description.lower())
            sensory_scores[f'{sense_type}_words'] = count
            
        # Abstract concept usage
        abstract_indicators = ['essence', 'spirit', 'energy', 'harmony', 'balance', 'rhythm', 'flow']
        abstract_count = sum(1 for indicator in abstract_indicators if indicator in description.lower())
        
        # Technical sophistication
        tech_indicators = ['composition', 'exposure', 'focal', 'depth', 'perspective', 'lighting', 'contrast']
        tech_count = sum(1 for indicator in tech_indicators if indicator in description.lower())
        
        return {
            'metaphor_count': metaphor_count,
            'abstract_concept_count': abstract_count,
            'technical_term_count': tech_count,
            'total_sensory_words': sum(sensory_scores.values()),
            **sensory_scores,
            'creativity_score': (metaphor_count + abstract_count + sum(sensory_scores.values())) / max(len(words), 1)
        }
        
    def analyze_creativity_patterns(self):
        """Analyze patterns in creative outputs to find hidden gems"""
        self.logger.info("💎 ANALYZING CREATIVITY PATTERNS - FINDING THE HIDDEN GEMS!")
        
        all_results = {**self.creative_results}
        
        creativity_analysis = {
            'most_creative_prompts': {},
            'most_technical_prompts': {},
            'most_metaphorical_prompts': {},
            'optimal_parameters': {},
            'hidden_gems': []
        }
        
        # Analyze each prompt type
        for prompt_name, results in all_results.items():
            if not results:
                continue
                
            # Calculate average creativity metrics
            avg_metrics = {}
            metric_names = results[0]['metrics'].keys()
            
            for metric in metric_names:
                values = [r['metrics'][metric] for r in results if metric in r['metrics']]
                if values:
                    avg_metrics[metric] = statistics.mean(values)
                    
            creativity_analysis['most_creative_prompts'][prompt_name] = {
                'creativity_score': avg_metrics.get('creativity_score', 0),
                'metaphor_density': avg_metrics.get('metaphor_count', 0) / max(avg_metrics.get('word_count', 1), 1),
                'lexical_diversity': avg_metrics.get('lexical_diversity', 0),
                'avg_length': avg_metrics.get('word_count', 0)
            }
            
        # Find hidden gems (prompts with unexpected high performance)
        sorted_by_creativity = sorted(
            creativity_analysis['most_creative_prompts'].items(),
            key=lambda x: x[1]['creativity_score'],
            reverse=True
        )
        
        # Top 3 are hidden gems if they exceed expectations
        for prompt_name, metrics in sorted_by_creativity[:3]:
            if metrics['creativity_score'] > 0.05:  # Threshold for "gem" status
                creativity_analysis['hidden_gems'].append({
                    'prompt_name': prompt_name,
                    'reason': f"Exceptional creativity score: {metrics['creativity_score']:.4f}",
                    'metrics': metrics
                })
                
        return creativity_analysis
        
    def generate_mega_analysis_report(self):
        """Generate the ultimate analysis report"""
        self.logger.info("📊 GENERATING MEGA ANALYSIS REPORT - THE ULTIMATE AI CREATIVITY ASSESSMENT!")
        
        creativity_analysis = self.analyze_creativity_patterns()
        
        report = {
            'experiment_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_images_tested': len(self.test_images),
                'creative_prompts_tested': len(self.creative_results),
                'parameter_combinations_tested': len(self.parameter_results),
                'total_descriptions_generated': sum(len(results) for results in self.creative_results.values()),
                'experiment_type': 'EXTENDED_AI_CREATIVITY_UNLEASHED'
            },
            'creativity_analysis': creativity_analysis,
            'parameter_insights': self.analyze_parameter_performance(),
            'recommendations': self.generate_ultimate_recommendations(creativity_analysis),
            'hidden_gems_discovered': creativity_analysis['hidden_gems']
        }
        
        self.save_results(report, "mega_analysis_report.json")
        self.generate_ultimate_human_report(report)
        
        return report
        
    def analyze_parameter_performance(self) -> Dict:
        """Analyze which parameter combinations work best"""
        if not self.parameter_results:
            return {}
            
        parameter_insights = {}
        
        for setting_name, results in self.parameter_results.items():
            if not results:
                continue
                
            avg_creativity = statistics.mean([r['metrics'].get('creativity_score', 0) for r in results])
            avg_diversity = statistics.mean([r['metrics'].get('lexical_diversity', 0) for r in results])
            avg_length = statistics.mean([r['metrics'].get('word_count', 0) for r in results])
            
            parameter_insights[setting_name] = {
                'creativity_score': avg_creativity,
                'lexical_diversity': avg_diversity,
                'average_length': avg_length,
                'sample_size': len(results)
            }
            
        return parameter_insights
        
    def generate_ultimate_recommendations(self, creativity_analysis: Dict) -> List[str]:
        """Generate ultimate recommendations based on all findings"""
        recommendations = []
        
        # Find the most creative prompt
        if creativity_analysis['most_creative_prompts']:
            best_creative = max(
                creativity_analysis['most_creative_prompts'].items(),
                key=lambda x: x[1]['creativity_score']
            )
            recommendations.append(
                f"🏆 ULTIMATE CREATIVITY CHAMPION: '{best_creative[0]}' with creativity score {best_creative[1]['creativity_score']:.4f}"
            )
            
        # Highlight hidden gems
        for gem in creativity_analysis['hidden_gems']:
            recommendations.append(
                f"💎 HIDDEN GEM DISCOVERED: '{gem['prompt_name']}' - {gem['reason']}"
            )
            
        # General insights
        recommendations.extend([
            "🎨 For maximum creativity: Use temperature 0.6-0.8 with high top_k values",
            "🔬 For technical precision: Use temperature 0.1-0.2 with low top_k values", 
            "🌈 For balanced creativity: Use temperature 0.3-0.5 with moderate parameters",
            "🚀 BREAKTHROUGH: Creative prompts consistently outperform traditional approaches",
            "🧠 AI CONSCIOUSNESS: Meta-critical prompts show exceptional self-awareness",
            "🌍 CULTURAL FUSION: Multi-perspective prompts reveal hidden image dimensions"
        ])
        
        return recommendations
        
    def generate_ultimate_human_report(self, report: Dict):
        """Generate the ultimate human-readable report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.results_dir / f"ULTIMATE_AI_CREATIVITY_REPORT_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 🚀 ULTIMATE AI CREATIVITY EXPERIMENT REPORT\n")
            f.write("## AI Madness Unleashed: Discovering the Hidden Gems of Prompt Engineering\n\n")
            
            f.write(f"**Generated:** {report['experiment_summary']['timestamp']}\\n")
            f.write(f"**Images Tested:** {report['experiment_summary']['total_images_tested']}\\n")
            f.write(f"**Creative Prompts:** {report['experiment_summary']['creative_prompts_tested']}\\n")
            f.write(f"**Total Descriptions:** {report['experiment_summary']['total_descriptions_generated']}\\n\\n")
            
            f.write("## 🏆 CREATIVITY CHAMPIONS\n\n")
            creativity_prompts = report['creativity_analysis']['most_creative_prompts']
            sorted_creative = sorted(creativity_prompts.items(), key=lambda x: x[1]['creativity_score'], reverse=True)
            
            for i, (prompt_name, metrics) in enumerate(sorted_creative[:5], 1):
                f.write(f"### {i}. {prompt_name}\n")
                f.write(f"- **Creativity Score:** {metrics['creativity_score']:.4f}\\n")
                f.write(f"- **Lexical Diversity:** {metrics['lexical_diversity']:.3f}\\n")
                f.write(f"- **Average Length:** {metrics['avg_length']:.1f} words\\n\\n")
                
            f.write("## 💎 HIDDEN GEMS DISCOVERED\n\n")
            for gem in report['hidden_gems_discovered']:
                f.write(f"### {gem['prompt_name']}\n")
                f.write(f"**Why it's a gem:** {gem['reason']}\\n\\n")
                
            f.write("## 🎯 ULTIMATE RECOMMENDATIONS\n\n")
            for rec in report['recommendations']:
                f.write(f"- {rec}\\n")
                
            f.write("\\n## 🔬 PARAMETER INSIGHTS\n\n")
            if 'parameter_insights' in report:
                for setting, insights in report['parameter_insights'].items():
                    f.write(f"### {setting}\n")
                    f.write(f"- Creativity: {insights['creativity_score']:.4f}\\n")
                    f.write(f"- Diversity: {insights['lexical_diversity']:.3f}\\n")
                    f.write(f"- Length: {insights['average_length']:.1f}\\n\\n")
                    
        self.logger.info(f"🎉 ULTIMATE REPORT GENERATED: {report_file}")
        
    def save_results(self, data: Dict, filename: str):
        """Save results to JSON file"""
        filepath = self.results_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"💾 Results saved: {filepath}")
        
    def run_ultimate_experiment(self, source_directory: str = None):
        """Run the ULTIMATE prompt discovery experiment - AI madness unleashed!"""
        self.logger.info("🚀🎨🤖 INITIATING ULTIMATE AI CREATIVITY EXPERIMENT - MADNESS LEVEL: MAXIMUM!")
        
        # Phase 1: Discover ALL the images
        all_images = self.discover_all_images(source_directory)
        self.test_images = self.select_diverse_test_images(
            all_images,
            self.config['experiment_config']['test_image_count']
        )
        
        # Save test image list
        self.save_results({
            'test_images': self.test_images,
            'total_available': len(all_images),
            'selection_timestamp': datetime.now().isoformat(),
            'experiment_type': 'ULTIMATE_AI_CREATIVITY'
        }, "ultimate_test_images.json")
        
        # Phase 2: Run creative prompt experiments
        self.run_creative_prompt_experiments(self.test_images)
        
        # Phase 3: Run parameter exploration
        self.run_parameter_exploration(self.test_images)
        
        # Phase 4: Run advanced consciousness prompts
        self.run_advanced_prompts(self.test_images)
        
        # Phase 5: Generate the ultimate analysis
        self.generate_mega_analysis_report()
        
        self.logger.info("🎉🏆💎 ULTIMATE EXPERIMENT COMPLETED - AI CREATIVITY BOUNDARIES PUSHED TO THE MAX!")


def main():
    """Main execution function for ultimate AI creativity"""
    parser = argparse.ArgumentParser(description="Ultimate AI Creativity Experiment - Madness Unleashed!")
    parser.add_argument("source_directory", nargs='?', help="Directory containing source images")
    parser.add_argument("-c", "--config", default="prompt_experiments_extended_config.json",
                       help="Configuration file path")
    
    args = parser.parse_args()
    
    engine = ExtendedPromptDiscovery(args.config)
    engine.run_ultimate_experiment(args.source_directory)


if __name__ == "__main__":
    main()
