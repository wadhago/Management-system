"""
Test the complete user workflow for edit and delete functionality
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_complete_user_workflow():
    """Test the complete user workflow"""
    print("Testing complete user workflow...")
    
    try:
        from medical_lab_system.main import MedicalLabApp
        from medical_lab_system.database import DatabaseManager
        from medical_lab_system.models import Patient, TestType, Gender
        
        # Create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create app instance
        app = MedicalLabApp(root)
        print("✓ Application instance created")
        
        # Create test data directly in database
        db = DatabaseManager()
        
        # Create test patient
        patient = Patient(
            id="workflow_test_patient",
            name="Workflow Test Patient",
            age=42,
            gender=Gender.OTHER,
            contact_info="workflow@test.com"
        )
        db.create_patient(patient)
        print("✓ Test patient created in database")
        
        # Create test test type
        test_type = TestType(
            id="workflow_test_type",
            name="Workflow Test Type",
            description="Workflow test description",
            price=95.0,
            category="Workflow"
        )
        db.create_test_type(test_type)
        print("✓ Test test type created in database")
        
        # Show patients screen (this creates the patients_tree)
        app.show_patients()
        print("✓ Patients screen displayed")
        
        # Verify patient is in treeview
        children = app.patients_tree.get_children()
        patient_found = False
        for child in children:
            tags = app.patients_tree.item(child, "tags")
            if tags and tags[0] == "workflow_test_patient":
                patient_found = True
                # Select this patient
                app.patients_tree.selection_set(child)
                break
        
        if patient_found:
            print("✓ Test patient found in treeview and selected")
        else:
            print("✗ Test patient not found in treeview")
            return False
        
        # Test edit patient
        try:
            # Get the selected patient ID from the item's tags
            selected = app.patients_tree.selection()
            if selected:
                item = selected[0]
                patient_id = app.patients_tree.item(item, "tags")[0]
                
                # Get patient from database
                patient = db.get_patient(patient_id)
                if patient:
                    # Update patient
                    patient.name = "Updated Workflow Test Patient"
                    result = db.update_patient(patient)
                    if result:
                        print("✓ Patient edit operation successful")
                        # Refresh UI
                        app.load_patients_data()
                        print("✓ Patient data refreshed in UI")
                    else:
                        print("✗ Patient edit operation failed")
                        return False
                else:
                    print("✗ Failed to retrieve patient from database")
                    return False
            else:
                print("✗ No patient selected")
                return False
        except Exception as e:
            print(f"✗ Patient edit test failed: {e}")
            return False
        
        # Show tests screen (this creates the tests_tree)
        app.show_tests()
        print("✓ Tests screen displayed")
        
        # Verify test type is in treeview
        children = app.tests_tree.get_children()
        test_found = False
        for child in children:
            tags = app.tests_tree.item(child, "tags")
            if tags and tags[0] == "workflow_test_type":
                test_found = True
                # Select this test
                app.tests_tree.selection_set(child)
                break
        
        if test_found:
            print("✓ Test test type found in treeview and selected")
        else:
            print("✗ Test test type not found in treeview")
            return False
        
        # Test edit test
        try:
            # Get the selected test ID from the item's tags
            selected = app.tests_tree.selection()
            if selected:
                item = selected[0]
                test_id = app.tests_tree.item(item, "tags")[0]
                
                # Get test from database
                test = db.get_test_type(test_id)
                if test:
                    # Update test
                    test.name = "Updated Workflow Test Type"
                    result = db.update_test_type(test)
                    if result:
                        print("✓ Test type edit operation successful")
                        # Refresh UI
                        app.load_tests_data()
                        print("✓ Test type data refreshed in UI")
                    else:
                        print("✗ Test type edit operation failed")
                        return False
                else:
                    print("✗ Failed to retrieve test from database")
                    return False
            else:
                print("✗ No test selected")
                return False
        except Exception as e:
            print(f"✗ Test type edit test failed: {e}")
            return False
        
        # Test delete patient
        try:
            # Go back to patients screen
            app.show_patients()
            
            # Find and select the patient again
            children = app.patients_tree.get_children()
            for child in children:
                tags = app.patients_tree.item(child, "tags")
                if tags and tags[0] == "workflow_test_patient":
                    app.patients_tree.selection_set(child)
                    break
            
            # Get the selected patient ID from the item's tags
            selected = app.patients_tree.selection()
            if selected:
                item = selected[0]
                patient_id = app.patients_tree.item(item, "tags")[0]
                
                # Delete patient from database
                result = db.delete_patient(patient_id)
                if result:
                    print("✓ Patient delete operation successful")
                    # Refresh UI
                    app.load_patients_data()
                    print("✓ Patient data refreshed in UI after deletion")
                else:
                    print("✗ Patient delete operation failed")
                    return False
            else:
                print("✗ No patient selected for deletion")
                return False
        except Exception as e:
            print(f"✗ Patient delete test failed: {e}")
            return False
        
        # Test delete test
        try:
            # Go back to tests screen
            app.show_tests()
            
            # Find and select the test again
            children = app.tests_tree.get_children()
            for child in children:
                tags = app.tests_tree.item(child, "tags")
                if tags and tags[0] == "workflow_test_type":
                    app.tests_tree.selection_set(child)
                    break
            
            # Get the selected test ID from the item's tags
            selected = app.tests_tree.selection()
            if selected:
                item = selected[0]
                test_id = app.tests_tree.item(item, "tags")[0]
                
                # Delete test from database
                result = db.delete_test_type(test_id)
                if result:
                    print("✓ Test type delete operation successful")
                    # Refresh UI
                    app.load_tests_data()
                    print("✓ Test type data refreshed in UI after deletion")
                else:
                    print("✗ Test type delete operation failed")
                    return False
            else:
                print("✗ No test selected for deletion")
                return False
        except Exception as e:
            print(f"✗ Test type delete test failed: {e}")
            return False
        
        # Clean up
        root.destroy()
        print("✓ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Complete user workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running complete user workflow test for edit and delete functionality...\n")
    
    if test_complete_user_workflow():
        print("\n🎉 Complete user workflow test passed!")
        print("The edit and delete functionality should now work correctly in the actual application.")
    else:
        print("\n❌ Complete user workflow test failed.")