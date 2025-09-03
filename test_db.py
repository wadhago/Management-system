#!/usr/bin/env python3
"""
Test script to verify database functionality
"""
import sys
import os

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

from medical_lab_system.database import DatabaseManager
from medical_lab_system.models import Patient, Gender

def test_database():
    print("Testing database functionality...")
    
    # Initialize database
    db = DatabaseManager()
    print("Database initialized successfully")
    
    # Test creating a patient
    patient = Patient(
        id="12345678",
        name="Test Patient",
        age=30,
        gender=Gender.MALE,
        contact_info="test@example.com"
    )
    
    result = db.create_patient(patient)
    print(f"Patient creation result: {result}")
    
    # Test retrieving patients
    patients = db.get_all_patients()
    print(f"Total patients in database: {len(patients)}")
    
    # Print patient details
    for p in patients:
        print(f"Patient: {p.name}, ID: {p.id}, Age: {p.age}")
    
    print("Database test completed successfully!")

if __name__ == "__main__":
    test_database()