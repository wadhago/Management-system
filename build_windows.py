import sys
import subprocess
import os
import shutil

def build_windows_exe():
    try:
        print("Building Windows executable...")
        
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
        
        # Build executable using PyInstaller
        print("Creating executable with PyInstaller...")
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "MedicalLabSystem",
            "--icon", "NONE",  # Add an icon file if you have one
            "main.py"
        ])
        
        # Move the executable to the final distribution directory
        if os.path.exists("dist/MedicalLabSystem.exe"):
            shutil.move("dist/MedicalLabSystem.exe", "../final_distribution/windows_desktop/MedicalLabSystem.exe")
            print("Windows executable created successfully!")
        else:
            print("Warning: Executable not found in expected location")
        
        # Clean up build files
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("MedicalLabSystem.spec"):
            os.remove("MedicalLabSystem.spec")
            
        return True
    except Exception as e:
        print(f"Error building Windows EXE: {e}")
        return False

if __name__ == "__main__":
    # Change to the project root directory
    os.chdir("..")
    build_windows_exe()