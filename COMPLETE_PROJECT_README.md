# Medical Laboratory Management System - Complete Project

This repository contains the complete Medical Laboratory Management System with three deployment options:

1. **Web Version** - A Flask-based web application
2. **Windows Desktop Version** - A native Windows application (EXE)
3. **macOS Desktop Version** - A native macOS application optimized for Apple Silicon (DMG/App)

## Project Structure

```
├── medical_lab_system/        # Original Tkinter desktop application
├── deployments/               # Deployment packages and build scripts
├── distribution/              # Initial distribution packages
├── final_distribution/        # Final distribution with all versions
│   ├── web_version/          # Complete Flask web application
│   ├── windows_desktop/      # Windows executable
│   ├── macos_desktop/        # macOS application bundle
│   ├── build_executables/    # Scripts to build executables
│   ├── README.md             # Main documentation
│   ├── BUILD_INSTRUCTIONS.md # Detailed build instructions
│   ├── SUMMARY.md            # Implementation summary
│   └── verify_installation.py # Verification script
├── build_executables.py      # Main build script
└── README.md                 # This file
```

## Features

- Patient Management
- Test and Analysis Management
- Sample Management
- Medical Report Management
- Billing and Payment Management
- User and Authorization Management
- Inventory Management
- Statistics and Reporting
- Multi-language Support (English and Arabic)

## Deployment Options

### 1. Web Version

A Flask-based web application that can be deployed on any server.

**Location**: `final_distribution/web_version/`

**To run**:
1. Navigate to the web_version directory
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Access via web browser at `http://localhost:5000`

### 2. Windows Desktop Version

A native Windows application packaged as an executable file.

**Location**: `final_distribution/windows_desktop/MedicalLabSystem.exe`

**To run**:
1. Navigate to the windows_desktop directory
2. Double-click `MedicalLabSystem.exe`

### 3. macOS Desktop Version

A native macOS application optimized for Apple Silicon processors.

**Location**: `final_distribution/macos_desktop/MedicalLabSystem.app`

**To run**:
1. Navigate to the macos_desktop directory
2. Double-click `MedicalLabSystem.app`

## Building Executables

To create the actual Windows EXE and macOS DMG files:

### For Windows:
1. Run `final_distribution/build_executables/build_windows.py` on a Windows machine

### For macOS (Apple Silicon):
1. Run `final_distribution/build_executables/build_macos.py` on a macOS machine with Apple Silicon

## Default Login Credentials

- Username: admin
- Password: admin123

## System Requirements

### Web Version:
- Python 3.7 or higher
- Flask and related dependencies

### Desktop Versions:
- Windows 7 or higher (for Windows version)
- macOS 10.12 or higher (for macOS version)
- Python 3.7 or higher (if rebuilding executables)

## Web Version Components

The web version includes:

- **Flask Application**: Complete backend with all routes and models
- **HTML Templates**: 21 templates for all system functions
- **CSS/Bootstrap**: Responsive design for all device sizes
- **JavaScript**: Client-side functionality
- **Database**: SQLite database integration

### HTML Templates:
1. `base.html` - Main layout template
2. `login.html` - User login page
3. `dashboard.html` - Main dashboard with statistics
4. `patients.html` - Patient list view
5. `patient_detail.html` - Individual patient details
6. `add_patient.html` - Add new patient form
7. `edit_patient.html` - Edit patient form
8. `tests.html` - Test types list
9. `add_test.html` - Add new test type form
10. `request_test.html` - Request tests for patient
11. `test_requests.html` - List of test requests
12. `test_request_detail.html` - Individual test request details
13. `create_report.html` - Create medical report
14. `reports.html` - Medical reports list
15. `report_detail.html` - Individual report details
16. `invoices.html` - Invoices list
17. `invoice_detail.html` - Individual invoice details
18. `statistics.html` - System statistics
19. `users.html` - User management
20. `add_user.html` - Add new user form
21. `settings.html` - System settings

## Desktop Version Components

The desktop versions include:

- **Source Code**: Complete Python application
- **Dependencies**: All required Python packages
- **Build Scripts**: PyInstaller configuration
- **Documentation**: Installation and usage instructions

## Verification

To verify the installation is correct, run:
```
cd final_distribution
python verify_installation.py
```

## Support

For issues with deployment or usage, please refer to the documentation in each directory or contact the development team.

## License

This project is proprietary and intended for use by authorized personnel only.