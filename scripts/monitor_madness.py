#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate Prompt Madness Monitor

Enhanced monitoring for the ultimate prompt madness experiment with detailed status
"""

import json
import time
import os
import subprocess
from pathlib import Path
from datetime import datetime

def format_time_remaining(start_time, completed, total):
    """Calculate and format estimated time remaining"""
    if completed <= 0 or not start_time:
        return "Calculating..."
    
    try:
        # Parse start time
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S,%f")
        now = datetime.now()
        elapsed = (now - start_dt).total_seconds()
        
        # Calculate rate and estimate
        rate = completed / elapsed  # items per second
        remaining = total - completed
        if rate > 0:
            eta_seconds = remaining / rate
            
            # Format ETA
            if eta_seconds < 3600:  # Less than 1 hour
                return f"{eta_seconds/60:.1f} minutes"
            elif eta_seconds < 86400:  # Less than 1 day
                hours = eta_seconds / 3600
                return f"{hours:.1f} hours"
            else:
                days = eta_seconds / 86400
                return f"{days:.1f} days"
        else:
            return "Unknown"
    except:
        return "Unknown"

def draw_progress_bar(current, total, width=40):
    """Draw a text progress bar"""
    if total <= 0:
        return "[" + " " * width + "]"
    
    progress = min(current / total, 1.0)
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{total} ({progress*100:.1f}%)"

def count_files_in_dir(directory, pattern="*"):
    """Count files matching pattern in directory"""
    try:
        if Path(directory).exists():
            return len(list(Path(directory).glob(pattern)))
    except:
        pass
    return 0

def get_log_stats(log_file):
    """Get detailed statistics from log file"""
    stats = {
        'total_lines': 0,
        'completed_prompts': 0,
        'current_prompt': 'Unknown',
        'current_image_number': 0,
        'current_image_path': 'Unknown',
        'experiment_start_time': None,
        'latest_activity': None,
        'error_count': 0,
        'discovered_images': 0,
        'total_prompts': 0,
        'images_processed_this_prompt': 0,
        'api_calls_made': 0,
        'last_api_call_time': None
    }
    
    try:
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                stats['total_lines'] = len(lines)
                
                for line in lines:
                    # Count completed prompts
                    if "Completed" in line and "descriptions generated" in line:
                        stats['completed_prompts'] += 1
                    
                    # Find current prompt being tested
                    if "Testing prompt:" in line:
                        try:
                            stats['current_prompt'] = line.split("Testing prompt: ")[1].strip()
                            stats['images_processed_this_prompt'] = 0  # Reset when new prompt starts
                        except:
                            pass
                    
                    # Track image processing progress
                    if "Processing image" in line:
                        try:
                            # Extract "Processing image X/Y" pattern
                            parts = line.split("Processing image ")[1].split("/")
                            if len(parts) >= 2:
                                stats['current_image_number'] = int(parts[0])
                                stats['images_processed_this_prompt'] = int(parts[0])
                        except:
                            pass
                    
                    # Track API calls and processing
                    if "Get description from Ollama" in line or "response" in line.lower():
                        stats['api_calls_made'] += 1
                        try:
                            timestamp_str = line.split(' - ')[0]
                            stats['last_api_call_time'] = timestamp_str
                        except:
                            pass
                    
                    # Track current image being processed
                    if "Failed to get description for" in line or "Processing image" in line:
                        try:
                            # Try to extract image path from various log formats
                            if "Failed to get description for" in line:
                                path = line.split("Failed to get description for ")[1].split(":")[0]
                                stats['current_image_path'] = path.split("/")[-1] if "/" in path else path.split("\\")[-1]
                        except:
                            pass
                    
                    # Find total prompts count
                    if "Testing" in line and "unique prompt variations" in line:
                        try:
                            words = line.split()
                            for word in words:
                                if word.isdigit():
                                    stats['total_prompts'] = int(word)
                                    break
                        except:
                            pass
                    
                    # Find discovered images count
                    if "Discovered" in line and "supported images" in line:
                        try:
                            words = line.split()
                            for word in words:
                                if word.isdigit():
                                    stats['discovered_images'] = int(word)
                                    break
                        except:
                            pass
                    
                    # Track experiment start
                    if "Ultimate Prompt Madness Discovery Engine Starting" in line:
                        try:
                            timestamp_str = line.split(' - ')[0]
                            stats['experiment_start_time'] = timestamp_str
                        except:
                            pass
                    
                    # Count errors
                    if "ERROR" in line or "Error" in line:
                        stats['error_count'] += 1
                
                # Get latest activity
                if lines:
                    stats['latest_activity'] = lines[-1].strip()
    except:
        pass
    
    return stats

def monitor_madness():
    """Enhanced monitoring for the ultimate prompt madness experiment"""
    output_dir = Path("prompt_experiments_madness")
    log_file = Path("ultimate_prompt_madness.log")
    
    print("ULTIMATE PROMPT MADNESS MONITOR")
    print("=" * 60)
    
    while True:
        try:
            # Clear screen for fresh display
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("ULTIMATE PROMPT MADNESS MONITOR")
            print("=" * 60)
            print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
            # Experiment Progress
            print("EXPERIMENT PROGRESS")
            print("-" * 40)
            log_stats = get_log_stats(log_file)
            
            if log_stats['total_lines'] > 0:
                print(f"Total Log Entries: {log_stats['total_lines']}")
                print(f"Images Discovered: {log_stats['discovered_images']}")
                print(f"Total Prompts to Test: {log_stats['total_prompts']}")
                print()
                
                # Current prompt progress
                print("CURRENT PROMPT STATUS")
                print("-" * 25)
                print(f"Current Prompt: {log_stats['current_prompt']}")
                print(f"Completed Prompts: {log_stats['completed_prompts']}")
                
                if log_stats['total_prompts'] > 0:
                    # Overall progress
                    progress_pct = (log_stats['completed_prompts'] / log_stats['total_prompts']) * 100
                    print(f"Overall Progress: {progress_pct:.1f}%")
                    prompt_bar = draw_progress_bar(log_stats['completed_prompts'], log_stats['total_prompts'], 30)
                    print(f"   {prompt_bar}")
                    
                    # Current prompt progress
                    if log_stats['discovered_images'] > 0:
                        current_img_progress = (log_stats['images_processed_this_prompt'] / log_stats['discovered_images']) * 100
                        print(f"Current Prompt Progress: {current_img_progress:.1f}%")
                        img_bar = draw_progress_bar(log_stats['images_processed_this_prompt'], log_stats['discovered_images'], 30)
                        print(f"   {img_bar}")
                        print(f"Current Image: {log_stats['current_image_number']}/{log_stats['discovered_images']}")
                        
                        if log_stats['current_image_path'] != 'Unknown':
                            print(f"Processing: {log_stats['current_image_path']}")
                    
                    # Time estimates
                    print()
                    print("TIME ANALYSIS")
                    print("-" * 15)
                    if log_stats['experiment_start_time']:
                        print(f"Started: {log_stats['experiment_start_time']}")
                        
                        # Calculate time remaining
                        if log_stats['completed_prompts'] > 0:
                            eta = format_time_remaining(log_stats['experiment_start_time'], 
                                                      log_stats['completed_prompts'], 
                                                      log_stats['total_prompts'])
                            print(f"Est. Time Remaining: {eta}")
                        
                        # Calculate processing rate
                        if log_stats['images_processed_this_prompt'] > 0:
                            try:
                                start_dt = datetime.strptime(log_stats['experiment_start_time'], "%Y-%m-%d %H:%M:%S,%f")
                                now = datetime.now()
                                elapsed_minutes = (now - start_dt).total_seconds() / 60
                                if elapsed_minutes > 0:
                                    rate = log_stats['images_processed_this_prompt'] / elapsed_minutes
                                    print(f"Processing Rate: {rate:.1f} images/min")
                            except:
                                pass
                
                print()
                print("SYSTEM STATUS")
                print("-" * 15)
                print(f"API Calls Made: {log_stats['api_calls_made']}")
                if log_stats['last_api_call_time']:
                    print(f"Last API Call: {log_stats['last_api_call_time']}")
                print(f"Error Count: {log_stats['error_count']}")
                
                if log_stats['latest_activity']:
                    print()
                    print("LATEST ACTIVITY")
                    print("-" * 16)
                    # Truncate long lines for display
                    latest = log_stats['latest_activity']
                    if len(latest) > 100:
                        latest = latest[:97] + "..."
                    print(f"Latest: {latest}")
                    
                # Calculate total progress across all prompts
                if log_stats['total_prompts'] > 0 and log_stats['discovered_images'] > 0:
                    total_operations = log_stats['total_prompts'] * log_stats['discovered_images']
                    completed_operations = (log_stats['completed_prompts'] * log_stats['discovered_images']) + log_stats['images_processed_this_prompt']
                    overall_pct = (completed_operations / total_operations) * 100
                    print()
                    print("TOTAL EXPERIMENT PROGRESS")
                    print("-" * 28)
                    print(f"Overall Completion: {overall_pct:.2f}%")
                    total_bar = draw_progress_bar(completed_operations, total_operations, 50)
                    print(f"   {total_bar}")
                    print(f"Operations: {completed_operations:,}/{total_operations:,}")
                    
            else:
                print("No log file activity detected")
            print()
            
            # File System Status
            print("RESULTS STATUS")
            print("-" * 40)
            
            # Results directory
            if output_dir.exists():
                result_files = count_files_in_dir(output_dir, "*_results.json")
                analysis_files = count_files_in_dir(output_dir, "ultimate_*_report_*.md")
                print(f"Results Files: {result_files}")
                print(f"Analysis Reports: {analysis_files}")
                
                # Count total descriptions generated
                total_descriptions = 0
                if result_files > 0:
                    for result_file in output_dir.glob("*_results.json"):
                        try:
                            with open(result_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                for results in data.values():
                                    total_descriptions += len(results)
                        except:
                            pass
                    print(f"Total Descriptions Generated: {total_descriptions}")
                
                # Check if experiment is complete
                if analysis_files > 0:
                    print()
                    print("EXPERIMENT COMPLETE!")
                    print("Analysis reports have been generated")
                    break
            else:
                print("Results directory not yet created")
            
            print()
            print("EXPERIMENTAL SCOPE")
            print("-" * 40)
            print("Chaos Mode: ENABLED")
            print("Parameter Mutations: ACTIVE")  
            print("Creative Prompt Variations: YES")
            print("Multi-model Support: AVAILABLE")
            print("Revolutionary Prompt Categories: 10+")
            
            print()
            print("Refreshing in 10 seconds... (Ctrl+C to stop)")
            print("=" * 60)
            
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"\nMonitor error: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    monitor_madness()
