#!/usr/bin/env python3
"""
Test script to verify the new database methods
"""
import sys
import os
from datetime import datetime, timedelta

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

from medical_lab_system.database import DatabaseManager

def test_new_database_methods():
    """Test the new database methods"""
    print("Testing new database methods...")
    
    # Initialize database
    db = DatabaseManager()
    print("✓ Database initialized successfully")
    
    # Test get_all_invoices method
    try:
        invoices = db.get_all_invoices()
        print(f"✓ get_all_invoices() returned {len(invoices)} invoices")
    except Exception as e:
        print(f"✗ get_all_invoices() failed with error: {e}")
        return False
    
    # Test get_test_requests_by_date_range method
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        requests = db.get_test_requests_by_date_range(start_date, end_date)
        print(f"✓ get_test_requests_by_date_range() returned {len(requests)} requests")
    except Exception as e:
        print(f"✗ get_test_requests_by_date_range() failed with error: {e}")
        return False
    
    # Test get_invoices_by_date_range method
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        invoices = db.get_invoices_by_date_range(start_date, end_date)
        print(f"✓ get_invoices_by_date_range() returned {len(invoices)} invoices")
    except Exception as e:
        print(f"✗ get_invoices_by_date_range() failed with error: {e}")
        return False
    
    # Test get_patients_by_registration_date_range method
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        patients = db.get_patients_by_registration_date_range(start_date, end_date)
        print(f"✓ get_patients_by_registration_date_range() returned {len(patients)} patients")
    except Exception as e:
        print(f"✗ get_patients_by_registration_date_range() failed with error: {e}")
        return False
    
    print("\n✅ All new database methods are working correctly!")
    return True

if __name__ == "__main__":
    try:
        success = test_new_database_methods()
        if success:
            print("\n🎉 New database methods are working correctly!")
        else:
            print("\n❌ New database methods tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ New database methods tests failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)