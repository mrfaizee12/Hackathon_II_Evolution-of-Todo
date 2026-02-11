#!/usr/bin/env python3
"""
Advanced script to fix backend import prefixes in Python files.

This script searches through all .py files in the project and updates import statements
based on the container's directory structure where WORKDIR is /app/backend/todo-service/src.
"""

import os
import re
from pathlib import Path


def fix_backend_imports_advanced(directory):
    """
    Fix backend import prefixes in all Python files within the given directory.
    This function understands the container's directory structure and adjusts imports accordingly.
    
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
                
                # Pattern to match imports starting with 'backend.'
                import_pattern = re.compile(r'(from|import)\s+backend\.([a-zA-Z_][a-zA-Z0-9_.]*)')
                
                # Replace backend. with the appropriate path based on the file's location
                def replace_import(match):
                    import_type = match.group(1)
                    module_path = match.group(2)
                    
                    # Determine if this is a service-specific import or a shared import
                    if any(service in module_path for service in ['todo_service', 'chatbot_service', 'recurring_engine', 'reminder_service']):
                        # For service-specific imports, adjust to relative path if in the same service
                        if 'todo-service' in str(file_path):
                            if module_path.startswith('todo_service'):
                                # Convert to relative import within the same service
                                return f"{import_type} {module_path.replace('todo_service.', '')}"
                        elif 'chatbot-service' in str(file_path):
                            if module_path.startswith('chatbot_service'):
                                return f"{import_type} {module_path.replace('chatbot_service.', '')}"
                        elif 'recurring-engine' in str(file_path):
                            if module_path.startswith('recurring_engine'):
                                return f"{import_type} {module_path.replace('recurring_engine.', '')}"
                        elif 'reminder-service' in str(file_path):
                            if module_path.startswith('reminder_service'):
                                return f"{import_type} {module_path.replace('reminder_service.', '')}"
                        
                        # For cross-service imports, keep as absolute
                        return f"{import_type} backend.{module_path}"
                    
                    # For infra and shared imports, keep as absolute
                    if module_path.startswith('infra.') or module_path.startswith('shared.'):
                        return f"{import_type} backend.{module_path}"
                    
                    # Default: keep as absolute import
                    return f"{import_type} backend.{module_path}"
                
                # Apply the replacement
                content = import_pattern.sub(replace_import, content)
                
                # Also handle the case where the import was completely removed by the previous script
                # If a file is in todo-service and imports infra or shared, it needs 'backend.' prefix
                if 'todo-service' in str(file_path) or 'chatbot-service' in str(file_path) or \
                   'recurring-engine' in str(file_path) or 'reminder-service' in str(file_path):
                    # Add backend prefix to infra and shared imports that might have been incorrectly changed
                    content = re.sub(r'(from|import)\s+(infra|shared)([.\w]*)', r'\1 backend.\2\3', content)
                
                # If content changed, write it back to the file
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated imports in: {file_path}")
                    changes_made += 1
    
    print(f"\nCompleted! Made changes to {changes_made} files.")


def restore_correct_imports(directory):
    """
    Restore correct backend imports that may have been incorrectly removed by the first script.
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
                
                # For files in service directories, if they import infra or shared without backend prefix, add it
                if any(service in str(file_path) for service in ['todo-service', 'chatbot-service', 'recurring-engine', 'reminder-service']):
                    # Add backend prefix to infra and shared imports
                    content = re.sub(r'(?<!backend\.)(from|import)\s+(infra|shared)([.\w]*)', r'\1 backend.\2\3', content)
                
                # If content changed, write it back to the file
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Restored backend prefix in: {file_path}")
                    changes_made += 1
    
    print(f"\nRestored backend prefixes in {changes_made} files.")


def main():
    # Get the project root directory (where this script is located)
    project_root = Path(__file__).parent
    
    print("Scanning for Python files to fix backend import prefixes...")
    print(f"Project root: {project_root}")
    
    # First, restore correct backend prefixes that may have been incorrectly removed
    backend_dir = project_root / "backend"
    if backend_dir.exists():
        restore_correct_imports(backend_dir)
        
        # Then apply advanced fixing
        fix_backend_imports_advanced(backend_dir)
    else:
        print(f"Warning: Backend directory not found at {backend_dir}")
    
    print("\nImport fixing completed!")
    print("\nFor your Kubernetes YAML, set PYTHONPATH to:")
    print("PYTHONPATH=/app:/app/backend")
    print("\nThis ensures that:")
    print("- /app allows imports from the root (like 'from shared.event_bus')")
    print("- /app/backend allows imports from backend (like 'from infra.config.validator')")


if __name__ == "__main__":
    main()