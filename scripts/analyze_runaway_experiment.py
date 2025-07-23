#!/usr/bin/env python3
"""
Ultimate Prompt Madness Recovery Analysis

Analyze the results from the runaway experiment and extract useful insights.
"""

import json
import statistics
from pathlib import Path
from datetime import datetime

def analyze_runaway_results():
    """Analyze the results from the runaway experiment"""
    print("ULTIMATE PROMPT MADNESS RECOVERY ANALYSIS")
    print("=" * 50)
    
    results_dir = Path("prompt_experiments_madness")
    if not results_dir.exists():
        print("❌ Results directory not found!")
        return
    
    # Find the massive results file
    results_files = list(results_dir.glob("*_results.json"))
    print(f"Found {len(results_files)} results files:")
    
    for file in results_files:
        file_size = file.stat().st_size
        print(f"  - {file.name}: {file_size:,} bytes")
    
    # Analyze the big file
    big_file = results_dir / "machine_learning_feature_extractor_stream_of_consciousness_results.json"
    if not big_file.exists():
        print("❌ Main results file not found!")
        return
    
    print(f"\nAnalyzing {big_file.name}...")
    
    try:
        with open(big_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get the results list
        prompt_name = list(data.keys())[0]
        results = data[prompt_name]
        
        print(f"Prompt analyzed: {prompt_name}")
        print(f"Total descriptions: {len(results)}")
        
        # Analyze metrics
        metrics_data = [r["metrics"] for r in results if "metrics" in r]
        
        if metrics_data:
            print(f"\nMETRICS ANALYSIS:")
            print("-" * 30)
            
            # Calculate averages
            avg_word_count = statistics.mean([m["word_count"] for m in metrics_data])
            avg_creativity = statistics.mean([m["creativity_score"] for m in metrics_data])
            avg_technical = statistics.mean([m["technical_depth"] for m in metrics_data])
            avg_emotional = statistics.mean([m["emotional_resonance"] for m in metrics_data])
            avg_lexical = statistics.mean([m["lexical_diversity"] for m in metrics_data])
            
            print(f"Average word count: {avg_word_count:.1f}")
            print(f"Average creativity score: {avg_creativity:.3f}")
            print(f"Average technical depth: {avg_technical:.3f}")
            print(f"Average emotional resonance: {avg_emotional:.3f}")
            print(f"Average lexical diversity: {avg_lexical:.3f}")
            
            # Find best and worst descriptions
            best_creativity = max(metrics_data, key=lambda x: x["creativity_score"])
            best_technical = max(metrics_data, key=lambda x: x["technical_depth"])
            best_emotional = max(metrics_data, key=lambda x: x["emotional_resonance"])
            
            print(f"\nBEST SCORES:")
            print(f"Best creativity: {best_creativity['creativity_score']:.3f}")
            print(f"Best technical: {best_technical['technical_depth']:.3f}")
            print(f"Best emotional: {best_emotional['emotional_resonance']:.3f}")
            
            # Analyze unique images processed
            unique_images = set(r["image_path"] for r in results)
            print(f"\nUnique images processed: {len(unique_images)}")
            
            # Check if chaos mode was used
            chaos_results = [r for r in results if r.get("chaos_mode", False)]
            base_results = [r for r in results if not r.get("chaos_mode", False)]
            
            print(f"Base mode descriptions: {len(base_results)}")
            print(f"Chaos mode descriptions: {len(chaos_results)}")
            
            if chaos_results and base_results:
                chaos_creativity = statistics.mean([r["metrics"]["creativity_score"] for r in chaos_results])
                base_creativity = statistics.mean([r["metrics"]["creativity_score"] for r in base_results])
                
                print(f"\nCHAOS MODE ANALYSIS:")
                print(f"Base creativity: {base_creativity:.3f}")
                print(f"Chaos creativity: {chaos_creativity:.3f}")
                print(f"Chaos improvement: {chaos_creativity - base_creativity:+.3f}")
        
        # Sample some descriptions
        print(f"\nSAMPLE DESCRIPTIONS:")
        print("-" * 40)
        
        # Show first, middle, and last descriptions
        sample_indices = [0, len(results)//2, len(results)-1]
        for i, idx in enumerate(sample_indices):
            if idx < len(results):
                desc = results[idx]["description"][:150] + "..." if len(results[idx]["description"]) > 150 else results[idx]["description"]
                print(f"\nSample {i+1} (#{idx+1}):")
                print(desc)
        
        # Generate summary report
        generate_recovery_report(data, prompt_name, results, metrics_data)
        
    except Exception as e:
        print(f"❌ Error analyzing results: {e}")

def generate_recovery_report(data, prompt_name, results, metrics_data):
    """Generate a recovery report"""
    report_file = f"recovery_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Ultimate Prompt Madness Recovery Analysis\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        
        f.write("## Incident Summary\n\n")
        f.write("The Ultimate Prompt Madness experiment experienced a runaway condition where it\n")
        f.write("got stuck processing a single prompt repeatedly instead of advancing through\n")
        f.write("all 63 planned prompts.\n\n")
        
        f.write("## Data Recovered\n\n")
        f.write(f"- **Prompt analyzed**: {prompt_name}\n")
        f.write(f"- **Total descriptions**: {len(results):,}\n")
        f.write(f"- **Unique images**: {len(set(r['image_path'] for r in results)):,}\n")
        f.write(f"- **Time span**: {results[0]['timestamp']} to {results[-1]['timestamp']}\n\n")
        
        if metrics_data:
            f.write("## Performance Metrics\n\n")
            f.write(f"- **Average word count**: {statistics.mean([m['word_count'] for m in metrics_data]):.1f}\n")
            f.write(f"- **Creativity score**: {statistics.mean([m['creativity_score'] for m in metrics_data]):.3f}\n")
            f.write(f"- **Technical depth**: {statistics.mean([m['technical_depth'] for m in metrics_data]):.3f}\n")
            f.write(f"- **Emotional resonance**: {statistics.mean([m['emotional_resonance'] for m in metrics_data]):.3f}\n")
            f.write(f"- **Lexical diversity**: {statistics.mean([m['lexical_diversity'] for m in metrics_data]):.3f}\n\n")
        
        f.write("## Lessons Learned\n\n")
        f.write("1. **Safety limits needed**: Implement maximum images per prompt\n")
        f.write("2. **Progress tracking**: Better loop control and exit conditions\n")
        f.write("3. **Resource monitoring**: File size and memory usage limits\n")
        f.write("4. **Incremental saves**: Save progress more frequently\n\n")
        
        f.write("## Recovery Actions Taken\n\n")
        f.write("1. ✅ Stopped runaway processes\n")
        f.write("2. ✅ Analyzed recovered data\n")
        f.write("3. ✅ Fixed loop control bugs\n")
        f.write("4. ✅ Added safety limits\n")
        f.write("5. ✅ Improved progress tracking\n\n")
        
        f.write("## Data Value\n\n")
        f.write("Despite the runaway condition, we obtained valuable data:\n")
        f.write(f"- Over {len(results):,} image descriptions from a single advanced prompt\n")
        f.write("- Comprehensive metrics on the 'machine learning feature extractor' prompt\n")
        f.write("- Chaos mode vs base mode comparison data\n")
        f.write("- Performance baselines for future experiments\n\n")
        
        f.write("The experiment is now ready to be restarted with improved controls.\n")
    
    print(f"\n💾 Recovery report saved to: {report_file}")

if __name__ == "__main__":
    analyze_runaway_results()
