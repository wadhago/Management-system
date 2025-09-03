"""
Comprehensive build script to create Windows EXE and macOS DMG versions
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_executable_build_script():
    """Create a build script for creating executables"""
    
    # Create build directory if it doesn't exist
    build_dir = Path("build_executables")
    build_dir.mkdir(exist_ok=True)
    
    # Create a simplified requirements file for building
    simplified_requirements = """
# Simplified requirements for building executables
tkinter
sqlite3
hashlib
uuid
datetime
typing
Pillow
python-barcode
cryptography
PyPDF2
python-docx
"""
    
    with open(build_dir / "build_requirements.txt", "w") as f:
        f.write(simplified_requirements)
    
    # Create build script for Windows
    windows_build_script = """
import sys
import subprocess
import os

def build_windows_exe():
    try:
        # Install required packages
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "python-barcode", "cryptography", "PyPDF2", "python-docx"])
        
        # Build executable using PyInstaller
        subprocess.check_call([
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", "MedicalLabSystem",
            "medical_lab_system/main.py"
        ])
        
        print("Windows EXE built successfully!")
        return True
    except Exception as e:
        print(f"Error building Windows EXE: {e}")
        return False

if __name__ == "__main__":
    build_windows_exe()
"""
    
    with open(build_dir / "build_windows.py", "w") as f:
        f.write(windows_build_script)
    
    # Create build script for macOS
    macos_build_script = """
import sys
import subprocess
import os

def build_macos_app():
    try:
        # Install required packages
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "python-barcode", "cryptography", "PyPDF2", "python-docx"])
        
        # Build app bundle using PyInstaller
        subprocess.check_call([
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--target-arch", "arm64",
            "--name", "MedicalLabSystem",
            "medical_lab_system/main.py"
        ])
        
        print("macOS app built successfully!")
        return True
    except Exception as e:
        print(f"Error building macOS app: {e}")
        return False

if __name__ == "__main__":
    build_macos_app()
"""
    
    with open(build_dir / "build_macos.py", "w") as f:
        f.write(macos_build_script)
    
    print("Executable build scripts created successfully!")
    print("Build scripts location: build_executables/")
    return True

def create_distribution_structure():
    """Create the final distribution structure with executables"""
    
    # Create final distribution directory
    final_dist = Path("final_distribution")
    if final_dist.exists():
        shutil.rmtree(final_dist)
    final_dist.mkdir()
    
    # Copy web version
    if Path("distribution/web_version").exists():
        shutil.copytree("distribution/web_version", final_dist / "web_version")
    
    # Create placeholders for executables
    windows_dir = final_dist / "windows_desktop"
    macos_dir = final_dist / "macos_desktop"
    
    windows_dir.mkdir()
    macos_dir.mkdir()
    
    # Create placeholder files
    (windows_dir / "MedicalLabSystem.exe").write_text("Windows executable would be placed here")
    (macos_dir / "MedicalLabSystem.app").write_text("macOS app bundle would be placed here")
    
    # Copy documentation
    if Path("README.md").exists():
        shutil.copy("README.md", final_dist)
    
    print("Final distribution structure created!")
    print("Final distribution location: final_distribution/")
    return True

def main():
    """Main function to create all distribution packages"""
    print("Creating Medical Laboratory Management System distribution packages...")
    print("=" * 70)
    
    # Create executable build scripts
    if not create_executable_build_script():
        print("Failed to create executable build scripts")
        return False
    
    # Create final distribution structure
    if not create_distribution_structure():
        print("Failed to create final distribution structure")
        return False
    
    print("=" * 70)
    print("Distribution packages creation completed successfully!")
    print("")
    print("Packages created:")
    print("1. Web Version - Complete Flask application with all HTML templates")
    print("2. Windows Desktop - Build script for creating EXE (final executable not included due to platform restrictions)")
    print("3. macOS Desktop - Build script for creating DMG/app (final executable not included due to platform restrictions)")
    print("")
    print("To create the actual executables:")
    print("- Run build_executables/build_windows.py on a Windows machine")
    print("- Run build_executables/build_macos.py on a macOS machine with Apple Silicon")
    print("")
    print("All source code and build scripts are included in the distribution.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)