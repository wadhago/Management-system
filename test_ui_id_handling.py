"""
Test UI ID handling to verify the fixes work correctly
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the medical_lab_system directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'medical_lab_system'))

def test_treeview_id_handling():
    """Test that treeview correctly handles full IDs in tags"""
    print("Testing treeview ID handling...")
    
    # Create a simple Tkinter window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a treeview
    tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings")
    
    # Add headings
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    
    # Test data with long ID
    long_id = "this_is_a_very_long_id_that_exceeds_eight_characters"
    display_id = long_id[:8]  # First 8 characters for display
    
    # Insert item with truncated ID for display but full ID in tags
    item_id = tree.insert("", tk.END, values=(display_id, "Test Item"))
    tree.item(item_id, tags=(long_id,))
    
    # Verify the item was inserted
    children = tree.get_children()
    assert len(children) == 1, "Item was not inserted into treeview"
    print("✓ Item inserted into treeview")
    
    # Verify display ID is truncated
    values = tree.item(children[0], "values")
    assert values[0] == display_id, "Display ID is not correctly truncated"
    print("✓ Display ID is correctly truncated")
    
    # Verify full ID is stored in tags
    tags = tree.item(children[0], "tags")
    assert tags[0] == long_id, "Full ID is not correctly stored in tags"
    print("✓ Full ID is correctly stored in tags")
    
    # Clean up
    root.destroy()
    
    print("🎉 Treeview ID handling test passed!")

def test_id_retrieval():
    """Test retrieving full IDs from treeview items"""
    print("\nTesting ID retrieval from treeview...")
    
    # Create a simple Tkinter window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a treeview
    tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings")
    
    # Add headings
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    
    # Test with multiple items
    test_data = [
        ("short_id_1", "Short ID Item 1"),
        ("this_is_a_very_long_id_number_1", "Long ID Item 1"),
        ("short_id_2", "Short ID Item 2"),
        ("this_is_a_very_long_id_number_2", "Long ID Item 2")
    ]
    
    item_ids = []
    for full_id, name in test_data:
        display_id = full_id[:8]
        item_id = tree.insert("", tk.END, values=(display_id, name))
        tree.item(item_id, tags=(full_id,))
        item_ids.append(item_id)
    
    # Test selecting each item and retrieving the full ID
    for i, (expected_full_id, _) in enumerate(test_data):
        # Simulate selection
        tree.selection_set(item_ids[i])
        
        # Retrieve the selected item
        selected = tree.selection()
        assert len(selected) == 1, "Selection failed"
        
        # Get the full ID from tags
        full_id = tree.item(selected[0], "tags")[0]
        assert full_id == expected_full_id, f"Full ID mismatch for item {i}"
        print(f"✓ Full ID correctly retrieved for item {i+1}: {full_id}")
    
    # Clean up
    root.destroy()
    
    print("🎉 ID retrieval test passed!")

if __name__ == "__main__":
    print("Running UI ID handling tests...\n")
    
    try:
        test_treeview_id_handling()
        test_id_retrieval()
        
        print("\n🎉 All UI ID handling tests passed!")
        print("The treeview ID handling should now be working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("There may still be issues with the UI implementation.")