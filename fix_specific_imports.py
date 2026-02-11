#!/usr/bin/env python3
"""
Final script to fix specific import issues in Python files.

This script addresses specific import issues in the container environment where 
WORKDIR is /app/backend/todo-service/src.
"""

import os
import re
from pathlib import Path


def fix_fallback_imports(directory):
    """
    Fix fallback imports that are incorrect for the container environment.
    
    Args:
        directory (str): Root directory to search for Python files
    """
    changes_made = 0
    
    # Walk through all Python files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix fallback imports for service-specific modules
                # When WORKDIR is /app/backend/todo-service/src, relative imports should work
                content = re.sub(
                    r'from todo_service\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                content = re.sub(
                    r'from chatbot_service\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                content = re.sub(
                    r'from recurring_engine\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                content = re.sub(
                    r'from reminder_service\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                
                # Fix fallback imports for service-specific modules (alternative pattern)
                content = re.sub(
                    r'from backend\.todo_service\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                content = re.sub(
                    r'from backend\.chatbot_service\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                content = re.sub(
                    r'from backend\.recurring_engine\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                content = re.sub(
                    r'from backend\.reminder_service\.src\.(\w+)\.(\w+) import',
                    r'from \1.\2 import',
                    content
                )
                
                # If content changed, write it back to the file
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Fixed fallback imports in: {file_path}")
                    changes_made += 1
    
    print(f"\nCompleted! Fixed fallback imports in {changes_made} files.")


def update_dockerfiles_pythonpath():
    """
    Update Dockerfiles to ensure correct PYTHONPATH is set.
    """
    dockerfiles = [
        "Dockerfiles/todo-service.Dockerfile",
        "Dockerfiles/chatbot-service.Dockerfile",
        "Dockerfiles/recurring-engine.Dockerfile",
        "Dockerfiles/reminder-service.Dockerfile"
    ]
    
    changes_made = 0
    
    for dockerfile_path in dockerfiles:
        full_path = Path(dockerfile_path)
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update PYTHONPATH to include both /app and /app/backend
            if 'ENV PYTHONPATH=' in content:
                # Replace existing PYTHONPATH with the correct one
                content = re.sub(
                    r'ENV PYTHONPATH=.*',
                    'ENV PYTHONPATH=/app:/app/backend',
                    content
                )
            else:
                # Add PYTHONPATH environment variable after WORKDIR
                content = re.sub(
                    r'(WORKDIR /app/backend/\w+-service/src)',
                    r'\1\nENV PYTHONPATH=/app:/app/backend',
                    content
                )
            
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated PYTHONPATH in: {dockerfile_path}")
                changes_made += 1
    
    print(f"\nUpdated PYTHONPATH in {changes_made} Dockerfiles.")


def main():
    # Get the project root directory (where this script is located)
    project_root = Path(__file__).parent
    
    print("Fixing specific import issues...")
    print(f"Project root: {project_root}")
    
    # Fix fallback imports
    backend_dir = project_root / "backend"
    if backend_dir.exists():
        fix_fallback_imports(backend_dir)
    
    # Update Dockerfiles with correct PYTHONPATH
    update_dockerfiles_pythonpath()
    
    print("\nAll fixes applied!")
    print("\nFor your Kubernetes YAML, ensure PYTHONPATH is set to:")
    print("PYTHONPATH=/app:/app/backend")
    print("\nThis ensures that:")
    print("- /app allows imports from the root (like 'from shared.event_bus')")
    print("- /app/backend allows imports from backend (like 'from infra.config.validator')")


if __name__ == "__main__":
    main()