"""
Comprehensive test to verify the fixes to edit and delete functionality
"""
import sys
import os
import sqlite3

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

from medical_lab_system.database import DatabaseManager
from medical_lab_system.models import Patient, TestType, Gender

def test_full_patient_lifecycle():
    """Test the full patient lifecycle: create, retrieve, update, delete"""
    print("Testing full patient lifecycle...")
    
    db = DatabaseManager()
    
    # 1. Create patient
    patient = Patient(
        id="comprehensive_patient_test",
        name="Comprehensive Test Patient",
        age=40,
        gender=Gender.OTHER,
        contact_info="comprehensive@test.com"
    )
    
    create_result = db.create_patient(patient)
    assert create_result, "Failed to create patient"
    print("✓ Patient created successfully")
    
    # 2. Retrieve patient
    retrieved_patient = db.get_patient("comprehensive_patient_test")
    assert retrieved_patient is not None, "Failed to retrieve patient"
    assert retrieved_patient.name == "Comprehensive Test Patient", "Patient name mismatch"
    assert retrieved_patient.age == 40, "Patient age mismatch"
    print("✓ Patient retrieved successfully")
    
    # 3. Update patient
    retrieved_patient.name = "Updated Comprehensive Patient"
    retrieved_patient.age = 45
    update_result = db.update_patient(retrieved_patient)
    assert update_result, "Failed to update patient"
    print("✓ Patient updated successfully")
    
    # 4. Verify update
    updated_patient = db.get_patient("comprehensive_patient_test")
    assert updated_patient.name == "Updated Comprehensive Patient", "Patient update not reflected"
    assert updated_patient.age == 45, "Patient age update not reflected"
    print("✓ Patient update verified")
    
    # 5. Delete patient
    delete_result = db.delete_patient("comprehensive_patient_test")
    assert delete_result, "Failed to delete patient"
    print("✓ Patient deleted successfully")
    
    # 6. Verify deletion
    deleted_patient = db.get_patient("comprehensive_patient_test")
    assert deleted_patient is None, "Patient still exists after deletion"
    print("✓ Patient deletion verified")
    
    print("🎉 Full patient lifecycle test passed!")

def test_full_test_type_lifecycle():
    """Test the full test type lifecycle: create, retrieve, update, delete"""
    print("\nTesting full test type lifecycle...")
    
    db = DatabaseManager()
    
    # 1. Create test type
    test_type = TestType(
        id="comprehensive_test_type_test",
        name="Comprehensive Test Type",
        description="Test for comprehensive testing",
        price=150.0,
        category="Comprehensive"
    )
    
    create_result = db.create_test_type(test_type)
    assert create_result, "Failed to create test type"
    print("✓ Test type created successfully")
    
    # 2. Retrieve test type
    retrieved_test = db.get_test_type("comprehensive_test_type_test")
    assert retrieved_test is not None, "Failed to retrieve test type"
    assert retrieved_test.name == "Comprehensive Test Type", "Test type name mismatch"
    assert retrieved_test.price == 150.0, "Test type price mismatch"
    print("✓ Test type retrieved successfully")
    
    # 3. Update test type
    retrieved_test.name = "Updated Comprehensive Test"
    retrieved_test.price = 200.0
    update_result = db.update_test_type(retrieved_test)
    assert update_result, "Failed to update test type"
    print("✓ Test type updated successfully")
    
    # 4. Verify update
    updated_test = db.get_test_type("comprehensive_test_type_test")
    assert updated_test.name == "Updated Comprehensive Test", "Test type update not reflected"
    assert updated_test.price == 200.0, "Test type price update not reflected"
    print("✓ Test type update verified")
    
    # 5. Delete test type
    delete_result = db.delete_test_type("comprehensive_test_type_test")
    assert delete_result, "Failed to delete test type"
    print("✓ Test type deleted successfully")
    
    # 6. Verify deletion
    deleted_test = db.get_test_type("comprehensive_test_type_test")
    assert deleted_test is None, "Test type still exists after deletion"
    print("✓ Test type deletion verified")
    
    print("🎉 Full test type lifecycle test passed!")

