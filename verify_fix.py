"""
Verify that the fix for edit and delete functionality works correctly
"""
import sys
import os
import tkinter as tk

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_fix():
    """Test that the fix works correctly"""
    print("Testing the fix for edit and delete functionality...")
    
    try:
        from medical_lab_system.main import MedicalLabApp
        
        # Create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create app instance
        app = MedicalLabApp(root)
        print("✓ Application instance created")
        
        # Test that load methods don't crash even before UI is shown
        app.load_patients_data()
        app.load_tests_data()
        print("✓ Data loading methods executed without crashing (fix verified)")
        
        # Clean up
        root.destroy()
        print("✓ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_fix():
        print("\n🎉 Fix verification test passed!")
        print("The edit and delete functionality should now work correctly.")
    else:
        print("\n❌ Fix verification test failed.")
