#!/usr/bin/env python3
"""
Comprehensive script to fix all import issues in the Python FastAPI project.

This script:
1. Fixes import statements in all Python files to work with container environment
2. Updates Dockerfiles with correct PYTHONPATH
3. Ensures modules are accessible in the container where WORKDIR is /app/backend/service-name/src
"""

import os
import re
import shutil
from pathlib import Path


def fix_import_statements(project_root):
    """
    Fix import statements in all Python files to work with container environment.
    
    Args:
        project_root (str): Root directory of the project
    """
    print("Fixing import statements in Python files...")
    
    changes_made = 0
    backend_dir = Path(project_root) / "backend"
    
    # Walk through all Python files in the backend directory
    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix imports that were incorrectly changed by previous scripts
                # For files in service directories, ensure infra and shared imports have 'backend.' prefix
                if any(service in str(file_path) for service in ['todo-service', 'chatbot-service', 'recurring-engine', 'reminder-service']):
                    # Add backend prefix to infra and shared imports that might have been incorrectly removed
                    content = re.sub(r'(?<!backend\.)(from|import)\s+(infra|shared)([.\w]*)', r'\1 backend.\2\3', content)
                
                # Fix fallback imports for service-specific modules
                # When WORKDIR is /app/backend/service-name/src, relative imports should work
                content = re.sub(
                    r'from (\w+)_service\.src\.(\w+)\.(\w+) import',
                    r'from \2.\3 import',
                    content
                )
                
                # Fix fallback imports for backend.service-specific modules
                content = re.sub(
                    r'from backend\.(\w+)_service\.src\.(\w+)\.(\w+) import',
                    r'from \2.\3 import',
                    content
                )
                
                # If content changed, write it back to the file
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"  Fixed imports in: {file_path}")
                    changes_made += 1
    
    print(f"Completed! Fixed imports in {changes_made} files.")


