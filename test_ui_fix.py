"""
Test script to verify UI functionality for adding patients and tests
"""
import sys
import os
from datetime import datetime
import uuid

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_ui_functions():
    print("Testing UI Functions...")
    
    try:
        # Import required modules
        from medical_lab_system.models import Patient, TestType, Gender
        from medical_lab_system.database import DatabaseManager
        
        # Initialize database
        db = DatabaseManager()
        print("✓ Database initialized successfully")
        
        # Test the load_patients_data function logic
        print("\nTesting Patient Loading...")
        patients = db.get_all_patients()
        print(f"Found {len(patients)} patients in database:")
        for patient in patients:
            print(f"  - ID: {patient.id[:8]}, Name: {patient.name}, Age: {patient.age}, Gender: {patient.gender.value}")
        
        # Test the load_tests_data function logic
        print("\nTesting Test Loading...")
        test_types = db.get_all_test_types()
        print(f"Found {len(test_types)} test types in database:")
        for test in test_types:
            print(f"  - ID: {test.id[:8]}, Name: {test.name}, Category: {test.category}, Price: ${test.price}")
            
        # Test adding a new patient through the UI logic
        print("\nTesting Adding New Patient...")
        new_patient = Patient(
            id=str(uuid.uuid4()),
            name="UI Test Patient",
            age=25,
            gender=Gender.FEMALE,
            contact_info="ui.test@example.com"
        )
        
        # This simulates what happens in the add_patient function
        result = db.create_patient(new_patient)
        print(f"Patient creation result: {result}")
        
        if result:
            print("✓ Patient created successfully through UI logic")
            # Now reload patients to see if the new one appears
            updated_patients = db.get_all_patients()
            print(f"Total patients after adding new one: {len(updated_patients)}")
            for patient in updated_patients:
                if patient.name == "UI Test Patient":
                    print(f"  - Found new patient: {patient.name}")
        else:
            print("✗ Failed to create patient through UI logic")
        
        # Test adding a new test through the UI logic
        print("\nTesting Adding New Test...")
        new_test = TestType(
            id=str(uuid.uuid4()),
            name="UI Test Type",
            description="Test for UI functionality",
            price=75.0,
            category="UI Testing"
        )
        
        # This simulates what happens in the add_test function
        result = db.create_test_type(new_test)
        print(f"Test type creation result: {result}")
        
        if result:
            print("✓ Test type created successfully through UI logic")
            # Now reload tests to see if the new one appears
            updated_tests = db.get_all_test_types()
            print(f"Total test types after adding new one: {len(updated_tests)}")
            for test in updated_tests:
                if test.name == "UI Test Type":
                    print(f"  - Found new test: {test.name}")
        else:
            print("✗ Failed to create test type through UI logic")
            
        print("\nUI functionality test completed!")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ui_functions()