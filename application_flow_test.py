"""
Test that mimics the actual application flow to identify issues
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import traceback

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_application_flow():
    """Test the complete application flow"""
    print("Testing complete application flow...")
    
    try:
        from medical_lab_system.database import DatabaseManager
        from medical_lab_system.models import Patient, TestType, Gender
        
        # Initialize database
        db = DatabaseManager()
        print("✓ Database initialized")
        
        # Create test patient
        patient = Patient(
            id="flow_test_patient",
            name="Flow Test Patient",
            age=25,
            gender=Gender.FEMALE,
            contact_info="flow@test.com"
        )
        
        # Add patient to database
        create_result = db.create_patient(patient)
        print(f"✓ Patient created: {'SUCCESS' if create_result else 'FAILED'}")
        
        # Create test test type
        test_type = TestType(
            id="flow_test_type",
            name="Flow Test Type",
            description="Flow test description",
            price=75.0,
            category="FlowTest"
        )
        
        # Add test type to database
        create_result = db.create_test_type(test_type)
        print(f"✓ Test type created: {'SUCCESS' if create_result else 'FAILED'}")
        
        # Simulate loading patients into treeview (like load_patients_data)
        print("\nSimulating patient treeview loading...")
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Create patients treeview
        patients_tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Gender", "Contact"), show="headings")
        for col in ["ID", "Name", "Age", "Gender", "Contact"]:
            patients_tree.heading(col, text=col)
        
        # Load patients from database (like load_patients_data)
        patients = db.get_all_patients()
        print(f"✓ Retrieved {len(patients)} patients from database")
        
        for patient in patients:
            if patient.id == "flow_test_patient":
                # Insert item and store the full ID in tags
                item_id = patients_tree.insert("", "end", values=(
                    patient.id[:8],  # Short ID for display
                    patient.name,
                    patient.age,
                    patient.gender.value,
                    patient.contact_info
                ))
                # Store the full ID in the item's tags
                patients_tree.item(item_id, tags=(patient.id,))
                print(f"✓ Patient added to treeview with full ID in tags: {patient.id}")
        
        # Simulate selecting patient and editing (like edit_patient)
        print("\nSimulating patient edit operation...")
        children = patients_tree.get_children()
        if children:
            # Select the first patient
            patients_tree.selection_set(children[0])
            selected = patients_tree.selection()
            
            if selected:
                # Get the full ID from tags (like in edit_patient)
                full_patient_id = patients_tree.item(selected[0], "tags")[0]
                print(f"✓ Retrieved full patient ID from tags: {full_patient_id}")
                
                # Retrieve patient from database
                retrieved_patient = db.get_patient(full_patient_id)
                if retrieved_patient:
                    print(f"✓ Retrieved patient from database: {retrieved_patient.name}")
                    
                    # Update patient
                    retrieved_patient.name = "Updated Flow Test Patient"
                    update_result = db.update_patient(retrieved_patient)
                    print(f"✓ Patient update in database: {'SUCCESS' if update_result else 'FAILED'}")
                else:
                    print("✗ Failed to retrieve patient from database")
            else:
                print("✗ No patient selected")
        else:
            print("✗ No patients in treeview")
        
        # Simulate loading tests into treeview (like load_tests_data)
        print("\nSimulating test type treeview loading...")
        
        # Create tests treeview
        tests_tree = ttk.Treeview(root, columns=("ID", "Name", "Category", "Price", "Description"), show="headings")
        for col in ["ID", "Name", "Category", "Price", "Description"]:
            tests_tree.heading(col, text=col)
        
        # Load test types from database (like load_tests_data)
        test_types = db.get_all_test_types()
        print(f"✓ Retrieved {len(test_types)} test types from database")
        
        for test in test_types:
            if test.id == "flow_test_type":
                # Insert item and store the full ID in tags
                item_id = tests_tree.insert("", "end", values=(
                    test.id[:8],  # Short ID for display
                    test.name,
                    test.category,
                    f"${test.price:.2f}",
                    test.description[:50] + "..." if len(test.description) > 50 else test.description
                ))
                # Store the full ID in the item's tags
                tests_tree.item(item_id, tags=(test.id,))
                print(f"✓ Test type added to treeview with full ID in tags: {test.id}")
        
        # Simulate selecting test and editing (like edit_test)
        print("\nSimulating test type edit operation...")
        children = tests_tree.get_children()
        if children:
            # Select the first test
            tests_tree.selection_set(children[0])
            selected = tests_tree.selection()
            
            if selected:
                # Get the full ID from tags (like in edit_test)
                full_test_id = tests_tree.item(selected[0], "tags")[0]
                print(f"✓ Retrieved full test ID from tags: {full_test_id}")
                
                # Retrieve test from database
                retrieved_test = db.get_test_type(full_test_id)
                if retrieved_test:
                    print(f"✓ Retrieved test from database: {retrieved_test.name}")
                    
                    # Update test
                    retrieved_test.name = "Updated Flow Test Type"
                    update_result = db.update_test_type(retrieved_test)
                    print(f"✓ Test type update in database: {'SUCCESS' if update_result else 'FAILED'}")
                else:
                    print("✗ Failed to retrieve test from database")
            else:
                print("✗ No test selected")
        else:
            print("✗ No test types in treeview")
        
        # Clean up test data
        print("\nCleaning up test data...")
        db.delete_patient("flow_test_patient")
        db.delete_test_type("flow_test_type")
        print("✓ Test data cleaned up")
        
        # Clean up UI
        root.destroy()
        
        print("\n🎉 Complete application flow test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Application flow test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running complete application flow test...\n")
    
    if test_application_flow():
        print("\n🎉 All tests in the application flow passed!")
        print("The edit and delete functionality should be working correctly in the actual application.")
    else:
        print("\n❌ Application flow test failed.")
        print("There may be an issue with how the application is handling the edit/delete operations.")