#!/usr/bin/env python3
"""
Deployment script for pushing the Medical Laboratory Management System to GitHub
"""
import os
import subprocess
import sys

def check_git():
    """Check if git is installed"""
    try:
        subprocess.check_output(["git", "--version"])
        print("Git is available")
        return True
    except Exception:
        print("Git is not installed or not in PATH")
        return False

def initialize_git_repo():
    """Initialize git repository if not already done"""
    try:
        # Check if already a git repo
        subprocess.check_output(["git", "rev-parse", "--git-dir"])
        print("Git repository already initialized")
        return True
    except Exception:
        # Initialize new repository
        try:
            subprocess.check_call(["git", "init"])
            print("Git repository initialized")
            return True
        except Exception as e:
            print(f"Failed to initialize git repository: {e}")
            return False

def create_gitignore():
    """Create .gitignore if it doesn't exist"""
    gitignore_path = ".gitignore"
    if not os.path.exists(gitignore_path):
        gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Medical Lab System specific
medical_lab.db
*.db
*.sqlite
*.sqlite3
"""
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        print(".gitignore created")
        return True
    else:
        print(".gitignore already exists")
        return True

def add_files_to_git():
    """Add all files to git"""
    try:
        subprocess.check_call(["git", "add", "."])
        print("All files added to git")
        return True
    except Exception as e:
        print(f"Failed to add files to git: {e}")
        return False

def create_initial_commit():
    """Create initial commit"""
    try:
        subprocess.check_call(["git", "commit", "-m", "Initial commit: Medical Laboratory Management System"])
        print("Initial commit created")
        return True
    except Exception as e:
        print(f"Failed to create initial commit: {e}")
        return False

def setup_github_repo(repo_name):
    """Setup GitHub repository (requires manual step)"""
    print(f"\nTo push to GitHub, follow these steps:")
    print(f"1. Create a new repository on GitHub named '{repo_name}'")
    print(f"2. Run the following commands:")
    print(f"   git remote add origin https://github.com/YOUR_USERNAME/{repo_name}.git")
    print(f"   git branch -M main")
    print(f"   git push -u origin main")
    print(f"\nReplace YOUR_USERNAME with your actual GitHub username.")

def main():
    """Main deployment function"""
    print("Medical Laboratory Management System - GitHub Deployment")
    print("=" * 60)
    
    # Check if git is available
    if not check_git():
        print("Please install git before proceeding")
        return 1
    
    # Initialize git repository
    if not initialize_git_repo():
        print("Failed to initialize git repository")
        return 1
    
    # Create .gitignore
    if not create_gitignore():
        print("Failed to create .gitignore")
        return 1
    
    # Add files to git
    if not add_files_to_git():
        print("Failed to add files to git")
        return 1
    
    # Create initial commit
    if not create_initial_commit():
        print("Failed to create initial commit")
        return 1
    
    # Setup GitHub repository
    setup_github_repo("medical-lab-system")
    
    print("\n🎉 Local git repository is ready for GitHub deployment!")
    print("Follow the instructions above to push to your GitHub repository.")
    return 0

if __name__ == "__main__":
    sys.exit(main())