import pytest
import sys
import os
from pathlib import Path

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to Python path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Print debug information
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")
print(f"Contents of project root: {os.listdir(project_root)}")