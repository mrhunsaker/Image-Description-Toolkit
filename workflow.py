#!/usr/bin/env python3
"""Workflow wrapper - forwards calls to scripts/workflow.py"""
import sys
import os
import subprocess

root_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(root_dir, "scripts")
workflow_script = os.path.join(scripts_dir, "workflow.py")
original_cwd = os.getcwd()

args_with_cwd = ['--original-cwd', original_cwd] + sys.argv[1:]
cmd = [sys.executable, workflow_script] + args_with_cwd

result = subprocess.run(cmd, cwd=scripts_dir)
sys.exit(result.returncode)
