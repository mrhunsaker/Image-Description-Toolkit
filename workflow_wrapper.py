#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Description Toolkit - Workflow Wrapper

This is a wrapper script that runs the actual workflow from the scripts directory.
It maintains backward compatibility for users expecting workflow.py in the root.
"""

import sys
import os
import subprocess

# Get the directory containing this script
root_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(root_dir, "scripts")
workflow_script = os.path.join(scripts_dir, "workflow.py")

# Forward all arguments to the actual workflow script
result = subprocess.run([sys.executable, workflow_script] + sys.argv[1:], cwd=scripts_dir)
sys.exit(result.returncode)
