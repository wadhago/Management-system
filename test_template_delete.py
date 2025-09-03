#!/usr/bin/env python3
"""
Test script to verify template delete functionality
"""
import sys
import os
import uuid
from datetime import datetime

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

from medical_lab_system.database import DatabaseManager
from medical_lab_system.models import TestType, TestTemplate

def test_template_delete():
    """Test the template delete functionality"""
    print("Testing template delete functionality...")
    
    # Initialize database
    db = DatabaseManager()
    
    # Create a test type first
    test_type = TestType(
        id=str(uuid.uuid4()),
        name="Template Delete Test",
        description="Test type for template deletion",
        price=100.0,
        category="Test"
    )
    
    if not db.create_test_type(test_type):
        print("Failed to create test type")
        return False
    
    print(f"Created test type: {test_type.name}")
    
    # Create a template for this test type
    template = TestTemplate(
        id=str(uuid.uuid4()),
        test_type_id=test_type.id,
        template_content="This is a test template for deletion testing."
    )
    
    if not db.create_test_template(template):
        print("Failed to create test template")
        # Clean up test type
        db.delete_test_type(test_type.id)
        return False
    
    print(f"Created template for test type: {test_type.name}")
    
    # Verify template exists
    retrieved_template = db.get_test_template_by_test_type(test_type.id)
    if not retrieved_template:
        print("Failed to retrieve created template")
        # Clean up
        db.delete_test_type(test_type.id)
        return False
    
    print("Template successfully created and retrieved")
    
    # Test deletion
    if not db.delete_test_template(retrieved_template.id):
        print("Failed to delete template")
        # Clean up
        db.delete_test_type(test_type.id)
        return False
    
    print("Template successfully deleted")
    
    # Verify template is deleted
    deleted_template = db.get_test_template_by_test_type(test_type.id)
    if deleted_template:
        print("Template still exists after deletion")
        # Clean up
        db.delete_test_type(test_type.id)
        return False
    
    print("Template deletion verified - template no longer exists")
    
    # Clean up test type
    db.delete_test_type(test_type.id)
    
    print("Test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = test_template_delete()
        if success:
            print("✅ Template delete functionality test PASSED")
        else:
            print("❌ Template delete functionality test FAILED")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Template delete functionality test FAILED with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)