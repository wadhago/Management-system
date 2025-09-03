"""
Debug script to test patient and test creation functionality
"""
import sys
import os
from datetime import datetime
import uuid

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def debug_patient_creation():
    print("Debugging Patient Creation...")
    
    try:
        # Import required modules
        from medical_lab_system.models import Patient, Gender
        from medical_lab_system.database import DatabaseManager
        
        # Initialize database
        db = DatabaseManager()
        print("✓ Database initialized successfully")
        
        # Check initial patient count
        initial_patients = db.get_all_patients()
        print(f"Initial patients in database: {len(initial_patients)}")
        
        # Create a new patient
        new_patient = Patient(
            id=str(uuid.uuid4()),
            name="Debug Test Patient",
            age=30,
            gender=Gender.MALE,
            contact_info="debug.test@example.com"
        )
        
        print(f"Creating patient: {new_patient.name}")
        
        # Try to create the patient
        result = db.create_patient(new_patient)
        print(f"Patient creation result: {result}")
        
        if result:
            print("✓ Patient created successfully in database")
            
            # Check updated patient count
            updated_patients = db.get_all_patients()
            print(f"Patients in database after creation: {len(updated_patients)}")
            
            # Verify the new patient is in the list
            found_patient = None
            for patient in updated_patients:
                if patient.id == new_patient.id:
                    found_patient = patient
                    break
            
            if found_patient:
                print(f"✓ New patient found in database: {found_patient.name}")
            else:
                print("✗ New patient NOT found in database")
        else:
            print("✗ Failed to create patient in database")
            
    except Exception as e:
        print(f"✗ Error during patient creation debug: {e}")
        import traceback
        traceback.print_exc()

def debug_test_creation():
    print("\nDebugging Test Creation...")
    
    try:
        # Import required modules
        from medical_lab_system.models import TestType
        from medical_lab_system.database import DatabaseManager
        
        # Initialize database
        db = DatabaseManager()
        print("✓ Database initialized successfully")
        
        # Check initial test count
        initial_tests = db.get_all_test_types()
        print(f"Initial test types in database: {len(initial_tests)}")
        
        # Create a new test type
        new_test = TestType(
            id=str(uuid.uuid4()),
            name="Debug Test Type",
            description="Test for debugging purposes",
            price=50.0,
            category="Debug"
        )
        
        print(f"Creating test: {new_test.name}")
        
        # Try to create the test type
        result = db.create_test_type(new_test)
        print(f"Test type creation result: {result}")
        
        if result:
            print("✓ Test type created successfully in database")
            
            # Check updated test count
            updated_tests = db.get_all_test_types()
            print(f"Test types in database after creation: {len(updated_tests)}")
            
            # Verify the new test is in the list
            found_test = None
            for test in updated_tests:
                if test.id == new_test.id:
                    found_test = test
                    break
            
            if found_test:
                print(f"✓ New test found in database: {found_test.name}")
            else:
                print("✗ New test NOT found in database")
        else:
            print("✗ Failed to create test type in database")
            
    except Exception as e:
        print(f"✗ Error during test creation debug: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_patient_creation()
    debug_test_creation()