"""
Test script to verify all modules of the Medical Laboratory Management System
"""
import sys
import os

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_modules():
    print("Testing Medical Laboratory Management System Modules...")
    
    # Test importing modules
    try:
        from medical_lab_system.models import Patient, Gender, TestType, Sample, SampleStatus
        from medical_lab_system.database import DatabaseManager
        from medical_lab_system.translations import _, set_language
        print("✓ All modules imported successfully")
    except Exception as e:
        print(f"✗ Error importing modules: {e}")
        return False
    
    # Test database initialization
    try:
        db = DatabaseManager()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return False
    
    # Test translation system
    try:
        # Test English
        set_language("en")
        english_text = _("Medical Laboratory Management System")
        assert english_text == "Medical Laboratory Management System"
        
        # Test Arabic
        set_language("ar")
        arabic_text = _("Medical Laboratory Management System")
        assert arabic_text == "نظام إدارة مختبر طبي"
        
        print("✓ Translation system working correctly")
    except Exception as e:
        print(f"✗ Error with translation system: {e}")
        return False
    
    # Test creating a patient
    try:
        import uuid
        from datetime import datetime
        
        patient = Patient(
            id=str(uuid.uuid4()),
            name="Test Patient",
            age=30,
            gender=Gender.MALE,
            contact_info="test@example.com"
        )
        
        success = db.create_patient(patient)
        assert success == True
        print("✓ Patient creation working correctly")
    except Exception as e:
        print(f"✗ Error creating patient: {e}")
        return False
    
    # Test creating a test type
    try:
        test_type = TestType(
            id=str(uuid.uuid4()),
            name="Blood Test",
            description="Complete blood count",
            price=50.0,
            category="Blood"
        )
        
        success = db.create_test_type(test_type)
        assert success == True
        print("✓ Test type creation working correctly")
    except Exception as e:
        print(f"✗ Error creating test type: {e}")
        return False
    
    print("All module tests passed! The application modules are working correctly.")
    return True

if __name__ == "__main__":
    test_modules()