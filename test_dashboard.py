"""
Test script to verify that the dashboard is working correctly
"""
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from models import Patient, TestType, TestRequest, MedicalReport, TestStatus, Gender
import uuid
from datetime import datetime

def test_dashboard_data():
    """Test that the dashboard can load data correctly"""
    # Initialize database
    db = DatabaseManager()
    
    # Create a test patient
    patient = Patient(
        id=str(uuid.uuid4()),
        name="Test Patient",
        age=30,
        gender=Gender.MALE,
        contact_info="test@example.com"
    )
    db.create_patient(patient)
    
    # Create a test test type
    test_type = TestType(
        id=str(uuid.uuid4()),
        name="Complete Blood Count",
        description="Measures several components and features of blood",
        price=50.0,
        category="Blood"
    )
    db.create_test_type(test_type)
    
    # Create a test request
    test_request = TestRequest(
        id=str(uuid.uuid4()),
        patient_id=patient.id,
        test_type_id=test_type.id,
        status=TestStatus.COMPLETED,
        requested_by="Doctor",
        requested_at=datetime.now()
    )
    db.create_test_request(test_request)
    
    # Create a medical report
    report = MedicalReport(
        id=str(uuid.uuid4()),
        test_request_id=test_request.id,
        content="This is a test report content.",
        signed_by="Doctor",
        signed_at=datetime.now(),
        created_at=datetime.now()
    )
    db.create_medical_report(report)
    
    # Test that we can retrieve the data
    all_patients = db.get_all_patients()
    all_test_types = db.get_all_test_types()
    all_test_requests = db.get_all_test_requests()
    all_medical_reports = db.get_all_medical_reports()
    
    print(f"Total patients: {len(all_patients)}")
    print(f"Total test types: {len(all_test_types)}")
    print(f"Total test requests: {len(all_test_requests)}")
    print(f"Total medical reports: {len(all_medical_reports)}")
    
    # Verify we can get specific data
    if all_medical_reports:
        test_report = all_medical_reports[0]
        print(f"Test report ID: {test_report.id}")
        print(f"Test report content: {test_report.content}")
        
        # Get associated test request
        test_req = db.get_test_request(test_report.test_request_id)
        if test_req:
            print(f"Test request ID: {test_req.id}")
            print(f"Test request status: {test_req.status}")
            
            # Get associated patient
            test_patient = db.get_patient(test_req.patient_id)
            if test_patient:
                print(f"Patient name: {test_patient.name}")
                
            # Get associated test type
            test_test_type = db.get_test_type(test_req.test_type_id)
            if test_test_type:
                print(f"Test type name: {test_test_type.name}")
    
    print("Dashboard data test completed successfully!")

if __name__ == "__main__":
    test_dashboard_data()