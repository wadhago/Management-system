# Medical Laboratory Management System

A comprehensive medical laboratory management system built with Python and Tkinter, supporting both English and Arabic languages.

## Features

1. **Patient Management**
   - Record patient data (name, age, gender, ID number, contact information)
   - Historical record of previous patient tests
   - Track current requests and previous reports

2. **Test and Analysis Management**
   - Comprehensive list of available test types (blood, urine, stool, radiology tests)
   - Create new test requests and link them to patients
   - Track test status (pending, in progress, completed)
   - Test pricing and linking to invoices

3. **Sample Management**
   - Generate barcodes for each sample for easy tracking
   - Record date and time of sample collection
   - Define sample status (valid, damaged, insufficient)
   - Track stages of sample processing

4. **Medical Report Management**
   - Design customizable test reports
   - Electronically sign reports from physicians
   - Send reports to patients via email
   - Save reports as archives

5. **Billing and Payment Management**
   - Automatically generate invoices based on requested tests
   - Support multiple payment methods
   - Track payments and manage accounts

6. **User and Authorization Management**
   - User account system (administrators, technicians, doctors)
   - Define authorizations based on user role
   - Secure login with passwords

7. **Inventory Management**
   - Track chemicals and medical consumables
   - Alerts when products are about to run out
   - Record purchase orders and monitor suppliers

8. **Integration Capabilities**
   - Potential integration with hospital systems
   - Integration with medical analysis devices
   - Support for EMR systems

9. **Notification System**
   - Staff notifications for new tests and completed reports
   - Patient reminders for appointments and results
   - Alerts for expiring materials

10. **Data Security**
    - Data encryption for privacy
    - Periodic data backups
    - Compliance with data protection regulations

11. **Reports and Statistics**
    - Daily and financial performance reports
    - Statistics on patients and tests
    - Data analysis tools

12. **Multilingual Interface**
    - User-friendly design
    - Support for English and Arabic
    - Easy language switching

## Installation

1. Clone or download the repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:
```bash
python main.py
```

### Default Login Credentials

- Username: `admin`
- Password: `admin123`

## System Architecture

The system is organized into the following modules:

- `main.py`: Main application entry point with GUI
- `models.py`: Data models and structures
- `database.py`: Database management and operations
- `config.py`: Configuration settings
- `translations.py`: Multilingual support
- `utils.py`: Utility functions (barcode generation, email, encryption)
- `requirements.txt`: Python package dependencies

## Technical Details

### Database

The system uses SQLite for data storage with the following main tables:
- Patients
- Test Types
- Test Requests
- Samples
- Medical Reports
- Invoices
- Users
- Inventory Items
- Purchase Orders

### Security

- Passwords are hashed using SHA-256
- Data encryption using the cryptography library
- Role-based access control

### Multilingual Support

The system supports both English and Arabic languages with a simple language switching mechanism.

## Module Details

### Patient Management
- Add, edit, view, and delete patient records
- Store comprehensive patient information
- Track patient history

### Test Management
- Define test types with pricing and categories
- Create test requests linked to patients
- Track test progress through different statuses

### Sample Management
- Create samples with unique barcodes
- Track sample collection date and time
- Update sample status (valid, damaged, insufficient)
- Generate barcode labels for samples

### Medical Reports
- Create detailed medical reports
- Electronic signature functionality for physicians
- Report distribution to patients
- Archive reports for future reference

### Billing System
- Automatic invoice generation
- Track payments and outstanding balances
- Support for multiple payment methods
- Financial reporting capabilities

### Inventory Management
- Track medical supplies and chemicals
- Set minimum stock levels with alerts
- Create purchase orders for suppliers
- Monitor expiration dates

### User Management
- Role-based access control (Admin, Technician, Doctor, Receptionist)
- User account creation and management
- Account activation/deactivation

### Statistics and Reporting
- Patient statistics and trends
- Test volume and popularity reports
- Financial performance metrics
- Inventory usage analysis

## Future Enhancements

1. Implement two-factor authentication
2. Add barcode scanning functionality
3. Integrate with medical devices
4. Add email/SMS notifications
5. Implement data backup and recovery
6. Add more detailed reporting features
7. Implement REST API for integration
8. Add mobile application support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please contact the development team.