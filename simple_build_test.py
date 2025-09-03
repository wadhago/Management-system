#!/usr/bin/env python3
"""
Simple test script to verify PyInstaller functionality
"""
import subprocess
import sys
import os

def test_pyinstaller():
    """Test if PyInstaller can build a simple script"""
    # Create a simple test script
    test_script = """
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Test Application")
    label = tk.Label(root, text="Hello, World!")
    label.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
"""
    
    with open("test_app.py", "w") as f:
        f.write(test_script)
    
    try:
        # Try to build with PyInstaller
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--windowed",
            "--name", "TestApp",
            "test_app.py"
        ], capture_output=True, text=True, timeout=60)
        
        print("Return code:", result.returncode)
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        # Clean up
        if os.path.exists("test_app.py"):
            os.remove("test_app.py")
        if os.path.exists("TestApp.spec"):
            os.remove("TestApp.spec")
        if os.path.exists("build"):
            import shutil
            shutil.rmtree("build")
        if os.path.exists("dist"):
            import shutil
            shutil.rmtree("dist")
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_pyinstaller()
    print("Test successful:", success)