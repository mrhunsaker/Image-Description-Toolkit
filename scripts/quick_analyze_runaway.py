#!/usr/bin/env python3
"""
Quick Data Analysis - Runaway Experiment Recovery

Analyze the massive results file without loading it entirely into memory.
"""

import json
import re
from pathlib import Path

def quick_analyze_results():
    """Quick analysis of the runaway experiment results"""
    
    print("QUICK ANALYSIS OF RUNAWAY EXPERIMENT")
    print("=" * 50)
    
    results_file = Path("prompt_experiments_madness/machine_learning_feature_extractor_stream_of_consciousness_results.json")
    
    if not results_file.exists():
        print("❌ Results file not found!")
        return
    
    # Get file size
    file_size = results_file.stat().st_size
    print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    
    # Count lines
    with open(results_file, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    print(f"Total lines: {line_count:,}")
    
    # Analyze key metrics by sampling
    print("\nSampling data for analysis...")
    
    descriptions = []
    timestamps = []
    chaos_count = 0
    base_count = 0
    word_counts = []
    creativity_scores = []
    technical_scores = []
    emotional_scores = []
    
    sample_size = 0
    
    with open(results_file, 'r', encoding='utf-8') as f:
        in_description = False
        current_entry = {}
        
        for line_num, line in enumerate(f):
            line = line.strip()
            
            # Sample every 100th entry to avoid memory issues
            if line_num % 100 == 0 and line_num > 0:
                if '"description":' in line:
                    # Extract description
                    desc_match = re.search(r'"description":\s*"([^"]*)', line)
                    if desc_match:
                        desc = desc_match.group(1)[:100]  # First 100 chars
                        descriptions.append(desc)
                
                elif '"timestamp":' in line:
                    # Extract timestamp
                    ts_match = re.search(r'"timestamp":\s*"([^"]*)', line)
                    if ts_match:
                        timestamps.append(ts_match.group(1))
                
                elif '"chaos_mode": true' in line:
                    chaos_count += 1
                    sample_size += 1
                
                elif '"chaos_mode": false' in line:
                    base_count += 1
                    sample_size += 1
                
                elif '"word_count":' in line:
                    # Extract word count
                    wc_match = re.search(r'"word_count":\s*(\d+)', line)
                    if wc_match:
                        word_counts.append(int(wc_match.group(1)))
                
                elif '"creativity_score":' in line:
                    # Extract creativity score
                    cs_match = re.search(r'"creativity_score":\s*([\d.]+)', line)
                    if cs_match:
                        creativity_scores.append(float(cs_match.group(1)))
                
                elif '"technical_depth":' in line:
                    # Extract technical depth
                    td_match = re.search(r'"technical_depth":\s*([\d.]+)', line)
                    if td_match:
                        technical_scores.append(float(td_match.group(1)))
                
                elif '"emotional_resonance":' in line:
                    # Extract emotional resonance
                    er_match = re.search(r'"emotional_resonance":\s*([\d.]+)', line)
                    if er_match:
                        emotional_scores.append(float(er_match.group(1)))
            
            # Stop after reasonable sample
            if line_num > 10000:
                break
    
    print(f"Analyzed sample of {sample_size} entries")
    
    # Calculate estimates
    total_entries_estimate = (line_count // 25)  # Rough estimate based on structure
    print(f"\nESTIMATED TOTALS:")
    print(f"Total descriptions: ~{total_entries_estimate:,}")
    print(f"Chaos mode entries: ~{chaos_count * (total_entries_estimate // sample_size if sample_size > 0 else 0):,}")
    print(f"Base mode entries: ~{base_count * (total_entries_estimate // sample_size if sample_size > 0 else 0):,}")
    
    # Time analysis
    if timestamps:
        print(f"\nTIME SPAN:")
        print(f"First timestamp: {timestamps[0]}")
        print(f"Last sampled: {timestamps[-1]}")
    
    # Metrics analysis
    if word_counts:
        avg_words = sum(word_counts) / len(word_counts)
        print(f"\nMETRICS (from sample):")
        print(f"Average word count: {avg_words:.1f}")
        print(f"Word count range: {min(word_counts)} - {max(word_counts)}")
    
    if creativity_scores:
        avg_creativity = sum(creativity_scores) / len(creativity_scores)
        print(f"Average creativity: {avg_creativity:.3f}")
        print(f"Max creativity: {max(creativity_scores):.3f}")
    
    if technical_scores:
        avg_technical = sum(technical_scores) / len(technical_scores)
        print(f"Average technical depth: {avg_technical:.3f}")
        print(f"Max technical: {max(technical_scores):.3f}")
    
    if emotional_scores:
        avg_emotional = sum(emotional_scores) / len(emotional_scores)
        print(f"Average emotional resonance: {avg_emotional:.3f}")
        print(f"Max emotional: {max(emotional_scores):.3f}")
    
    # Sample descriptions
    if descriptions:
        print(f"\nSAMPLE DESCRIPTIONS:")
        print("-" * 30)
        for i, desc in enumerate(descriptions[:5]):
            print(f"{i+1}. {desc}...")
    
    print(f"\n💡 KEY INSIGHTS:")
    print("✅ Successfully tested the 'machine learning feature extractor' prompt")
    print("✅ Generated massive dataset with both base and chaos mode variations")
    print("✅ Comprehensive metrics available for analysis")
    print("⚠️  Script got stuck in infinite loop on single prompt")
    print("⚠️  Need to fix loop control before next experiment")
    
    print(f"\n📊 DATA VALUE:")
    print(f"Despite the runaway condition, we have valuable data:")
    print(f"- Extensive testing of one advanced prompt")
    print(f"- Chaos mode vs base mode comparison data")
    print(f"- {len(word_counts)} data points for performance analysis")
    print(f"- File size: {file_size/1024/1024:.1f} MB of structured data")

if __name__ == "__main__":
    quick_analyze_results()
