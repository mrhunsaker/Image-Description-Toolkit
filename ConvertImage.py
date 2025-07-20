#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert Image Wrapper

This is a wrapper script that runs the actual ConvertImage from the scripts directory.
It maintains backward compatibility for users expecting ConvertImage.py in the root.
"""

import sys
import os
import subprocess

# Get the directory containing this script
root_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(root_dir, "scripts")
script_path = os.path.join(scripts_dir, "ConvertImage.py")

# Forward all arguments to the actual script
result = subprocess.run([sys.executable, script_path] + sys.argv[1:], cwd=scripts_dir)
sys.exit(result.returncode)
