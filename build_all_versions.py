#!/usr/bin/env python3
"""
Comprehensive build script for all versions of the Medical Laboratory Management System
"""
import os
import sys
import subprocess
import shutil

def build_web_version():
    """Build and package the web version"""
    print("Building web version...")
    
    try:
        # Create web version directory in final distribution
        web_dist_path = "final_distribution/web_version"
        if os.path.exists(web_dist_path):
            shutil.rmtree(web_dist_path)
        
        # Copy web version files
        shutil.copytree("deployments/web_version", web_dist_path)
        
        # Create a requirements.txt for the web version
        web_requirements = [
            "Flask==2.3.2",
            "Flask-SQLAlchemy==3.0.5",
            "Flask-Login==0.6.3",
            "python-barcode==0.15.1",
            "Pillow==9.5.0",
            "cryptography==41.0.2",
            "reportlab==4.0.4",
            "PyPDF2==3.0.1",
            "python-docx==0.8.11",
            "Bootstrap-Flask==2.3.1"
        ]
        
        with open(f"{web_dist_path}/requirements.txt", "w") as f:
            f.write("\n".join(web_requirements))
        
        # Create a README for the web version
        readme_content = """# Medical Laboratory Management System - Web Version

## Description
This is the web version of the Medical Laboratory Management System built with Flask.

## Requirements
- Python 3.7 or higher
- All dependencies listed in requirements.txt

## Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Access the application at http://localhost:5000

## Default Credentials
- Username: admin
- Password: admin123

## Features
- Patient management
- Test requests and tracking
- Medical report generation
- Billing and invoicing
- User management
- Statistics and reporting
"""
        
        with open(f"{web_dist_path}/README.md", "w") as f:
            f.write(readme_content)
        
        print("Web version built successfully!")
        return True
    except Exception as e:
        print(f"Error building web version: {e}")
        return False

def build_windows_version():
    """Build the Windows executable"""
    print("Building Windows version...")
    
    try:
        # Run the Windows build script
        result = subprocess.run([
            sys.executable, 
            "build_executables/build_windows.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Windows version built successfully!")
            return True
        else:
            print(f"Error building Windows version: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error building Windows version: {e}")
        return False

def build_macos_version():
    """Build the macOS application bundle"""
    print("Building macOS version...")
    
    try:
        # Run the macOS build script
        result = subprocess.run([
            sys.executable, 
            "build_executables/build_macos.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("macOS version built successfully!")
            return True
        else:
            print(f"Error building macOS version: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error building macOS version: {e}")
        return False

def create_distribution_package():
    """Create a comprehensive distribution package"""
    print("Creating distribution package...")
    
    try:
        # Create main README
        main_readme = """# Medical Laboratory Management System - Complete Distribution

This package contains all versions of the Medical Laboratory Management System:

## 1. Web Version
- Located in: `web_version/`
- A Flask-based web application that can be deployed on any server
- Access via web browser

## 2. Windows Desktop Version
- Located in: `windows_desktop/`
- Standalone executable for Windows systems
- File: `MedicalLabSystem.exe`

## 3. macOS Desktop Version
- Located in: `macos_desktop/`
- Application bundle for macOS systems
- File: `MedicalLabSystem.app`

## Installation Instructions

### Web Version
1. Navigate to the `web_version` directory
2. Follow the instructions in `web_version/README.md`

### Windows Desktop Version
1. Navigate to the `windows_desktop` directory
2. Double-click `MedicalLabSystem.exe` to run

### macOS Desktop Version
1. Navigate to the `macos_desktop` directory
2. Drag `MedicalLabSystem.app` to your Applications folder
3. Right-click and select "Open" (first time only due to security settings)

## Default Credentials
For all versions:
- Username: admin
- Password: admin123

## System Requirements
- Web Version: Any modern web browser, Python 3.7+
- Windows Version: Windows 7 or higher
- macOS Version: macOS 11.0 (Big Sur) or higher with Apple Silicon
"""
        
        with open("final_distribution/README.md", "w") as f:
            f.write(main_readme)
        
        print("Distribution package created successfully!")
        return True
    except Exception as e:
        print(f"Error creating distribution package: {e}")
        return False

def main():
    """Main build function"""
    print("Starting build process for all versions...")
    
    # Create final distribution directory if it doesn't exist
    if not os.path.exists("final_distribution"):
        os.makedirs("final_distribution")
    
    # Build all versions
    success = True
    
    success &= build_web_version()
    success &= build_windows_version()
    success &= build_macos_version()
    success &= create_distribution_package()
    
    if success:
        print("\nAll versions built successfully!")
        print("Distribution package is ready in the 'final_distribution' directory.")
    else:
        print("\nSome builds failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())