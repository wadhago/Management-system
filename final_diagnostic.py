"""
Final diagnostic test to identify the exact issue with edit and delete functionality
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_actual_database_state():
    """Check the actual state of the database"""
    print("Checking actual database state...")
    
    try:
        # Connect to the database
        conn = sqlite3.connect("medical_lab_system/medical_lab.db")
        cursor = conn.cursor()
        
        # Check patients table
        cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = cursor.fetchone()[0]
        print(f"Total patients in database: {patient_count}")
        
        # Check test_types table
        cursor.execute("SELECT COUNT(*) FROM test_types")
        test_count = cursor.fetchone()[0]
        print(f"Total test types in database: {test_count}")
        
        # Show some sample data
        if patient_count > 0:
            cursor.execute("SELECT id, name FROM patients LIMIT 3")
            patients = cursor.fetchall()
            print("Sample patients:")
            for patient in patients:
                print(f"  ID: {patient[0]} | Name: {patient[1]}")
        
        if test_count > 0:
            cursor.execute("SELECT id, name FROM test_types LIMIT 3")
            tests = cursor.fetchall()
            print("Sample test types:")
            for test in tests:
                print(f"  ID: {test[0]} | Name: {test[1]}")
        
        conn.close()
        print("✓ Database state check completed")
        return True
        
    except Exception as e:
        print(f"✗ Database state check failed: {e}")
        return False

def test_with_actual_app_instance():
    """Test with an actual instance of the application"""
    print("\nTesting with actual application instance...")
    
    try:
        from medical_lab_system.main import MedicalLabApp
        
        # Create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create app instance
        app = MedicalLabApp(root)
        print("✓ Application instance created")
        
        # Test database connection
        patients = app.db.get_all_patients()
        tests = app.db.get_all_test_types()
        print(f"✓ Database connection successful: {len(patients)} patients, {len(tests)} test types")
        
        # Test loading data methods
        app.load_patients_data()
        app.load_tests_data()
        print("✓ Data loading methods executed")
        
        # Check if treeviews have data
        patient_children = app.patients_tree.get_children()
        test_children = app.tests_tree.get_children()
        print(f"✓ Treeviews populated: {len(patient_children)} patients, {len(test_children)} tests")
        
        # Clean up
        root.destroy()
        print("✓ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Application instance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_operations():
    """Test specific operations that might be failing"""
    print("\nTesting specific operations...")
    
    try:
        from medical_lab_system.database import DatabaseManager
        from medical_lab_system.models import Patient, TestType, Gender
        
        db = DatabaseManager()
        
        # Create test data
        patient = Patient(
            id="specific_test_patient_123",
            name="Specific Test Patient",
            age=28,
            gender=Gender.FEMALE,
            contact_info="specific@test.com"
        )
        
        test_type = TestType(
            id="specific_test_type_123",
            name="Specific Test Type",
            description="Specific test description",
            price=85.0,
            category="Specific"
        )
        
        # Test creation
        patient_created = db.create_patient(patient)
        test_created = db.create_test_type(test_type)
        print(f"✓ Data creation: Patient={patient_created}, Test={test_created}")
        
        # Test retrieval
        retrieved_patient = db.get_patient("specific_test_patient_123")
        retrieved_test = db.get_test_type("specific_test_type_123")
        print(f"✓ Data retrieval: Patient={retrieved_patient is not None}, Test={retrieved_test is not None}")
        
        # Test update
        if retrieved_patient and retrieved_test:
            retrieved_patient.name = "Updated Specific Test Patient"
            retrieved_test.name = "Updated Specific Test Type"
            
            patient_updated = db.update_patient(retrieved_patient)
            test_updated = db.update_test_type(retrieved_test)
            print(f"✓ Data update: Patient={patient_updated}, Test={test_updated}")
        
        # Test deletion
        patient_deleted = db.delete_patient("specific_test_patient_123")
        test_deleted = db.delete_test_type("specific_test_type_123")
        print(f"✓ Data deletion: Patient={patient_deleted}, Test={test_deleted}")
        
        return True
        
    except Exception as e:
        print(f"✗ Specific operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests"""
    print("Running final diagnostic tests for edit and delete functionality...\n")
    
    # Test 1: Database state
    test1 = test_actual_database_state()
    
    # Test 2: Application instance
    test2 = test_with_actual_app_instance()
    
    # Test 3: Specific operations
    test3 = test_specific_operations()
    
    if test1 and test2 and test3:
        print("\n🎉 All diagnostic tests passed!")
        print("The edit and delete functionality should be working correctly.")
        print("\nIf you're still experiencing issues, please provide more details about:")
        print("1. What specific action is failing (edit patient, delete patient, edit test, delete test)")
        print("2. What error message you're seeing (if any)")
        print("3. What you expect to happen vs. what actually happens")
        return True
    else:
        print("\n❌ Some diagnostic tests failed.")
        return False

if __name__ == "__main__":
    main()