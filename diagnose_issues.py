"""
Diagnostic script to identify issues with edit and delete functionality
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

from medical_lab_system.database import DatabaseManager
from medical_lab_system.models import Patient, TestType, Gender

def test_database_layer():
    """Test the database layer functionality"""
    print("Testing database layer...")
    
    # Initialize database
    db = DatabaseManager()
    print("✓ Database manager initialized")
    
    # Create test patient
    patient = Patient(
        id="diag_patient_12345",
        name="Diagnosis Patient",
        age=25,
        gender=Gender.FEMALE,
        contact_info="diagnostic@test.com"
    )
    
    # Test create patient
    try:
        create_result = db.create_patient(patient)
        print(f"✓ Patient creation: {'SUCCESS' if create_result else 'FAILED'}")
    except Exception as e:
        print(f"✗ Patient creation failed with error: {e}")
        return False
    
    # Test retrieve patient
    try:
        retrieved_patient = db.get_patient("diag_patient_12345")
        if retrieved_patient:
            print("✓ Patient retrieval: SUCCESS")
            print(f"  Retrieved patient name: {retrieved_patient.name}")
        else:
            print("✗ Patient retrieval: FAILED - Patient not found")
            return False
    except Exception as e:
        print(f"✗ Patient retrieval failed with error: {e}")
        return False
    
    # Test update patient
    try:
        retrieved_patient.name = "Updated Diagnosis Patient"
        update_result = db.update_patient(retrieved_patient)
        print(f"✓ Patient update: {'SUCCESS' if update_result else 'FAILED'}")
        
        # Verify update
        updated_patient = db.get_patient("diag_patient_12345")
        if updated_patient and updated_patient.name == "Updated Diagnosis Patient":
            print("✓ Patient update verification: SUCCESS")
        else:
            print("✗ Patient update verification: FAILED")
    except Exception as e:
        print(f"✗ Patient update failed with error: {e}")
        return False
    
    # Test delete patient
    try:
        delete_result = db.delete_patient("diag_patient_12345")
        print(f"✓ Patient deletion: {'SUCCESS' if delete_result else 'FAILED'}")
        
        # Verify deletion
        deleted_patient = db.get_patient("diag_patient_12345")
        if deleted_patient is None:
            print("✓ Patient deletion verification: SUCCESS")
        else:
            print("✗ Patient deletion verification: FAILED - Patient still exists")
    except Exception as e:
        print(f"✗ Patient deletion failed with error: {e}")
        return False
    
    return True

def test_test_type_database_layer():
    """Test the test type database functionality"""
    print("\nTesting test type database layer...")
    
    # Initialize database
    db = DatabaseManager()
    print("✓ Database manager initialized")
    
    # Create test test type
    test_type = TestType(
        id="diag_test_12345",
        name="Diagnostic Test",
        description="Test for diagnostic purposes",
        price=100.0,
        category="Diagnostic"
    )
    
    # Test create test type
    try:
        create_result = db.create_test_type(test_type)
        print(f"✓ Test type creation: {'SUCCESS' if create_result else 'FAILED'}")
    except Exception as e:
        print(f"✗ Test type creation failed with error: {e}")
        return False
    
    # Test retrieve test type
    try:
        retrieved_test = db.get_test_type("diag_test_12345")
        if retrieved_test:
            print("✓ Test type retrieval: SUCCESS")
            print(f"  Retrieved test name: {retrieved_test.name}")
        else:
            print("✗ Test type retrieval: FAILED - Test not found")
            return False
    except Exception as e:
        print(f"✗ Test type retrieval failed with error: {e}")
        return False
    
    # Test update test type
    try:
        retrieved_test.name = "Updated Diagnostic Test"
        update_result = db.update_test_type(retrieved_test)
        print(f"✓ Test type update: {'SUCCESS' if update_result else 'FAILED'}")
        
        # Verify update
        updated_test = db.get_test_type("diag_test_12345")
        if updated_test and updated_test.name == "Updated Diagnostic Test":
            print("✓ Test type update verification: SUCCESS")
        else:
            print("✗ Test type update verification: FAILED")
    except Exception as e:
        print(f"✗ Test type update failed with error: {e}")
        return False
    
    # Test delete test type
    try:
        delete_result = db.delete_test_type("diag_test_12345")
        print(f"✓ Test type deletion: {'SUCCESS' if delete_result else 'FAILED'}")
        
        # Verify deletion
        deleted_test = db.get_test_type("diag_test_12345")
        if deleted_test is None:
            print("✓ Test type deletion verification: SUCCESS")
        else:
            print("✗ Test type deletion verification: FAILED - Test still exists")
    except Exception as e:
        print(f"✗ Test type deletion failed with error: {e}")
        return False
    
    return True

def inspect_database_contents():
    """Inspect the actual database contents"""
    print("\nInspecting database contents...")
    
    try:
        conn = sqlite3.connect("medical_lab_system/medical_lab.db")
        cursor = conn.cursor()
        
        # Check patients table
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        print(f"Number of patients in database: {patient_count}")
        
        # Check test_types table
        cursor.execute("SELECT COUNT(*) FROM test_types")
        test_count = cursor.fetchone()[0]
        print(f"Number of test types in database: {test_count}")
        
        # Show first few patients
        if patient_count > 0:
            cursor.execute("SELECT id, name FROM patients LIMIT 3")
            patients = cursor.fetchall()
            print("Sample patients:")
            for patient in patients:
                print(f"  ID: {patient[0]}, Name: {patient[1]}")
        
        # Show first few test types
        if test_count > 0:
            cursor.execute("SELECT id, name FROM test_types LIMIT 3")
            tests = cursor.fetchall()
            print("Sample test types:")
            for test in tests:
                print(f"  ID: {test[0]}, Name: {test[1]}")
        
        conn.close()
        print("✓ Database inspection completed")
        
    except Exception as e:
        print(f"✗ Database inspection failed with error: {e}")

if __name__ == "__main__":
    print("Running diagnostic tests for edit and delete functionality...\n")
    
    # Test database layer for patients
    patient_success = test_database_layer()
    
    # Test database layer for test types
    test_success = test_test_type_database_layer()
    
    # Inspect database contents
    inspect_database_contents()
    
    if patient_success and test_success:
        print("\n🎉 All diagnostic tests passed! The database layer is working correctly.")
        print("If the UI is still not working, the issue is likely in the UI layer.")
    else:
        print("\n❌ Some diagnostic tests failed. There may be issues with the database layer.")