def test_id_handling():
    """Test ID handling with long IDs that need truncation"""
    print("\nTesting ID handling with truncation...")
    
    db = DatabaseManager()
    
    # Create patient with long ID
    long_patient_id = "this_is_a_very_long_patient_id_that_exceeds_eight_characters"
    patient = Patient(
        id=long_patient_id,
        name="Long ID Patient",
        age=35,
        gender=Gender.FEMALE,
        contact_info="longid@test.com"
    )
    
    create_result = db.create_patient(patient)
    assert create_result, "Failed to create patient with long ID"
    print("✓ Patient with long ID created successfully")
    
    # Retrieve patient with long ID
    retrieved_patient = db.get_patient(long_patient_id)
    assert retrieved_patient is not None, "Failed to retrieve patient with long ID"
    assert retrieved_patient.id == long_patient_id, "Patient ID mismatch"
    print("✓ Patient with long ID retrieved successfully")
    
    # Update patient with long ID
    retrieved_patient.name = "Updated Long ID Patient"
    update_result = db.update_patient(retrieved_patient)
    assert update_result, "Failed to update patient with long ID"
    print("✓ Patient with long ID updated successfully")
    
    # Delete patient with long ID
    delete_result = db.delete_patient(long_patient_id)
    assert delete_result, "Failed to delete patient with long ID"
    print("✓ Patient with long ID deleted successfully")
    
    # Create test type with long ID
    long_test_id = "this_is_a_very_long_test_type_id_that_exceeds_eight_characters"
    test_type = TestType(
        id=long_test_id,
        name="Long ID Test",
        description="Test with long ID",
        price=125.0,
        category="LongID"
    )
    
    create_result = db.create_test_type(test_type)
    assert create_result, "Failed to create test type with long ID"
    print("✓ Test type with long ID created successfully")
    
    # Retrieve test type with long ID
    retrieved_test = db.get_test_type(long_test_id)
    assert retrieved_test is not None, "Failed to retrieve test type with long ID"
    assert retrieved_test.id == long_test_id, "Test type ID mismatch"
    print("✓ Test type with long ID retrieved successfully")
    
    # Update test type with long ID
    retrieved_test.name = "Updated Long ID Test"
    update_result = db.update_test_type(retrieved_test)
    assert update_result, "Failed to update test type with long ID"
    print("✓ Test type with long ID updated successfully")
    
    # Delete test type with long ID
    delete_result = db.delete_test_type(long_test_id)
    assert delete_result, "Failed to delete test type with long ID"
    print("✓ Test type with long ID deleted successfully")
    
    print("🎉 ID handling test passed!")

def inspect_database_state():
    """Inspect the current state of the database"""
    print("\nInspecting database state...")
    
    try:
        conn = sqlite3.connect("medical_lab_system/medical_lab.db")
        cursor = conn.cursor()
        
        # Check if our test records were properly cleaned up
        cursor.execute("SELECT COUNT(*) FROM patients WHERE id LIKE 'comprehensive_%' OR id LIKE 'this_is_a_very_long_%'")
        patient_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM test_types WHERE id LIKE 'comprehensive_%' OR id LIKE 'this_is_a_very_long_%'")
        test_count = cursor.fetchone()[0]
        
        conn.close()
        
        if patient_count == 0 and test_count == 0:
            print("✓ Database is clean - no test records found")
        else:
            print(f"⚠ Database has {patient_count} test patient records and {test_count} test type records")
            print("  This is not necessarily an error - just informational")
            
    except Exception as e:
        print(f"✗ Database inspection failed: {e}")

if __name__ == "__main__":
    print("Running comprehensive tests for edit and delete functionality...\n")
    
    try:
        test_full_patient_lifecycle()
        test_full_test_type_lifecycle()
        test_id_handling()
        inspect_database_state()
        
        print("\n🎉 All comprehensive tests passed!")
        print("The edit and delete functionality should now be working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("There may still be issues with the implementation.")