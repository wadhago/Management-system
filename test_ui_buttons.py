"""
Test script to verify the UI buttons for edit and delete functionality
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

# Mock the required imports for testing
import unittest
from unittest.mock import Mock, patch

class TestUIButtons(unittest.TestCase):
    
    def setUp(self):
        # Create a mock app instance
        self.app = Mock()
        self.app.db = Mock()
        
        # Mock patient data
        self.sample_patient = Mock()
        self.sample_patient.id = "test_patient_1"
        self.sample_patient.name = "Test Patient"
        self.sample_patient.age = 30
        self.sample_patient.gender = Mock(value="Male")
        self.sample_patient.contact_info = "test@example.com"
        
        # Mock test type data
        self.sample_test = Mock()
        self.sample_test.id = "test_type_1"
        self.sample_test.name = "Test Blood Count"
        self.sample_test.description = "Measures blood components"
        self.sample_test.price = 50.0
        self.sample_test.category = "Blood"
        
        # Setup mock database methods
        self.app.db.get_patient.return_value = self.sample_patient
        self.app.db.update_patient.return_value = True
        self.app.db.delete_patient.return_value = True
        
        self.app.db.get_test_type.return_value = self.sample_test
        self.app.db.update_test_type.return_value = True
        self.app.db.delete_test_type.return_value = True
    
    @patch('tkinter.messagebox.showwarning')
    def test_edit_patient_no_selection(self, mock_warning):
        """Test edit patient when no patient is selected"""
        # Mock the tree selection to return empty
        self.app.patients_tree = Mock()
        self.app.patients_tree.selection.return_value = []
        
        # Import the actual method
        sys.path.append('medical_lab_system')
        from medical_lab_system.main import MedicalLabApp
        
        # Call the edit_patient method
        MedicalLabApp.edit_patient(self.app)
        
        # Verify that warning was shown
        mock_warning.assert_called_once()
    
    @patch('tkinter.messagebox.showwarning')
    def test_delete_patient_no_selection(self, mock_warning):
        """Test delete patient when no patient is selected"""
        # Mock the tree selection to return empty
        self.app.patients_tree = Mock()
        self.app.patients_tree.selection.return_value = []
        
        # Import the actual method
        sys.path.append('medical_lab_system')
        from medical_lab_system.main import MedicalLabApp
        
        # Call the delete_patient method
        MedicalLabApp.delete_patient(self.app)
        
        # Verify that warning was shown
        mock_warning.assert_called_once()
    
    @patch('tkinter.messagebox.showwarning')
    def test_edit_test_no_selection(self, mock_warning):
        """Test edit test when no test is selected"""
        # Mock the tree selection to return empty
        self.app.tests_tree = Mock()
        self.app.tests_tree.selection.return_value = []
        
        # Import the actual method
        sys.path.append('medical_lab_system')
        from medical_lab_system.main import MedicalLabApp
        
        # Call the edit_test method
        MedicalLabApp.edit_test(self.app)
        
        # Verify that warning was shown
        mock_warning.assert_called_once()
    
    @patch('tkinter.messagebox.showwarning')
    def test_delete_test_no_selection(self, mock_warning):
        """Test delete test when no test is selected"""
        # Mock the tree selection to return empty
        self.app.tests_tree = Mock()
        self.app.tests_tree.selection.return_value = []
        
        # Import the actual method
        sys.path.append('medical_lab_system')
        from medical_lab_system.main import MedicalLabApp
        
        # Call the delete_test method
        MedicalLabApp.delete_test(self.app)
        
        # Verify that warning was shown
        mock_warning.assert_called_once()

if __name__ == "__main__":
    unittest.main()