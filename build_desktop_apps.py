#!/usr/bin/env python3
"""
Build script for creating desktop applications for Windows and macOS
"""
import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully")
            return True
        except Exception as e:
            print(f"Failed to install PyInstaller: {e}")
            return False

def build_windows_app():
    """Build Windows executable"""
    print("Building Windows application...")
    
    try:
        # Change to the desktop source directory
        os.chdir("medical_lab_system")
        
        # Build the executable
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "MedicalLabSystem",
            "main.py"
        ])
        
        # Move the executable to the distribution directory
        if os.path.exists("dist/MedicalLabSystem.exe"):
            shutil.move("dist/MedicalLabSystem.exe", "../final_distribution/windows_desktop/MedicalLabSystem.exe")
            print("Windows executable created successfully!")
        else:
            print("Warning: Windows executable not found in expected location")
        
        # Clean up build files
        cleanup_build_files()
        
        # Return to original directory
        os.chdir("..")
        return True
        
    except Exception as e:
        print(f"Error building Windows application: {e}")
        os.chdir("..")
        return False

def build_macos_app():
    """Build macOS application bundle"""
    print("Building macOS application...")
    
    try:
        # Change to the desktop source directory
        os.chdir("medical_lab_system")
        
        # Build the application bundle
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--windowed",
            "--name", "MedicalLabSystem",
            "--osx-bundle-identifier", "com.medical.lab.system",
            "main.py"
        ])
        
        # Move the app bundle to the distribution directory
        if os.path.exists("dist/MedicalLabSystem.app"):
            shutil.move("dist/MedicalLabSystem.app", "../final_distribution/macos_desktop/MedicalLabSystem.app")
            print("macOS application bundle created successfully!")
        else:
            print("Warning: macOS application bundle not found in expected location")
        
        # Clean up build files
        cleanup_build_files()
        
        # Return to original directory
        os.chdir("..")
        return True
        
    except Exception as e:
        print(f"Error building macOS application: {e}")
        os.chdir("..")
        return False

def cleanup_build_files():
    """Clean up temporary build files"""
    try:
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("MedicalLabSystem.spec"):
            os.remove("MedicalLabSystem.spec")
    except Exception as e:
        print(f"Warning: Error during cleanup: {e}")

def main():
    """Main build function"""
    print("Medical Laboratory Management System - Desktop Application Builder")
    print("=" * 70)
    
    # Check if PyInstaller is available
    if not check_pyinstaller():
        print("Cannot proceed without PyInstaller")
        return 1
    
    # Get platform from command line argument or auto-detect
    platform = "all"
    if len(sys.argv) > 1:
        platform = sys.argv[1].lower()
    
    success = True
    
    if platform in ["all", "windows"]:
        success &= build_windows_app()
    
    if platform in ["all", "macos"]:
        success &= build_macos_app()
    
    if success:
        print("\n🎉 Desktop applications built successfully!")
        print("Find the executables in the final_distribution directory:")
        print("- Windows: final_distribution/windows_desktop/MedicalLabSystem.exe")
        print("- macOS: final_distribution/macos_desktop/MedicalLabSystem.app")
        return 0
    else:
        print("\n❌ Some builds failed. Check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())