"""
Entrypoint for Streamlit Web Application.
Runs the main app located in src/ui/app.py.
"""

from pathlib import Path
import sys

# Ensure root directory is in python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Run the UI application
from src.ui.app import *