def update_dockerfiles_pythonpath(project_root):
    """
    Update all Dockerfiles with the correct PYTHONPATH.
    
    Args:
        project_root (str): Root directory of the project
    """
    print("Updating Dockerfiles with correct PYTHONPATH...")
    
    dockerfiles = [
        Path(project_root) / "Dockerfiles" / "todo-service.Dockerfile",
        Path(project_root) / "Dockerfiles" / "chatbot-service.Dockerfile",
        Path(project_root) / "Dockerfiles" / "recurring-engine.Dockerfile",
        Path(project_root) / "Dockerfiles" / "reminder-service.Dockerfile"
    ]
    
    changes_made = 0
    
    for dockerfile_path in dockerfiles:
        if dockerfile_path.exists():
            with open(dockerfile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update or add PYTHONPATH environment variable
            if 'ENV PYTHONPATH=' in content:
                # Replace existing PYTHONPATH with the correct one
                content = re.sub(
                    r'ENV PYTHONPATH=.*',
                    'ENV PYTHONPATH=/app:/app/backend',
                    content
                )
            else:
                # Add PYTHONPATH environment variable after the WORKDIR instruction for service
                content = re.sub(
                    r'(WORKDIR /app/backend/\w+-service/src)',
                    r'\1\nENV PYTHONPATH=/app:/app/backend',
                    content
                )
            
            if content != original_content:
                with open(dockerfile_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  Updated PYTHONPATH in: {dockerfile_path}")
                changes_made += 1
        else:
            print(f"  Warning: Dockerfile not found: {dockerfile_path}")
    
    print(f"Completed! Updated PYTHONPATH in {changes_made} Dockerfiles.")


def update_kubernetes_deployments(project_root):
    """
    Update Kubernetes deployment files to set the correct PYTHONPATH.
    
    Args:
        project_root (str): Root directory of the project
    """
    print("Updating Kubernetes deployments with correct PYTHONPATH...")
    
    deployment_files = [
        Path(project_root) / "todo-service-deployment.yaml",
        Path(project_root) / "chatbot-service-deployment.yaml",
        Path(project_root) / "recurring-engine-deployment.yaml",
        Path(project_root) / "reminder-service-deployment.yaml",
        Path(project_root) / "backend-deployment.yaml"
    ]
    
    changes_made = 0
    
    for deployment_path in deployment_files:
        if deployment_path.exists():
            with open(deployment_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Add PYTHONPATH environment variable if not already present
            # Look for the containers section and add PYTHONPATH to environment variables
            lines = content.split('\n')
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                new_lines.append(line)
                
                # If we find the 'containers:' line, look for the next 'env:' section or add one
                if 'containers:' in line:
                    # Look ahead for the next 'env:' section or add environment variables
                    j = i + 1
                    env_section_found = False
                    
                    # Find the next 'env:' section or the end of the container definition
                    while j < len(lines) and not lines[j].strip().startswith('- name:'):  # Next container
                        if 'env:' in lines[j]:
                            env_section_found = True
                            
                            # Check if PYTHONPATH is already set
                            pythonpath_exists = False
                            k = j + 1
                            while k < len(lines) and not lines[k].strip().startswith('- name:') and not lines[k].strip().startswith('ports:'):
                                if 'PYTHONPATH' in lines[k]:
                                    pythonpath_exists = True
                                    break
                                k += 1
                            
                            if not pythonpath_exists:
                                # Insert PYTHONPATH after the 'env:' line
                                indent_level = len(lines[j]) - len(lines[j].lstrip())
                                new_lines.insert(j + 1, ' ' * (indent_level + 2) + '- name: PYTHONPATH')
                                new_lines.insert(j + 2, ' ' * (indent_level + 4) + 'value: "/app:/app/backend"')
                            
                            break
                        j += 1
                    
                    # If no env section was found, add one
                    if not env_section_found:
                        # Find where to insert the env section (after image, before ports)
                        j = i + 1
                        while j < len(lines) and not lines[j].strip().startswith('- name:'):  # Next container
                            if 'image:' in lines[j]:
                                # Insert env section after the image line
                                indent_level = len(lines[j]) - len(lines[j].lstrip())
                                new_lines.insert(j + 1, ' ' * indent_level + 'env:')
                                new_lines.insert(j + 2, ' ' * (indent_level + 2) + '- name: PYTHONPATH')
                                new_lines.insert(j + 3, ' ' * (indent_level + 4) + 'value: "/app:/app/backend"')
                                break
                            j += 1
                
                i += 1
            
            content = '\n'.join(new_lines)
            
            if content != original_content:
                with open(deployment_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  Updated PYTHONPATH in: {deployment_path}")
                changes_made += 1
        else:
            print(f"  Warning: Deployment file not found: {deployment_path}")
    
    print(f"Completed! Updated PYTHONPATH in {changes_made} Kubernetes deployment files.")


def main():
    # Get the project root directory (where this script is located)
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    print("=" * 60)
    print("COMPREHENSIVE PYTHON IMPORT FIX SCRIPT")
    print("=" * 60)
    
    # Step 1: Fix import statements in Python files
    fix_import_statements(project_root)
    
    print()
    
    # Step 2: Update Dockerfiles with correct PYTHONPATH
    update_dockerfiles_pythonpath(project_root)
    
    print()
    
    # Step 3: Update Kubernetes deployments with correct PYTHONPATH
    update_kubernetes_deployments(project_root)
    
    print()
    print("=" * 60)
    print("ALL FIXES APPLIED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("SUMMARY:")
    print("- Fixed import statements in Python files to work with container environment")
    print("- Updated Dockerfiles with PYTHONPATH=/app:/app/backend")
    print("- Updated Kubernetes deployments with PYTHONPATH=/app:/app/backend")
    print()
    print("NEXT STEPS:")
    print("1. Rebuild all Docker images with --no-cache flag")
    print("2. Load the new images into Minikube")
    print("3. Delete and recreate Kubernetes pods to use new images")
    print()
    print("Example commands:")
    print("  docker build --no-cache -f ./Dockerfiles/todo-service.Dockerfile -t todo-service:1.0.0 .")
    print("  docker build --no-cache -f ./Dockerfiles/chatbot-service.Dockerfile -t chatbot-service:1.0.0 .")
    print("  docker build --no-cache -f ./Dockerfiles/recurring-engine.Dockerfile -t recurring-engine:1.0.0 .")
    print("  docker build --no-cache -f ./Dockerfiles/reminder-service.Dockerfile -t reminder-service:1.0.0 .")
    print("  minikube image load todo-service:1.0.0")
    print("  minikube image load chatbot-service:1.0.0")
    print("  minikube image load recurring-engine:1.0.0")
    print("  minikube image load reminder-service:1.0.0")
    print("  kubectl delete pods --all -n todo-chatbot")


if __name__ == "__main__":
    main()