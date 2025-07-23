#!/usr/bin/env python3
"""
Experiment Monitor - Track progress of prompt discovery experiments
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

def monitor_experiment():
    """Monitor the running experiment and provide progress updates"""
    scripts_dir = Path(__file__).parent
    results_dir = scripts_dir / "prompt_experiments"
    log_file = scripts_dir / "experiment_output.log"
    
    print("🔬 Prompt Discovery Experiment Monitor")
    print("=" * 50)
    
    start_time = datetime.now()
    
    while True:
        # Check if results directory exists and has files
        if results_dir.exists():
            result_files = list(results_dir.glob("*_results.json"))
            if result_files:
                print(f"\n📊 Progress Update - {datetime.now().strftime('%H:%M:%S')}")
                print(f"⏱️  Running for: {datetime.now() - start_time}")
                print(f"📁 Results files created: {len(result_files)}")
                
                for file in result_files:
                    try:
                        with open(file, 'r') as f:
                            data = json.load(f)
                            if isinstance(data, dict):
                                # Count total results
                                count = 0
                                for key, value in data.items():
                                    if isinstance(value, list):
                                        count += len(value)
                                    elif isinstance(value, dict):
                                        count += 1
                                print(f"  📋 {file.stem}: {count} descriptions")
                            else:
                                print(f"  📋 {file.stem}: Data ready")
                    except:
                        print(f"  📋 {file.stem}: In progress...")
                        
        # Check log file for latest activity
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line:
                            print(f"🔍 Latest: {last_line[-100:]}...")  # Last 100 chars
            except:
                pass
                
        # Check if experiment is complete
        expected_files = [
            "baseline_results.json",
            "technical_quality_results.json", 
            "detailed_narrative_results.json",
            "color_analysis_results.json",
            "social_media_appeal_results.json",
            "accessibility_description_results.json",
            "mood_atmosphere_results.json",
            "analysis_report.json"
        ]
        
        completed_files = [f for f in expected_files if (results_dir / f).exists()]
        completion_percentage = (len(completed_files) / len(expected_files)) * 100
        
        print(f"📈 Completion: {completion_percentage:.1f}% ({len(completed_files)}/{len(expected_files)} phases)")
        
        if len(completed_files) == len(expected_files):
            print("\n🎉 EXPERIMENT COMPLETE!")
            print("📊 All phases finished successfully")
            print(f"⏱️  Total time: {datetime.now() - start_time}")
            print(f"📁 Results in: {results_dir}")
            break
            
        print("-" * 30)
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    try:
        monitor_experiment()
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Monitor error: {e}")
