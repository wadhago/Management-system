# Medical Laboratory Management System - Complete Distribution Package

## Overview
This package contains all versions of the Medical Laboratory Management System:

1. **Web Version** - A Flask-based web application
2. **Windows Desktop Version** - Source code and build instructions for Windows
3. **macOS Desktop Version** - Source code and build instructions for macOS

## 1. Web Version

### Location
`web_version/`

### Description
A complete Flask web application with all HTML templates and necessary files.

### Requirements
- Python 3.7 or higher
- All dependencies listed in `web_version/requirements.txt`

### Installation and Running
1. Navigate to the `web_version` directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Access the application at http://localhost:5000

### Default Credentials
- Username: admin
- Password: admin123

## 2. Windows Desktop Version

### Location
`windows_desktop/`

### Description
Contains the source code and build scripts needed to create a Windows executable.

### Requirements for Building
- Windows operating system
- Python 3.7 or higher
- PyInstaller (`pip install pyinstaller`)

### Building the Executable
1. Copy the `medical_lab_system` directory to a Windows machine
2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
3. Build the executable:
   ```cmd
   pyinstaller --onefile --windowed --name MedicalLabSystem main.py
   ```
4. The executable will be created in the `dist` directory

### Running the Application
After building, simply double-click the `MedicalLabSystem.exe` file.

## 3. macOS Desktop Version

### Location
`macos_desktop/`

### Description
Contains the source code and build scripts needed to create a macOS application bundle.

### Requirements for Building
- macOS system (preferably with Apple Silicon for optimal performance)
- Python 3.7 or higher
- PyInstaller (`pip install pyinstaller`)

### Building the Application Bundle
1. Copy the `medical_lab_system` directory to a macOS machine
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the application bundle:
   ```bash
   pyinstaller --windowed --name MedicalLabSystem main.py
   ```
4. For Apple Silicon optimization:
   ```bash
   pyinstaller --windowed --target-arch arm64 --name MedicalLabSystem main.py
   ```
5. The application bundle will be created in the `dist` directory

### Running the Application
After building, drag `MedicalLabSystem.app` to your Applications folder and run it.

## Directory Structure
```
final_distribution/
├── web_version/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── patients.html
│   │   ├── patient_detail.html
│   │   ├── add_patient.html
│   │   ├── edit_patient.html
│   │   ├── tests.html
│   │   ├── add_test.html
│   │   ├── request_test.html
│   │   ├── test_requests.html
│   │   ├── test_request_detail.html
│   │   ├── create_report.html
│   │   ├── reports.html
│   │   ├── report_detail.html
│   │   ├── invoices.html
│   │   ├── invoice_detail.html
│   │   ├── statistics.html
│   │   ├── users.html
│   │   ├── add_user.html
│   │   └── settings.html
│   └── README.md
├── windows_desktop/
│   └── MedicalLabSystem.exe (placeholder - build on Windows)
├── macos_desktop/
│   └── MedicalLabSystem.app (placeholder - build on macOS)
├── build_executables/
│   ├── build_windows.py
│   ├── build_macos.py
│   └── build_requirements.txt
└── README.md
```

## Features Included in All Versions
- Patient management (add, edit, view, delete)
- Test management (create test types, request tests)
- Medical report generation and management
- Billing and invoicing system
- User management with role-based access control
- Inventory management
- Statistics and reporting dashboard
- Multi-language support
- Data encryption and security features
- Barcode generation for samples
- PDF report generation

## Technical Notes
1. The database (`medical_lab.db`) is shared across all versions
2. All versions use the same core business logic from the `models.py` and `database.py` files
3. The web version uses Flask for the backend and Bootstrap for the frontend
4. The desktop versions use Tkinter for the GUI
5. All versions support the same functionality with different interfaces

## Troubleshooting
1. **Database issues**: Ensure the `medical_lab.db` file has proper read/write permissions
2. **Missing dependencies**: Install all packages listed in `requirements.txt`
3. **Port conflicts**: Change the port in `app.py` if port 5000 is already in use
4. **Build errors**: Ensure all development tools are properly installed on the target platform

## Support
For issues with building or running any version, please check:
1. Python version compatibility (3.7+ recommended)
2. All required dependencies are installed
3. Sufficient system resources (memory, disk space)
4. Proper file permissions