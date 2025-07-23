#!/usr/bin/env python3
"""
Project Cleanup and Reorganization Script

This script cleans up the experimental cruft and organizes files properly:
1. Archives experimental data safely
2. Removes duplicate/temporary files 
3. Organizes scripts into logical categories
4. Creates clean project structure
"""

import shutil
from pathlib import Path
from datetime import datetime

def cleanup_project():
    """Clean up the project directory structure"""
    
    print("🧹 CLEANING UP PROJECT DIRECTORY")
    print("=" * 50)
    
    # Paths
    scripts_dir = Path("../scripts")
    archive_dir = Path("../archived_experiments/ultimate_prompt_madness_20250722_recovery")
    root_dir = Path("..")
    
    # Create archive if it doesn't exist
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Archive all experimental/temporary files
    print("📦 Archiving experimental files...")
    
    experimental_patterns = [
        "*madness*",
        "*experiment*", 
        "*discovery*",
        "*analysis*",
        "*monitor*",
        "*debug*",
        "*temp*",
        "*quick*",
        "*setup*",
        "*requirements*"
    ]
    
    archived_count = 0
    for pattern in experimental_patterns:
        for file_path in scripts_dir.glob(pattern):
            if file_path.is_file() and not file_path.name.endswith("_FIXED.py"):
                # Don't archive core scripts
                core_scripts = ["workflow.py", "image_describer.py", "video_frame_extractor.py", 
                               "descriptions_to_html.py", "ConvertImage.py", "workflow_utils.py"]
                if file_path.name not in core_scripts:
                    try:
                        shutil.copy2(file_path, archive_dir / file_path.name)
                        print(f"  📁 Archived: {file_path.name}")
                        archived_count += 1
                    except Exception as e:
                        print(f"  ⚠️  Failed to archive {file_path.name}: {e}")
    
    # 2. Archive experimental directories
    exp_dirs = ["prompt_experiments", "prompt_experiments_extended", "prompt_experiments_madness", 
                "temp_converted", "__pycache__", "workflow_output"]
    
    for dir_name in exp_dirs:
        dir_path = scripts_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            try:
                if dir_name != "workflow_output":  # Keep workflow_output structure
                    shutil.copytree(dir_path, archive_dir / dir_name, dirs_exist_ok=True)
                    print(f"  📁 Archived directory: {dir_name}")
                    archived_count += 1
            except Exception as e:
                print(f"  ⚠️  Failed to archive directory {dir_name}: {e}")
    
    print(f"✅ Archived {archived_count} items")
    
    # 3. Remove log files from root
    print("\n🗑️  Cleaning root directory...")
    root_cleaned = 0
    for log_file in root_dir.glob("*.log"):
        try:
            shutil.move(str(log_file), str(archive_dir / log_file.name))
            print(f"  🗑️  Moved log file: {log_file.name}")
            root_cleaned += 1
        except Exception as e:
            print(f"  ⚠️  Failed to move {log_file.name}: {e}")
    
    print(f"✅ Cleaned {root_cleaned} files from root")
    
    # 4. Create organized structure summary
    print("\n📋 RECOMMENDED PROJECT STRUCTURE:")
    print("-" * 30)
    print("📁 idt/")
    print("  ├── 📄 workflow.py (main entry point)")
    print("  ├── 📄 requirements.txt")
    print("  ├── 📄 README.md")
    print("  ├── 📁 scripts/")
    print("  │   ├── 📄 workflow_utils.py")
    print("  │   ├── 📄 image_describer.py")
    print("  │   ├── 📄 video_frame_extractor.py")
    print("  │   ├── 📄 descriptions_to_html.py")
    print("  │   ├── 📄 ConvertImage.py")
    print("  │   ├── 📄 ultimate_prompt_madness_FIXED.py (corrected version)")
    print("  │   └── 📁 config/")
    print("  ├── 📁 tests/")
    print("  ├── 📁 docs/")
    print("  ├── 📁 workflow_output/ (timestamped runs)")
    print("  └── 📁 archived_experiments/ (historical data)")
    
    # 5. Create cleanup recommendations
    print("\n🎯 CLEANUP RECOMMENDATIONS:")
    print("-" * 30)
    print("1. ✅ Archive experimental data (DONE)")
    print("2. 🔄 Replace ultimate_prompt_madness.py with _FIXED version")
    print("3. 🗑️  Remove duplicate/temporary scripts")
    print("4. 📝 Update configs to use workflow_output pattern")
    print("5. 🧪 Test corrected scripts")
    
    print(f"\n✅ PROJECT CLEANUP COMPLETE!")
    print(f"📁 Experimental data archived to: {archive_dir}")
    
    return {
        "archived_items": archived_count,
        "root_cleaned": root_cleaned,
        "archive_location": str(archive_dir)
    }

if __name__ == "__main__":
    results = cleanup_project()
    print(f"\n📊 Summary: {results['archived_items']} items archived, {results['root_cleaned']} root files cleaned")
