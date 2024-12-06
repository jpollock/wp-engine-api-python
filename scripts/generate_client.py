#!/usr/bin/env python3
"""Script to generate API client code from swagger specification."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    """Generate API client code from swagger specification."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.absolute()
    
    # Paths
    swagger_file = project_root / "swagger.json"
    generated_dir = project_root / "generated"
    target_dir = project_root / "src" / "wp_engine_api" / "generated"
    
    # Check if swagger file exists
    if not swagger_file.exists():
        print(f"Error: swagger.json not found at {swagger_file}")
        sys.exit(1)
    
    # Create or clean the generated directory
    if generated_dir.exists():
        shutil.rmtree(generated_dir)
    generated_dir.mkdir(exist_ok=True)
    
    # Create or clean the target directory
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(exist_ok=True, parents=True)
    
    # Generate the client code
    cmd = [
        "openapi-generator-cli",
        "generate",
        "-i", str(swagger_file),
        "-g", "python",
        "-o", str(generated_dir),
        "--package-name", "wp_engine_api.generated"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating client code: {e}")
        sys.exit(1)
    
    # Move generated files to target directory
    generated_package = generated_dir / "wp_engine_api" / "generated"
    if not generated_package.exists():
        print(f"Error: Generated package not found at {generated_package}")
        sys.exit(1)
    
    # Copy files
    try:
        # Copy all files from generated package
        for item in generated_package.iterdir():
            if item.is_file():
                shutil.copy2(item, target_dir)
            elif item.is_dir():
                shutil.copytree(item, target_dir / item.name)
        
        print(f"Successfully generated client code in {target_dir}")
    except Exception as e:
        print(f"Error copying generated files: {e}")
        sys.exit(1)
    finally:
        # Clean up
        shutil.rmtree(generated_dir)

if __name__ == "__main__":
    main()
