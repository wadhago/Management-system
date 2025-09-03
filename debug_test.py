"""
Debug test to identify specific issues with edit and delete functionality
"""
import sys
import os
import traceback

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from medical_lab_system.database import DatabaseManager
        print("✓ DatabaseManager imported successfully")
        
        from medical_lab_system.models import Patient, TestType, Gender
        print("✓ Models imported successfully")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False

def test_database_operations():
    """Test database operations specifically"""
    print("\nTesting database operations...")
    try:
        from medical_lab_system.database import DatabaseManager
        from medical_lab_system.models import Patient, TestType, Gender
        
        db = DatabaseManager()
        print("✓ Database manager initialized")
        
        # Test patient operations
        patient = Patient(
            id="debug_patient_123",
            name="Debug Patient",
            age=30,
            gender=Gender.MALE,
            contact_info="debug@test.com"
        )
        
        # Create
        create_result = db.create_patient(patient)
        print(f"✓ Patient creation: {'SUCCESS' if create_result else 'FAILED'}")
        
        # Retrieve
        retrieved_patient = db.get_patient("debug_patient_123")
        if retrieved_patient:
            print("✓ Patient retrieval: SUCCESS")
        else:
            print("✗ Patient retrieval: FAILED")
            return False
        
        # Update
        retrieved_patient.name = "Updated Debug Patient"
        update_result = db.update_patient(retrieved_patient)
        print(f"✓ Patient update: {'SUCCESS' if update_result else 'FAILED'}")
        
        # Delete
        delete_result = db.delete_patient("debug_patient_123")
        print(f"✓ Patient deletion: {'SUCCESS' if delete_result else 'FAILED'}")
        
        # Test test type operations
        test_type = TestType(
            id="debug_test_123",
            name="Debug Test",
            description="Debug test description",
            price=100.0,
            category="Debug"
        )
        
        # Create
        create_result = db.create_test_type(test_type)
        print(f"✓ Test type creation: {'SUCCESS' if create_result else 'FAILED'}")
        
        # Retrieve
        retrieved_test = db.get_test_type("debug_test_123")
        if retrieved_test:
            print("✓ Test type retrieval: SUCCESS")
        else:
            print("✗ Test type retrieval: FAILED")
            return False
        
        # Update
        retrieved_test.name = "Updated Debug Test"
        update_result = db.update_test_type(retrieved_test)
        print(f"✓ Test type update: {'SUCCESS' if update_result else 'FAILED'}")
        
        # Delete
        delete_result = db.delete_test_type("debug_test_123")
        print(f"✓ Test type deletion: {'SUCCESS' if delete_result else 'FAILED'}")
        
        return True
        
    except Exception as e:
        print(f"✗ Database operations failed: {e}")
        traceback.print_exc()
        return False

def test_ui_components():
    """Test UI components specifically"""
    print("\nTesting UI components...")
    try:
        import tkinter as tk
        from tkinter import ttk
        print("✓ Tkinter imported successfully")
        
        # Create a simple test window
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Create treeview
        tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        
        # Test inserting item with tags
        item_id = tree.insert("", "end", values=("disp_id", "Test Item"))
        tree.item(item_id, tags=("full_id_1234567890",))
        
        # Test retrieving tags
        tree.selection_set(item_id)
        selected = tree.selection()[0]
        full_id = tree.item(selected, "tags")[0]
        
        if full_id == "full_id_1234567890":
            print("✓ Treeview tag handling: SUCCESS")
        else:
            print("✗ Treeview tag handling: FAILED")
            return False
        
        root.destroy()
        print("✓ UI components test completed")
        return True
        
    except Exception as e:
        print(f"✗ UI components test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running debug tests for edit and delete functionality...\n")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Cannot proceed.")
        sys.exit(1)
    
    # Test database operations
    if not test_database_operations():
        print("\n❌ Database operation tests failed.")
        sys.exit(1)
    
    # Test UI components
    if not test_ui_components():
        print("\n❌ UI component tests failed.")
        sys.exit(1)
    
    print("\n🎉 All debug tests passed!")
    print("The edit and delete functionality should be working correctly.")
    print("\nIf you're still experiencing issues, please provide more details about:")
    print("1. What specific action is failing (edit patient, delete patient, edit test, delete test)")
    print("2. What error message you're seeing (if any)")
    print("3. What you expect to happen vs. what actually happens")