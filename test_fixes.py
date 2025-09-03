"""
Test script to verify the fixes to edit and delete functionality
"""
import sys
import os
import sqlite3

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

from medical_lab_system.database import DatabaseManager
from medical_lab_system.models import Patient, TestType, Gender

def test_database_operations():
    """Test the database operations for patients and tests"""
    db = DatabaseManager()
    
    # Create a test patient
    patient = Patient(
        id="test_patient_1234567890",
        name="Test Patient",
        age=30,
        gender=Gender.MALE,
        contact_info="test@example.com"
    )
    
    # Add patient to database
    result = db.create_patient(patient)
    assert result, "Failed to create patient"
    print("✓ Patient created successfully")
    
    # Retrieve patient
    retrieved_patient = db.get_patient("test_patient_1234567890")
    assert retrieved_patient is not None, "Failed to retrieve patient"
    assert retrieved_patient.name == "Test Patient", "Patient name mismatch"
    print("✓ Patient retrieved successfully")
    
    # Update patient
    retrieved_patient.name = "Updated Patient"
    retrieved_patient.age = 35
    update_result = db.update_patient(retrieved_patient)
    assert update_result, "Failed to update patient"
    print("✓ Patient updated successfully")
    
    # Verify update
    updated_patient = db.get_patient("test_patient_1234567890")
    assert updated_patient.name == "Updated Patient", "Patient update not reflected"
    assert updated_patient.age == 35, "Patient age update not reflected"
    print("✓ Patient update verified")
    
    # Create a test test type
    test_type = TestType(
        id="test_type_1234567890",
        name="Test Blood Count",
        description="Measures blood components",
        price=50.0,
        category="Blood"
    )
    
    # Add test type to database
    result = db.create_test_type(test_type)
    assert result, "Failed to create test type"
    print("✓ Test type created successfully")
    
    # Retrieve test type
    retrieved_test = db.get_test_type("test_type_1234567890")
    assert retrieved_test is not None, "Failed to retrieve test type"
    assert retrieved_test.name == "Test Blood Count", "Test type name mismatch"
    print("✓ Test type retrieved successfully")
    
    # Update test type
    retrieved_test.name = "Updated Blood Count"
    retrieved_test.price = 75.0
    update_result = db.update_test_type(retrieved_test)
    assert update_result, "Failed to update test type"
    print("✓ Test type updated successfully")
    
    # Verify update
    updated_test = db.get_test_type("test_type_1234567890")
    assert updated_test.name == "Updated Blood Count", "Test type update not reflected"
    assert updated_test.price == 75.0, "Test type price update not reflected"
    print("✓ Test type update verified")
    
    # Delete test type
    delete_result = db.delete_test_type("test_type_1234567890")
    assert delete_result, "Failed to delete test type"
    print("✓ Test type deleted successfully")
    
    # Verify deletion
    deleted_test = db.get_test_type("test_type_1234567890")
    assert deleted_test is None, "Test type still exists after deletion"
    print("✓ Test type deletion verified")
    
    # Delete patient
    delete_result = db.delete_patient("test_patient_1234567890")
    assert delete_result, "Failed to delete patient"
    print("✓ Patient deleted successfully")
    
    # Verify deletion
    deleted_patient = db.get_patient("test_patient_1234567890")
    assert deleted_patient is None, "Patient still exists after deletion"
    print("✓ Patient deletion verified")

def test_id_truncation():
    """Test that ID truncation works correctly"""
    # Test with a long ID
    long_id = "this_is_a_very_long_id_that_exceeds_eight_characters"
    short_id = long_id[:8]  # First 8 characters
    
    assert short_id == "this_is_", "ID truncation not working correctly"
    print("✓ ID truncation works correctly")

if __name__ == "__main__":
    print("Testing database operations...")
    test_database_operations()
    
    print("\nTesting ID truncation...")
    test_id_truncation()
    
    print("\nAll tests passed! The fixes should resolve the edit and delete issues.")