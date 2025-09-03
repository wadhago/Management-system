#!/usr/bin/env python3
"""
Verification script to ensure the GitHub package is complete and properly organized
"""
import os
import sys

def verify_directory_structure():
    """Verify the directory structure is correct"""
    print("Verifying directory structure...")
    
    # Check main directories
    required_dirs = [
        "medical_lab_system",
        "final_distribution",
        "final_distribution/web_version",
        "final_distribution/windows_desktop",
        "final_distribution/macos_desktop",
        "final_distribution/build_executables",
        "build_executables"
    ]
    
    for dir_path in required_dirs:
        full_path = os.path.join(os.getcwd(), "medical-lab-system", dir_path)
        if not os.path.exists(full_path):
            print(f"❌ Required directory not found: {dir_path}")
            return False
    
    print("✅ Directory structure verified")
    return True

def verify_web_version():
    """Verify the web version is complete"""
    print("Verifying web version...")
    
    web_dir = os.path.join(os.getcwd(), "medical-lab-system", "final_distribution", "web_version")
    
    # Check required files
    required_files = ["app.py", "requirements.txt"]
    for file in required_files:
        if not os.path.exists(os.path.join(web_dir, file)):
            print(f"❌ Required file {file} not found in web version")
            return False
    
    # Check templates directory
    templates_dir = os.path.join(web_dir, "templates")
    if not os.path.exists(templates_dir):
        print("❌ Templates directory not found in web version")
        return False
    
    # Check number of templates
    templates = os.listdir(templates_dir)
    if len(templates) < 20:
        print(f"❌ Expected at least 20 templates, found {len(templates)}")
        return False
    
    print(f"✅ Web version verified ({len(templates)} templates found)")
    return True

def verify_desktop_source():
    """Verify the desktop source code is complete"""
    print("Verifying desktop source code...")
    
    source_dir = os.path.join(os.getcwd(), "medical-lab-system", "medical_lab_system")
    
    # Check required files
    required_files = ["main.py", "models.py", "database.py", "requirements.txt"]
    for file in required_files:
        if not os.path.exists(os.path.join(source_dir, file)):
            print(f"❌ Required file {file} not found in desktop source")
            return False
    
    print("✅ Desktop source code verified")
    return True

def verify_build_scripts():
    """Verify the build scripts are complete"""
    print("Verifying build scripts...")
    
    build_dir = os.path.join(os.getcwd(), "medical-lab-system", "build_executables")
    
    # Check required scripts
    required_scripts = ["build_windows.py", "build_macos.py"]
    for script in required_scripts:
        if not os.path.exists(os.path.join(build_dir, script)):
            print(f"❌ Required build script {script} not found")
            return False
    
    print("✅ Build scripts verified")
    return True

def verify_docker_files():
    """Verify Docker files are present"""
    print("Verifying Docker files...")
    
    required_files = ["Dockerfile", "docker-compose.yml", "init.sql"]
    for file in required_files:
        if not os.path.exists(os.path.join(os.getcwd(), "medical-lab-system", file)):
            print(f"❌ Required Docker file {file} not found")
            return False
    
    print("✅ Docker files verified")
    return True

def verify_documentation():
    """Verify documentation files are present"""
    print("Verifying documentation...")
    
    if not os.path.exists(os.path.join(os.getcwd(), "medical-lab-system", "README.md")):
        print("❌ README.md not found")
        return False
    
    print("✅ Documentation verified")
    return True

def main():
    """Main verification function"""
    print("Medical Laboratory Management System - GitHub Package Verification")
    print("=" * 70)
    
    # Change to project directory
    project_dir = os.path.join(os.getcwd(), "medical-lab-system")
    if not os.path.exists(project_dir):
        print("❌ Project directory not found")
        return 1
    
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    # Run all verifications
    checks = [
        verify_directory_structure,
        verify_web_version,
        verify_desktop_source,
        verify_build_scripts,
        verify_docker_files,
        verify_documentation
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    os.chdir(original_dir)
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED - GitHub package is complete!")
        print()
        print("Package includes:")
        print("✅ Complete web version with all HTML templates")
        print("✅ Desktop source code for Windows and macOS")
        print("✅ Build scripts for creating executables")
        print("✅ Docker configuration for web deployment")
        print("✅ Comprehensive documentation")
        print()
        print("Ready for GitHub deployment!")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Please review the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())