#!/usr/bin/env python3
"""
Multi-Model Prompt Madness Monitor

Real-time monitoring for the multi-model prompt discovery experiment.
Shows progress across all models, response times, success rates, and comparative performance.
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import statistics

class MultiModelMadnessMonitor:
    def __init__(self, log_file="multi_model_prompt_madness.log", results_dir="multi_model_prompt_experiments"):
        self.log_file = log_file
        self.results_dir = Path(results_dir)
        self.start_time = None
        self.last_update = None
        self.model_stats = {}
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def parse_log_line(self, line):
        """Parse a log line for relevant information"""
        if " - INFO - " in line and "Testing prompt:" in line:
            return {"type": "prompt_start", "prompt": line.split("Testing prompt: ")[-1].strip()}
        elif " - INFO - " in line and "Processing image" in line:
            return {"type": "image_progress", "line": line}
        elif " - INFO - " in line and "Completed" in line and "descriptions from" in line:
            parts = line.split("Completed ")[-1].split(":")
            if len(parts) > 1:
                prompt = parts[0].strip()
                desc_info = parts[1].strip()
                return {"type": "prompt_complete", "prompt": prompt, "info": desc_info}
        elif " - ERROR - " in line:
            return {"type": "error", "line": line}
        elif " - WARNING - " in line:
            return {"type": "warning", "line": line}
        return None
    
    def analyze_results_files(self):
        """Analyze existing results files"""
        if not self.results_dir.exists():
            return {}
        
        analysis = {
            "models": {},
            "prompts": {},
            "total_descriptions": 0,
            "files_found": 0
        }
        
        for results_file in self.results_dir.glob("multi_model_*_results.json"):
            analysis["files_found"] += 1
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for prompt_name, results in data.items():
                    if prompt_name not in analysis["prompts"]:
                        analysis["prompts"][prompt_name] = {
                            "total_descriptions": 0,
                            "models": {},
                            "avg_response_time": 0,
                            "avg_creativity": 0,
                            "avg_technical": 0,
                            "avg_emotional": 0
                        }
                    
                    response_times = []
                    creativity_scores = []
                    technical_scores = []
                    emotional_scores = []
                    
                    for result in results:
                        model_name = result.get("model_name", "unknown")
                        
                        # Track per model
                        if model_name not in analysis["models"]:
                            analysis["models"][model_name] = {
                                "descriptions": 0,
                                "response_times": [],
                                "creativity_scores": [],
                                "technical_scores": [],
                                "emotional_scores": []
                            }
                        
                        analysis["models"][model_name]["descriptions"] += 1
                        analysis["total_descriptions"] += 1
                        analysis["prompts"][prompt_name]["total_descriptions"] += 1
                        
                        # Track per prompt per model
                        if model_name not in analysis["prompts"][prompt_name]["models"]:
                            analysis["prompts"][prompt_name]["models"][model_name] = 0
                        analysis["prompts"][prompt_name]["models"][model_name] += 1
                        
                        # Collect metrics
                        if "response_time" in result:
                            rt = result["response_time"]
                            response_times.append(rt)
                            analysis["models"][model_name]["response_times"].append(rt)
                        
                        if "metrics" in result:
                            metrics = result["metrics"]
                            if "creativity_score" in metrics:
                                cs = metrics["creativity_score"]
                                creativity_scores.append(cs)
                                analysis["models"][model_name]["creativity_scores"].append(cs)
                            if "technical_depth" in metrics:
                                ts = metrics["technical_depth"]
                                technical_scores.append(ts)
                                analysis["models"][model_name]["technical_scores"].append(ts)
                            if "emotional_resonance" in metrics:
                                es = metrics["emotional_resonance"]
                                emotional_scores.append(es)
                                analysis["models"][model_name]["emotional_scores"].append(es)
                    
                    # Calculate prompt averages
                    if response_times:
                        analysis["prompts"][prompt_name]["avg_response_time"] = statistics.mean(response_times)
                    if creativity_scores:
                        analysis["prompts"][prompt_name]["avg_creativity"] = statistics.mean(creativity_scores)
                    if technical_scores:
                        analysis["prompts"][prompt_name]["avg_technical"] = statistics.mean(technical_scores)
                    if emotional_scores:
                        analysis["prompts"][prompt_name]["avg_emotional"] = statistics.mean(emotional_scores)
                        
            except Exception as e:
                print(f"Error reading {results_file}: {e}")
        
        return analysis
    
    def get_latest_activity(self):
        """Get the latest activity from the log file"""
        if not os.path.exists(self.log_file):
            return []
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Get last 20 lines and parse them
            recent_lines = lines[-20:] if len(lines) > 20 else lines
            activities = []
            
            for line in recent_lines:
                parsed = self.parse_log_line(line.strip())
                if parsed:
                    # Extract timestamp
                    if " - " in line:
                        timestamp_str = line.split(" - ")[0]
                        try:
                            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                            parsed["timestamp"] = timestamp
                        except:
                            parsed["timestamp"] = datetime.now()
                    activities.append(parsed)
            
            return activities[-10:]  # Return last 10 activities
            
        except Exception as e:
            return [{"type": "error", "line": f"Failed to read log: {e}"}]
    
    def display_status(self):
        """Display the current status"""
        self.clear_screen()
        
        print("=" * 80)
        print("MULTI-MODEL PROMPT MADNESS EXPERIMENT MONITOR")
        print("=" * 80)
        print(f"Monitoring: {self.log_file}")
        print(f"Results Directory: {self.results_dir}")
        print(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Analyze results
        analysis = self.analyze_results_files()
        
        # Overall Statistics
        print("OVERALL PROGRESS")
        print("-" * 40)
        print(f"Result Files Found: {analysis['files_found']}")
        print(f"Total Descriptions Generated: {analysis['total_descriptions']}")
        print(f"Models Active: {len(analysis['models'])}")
        print(f"Prompts Tested: {len(analysis['prompts'])}")
        print()
        
        # Model Performance Comparison
        if analysis["models"]:
            print("MODEL PERFORMANCE COMPARISON")
            print("-" * 60)
            print(f"{'Model':<20} {'Descriptions':<12} {'Avg Time':<10} {'Creativity':<10} {'Technical':<10} {'Emotional':<10}")
            print("-" * 60)
            
            for model_name, stats in analysis["models"].items():
                avg_time = statistics.mean(stats["response_times"]) if stats["response_times"] else 0
                avg_creativity = statistics.mean(stats["creativity_scores"]) if stats["creativity_scores"] else 0
                avg_technical = statistics.mean(stats["technical_scores"]) if stats["technical_scores"] else 0
                avg_emotional = statistics.mean(stats["emotional_scores"]) if stats["emotional_scores"] else 0
                
                print(f"{model_name:<20} {stats['descriptions']:<12} {avg_time:<10.2f} {avg_creativity:<10.3f} {avg_technical:<10.3f} {avg_emotional:<10.3f}")
            print()
        
        # Prompt Progress
        if analysis["prompts"]:
            print("PROMPT TESTING PROGRESS")
            print("-" * 80)
            print(f"{'Prompt':<35} {'Descriptions':<12} {'Models':<8} {'Avg Time':<10} {'Best Metric':<15}")
            print("-" * 80)
            
            for prompt_name, stats in list(analysis["prompts"].items())[:10]:  # Show first 10
                model_count = len(stats["models"])
                best_metric = max(stats["avg_creativity"], stats["avg_technical"], stats["avg_emotional"])
                best_type = "Creativity" if best_metric == stats["avg_creativity"] else "Technical" if best_metric == stats["avg_technical"] else "Emotional"
                best_display = f"{best_type}: {best_metric:.3f}"
                
                prompt_display = prompt_name[:34] + "..." if len(prompt_name) > 34 else prompt_name
                print(f"{prompt_display:<35} {stats['total_descriptions']:<12} {model_count:<8} {stats['avg_response_time']:<10.2f} {best_display:<15}")
            
            if len(analysis["prompts"]) > 10:
                print(f"... and {len(analysis['prompts']) - 10} more prompts")
            print()
        
        # Recent Activity
        activities = self.get_latest_activity()
        if activities:
            print("RECENT ACTIVITY")
            print("-" * 40)
            for activity in activities[-5:]:  # Show last 5 activities
                timestamp = activity.get("timestamp", datetime.now()).strftime("%H:%M:%S")
                if activity["type"] == "prompt_start":
                    print(f"{timestamp} - Started testing: {activity['prompt']}")
                elif activity["type"] == "image_progress":
                    if "Processing image" in activity["line"]:
                        # Extract image info
                        parts = activity["line"].split("Processing image ")
                        if len(parts) > 1:
                            image_info = parts[1].split(":")[0]
                            print(f"{timestamp} - Processing image {image_info}")
                elif activity["type"] == "prompt_complete":
                    print(f"{timestamp} - Completed {activity['prompt']}: {activity['info']}")
                elif activity["type"] == "error":
                    error_msg = activity["line"].split(" - ERROR - ")[-1][:50]
                    print(f"{timestamp} - ERROR: {error_msg}...")
                elif activity["type"] == "warning":
                    warning_msg = activity["line"].split(" - WARNING - ")[-1][:50]
                    print(f"{timestamp} - WARNING: {warning_msg}...")
            print()
        
        # Model Rankings
        if analysis["models"] and len(analysis["models"]) > 1:
            print("MODEL RANKINGS")
            print("-" * 40)
            
            # Rank by speed (lower is better)
            speed_ranking = sorted(
                [(name, statistics.mean(stats["response_times"]) if stats["response_times"] else 999) 
                 for name, stats in analysis["models"].items()],
                key=lambda x: x[1]
            )
            print("Speed (fastest first):")
            for i, (model, time_val) in enumerate(speed_ranking[:3], 1):
                print(f"  {i}. {model}: {time_val:.2f}s")
            
            # Rank by creativity
            creativity_ranking = sorted(
                [(name, statistics.mean(stats["creativity_scores"]) if stats["creativity_scores"] else 0) 
                 for name, stats in analysis["models"].items()],
                key=lambda x: x[1], reverse=True
            )
            print("Creativity (highest first):")
            for i, (model, score) in enumerate(creativity_ranking[:3], 1):
                print(f"  {i}. {model}: {score:.3f}")
            
            # Rank by technical depth
            technical_ranking = sorted(
                [(name, statistics.mean(stats["technical_scores"]) if stats["technical_scores"] else 0) 
                 for name, stats in analysis["models"].items()],
                key=lambda x: x[1], reverse=True
            )
            print("Technical Depth (highest first):")
            for i, (model, score) in enumerate(technical_ranking[:3], 1):
                print(f"  {i}. {model}: {score:.3f}")
            print()
        
        # Progress Estimate
        total_expected = len(analysis["prompts"]) * len(analysis["models"]) if analysis["models"] else 0
        if total_expected > 0:
            progress_percentage = (analysis["total_descriptions"] / total_expected) * 100
            print(f"ESTIMATED PROGRESS: {progress_percentage:.1f}%")
            
            if progress_percentage > 0:
                # Estimate time remaining
                files_completed = len([p for p in analysis["prompts"].values() if p["total_descriptions"] > 0])
                if files_completed > 0:
                    avg_time_per_prompt = sum(p["avg_response_time"] for p in analysis["prompts"].values()) / files_completed
                    remaining_prompts = len(analysis["prompts"]) - files_completed
                    estimated_remaining = remaining_prompts * avg_time_per_prompt
                    
                    if estimated_remaining > 60:
                        print(f"Estimated time remaining: {estimated_remaining/60:.1f} minutes")
                    else:
                        print(f"Estimated time remaining: {estimated_remaining:.0f} seconds")
            print()
        
        print("=" * 80)
        print("Press Ctrl+C to exit monitoring")
        print("Refreshing every 10 seconds...")
    
    def monitor(self):
        """Main monitoring loop"""
        try:
            while True:
                self.display_status()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        except Exception as e:
            print(f"\nMonitoring error: {e}")

def main():
    """Main entry point"""
    monitor = MultiModelMadnessMonitor()
    monitor.monitor()

if __name__ == "__main__":
    main()
