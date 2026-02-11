#!/usr/bin/env python3
"""
Script to fix backend import prefixes in Python files.

This script searches through all .py files in the project and updates import statements
to remove the 'backend.' prefix, which causes ModuleNotFoundError when running in containers.
"""

import os
import re
from pathlib import Path


def fix_backend_imports(directory):
    """
    Fix backend import prefixes in all Python files within the given directory.
    
    Args:
        directory (str): Root directory to search for Python files
    """
    # Define the pattern to match import statements with 'backend.' prefix
    import_pattern = re.compile(r'(from|import)\s+backend\.(\w+)')
    
    # Counter for changes made
    changes_made = 0
    
    # Walk through all Python files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find and replace backend import patterns
                original_content = content
                content = re.sub(import_pattern, r'\1 \2', content)
                
                # Special handling for deeper nested imports like backend.infra.config.validator
                deep_import_pattern = re.compile(r'(from|import)\s+backend\.((?:\w+\.)+\w+)')
                content = re.sub(deep_import_pattern, r'\1 \2', content)
                
                # If content changed, write it back to the file
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated imports in: {file_path}")
                    changes_made += 1
    
    print(f"\nCompleted! Made changes to {changes_made} files.")


def main():
    # Get the project root directory (where this script is located)
    project_root = Path(__file__).parent
    
    print("Scanning for Python files to fix backend import prefixes...")
    print(f"Project root: {project_root}")
    
    # Fix imports in the backend directory
    backend_dir = project_root / "backend"
    if backend_dir.exists():
        fix_backend_imports(backend_dir)
    else:
        print(f"Warning: Backend directory not found at {backend_dir}")
    
    print("\nImport fixing completed!")
    print("\nFor your Kubernetes YAML, set PYTHONPATH to:")
    print("PYTHONPATH=/app:/app/backend")


if __name__ == "__main__":
    main()