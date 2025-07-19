#!/usr/bin/env python3
"""
Video Frame Extractor
Extracts frames from video files based on configurable options including scene change detection.
"""

import cv2
import os
import json
import argparse
import numpy as np
from pathlib import Path
from typing import List
import time
import logging
from datetime import datetime

class VideoFrameExtractor:
    def __init__(self, config_file: str = "frame_extractor_config.json"):
        self.supported_formats = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
        self.config = self.load_config(config_file)
        self.setup_logging()
        print("VideoFrameExtractor initialized successfully")
        
    def setup_logging(self):
        """Set up logging to both console and file"""
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"frame_extractor_{timestamp}.log"
        
        # Create logger
        self.logger = logging.getLogger(f"frame_extractor_{timestamp}")
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Create file handler
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Frame extractor started. Log file: {os.path.abspath(log_filename)}")
        self.logger.info(f"Working directory: {os.getcwd()}")
        
    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    print(f"Config file {config_file} is empty. Creating default config.")
                    return self.create_default_config(config_file)
                return json.loads(content)
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Creating default config.")
            return self.create_default_config(config_file)
        except json.JSONDecodeError as e:
            print(f"Error parsing config file {config_file}: {e}")
            print("Creating default config.")
            return self.create_default_config(config_file)
    
    def create_default_config(self, config_file: str) -> dict:
        """Create a default configuration file and return the config"""
        default_config = {
            "extraction_mode": "time_interval",
            "time_interval_seconds": 5.0,
            "scene_change_threshold": 30.0,
            "min_scene_duration_seconds": 1.0,
            "output_directory": "extracted_frames",
            "preserve_directory_structure": False,
            "image_quality": 95,
            "resize_width": None,
            "resize_height": None,
            "frame_prefix": "frame",
            "start_time_seconds": 0,
            "end_time_seconds": None,
            "max_frames_per_video": None,
            "skip_existing": False,
            "log_progress": True
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            
            print(f"Created default config file: {config_file}")
            print("You can edit this file to customize extraction settings.")
        except Exception as e:
            print(f"Warning: Could not create config file {config_file}: {e}")
            print("Using default configuration in memory.")
        
        return default_config
    
    def calculate_scene_change(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Calculate the difference between two frames as a percentage"""
        if frame1 is None or frame2 is None:
            return 0.0

        # Convert to grayscale for comparison
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Calculate percentage of pixels that changed significantly
        threshold = 30  # Pixel difference threshold
        changed_pixels = np.sum(diff > threshold)
        total_pixels = diff.shape[0] * diff.shape[1]
        
        return (changed_pixels / total_pixels) * 100
    
    def extract_frames_time_interval(self, video_path: str, output_dir: str) -> List[str]:
        """Extract frames at regular time intervals"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        interval_frames = int(fps * self.config["time_interval_seconds"])
        start_frame = int(fps * self.config["start_time_seconds"])
        end_frame = int(fps * self.config["end_time_seconds"]) if self.config["end_time_seconds"] else total_frames
        
        extracted_files = []
        frame_count = 0
        current_frame = start_frame
        
        if self.config["log_progress"]:
            print(f"  Video info: {duration:.1f}s, {fps:.1f} FPS, {total_frames} frames")
            print(f"  Extracting every {self.config['time_interval_seconds']}s")
        
        while current_frame < end_frame:
            if self.config["max_frames_per_video"] and frame_count >= self.config["max_frames_per_video"]:
                break
                
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Resize if specified
            if self.config["resize_width"] or self.config["resize_height"]:
                frame = self.resize_frame(frame)
            
            # Save frame
            timestamp = current_frame / fps
            filename = f"{self.config['frame_prefix']}_{timestamp:.2f}s.jpg"
            output_path = os.path.join(output_dir, filename)
            
            cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, self.config["image_quality"]])
            extracted_files.append(output_path)
            
            frame_count += 1
            current_frame += interval_frames
            
            if self.config["log_progress"] and frame_count % 10 == 0:
                print(f"    Extracted {frame_count} frames...")
                print(f"    Latest file saved: {os.path.abspath(output_path)}")
        
        cap.release()
        return extracted_files
    
    def extract_frames_scene_change(self, video_path: str, output_dir: str) -> List[str]:
        """Extract frames when scene changes are detected"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return []
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        start_frame = int(fps * self.config["start_time_seconds"])
        end_frame = int(fps * self.config["end_time_seconds"]) if self.config["end_time_seconds"] else total_frames
        min_scene_frames = int(fps * self.config["min_scene_duration_seconds"])
        
        extracted_files = []
        frame_count = 0
        last_scene_frame = start_frame
        prev_frame = None
        
        if self.config["log_progress"]:
            print(f"  Video info: {duration:.1f}s, {fps:.1f} FPS, {total_frames} frames")
            print(f"  Scene change threshold: {self.config['scene_change_threshold']}%")
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        for current_frame_num in range(start_frame, end_frame):
            if self.config["max_frames_per_video"] and frame_count >= self.config["max_frames_per_video"]:
                break
            
            ret, frame = cap.read()
            if not ret:
                break
            
            # Check for scene change
            if prev_frame is not None:
                change_percentage = self.calculate_scene_change(prev_frame, frame)
                
                # If significant change and minimum time has passed
                if (change_percentage > self.config["scene_change_threshold"] and 
                    current_frame_num - last_scene_frame >= min_scene_frames):
                    
                    # Resize if specified
                    save_frame = frame
                    if self.config["resize_width"] or self.config["resize_height"]:
                        save_frame = self.resize_frame(frame)
                    
                    # Save frame
                    timestamp = current_frame_num / fps
                    filename = f"{self.config['frame_prefix']}_scene_{timestamp:.2f}s.jpg"
                    output_path = os.path.join(output_dir, filename)
                    
                    cv2.imwrite(output_path, save_frame, [cv2.IMWRITE_JPEG_QUALITY, self.config["image_quality"]])
                    extracted_files.append(output_path)
                    
                    frame_count += 1
                    last_scene_frame = current_frame_num
                    
                    if self.config["log_progress"]:
                        print(f"    Scene change detected at {timestamp:.2f}s ({change_percentage:.1f}% change)")
                        print(f"    Saved frame: {os.path.abspath(output_path)}")
            
            prev_frame = frame.copy()
        
        cap.release()
        return extracted_files
    
    def resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame based on config settings"""
        height, width = frame.shape[:2]
        new_width = self.config["resize_width"]
        new_height = self.config["resize_height"]
        
        if new_width and new_height:
            return cv2.resize(frame, (new_width, new_height))
        elif new_width:
            ratio = new_width / width
            new_height = int(height * ratio)
            return cv2.resize(frame, (new_width, new_height))
        elif new_height:
            ratio = new_height / height
            new_width = int(width * ratio)
            return cv2.resize(frame, (new_width, new_height))
        
        return frame
    
    def process_video(self, video_path: str) -> List[str]:
        """Process a single video file"""
        if self.config["log_progress"]:
            print(f"Processing: {video_path}")
        
        print(f"Video file stem (name without extension): {Path(video_path).stem}")
        
        # Create output directory
        if self.config["preserve_directory_structure"]:
            # Get relative path from current directory
            rel_path = os.path.relpath(video_path)
            print(f"Relative path from current dir: {rel_path}")
            print(f"Directory part: {os.path.dirname(rel_path)}")
            output_subdir = os.path.join(
                self.config["output_directory"],
                os.path.dirname(rel_path),
                Path(video_path).stem
            )
        else:
            # Simple flat structure: just output_directory/video_name
            # Don't use relative paths - just the video filename
            output_subdir = os.path.join(
                self.config["output_directory"],
                Path(video_path).stem
            )
        
        print(f"Creating output directory: {output_subdir}")
        os.makedirs(output_subdir, exist_ok=True)
        print(f"Output directory: {os.path.abspath(output_subdir)}")
        
        # Check if we should skip existing
        if self.config["skip_existing"]:
            existing_files = os.listdir(output_subdir)
            if existing_files:
                print(f"  Skipping: Output directory not empty")
                print(f"  Found {len(existing_files)} existing files in: {os.path.abspath(output_subdir)}")
                print(f"  First few files: {existing_files[:5]}")
                print(f"  To process anyway, set 'skip_existing': false in config or delete the directory")
                return []
        
        # Extract frames based on mode
        if self.config["extraction_mode"] == "time_interval":
            extracted_files = self.extract_frames_time_interval(video_path, output_subdir)
        elif self.config["extraction_mode"] == "scene_change":
            extracted_files = self.extract_frames_scene_change(video_path, output_subdir)
        else:
            print(f"  Error: Unknown extraction mode '{self.config['extraction_mode']}'")
            return []
        
        # Log summary for this video
        if extracted_files:
            print(f"  Extracted {len(extracted_files)} frames to: {os.path.abspath(output_subdir)}")
            print(f"  First frame: {os.path.basename(extracted_files[0])}")
            print(f"  Last frame: {os.path.basename(extracted_files[-1])}")
        
        return extracted_files
    
    def find_video_files(self, directory: str) -> List[str]:
        """Find all video files in directory and subdirectories"""
        video_files = []
        abs_directory = os.path.abspath(directory)
        
        print(f"Searching for video files in: {abs_directory}")
            
        if not os.path.exists(directory):
            print(f"Error: Directory does not exist: {abs_directory}")
            return video_files
            
        dir_count = 0
        total_files_checked = 0
        
        for root, dirs, files in os.walk(directory):
            dir_count += 1
            total_files_checked += len(files)
            
            # Print progress every 10 directories
            if dir_count % 10 == 1:
                print(f"Checking directory {dir_count}: {root}")
            
            for file in files:
                file_suffix = Path(file).suffix.lower()
                if file_suffix in self.supported_formats:
                    full_path = os.path.join(root, file)
                    video_files.append(full_path)
                    # Print first 10 found videos, then show summary
                    if len(video_files) <= 10:
                        print(f"Found video file: {full_path}")
                    elif len(video_files) == 11:
                        print("... (additional videos found, showing count only)")
        
        print(f"Search complete: {dir_count} directories, {total_files_checked} files checked")
        print(f"Total video files found: {len(video_files)}")
            
        return video_files
    
    def run(self, input_path: str):
        """Main execution method"""
        start_time = time.time()
        
        print("Video Frame Extractor")
        print("===================")
        print(f"Mode: {self.config['extraction_mode']}")
        print(f"Output directory: {self.config['output_directory']}")
        print(f"Full output path: {os.path.abspath(self.config['output_directory'])}")
        print("")
        
        # Find video files
        if os.path.isfile(input_path):
            if Path(input_path).suffix.lower() in self.supported_formats:
                video_files = [input_path]
            else:
                print(f"Error: {input_path} is not a supported video format")
                return
        else:
            video_files = self.find_video_files(input_path)
        
        if not video_files:
            print("No video files found.")
            return
        
        print(f"Found {len(video_files)} video file(s)")
        for i, video in enumerate(video_files, 1):
            print(f"  {i}. {video}")
        print("")
        
        # Process videos
        total_extracted = 0
        for i, video_path in enumerate(video_files, 1):
            print(f"[{i}/{len(video_files)}]")
            extracted = self.process_video(video_path)
            total_extracted += len(extracted)
            
            if self.config["log_progress"]:
                print(f"  Extracted {len(extracted)} frames")
            print("")
        
        # Summary
        elapsed_time = time.time() - start_time
        print("Summary")
        print("=======")
        print(f"Processed {len(video_files)} video(s)")
        print(f"Extracted {total_extracted} frame(s)")
        print(f"Time elapsed: {elapsed_time:.1f} seconds")
        print(f"Output directory: {os.path.abspath(self.config['output_directory'])}")
        
        # Help user find the files
        if total_extracted > 0:
            print("\n" + "="*50)
            print("WHERE TO FIND YOUR EXTRACTED FRAMES:")
            print("="*50)
            
            # Check if output directory exists and list its contents
            output_dir = os.path.abspath(self.config['output_directory'])
            if os.path.exists(output_dir):
                print(f"Main output directory: {output_dir}")
                
                # List all subdirectories
                try:
                    for root, dirs, files in os.walk(output_dir):
                        if files:  # Only show directories that contain files
                            print(f"  Directory: {root}")
                            print(f"    Contains {len(files)} files")
                            if files:
                                print(f"    Sample files: {files[:3]}")
                except Exception as e:
                    print(f"Error listing directories: {e}")
            else:
                print(f"Warning: Output directory {output_dir} does not exist!")
            
            print("\nTo open the directory in Windows Explorer:")
            print(f'explorer "{output_dir}"')
            print("="*50)

def main():
    parser = argparse.ArgumentParser(description="Extract frames from video files")
    parser.add_argument("input", help="Input video file or directory")
    parser.add_argument("-c", "--config", default="frame_extractor_config.json",
                       help="Path to config file (default: frame_extractor_config.json)")
    
    # Extraction mode options (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--time", type=float, metavar="SECONDS",
                           help="Use time interval extraction mode with specified interval in seconds (overrides config)")
    mode_group.add_argument("--scene", type=float, metavar="THRESHOLD",
                           help="Use scene change detection mode with specified threshold percentage (overrides config)")
    
    args = parser.parse_args()
    
    extractor = VideoFrameExtractor(args.config)
    
    # Override extraction mode based on command line arguments
    if args.time is not None:
        extractor.config["extraction_mode"] = "time_interval"
        extractor.config["time_interval_seconds"] = args.time
        print(f"Command line override: Using time interval extraction mode ({args.time}s intervals)")
    elif args.scene is not None:
        extractor.config["extraction_mode"] = "scene_change"
        extractor.config["scene_change_threshold"] = args.scene
        print(f"Command line override: Using scene change detection mode ({args.scene}% threshold)")
    
    extractor.run(args.input)

if __name__ == "__main__":
    main()
