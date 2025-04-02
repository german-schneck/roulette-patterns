#!/usr/bin/env python3
"""
Starter script for the Advanced American Roulette Strategy Analyzer.
"""
import sys
import os

# Ensure src is in the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import and run the main function
from src.main import main

if __name__ == "__main__":
    main() 