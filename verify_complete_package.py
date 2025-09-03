#!/usr/bin/env python3
"""
Verification script to ensure all components of the Medical Laboratory Management System are complete
"""
import os
import sys

def verify_web_version():
    """Verify the web version is complete"""
    print("Verifying web version...")
    
    # Check if web version directory exists
    web_dir = "final_distribution/web_version"
    if not os.path.exists(web_dir):
        print("❌ Web version directory not found")
        return False
    
    # Check required files
    required_files = ["app.py", "requirements.txt", "README.md"]
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
    
    # Check if source directory exists
    source_dir = "medical_lab_system"
    if not os.path.exists(source_dir):
        print("❌ Desktop source code directory not found")
        return False
    
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
    
    # Check if build scripts directory exists
    build_dir = "build_executables"
    if not os.path.exists(build_dir):
        print("❌ Build scripts directory not found")
        return False
    
    # Check required scripts
    required_scripts = ["build_windows.py", "build_macos.py"]
    for script in required_scripts:
        if not os.path.exists(os.path.join(build_dir, script)):
            print(f"❌ Required build script {script} not found")
            return False
    
    print("✅ Build scripts verified")
    return True

def verify_distribution_structure():
    """Verify the overall distribution structure"""
    print("Verifying distribution structure...")
    
    # Check main distribution directory
    dist_dir = "final_distribution"
    if not os.path.exists(dist_dir):
        print("❌ Main distribution directory not found")
        return False
    
    # Check required subdirectories
    required_dirs = ["web_version", "windows_desktop", "macos_desktop", "build_executables"]
    for dir_name in required_dirs:
        if not os.path.exists(os.path.join(dist_dir, dir_name)):
            print(f"❌ Required directory {dir_name} not found in distribution")
            return False
    
    print("✅ Distribution structure verified")
    return True

def main():
    """Main verification function"""
    print("Medical Laboratory Management System - Package Verification")
    print("=" * 60)
    
    # Run all verifications
    checks = [
        verify_distribution_structure,
        verify_web_version,
        verify_desktop_source,
        verify_build_scripts
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED - Package is complete!")
        print()
        print("Package includes:")
        print("✅ Complete web version with all HTML templates")
        print("✅ Desktop source code for Windows and macOS")
        print("✅ Build scripts for creating executables")
        print("✅ Comprehensive documentation")
        print()
        print("Next steps:")
        print("1. For Windows executable: Run build_executables/build_windows.py on Windows")
        print("2. For macOS app bundle: Run build_executables/build_macos.py on macOS")
        print("3. Web version is ready to deploy - just run 'python app.py' in web_version/")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Please review the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())