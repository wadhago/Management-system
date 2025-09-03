import sys
import subprocess
import os
import shutil

def build_macos_app():
    try:
        print("Building macOS application...")
        
        # Change to the medical_lab_system directory
        os.chdir("medical_lab_system")
        
        # Install required packages
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "python-barcode", "cryptography", "PyPDF2", "python-docx"])
        
        # Check if PyInstaller is installed, if not install it
        try:
            import PyInstaller
        except ImportError:
            print("Installing PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Build app bundle using PyInstaller
        print("Creating application bundle with PyInstaller...")
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--windowed",
            "--target-arch", "arm64",  # For Apple Silicon
            "--name", "MedicalLabSystem",
            "--osx-bundle-identifier", "com.medical.lab.system",
            "main.py"
        ])
        
        # Create proper .app bundle structure
        app_bundle_path = "dist/MedicalLabSystem.app"
        if os.path.exists(app_bundle_path):
            # Move the app bundle to the final distribution directory
            shutil.move(app_bundle_path, "../final_distribution/macos_desktop/MedicalLabSystem.app")
            print("macOS application bundle created successfully!")
        else:
            print("Warning: App bundle not found in expected location")
        
        # Clean up build files
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("MedicalLabSystem.spec"):
            os.remove("MedicalLabSystem.spec")
            
        return True
    except Exception as e:
        print(f"Error building macOS app: {e}")
        return False

if __name__ == "__main__":
    # Change to the project root directory
    os.chdir("..")
    build_macos_app()