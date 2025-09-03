"""
Interactive test to simulate UI button clicks and identify issues
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import traceback

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

class MockApp:
    """Mock application class to test functionality"""
    
    def __init__(self):
        from medical_lab_system.database import DatabaseManager
        from medical_lab_system.models import Patient, TestType, Gender
        
        self.db = DatabaseManager()
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        
        # Create treeviews
        self.patients_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Age", "Gender", "Contact"), show="headings")
        self.tests_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Category", "Price", "Description"), show="headings")
        
        # Add some test data to database
        self.setup_test_data()
        self.load_patients_data()
        self.load_tests_data()
    
    def setup_test_data(self):
        """Set up test data in the database"""
        from medical_lab_system.models import Patient, TestType, Gender
        
        # Create test patient
        patient = Patient(
            id="interactive_test_patient",
            name="Interactive Test Patient",
            age=35,
            gender=Gender.MALE,
            contact_info="interactive@test.com"
        )
        self.db.create_patient(patient)
        
        # Create test test type
        test_type = TestType(
            id="interactive_test_type",
            name="Interactive Test Type",
            description="Interactive test description",
            price=125.0,
            category="Interactive"
        )
        self.db.create_test_type(test_type)
    
    def load_patients_data(self):
        """Load patients into treeview"""
        # Clear existing data
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Load patients from database
        patients = self.db.get_all_patients()
        
        for patient in patients:
            if patient.id == "interactive_test_patient":
                # Insert item and store the full ID in tags
                item_id = self.patients_tree.insert("", tk.END, values=(
                    patient.id[:8],  # Short ID for display
                    patient.name,
                    patient.age,
                    patient.gender.value,
                    patient.contact_info
                ))
                # Store the full ID in the item's tags
                self.patients_tree.item(item_id, tags=(patient.id,))
    
    def load_tests_data(self):
        """Load tests into treeview"""
        # Clear existing data
        for item in self.tests_tree.get_children():
            self.tests_tree.delete(item)
        
        # Load test types from database
        test_types = self.db.get_all_test_types()
        
        for test in test_types:
            if test.id == "interactive_test_type":
                # Insert item and store the full ID in tags
                item_id = self.tests_tree.insert("", tk.END, values=(
                    test.id[:8],  # Short ID for display
                    test.name,
                    test.category,
                    f"${test.price:.2f}",
                    test.description[:50] + "..." if len(test.description) > 50 else test.description
                ))
                # Store the full ID in the item's tags
                self.tests_tree.item(item_id, tags=(test.id,))
    
    def test_edit_patient(self):
        """Test the edit patient functionality"""
        print("Testing edit patient functionality...")
        
        # Select the patient
        children = self.patients_tree.get_children()
        if not children:
            print("✗ No patients in treeview")
            return False
        
        # Select the first patient
        self.patients_tree.selection_set(children[0])
        
        # Try to edit patient
        try:
            selected = self.patients_tree.selection()
            if not selected:
                print("✗ No patient selected")
                return False
            
            # Get the full ID from tags
            item = selected[0]
            patient_id = self.patients_tree.item(item, "tags")[0]
            print(f"✓ Retrieved patient ID from tags: {patient_id}")
            
            # Get patient from database
            patient = self.db.get_patient(patient_id)
            if not patient:
                print("✗ Failed to retrieve patient from database")
                return False
            
            print(f"✓ Retrieved patient from database: {patient.name}")
            
            # Update patient
            patient.name = "Updated Interactive Test Patient"
            result = self.db.update_patient(patient)
            if not result:
                print("✗ Failed to update patient in database")
                return False
            
            print("✓ Patient updated in database")
            
            # Reload data to verify
            self.load_patients_data()
            print("✓ Patient data reloaded")
            
            return True
            
        except Exception as e:
            print(f"✗ Edit patient failed: {e}")
            traceback.print_exc()
            return False
    
    def test_delete_patient(self):
        """Test the delete patient functionality"""
        print("\nTesting delete patient functionality...")
        
        # Select the patient
        children = self.patients_tree.get_children()
        if not children:
            print("✗ No patients in treeview")
            return False
        
        # Select the first patient
        self.patients_tree.selection_set(children[0])
        
        # Try to delete patient
        try:
            selected = self.patients_tree.selection()
            if not selected:
                print("✗ No patient selected")
                return False
            
            # Get the full ID from tags
            item = selected[0]
            patient_id = self.patients_tree.item(item, "tags")[0]
            print(f"✓ Retrieved patient ID from tags: {patient_id}")
            
            # Delete patient from database
            result = self.db.delete_patient(patient_id)
            if not result:
                print("✗ Failed to delete patient from database")
                return False
            
            print("✓ Patient deleted from database")
            
            # Reload data to verify
            self.load_patients_data()
            print("✓ Patient data reloaded")
            
            return True
            
        except Exception as e:
            print(f"✗ Delete patient failed: {e}")
            traceback.print_exc()
            return False
    
    def test_edit_test(self):
        """Test the edit test functionality"""
        print("\nTesting edit test functionality...")
        
        # Select the test
        children = self.tests_tree.get_children()
        if not children:
            print("✗ No tests in treeview")
            return False
        
        # Select the first test
        self.tests_tree.selection_set(children[0])
        
        # Try to edit test
        try:
            selected = self.tests_tree.selection()
            if not selected:
                print("✗ No test selected")
                return False
            
            # Get the full ID from tags
            item = selected[0]
            test_id = self.tests_tree.item(item, "tags")[0]
            print(f"✓ Retrieved test ID from tags: {test_id}")
            
            # Get test from database
            test = self.db.get_test_type(test_id)
            if not test:
                print("✗ Failed to retrieve test from database")
                return False
            
            print(f"✓ Retrieved test from database: {test.name}")
            
            # Update test
            test.name = "Updated Interactive Test Type"
            result = self.db.update_test_type(test)
            if not result:
                print("✗ Failed to update test in database")
                return False
            
            print("✓ Test updated in database")
            
            # Reload data to verify
            self.load_tests_data()
            print("✓ Test data reloaded")
            
            return True
            
        except Exception as e:
            print(f"✗ Edit test failed: {e}")
            traceback.print_exc()
            return False
    
    def test_delete_test(self):
        """Test the delete test functionality"""
        print("\nTesting delete test functionality...")
        
        # Select the test
        children = self.tests_tree.get_children()
        if not children:
            print("✗ No tests in treeview")
            return False
        
        # Select the first test
        self.tests_tree.selection_set(children[0])
        
        # Try to delete test
        try:
            selected = self.tests_tree.selection()
            if not selected:
                print("✗ No test selected")
                return False
            
            # Get the full ID from tags
            item = selected[0]
            test_id = self.tests_tree.item(item, "tags")[0]
            print(f"✓ Retrieved test ID from tags: {test_id}")
            
            # Delete test from database
            result = self.db.delete_test_type(test_id)
            if not result:
                print("✗ Failed to delete test from database")
                return False
            
            print("✓ Test deleted from database")
            
            # Reload data to verify
            self.load_tests_data()
            print("✓ Test data reloaded")
            
            return True
            
        except Exception as e:
            print(f"✗ Delete test failed: {e}")
            traceback.print_exc()
            return False
    
    def cleanup(self):
        """Clean up test data"""
        try:
            self.db.delete_patient("interactive_test_patient")
            self.db.delete_test_type("interactive_test_type")
            self.root.destroy()
            print("\n✓ Test data cleaned up")
        except:
            pass

def run_interactive_tests():
    """Run all interactive tests"""
    print("Running interactive tests for edit and delete functionality...\n")
    
    app = MockApp()
    
    try:
        # Test all functionality
        edit_patient_success = app.test_edit_patient()
        delete_patient_success = app.test_delete_patient()
        
        # Recreate test data for test operations
        app.setup_test_data()
        app.load_tests_data()
        
        edit_test_success = app.test_edit_test()
        delete_test_success = app.test_delete_test()
        
        # Clean up
        app.cleanup()
        
        if edit_patient_success and delete_patient_success and edit_test_success and delete_test_success:
            print("\n🎉 All interactive tests passed!")
            print("The edit and delete functionality should be working correctly.")
            return True
        else:
            print("\n❌ Some interactive tests failed.")
            return False
            
    except Exception as e:
        print(f"✗ Interactive tests failed with exception: {e}")
        traceback.print_exc()
        app.cleanup()
        return False

if __name__ == "__main__":
    if run_interactive_tests():
        print("\n✅ All functionality tests passed!")
    else:
        print("\n❌ Some tests failed. There may be an issue with the implementation.")