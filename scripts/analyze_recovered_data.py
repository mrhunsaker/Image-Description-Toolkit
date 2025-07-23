#!/usr/bin/env python3
"""
Quick Analysis of Recovered Runaway Experiment Data
Analyzes the machine_learning_feature_extractor data without loading the entire file
"""

import json
import re
from collections import defaultdict, Counter
from datetime import datetime
import os

def analyze_recovered_data():
    """Analyze the massive runaway experiment results"""
    
    results_file = "prompt_experiments_madness/machine_learning_feature_extractor_stream_of_consciousness_results.json"
    
    if not os.path.exists(results_file):
        print(f"❌ Results file not found: {results_file}")
        return
    
    print("🔍 ANALYZING RECOVERED RUNAWAY EXPERIMENT DATA")
    print("=" * 60)
    
    # Get file stats
    file_size = os.path.getsize(results_file)
    with open(results_file, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    
    print(f"📄 File Stats:")
    print(f"   • File Size: {file_size / (1024*1024):.1f} MB")
    print(f"   • Total Lines: {line_count:,}")
    print()
    
    # Sample analysis - read every 1000th line to get representative data
    print("🎯 SAMPLING ANALYSIS (every 1000th line)")
    print("-" * 40)
    
    sample_data = []
    timestamps = []
    descriptions = []
    metrics_data = []
    prompt_variations = Counter()
    chaos_vs_base = {"chaos": 0, "base": 0}
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i % 1000 == 0 or '"description":' in line:
                    if '"description":' in line:
                        # Extract description text
                        match = re.search(r'"description":\s*"([^"]*)"', line)
                        if match:
                            desc = match.group(1)
                            descriptions.append(desc)
                    
                    if '"timestamp":' in line:
                        # Extract timestamp
                        match = re.search(r'"timestamp":\s*"([^"]*)"', line)
                        if match:
                            timestamps.append(match.group(1))
                    
                    if '"prompt_name":' in line:
                        # Extract prompt variation
                        match = re.search(r'"prompt_name":\s*"([^"]*)"', line)
                        if match:
                            prompt_variations[match.group(1)] += 1
                    
                    if '"chaos_mode":' in line:
                        # Track chaos vs base mode
                        if '"chaos_mode": true' in line:
                            chaos_vs_base["chaos"] += 1
                        else:
                            chaos_vs_base["base"] += 1
                    
                    if '"word_count":' in line:
                        # Extract metrics
                        match = re.search(r'"word_count":\s*(\d+)', line)
                        if match:
                            metrics_data.append(int(match.group(1)))
    
    except Exception as e:
        print(f"⚠️  Error during sampling: {e}")
    
    # Analyze timestamps to determine experiment duration
    if timestamps:
        first_time = datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))
        last_time = datetime.fromisoformat(timestamps[-1].replace('Z', '+00:00'))
        duration = last_time - first_time
        
        print(f"⏱️  Experiment Timeline:")
        print(f"   • Started: {first_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   • Ended: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   • Duration: {duration}")
        print(f"   • Total Samples: {len(descriptions):,}")
        print()
    
    # Analyze prompt variations
    print(f"🎨 PROMPT VARIATIONS DISCOVERED:")
    print("-" * 40)
    for prompt, count in prompt_variations.most_common():
        print(f"   • {prompt}: {count:,} samples")
    print()
    
    # Chaos vs Base mode analysis
    print(f"🌪️  CHAOS MODE vs BASE MODE:")
    print("-" * 40)
    total_modes = sum(chaos_vs_base.values())
    if total_modes > 0:
        chaos_pct = (chaos_vs_base["chaos"] / total_modes) * 100
        base_pct = (chaos_vs_base["base"] / total_modes) * 100
        print(f"   • Chaos Mode: {chaos_vs_base['chaos']:,} samples ({chaos_pct:.1f}%)")
        print(f"   • Base Mode: {chaos_vs_base['base']:,} samples ({base_pct:.1f}%)")
    print()
    
    # Analyze description quality
    if descriptions:
        print(f"📝 DESCRIPTION ANALYSIS:")
        print("-" * 40)
        print(f"   • Total Descriptions Sampled: {len(descriptions):,}")
        
        # Sample descriptions for quality assessment
        if len(descriptions) >= 3:
            print(f"   • Sample Early Description:")
            print(f"     '{descriptions[0][:100]}...'")
            print(f"   • Sample Mid Description:")
            print(f"     '{descriptions[len(descriptions)//2][:100]}...'")
            print(f"   • Sample Late Description:")
            print(f"     '{descriptions[-1][:100]}...'")
        print()
    
    # Metrics analysis
    if metrics_data:
        avg_words = sum(metrics_data) / len(metrics_data)
        print(f"📊 METRICS ANALYSIS:")
        print("-" * 40)
        print(f"   • Average Word Count: {avg_words:.1f}")
        print(f"   • Min Word Count: {min(metrics_data)}")
        print(f"   • Max Word Count: {max(metrics_data)}")
        print()
    
    # Recovery value assessment
    print(f"💎 DATA RECOVERY VALUE ASSESSMENT:")
    print("-" * 40)
    estimated_descriptions = line_count // 30  # Rough estimate based on JSON structure
    print(f"   • Estimated Total Descriptions: {estimated_descriptions:,}")
    print(f"   • Data Quality: {'HIGH' if len(prompt_variations) > 1 else 'MEDIUM'}")
    print(f"   • Experimental Value: {'EXCELLENT' if chaos_vs_base['chaos'] > 0 else 'GOOD'}")
    print(f"   • Recovery Recommendation: {'ANALYZE FURTHER' if estimated_descriptions > 1000 else 'RESTART EXPERIMENT'}")
    print()
    
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    
    return {
        "file_size_mb": file_size / (1024*1024),
        "line_count": line_count,
        "estimated_descriptions": estimated_descriptions,
        "prompt_variations": len(prompt_variations),
        "chaos_samples": chaos_vs_base["chaos"],
        "base_samples": chaos_vs_base["base"]
    }

if __name__ == "__main__":
    analyze_recovered_data()
