"""
Main application file for the Medical Laboratory Management System
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from typing import List, Optional
import hashlib
import uuid
from database import DatabaseManager
from models import (
    Patient, TestType, TestRequest, Sample, MedicalReport, 
    Invoice, User, InventoryItem, PurchaseOrder, Gender, 
    TestStatus, SampleStatus, UserRole, PaymentMethod
)
from utils import generate_barcode, send_email, encrypt_data, decrypt_data
from translations import _, set_language

class MedicalLabApp:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Medical Laboratory Management System"))
        self.root.geometry("1200x800")
        
        # Initialize database
        self.db = DatabaseManager()
        
        # Current user
        self.current_user = None
        
        # Setup UI
        self.setup_ui()
        
        # Load initial data
        self.load_initial_data()
    
    def setup_ui(self):
        # Create main frames
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.footer_frame = ttk.Frame(self.root)
        self.footer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Header with login info and language selector
        self.setup_header()
        
        # Navigation
        self.setup_navigation()
        
        # Initial content
        self.show_login_screen()
    
    def setup_header(self):
        # Language selector
        lang_frame = ttk.Frame(self.header_frame)
        lang_frame.pack(side=tk.RIGHT)
        
        ttk.Label(lang_frame, text=_("Language:")).pack(side=tk.LEFT)
        
        self.lang_var = tk.StringVar(value="en")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                 values=["en", "ar"], state="readonly", width=5)
        lang_combo.pack(side=tk.LEFT, padx=5)
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # User info
        self.user_label = ttk.Label(self.header_frame, text=_("Not logged in"))
        self.user_label.pack(side=tk.RIGHT, padx=20)
        
        # Logout button
        self.logout_btn = ttk.Button(self.header_frame, text=_("Logout"), 
                                    command=self.logout, state=tk.DISABLED)
        self.logout_btn.pack(side=tk.RIGHT)
    
    def setup_navigation(self):
        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(fill=tk.Y, side=tk.LEFT, padx=5, pady=5)
        
        # Navigation buttons (will be enabled after login)
        self.nav_buttons = {}
        nav_items = [
            (_("Dashboard"), self.show_dashboard),
            (_("Patients"), self.show_patients),
            (_("Tests"), self.show_tests),
            (_("Samples"), self.show_samples),
            (_("Reports"), self.show_reports),
            (_("Billing"), self.show_billing),
            (_("Inventory"), self.show_inventory),
            (_("Users"), self.show_users),
            (_("Statistics"), self.show_statistics)
        ]
        
        for i, (text, command) in enumerate(nav_items):
            btn = ttk.Button(self.nav_frame, text=text, command=command, 
                            width=15, state=tk.DISABLED)
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons[text] = btn
    
    def change_language(self, event=None):
        # Change the language
        lang = self.lang_var.get()
        set_language(lang)
        
        # Update UI elements
        self.root.title(_("Medical Laboratory Management System"))
        self.user_label.config(text=_("Not logged in") if not self.current_user else 
                              _("Logged in as: {} ({})").format(
                                  self.current_user.username, _(self.current_user.role.value)))
        self.logout_btn.config(text=_("Logout"))
        
        # Update navigation buttons
        nav_items = [
            (_("Dashboard"), self.show_dashboard),
            (_("Patients"), self.show_patients),
            (_("Tests"), self.show_tests),
            (_("Samples"), self.show_samples),
            (_("Reports"), self.show_reports),
            (_("Billing"), self.show_billing),
            (_("Inventory"), self.show_inventory),
            (_("Users"), self.show_users),
            (_("Statistics"), self.show_statistics)
        ]
        
        # Update button texts
        for i, (text, _) in enumerate(nav_items):
            btn = list(self.nav_buttons.values())[i]
            btn.config(text=text)
        
        # Show current screen again to update texts
        if hasattr(self, 'current_screen'):
            self.current_screen()
    
    def load_initial_data(self):
        # Create admin user if not exists
        admin_user = self.db.get_user_by_username("admin")
        if not admin_user:
            admin = User(
                id=str(uuid.uuid4()),
                username="admin",
                email="admin@lab.com",
                password_hash=self.hash_password("admin123"),
                role=UserRole.ADMIN
            )
            self.db.create_user(admin)
        
        # Create some sample test types if none exist
        test_types = self.db.get_all_test_types()
        if not test_types:
            sample_tests = [
                TestType(str(uuid.uuid4()), _("Complete Blood Count"), 
                        _("Measures several components and features of blood"), 50.0, _("Blood")),
                TestType(str(uuid.uuid4()), _("Urinalysis"), 
                        _("Analysis of urine components"), 30.0, _("Urine")),
                TestType(str(uuid.uuid4()), _("Stool Analysis"), 
                        _("Examination of stool sample"), 40.0, _("Stool")),
                TestType(str(uuid.uuid4()), _("X-Ray Chest"), 
                        _("Chest X-Ray imaging"), 100.0, _("Radiology"))
            ]
            
            for test in sample_tests:
                self.db.create_test_type(test)
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_login_screen(self):
        self.current_screen = self.show_login_screen
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Login form
        login_frame = ttk.Frame(self.content_frame)
        login_frame.pack(expand=True)
        
        ttk.Label(login_frame, text=_("Login"), font=("Arial", 16)).pack(pady=10)
        
        ttk.Label(login_frame, text=_("Username:")).pack()
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.pack(pady=5)
        
        ttk.Label(login_frame, text=_("Password:")).pack()
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(login_frame, text=_("Login"), 
                  command=self.login).pack(pady=10)
        
        # Demo login info
        ttk.Label(login_frame, 
                 text=_("Demo: admin / admin123")).pack(pady=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror(_("Error"), _("Please enter both username and password"))
            return
        
        hashed_password = self.hash_password(password)
        user = self.db.authenticate_user(username, hashed_password)
        
        if user:
            self.current_user = user
            self.user_label.config(text=_("Logged in as: {} ({})").format(
                user.username, _(user.role.value)))
            self.logout_btn.config(state=tk.NORMAL)
            
            # Enable navigation buttons based on role
            self.enable_navigation()
            
            # Show dashboard
            self.show_dashboard()
        else:
            messagebox.showerror(_("Error"), _("Invalid username or password"))
    
    def logout(self):
        self.current_user = None
        self.user_label.config(text=_("Not logged in"))
        self.logout_btn.config(state=tk.DISABLED)
        
        # Disable navigation
        for btn in self.nav_buttons.values():
            btn.config(state=tk.DISABLED)
        
        # Show login screen
        self.show_login_screen()
    
    def enable_navigation(self):
        # Enable all buttons for admin
        if self.current_user.role == UserRole.ADMIN:
            for btn in self.nav_buttons.values():
                btn.config(state=tk.NORMAL)
        else:
            # Enable based on role (simplified for demo)
            for btn in self.nav_buttons.values():
                btn.config(state=tk.NORMAL)
    
    def show_dashboard(self):
        self.current_screen = self.show_dashboard
        self.clear_content()
        
        ttk.Label(self.content_frame, text=_("Dashboard"), 
                 font=("Arial", 16)).pack(pady=10)
        
        # Stats cards
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Sample stats (in a real app, these would come from the database)
        stats = [
            (_("Total Patients"), "125"),
            (_("Pending Tests"), "24"),
            (_("Completed Today"), "18"),
            (_("Inventory Items"), "42")
        ]
        
        for i, (label, value) in enumerate(stats):
            card = ttk.Frame(stats_frame, relief=tk.RAISED, borderwidth=1)
            card.grid(row=0, column=i, padx=5, sticky="ew")
            stats_frame.grid_columnconfigure(i, weight=1)
            
            ttk.Label(card, text=label, font=("Arial", 10)).pack(pady=5)
            ttk.Label(card, text=value, font=("Arial", 16, "bold")).pack(pady=5)
        
        # Recent activity
        ttk.Label(self.content_frame, text=_("Recent Activity"), 
                 font=("Arial", 12)).pack(pady=(20, 10))
        
        activity_frame = ttk.Frame(self.content_frame)
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Sample activity (would come from database in real app)
        activities = [
            _("Patient John Doe registered"),
            _("Blood test requested for Jane Smith"),
            _("X-Ray report signed by Dr. Johnson"),
            _("Inventory item 'Reagent A' low stock alert")
        ]
        
        for activity in activities:
            ttk.Label(activity_frame, text=f"• {activity}").pack(anchor=tk.W, pady=2)
    
    def show_patients(self):
        self.current_screen = self.show_patients
        self.clear_content()
        
        # Patients header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("Patients Management"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text=_("Add Patient"), 
                  command=self.add_patient).pack(side=tk.RIGHT)
        
        # Patients table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create treeview
        columns = (_("ID"), _("Name"), _("Age"), _("Gender"), _("Contact"))
        self.patients_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.patients_tree.yview)
        self.patients_tree.configure(yscroll=scrollbar.set)
        
        self.patients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load patients data
        self.load_patients_data()
        
        # Add action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text=_("View Details"), 
                  command=self.view_patient_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Edit Patient"), 
                  command=self.edit_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Delete Patient"), 
                  command=self.delete_patient).pack(side=tk.LEFT, padx=5)
    
    def load_patients_data(self):
        # Clear existing data
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Load patients from database
        patients = self.db.get_all_patients()
        
        for patient in patients:
            self.patients_tree.insert("", tk.END, values=(
                patient.id[:8],  # Short ID for display
                patient.name,
                patient.age,
                _(patient.gender.value),
                patient.contact_info
            ))
    
    def add_patient(self):
        # Create add patient dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(_("Add New Patient"))
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text=_("Name:")).pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Age:")).pack(pady=5)
        age_entry = ttk.Entry(dialog, width=40)
        age_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Gender:")).pack(pady=5)
        gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(dialog, textvariable=gender_var,
                                   values=[_("Male"), _("Female"), _("Other")],
                                   state="readonly", width=37)
        gender_combo.pack(pady=5)
        
        ttk.Label(dialog, text=_("Contact Info:")).pack(pady=5)
        contact_entry = ttk.Entry(dialog, width=40)
        contact_entry.pack(pady=5)
        
        def save_patient():
            name = name_entry.get().strip()
            age_str = age_entry.get().strip()
            gender_text = gender_var.get()
            contact = contact_entry.get().strip()
            
            # Validation
            if not name:
                messagebox.showerror(_("Error"), _("Please enter patient name"))
                return
            
            try:
                age = int(age_str)
                if age < 0 or age > 150:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(_("Error"), _("Please enter a valid age"))
                return
            
            if not gender_text:
                messagebox.showerror(_("Error"), _("Please select gender"))
                return
            
            # Map gender text to enum
            gender_map = {
                _("Male"): Gender.MALE,
                _("Female"): Gender.FEMALE,
                _("Other"): Gender.OTHER
            }
            gender = gender_map.get(gender_text, Gender.OTHER)
            
            # Create patient
            patient = Patient(
                id=str(uuid.uuid4()),
                name=name,
                age=age,
                gender=gender,
                contact_info=contact
            )
            
            if self.db.create_patient(patient):
                messagebox.showinfo(_("Success"), _("Patient added successfully"))
                dialog.destroy()
                self.load_patients_data()
            else:
                messagebox.showerror(_("Error"), _("Failed to add patient"))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=_("Save"), command=save_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Cancel"), 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        name_entry.focus()
    
    def view_patient_details(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning(_("Warning"), _("Please select a patient"))
            return
        
        # In a real app, this would show detailed patient information
        messagebox.showinfo(_("Patient Details"), _("Patient details would be shown here"))
    
    def edit_patient(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning(_("Warning"), _("Please select a patient"))
            return
        
        # In a real app, this would open an edit dialog
        messagebox.showinfo(_("Edit Patient"), _("Edit patient functionality would be implemented here"))
    
    def delete_patient(self):
        selected = self.patients_tree.selection()
        if not selected:
            messagebox.showwarning(_("Warning"), _("Please select a patient"))
            return
        
        if messagebox.askyesno(_("Confirm Delete"), 
                              _("Are you sure you want to delete this patient?")):
            # In a real app, this would delete the patient from database
            messagebox.showinfo(_("Delete Patient"), _("Patient deleted successfully"))
            self.load_patients_data()
    
    def show_tests(self):
        self.current_screen = self.show_tests
        self.clear_content()
        
        # Tests header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("Tests Management"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text=_("Add Test"), 
                  command=self.add_test).pack(side=tk.RIGHT)
        
        # Tests table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create treeview
        columns = (_("ID"), _("Name"), _("Category"), _("Price"), _("Description"))
        self.tests_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tests_tree.heading(col, text=col)
            self.tests_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.tests_tree.yview)
        self.tests_tree.configure(yscroll=scrollbar.set)
        
        self.tests_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load tests data
        self.load_tests_data()
    
    def load_tests_data(self):
        # Clear existing data
        for item in self.tests_tree.get_children():
            self.tests_tree.delete(item)
        
        # Load test types from database
        test_types = self.db.get_all_test_types()
        
        for test in test_types:
            self.tests_tree.insert("", tk.END, values=(
                test.id[:8],  # Short ID for display
                test.name,
                _(test.category),
                f"${test.price:.2f}",
                test.description[:50] + "..." if len(test.description) > 50 else test.description
            ))
    
    def add_test(self):
        # Create add test dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(_("Add New Test"))
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text=_("Test Name:")).pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Category:")).pack(pady=5)
        category_entry = ttk.Entry(dialog, width=40)
        category_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Price:")).pack(pady=5)
        price_entry = ttk.Entry(dialog, width=40)
        price_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Description:")).pack(pady=5)
        desc_text = tk.Text(dialog, width=40, height=5)
        desc_text.pack(pady=5)
        
        def save_test():
            name = name_entry.get().strip()
            category = category_entry.get().strip()
            price_str = price_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            
            # Validation
            if not name:
                messagebox.showerror(_("Error"), _("Please enter test name"))
                return
            
            if not category:
                messagebox.showerror(_("Error"), _("Please enter category"))
                return
            
            try:
                price = float(price_str)
                if price < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(_("Error"), _("Please enter a valid price"))
                return
            
            # Create test type
            test_type = TestType(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                price=price,
                category=category
            )
            
            if self.db.create_test_type(test_type):
                messagebox.showinfo(_("Success"), _("Test added successfully"))
                dialog.destroy()
                self.load_tests_data()
            else:
                messagebox.showerror(_("Error"), _("Failed to add test"))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=_("Save"), command=save_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Cancel"), 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        name_entry.focus()
    
    def show_samples(self):
        self.current_screen = self.show_samples
        self.clear_content()
        
        # Samples header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("Sample Management"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text=_("Add Sample"), 
                  command=self.add_sample).pack(side=tk.RIGHT)
        
        # Samples table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create treeview
        columns = (_("ID"), _("Barcode"), _("Test Request"), _("Collected At"), _("Status"))
        self.samples_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.samples_tree.heading(col, text=col)
            self.samples_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.samples_tree.yview)
        self.samples_tree.configure(yscroll=scrollbar.set)
        
        self.samples_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load samples data
        self.load_samples_data()
        
        # Add action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text=_("View Details"), 
                  command=self.view_sample_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Update Status"), 
                  command=self.update_sample_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Generate Barcode"), 
                  command=self.generate_sample_barcode).pack(side=tk.LEFT, padx=5)
    
    def load_samples_data(self):
        # Clear existing data
        for item in self.samples_tree.get_children():
            self.samples_tree.delete(item)
        
        # In a real app, this would load samples from database
        # For now, we'll show a message
        self.samples_tree.insert("", tk.END, values=(
            _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("No samples in database")
        ))
    
    def add_sample(self):
        # Create add sample dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(_("Add New Sample"))
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text=_("Test Request ID:")).pack(pady=5)
        request_entry = ttk.Entry(dialog, width=40)
        request_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Barcode:")).pack(pady=5)
        barcode_entry = ttk.Entry(dialog, width=40)
        barcode_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Status:")).pack(pady=5)
        status_var = tk.StringVar()
        status_combo = ttk.Combobox(dialog, textvariable=status_var,
                                   values=[_("Valid"), _("Damaged"), _("Insufficient")],
                                   state="readonly", width=37)
        status_combo.pack(pady=5)
        
        ttk.Label(dialog, text=_("Notes:")).pack(pady=5)
        notes_text = tk.Text(dialog, width=40, height=5)
        notes_text.pack(pady=5)
        
        def save_sample():
            request_id = request_entry.get().strip()
            barcode = barcode_entry.get().strip()
            status_text = status_var.get()
            notes = notes_text.get("1.0", tk.END).strip()
            
            # Validation
            if not request_id:
                messagebox.showerror(_("Error"), _("Please enter test request ID"))
                return
            
            if not barcode:
                messagebox.showerror(_("Error"), _("Please enter barcode"))
                return
            
            if not status_text:
                messagebox.showerror(_("Error"), _("Please select status"))
                return
            
            # Map status text to enum
            status_map = {
                _("Valid"): SampleStatus.VALID,
                _("Damaged"): SampleStatus.DAMAGED,
                _("Insufficient"): SampleStatus.INSUFFICIENT
            }
            status = status_map.get(status_text, SampleStatus.VALID)
            
            # Create sample
            sample = Sample(
                id=str(uuid.uuid4()),
                test_request_id=request_id,
                barcode=barcode,
                collected_at=datetime.now(),
                status=status,
                notes=notes
            )
            
            # In a real app, this would save to database
            messagebox.showinfo(_("Success"), _("Sample added successfully"))
            dialog.destroy()
            self.load_samples_data()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=_("Save"), command=save_sample).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Cancel"), 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        request_entry.focus()
    
    def view_sample_details(self):
        messagebox.showinfo(_("Sample Details"), _("Sample details would be shown here"))
    
    def update_sample_status(self):
        messagebox.showinfo(_("Update Status"), _("Sample status update functionality would be implemented here"))
    
    def generate_sample_barcode(self):
        messagebox.showinfo(_("Generate Barcode"), _("Barcode generation functionality would be implemented here"))
    
    def show_reports(self):
        self.current_screen = self.show_reports
        self.clear_content()
        
        # Reports header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("Medical Reports"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text=_("Create Report"), 
                  command=self.create_report).pack(side=tk.RIGHT)
        
        # Reports table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create treeview
        columns = (_("ID"), _("Test Request"), _("Signed By"), _("Signed At"), _("Status"))
        self.reports_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.reports_tree.heading(col, text=col)
            self.reports_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.reports_tree.yview)
        self.reports_tree.configure(yscroll=scrollbar.set)
        
        self.reports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load reports data
        self.load_reports_data()
        
        # Add action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text=_("View Report"), 
                  command=self.view_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Sign Report"), 
                  command=self.sign_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Send Report"), 
                  command=self.send_report).pack(side=tk.LEFT, padx=5)
    
    def load_reports_data(self):
        # Clear existing data
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        
        # In a real app, this would load reports from database
        # For now, we'll show a message
        self.reports_tree.insert("", tk.END, values=(
            _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("No reports in database")
        ))
    
    def create_report(self):
        # Create report dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(_("Create Medical Report"))
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text=_("Test Request ID:")).pack(pady=5)
        request_entry = ttk.Entry(dialog, width=50)
        request_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Report Content:")).pack(pady=5)
        content_text = tk.Text(dialog, width=50, height=15)
        content_text.pack(pady=5)
        
        def save_report():
            request_id = request_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            
            # Validation
            if not request_id:
                messagebox.showerror(_("Error"), _("Please enter test request ID"))
                return
            
            if not content:
                messagebox.showerror(_("Error"), _("Please enter report content"))
                return
            
            # Create report
            report = MedicalReport(
                id=str(uuid.uuid4()),
                test_request_id=request_id,
                content=content,
                signed_by=self.current_user.id if self.current_user else "N/A",
                signed_at=datetime.now()
            )
            
            # In a real app, this would save to database
            messagebox.showinfo(_("Success"), _("Report created successfully"))
            dialog.destroy()
            self.load_reports_data()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=_("Save"), command=save_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Cancel"), 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        request_entry.focus()
    
    def view_report(self):
        messagebox.showinfo(_("View Report"), _("Report viewing functionality would be implemented here"))
    
    def sign_report(self):
        messagebox.showinfo(_("Sign Report"), _("Report signing functionality would be implemented here"))
    
    def send_report(self):
        messagebox.showinfo(_("Send Report"), _("Report sending functionality would be implemented here"))
    
    def show_billing(self):
        self.current_screen = self.show_billing
        self.clear_content()
        
        # Billing header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("Billing and Payments"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text=_("Create Invoice"), 
                  command=self.create_invoice).pack(side=tk.RIGHT)
        
        # Billing table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create treeview
        columns = (_("ID"), _("Patient"), _("Amount"), _("Paid"), _("Status"), _("Date"))
        self.billing_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.billing_tree.heading(col, text=col)
            self.billing_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.billing_tree.yview)
        self.billing_tree.configure(yscroll=scrollbar.set)
        
        self.billing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load billing data
        self.load_billing_data()
        
        # Add action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text=_("View Invoice"), 
                  command=self.view_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Process Payment"), 
                  command=self.process_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Generate Report"), 
                  command=self.generate_billing_report).pack(side=tk.LEFT, padx=5)
    
    def load_billing_data(self):
        # Clear existing data
        for item in self.billing_tree.get_children():
            self.billing_tree.delete(item)
        
        # In a real app, this would load billing data from database
        # For now, we'll show a message
        self.billing_tree.insert("", tk.END, values=(
            _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("N/A")
        ))
    
    def create_invoice(self):
        # Create invoice dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(_("Create Invoice"))
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text=_("Patient ID:")).pack(pady=5)
        patient_entry = ttk.Entry(dialog, width=40)
        patient_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Test Request IDs (comma separated):")).pack(pady=5)
        requests_entry = ttk.Entry(dialog, width=40)
        requests_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Total Amount:")).pack(pady=5)
        amount_entry = ttk.Entry(dialog, width=40)
        amount_entry.pack(pady=5)
        
        def save_invoice():
            patient_id = patient_entry.get().strip()
            requests_str = requests_entry.get().strip()
            amount_str = amount_entry.get().strip()
            
            # Validation
            if not patient_id:
                messagebox.showerror(_("Error"), _("Please enter patient ID"))
                return
            
            if not requests_str:
                messagebox.showerror(_("Error"), _("Please enter test request IDs"))
                return
            
            try:
                amount = float(amount_str)
                if amount < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(_("Error"), _("Please enter a valid amount"))
                return
            
            # Parse request IDs
            request_ids = [rid.strip() for rid in requests_str.split(",")]
            
            # Create invoice
            invoice = Invoice(
                id=str(uuid.uuid4()),
                patient_id=patient_id,
                test_request_ids=request_ids,
                total_amount=amount,
                paid_amount=0.0
            )
            
            # In a real app, this would save to database
            messagebox.showinfo(_("Success"), _("Invoice created successfully"))
            dialog.destroy()
            self.load_billing_data()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=_("Save"), command=save_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Cancel"), 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        patient_entry.focus()
    
    def view_invoice(self):
        messagebox.showinfo(_("View Invoice"), _("Invoice viewing functionality would be implemented here"))
    
    def process_payment(self):
        messagebox.showinfo(_("Process Payment"), _("Payment processing functionality would be implemented here"))
    
    def generate_billing_report(self):
        messagebox.showinfo(_("Generate Report"), _("Billing report generation functionality would be implemented here"))
    
    def show_inventory(self):
        self.current_screen = self.show_inventory
        self.clear_content()
        
        # Inventory header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("Inventory Management"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text=_("Add Item"), 
                  command=self.add_inventory_item).pack(side=tk.RIGHT)
        
        # Inventory table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create treeview
        columns = (_("ID"), _("Name"), _("Quantity"), _("Min Quantity"), _("Supplier"), _("Expiry Date"))
        self.inventory_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscroll=scrollbar.set)
        
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load inventory data
        self.load_inventory_data()
        
        # Add action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text=_("View Details"), 
                  command=self.view_inventory_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Update Quantity"), 
                  command=self.update_inventory_quantity).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Create Purchase Order"), 
                  command=self.create_purchase_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Low Stock Alert"), 
                  command=self.show_low_stock_alerts).pack(side=tk.LEFT, padx=5)
    
    def load_inventory_data(self):
        # Clear existing data
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # In a real app, this would load inventory items from database
        # For now, we'll show a message
        self.inventory_tree.insert("", tk.END, values=(
            _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("N/A")
        ))
    
    def add_inventory_item(self):
        # Create add inventory item dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(_("Add Inventory Item"))
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text=_("Item Name:")).pack(pady=5)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Description:")).pack(pady=5)
        desc_text = tk.Text(dialog, width=40, height=3)
        desc_text.pack(pady=5)
        
        ttk.Label(dialog, text=_("Quantity:")).pack(pady=5)
        quantity_entry = ttk.Entry(dialog, width=40)
        quantity_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Minimum Quantity:")).pack(pady=5)
        min_quantity_entry = ttk.Entry(dialog, width=40)
        min_quantity_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Supplier:")).pack(pady=5)
        supplier_entry = ttk.Entry(dialog, width=40)
        supplier_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Expiry Date (YYYY-MM-DD):")).pack(pady=5)
        expiry_entry = ttk.Entry(dialog, width=40)
        expiry_entry.pack(pady=5)
        
        def save_inventory_item():
            name = name_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            quantity_str = quantity_entry.get().strip()
            min_quantity_str = min_quantity_entry.get().strip()
            supplier = supplier_entry.get().strip()
            expiry_str = expiry_entry.get().strip()
            
            # Validation
            if not name:
                messagebox.showerror(_("Error"), _("Please enter item name"))
                return
            
            try:
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(_("Error"), _("Please enter a valid quantity"))
                return
            
            try:
                min_quantity = int(min_quantity_str)
                if min_quantity < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(_("Error"), _("Please enter a valid minimum quantity"))
                return
            
            # Parse expiry date if provided
            expiry_date = None
            if expiry_str:
                try:
                    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(_("Error"), _("Please enter a valid expiry date (YYYY-MM-DD)"))
                    return
            
            # Create inventory item
            item = InventoryItem(
                id=str(uuid.uuid4()),
                name=name,
                description=description,
                quantity=quantity,
                min_quantity=min_quantity,
                supplier=supplier,
                expiry_date=expiry_date
            )
            
            # In a real app, this would save to database
            messagebox.showinfo(_("Success"), _("Inventory item added successfully"))
            dialog.destroy()
            self.load_inventory_data()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=_("Save"), command=save_inventory_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Cancel"), 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        name_entry.focus()
    
    def view_inventory_item(self):
        messagebox.showinfo(_("View Item"), _("Inventory item details would be shown here"))
    
    def update_inventory_quantity(self):
        messagebox.showinfo(_("Update Quantity"), _("Inventory quantity update functionality would be implemented here"))
    
    def create_purchase_order(self):
        messagebox.showinfo(_("Purchase Order"), _("Purchase order creation functionality would be implemented here"))
    
    def show_low_stock_alerts(self):
        messagebox.showinfo(_("Low Stock Alerts"), _("Low stock alerts would be shown here"))
    
    def show_users(self):
        self.current_screen = self.show_users
        self.clear_content()
        
        # Users header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("User Management"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        ttk.Button(header_frame, text=_("Add User"), 
                  command=self.add_user).pack(side=tk.RIGHT)
        
        # Users table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Create treeview
        columns = (_("ID"), _("Username"), _("Email"), _("Role"), _("Active"), _("Last Login"))
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, 
                                 command=self.users_tree.yview)
        self.users_tree.configure(yscroll=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load users data
        self.load_users_data()
        
        # Add action buttons
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text=_("View Details"), 
                  command=self.view_user_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Edit User"), 
                  command=self.edit_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text=_("Disable User"), 
                  command=self.disable_user).pack(side=tk.LEFT, padx=5)
    
    def load_users_data(self):
        # Clear existing data
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # In a real app, this would load users from database
        # For now, we'll show a message
        self.users_tree.insert("", tk.END, values=(
            _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("N/A"), _("N/A")
        ))
    
    def add_user(self):
        # Create add user dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(_("Add User"))
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        ttk.Label(dialog, text=_("Username:")).pack(pady=5)
        username_entry = ttk.Entry(dialog, width=40)
        username_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Email:")).pack(pady=5)
        email_entry = ttk.Entry(dialog, width=40)
        email_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Password:")).pack(pady=5)
        password_entry = ttk.Entry(dialog, width=40, show="*")
        password_entry.pack(pady=5)
        
        ttk.Label(dialog, text=_("Role:")).pack(pady=5)
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(dialog, textvariable=role_var,
                                 values=[_("Admin"), _("Technician"), _("Doctor"), _("Receptionist")],
                                 state="readonly", width=37)
        role_combo.pack(pady=5)
        
        ttk.Label(dialog, text=_("Active:")).pack(pady=5)
        active_var = tk.BooleanVar(value=True)
        active_check = ttk.Checkbutton(dialog, variable=active_var)
        active_check.pack(pady=5)
        
        def save_user():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()
            role_text = role_var.get()
            is_active = active_var.get()
            
            # Validation
            if not username:
                messagebox.showerror(_("Error"), _("Please enter username"))
                return
            
            if not email:
                messagebox.showerror(_("Error"), _("Please enter email"))
                return
            
            if not password:
                messagebox.showerror(_("Error"), _("Please enter password"))
                return
            
            if not role_text:
                messagebox.showerror(_("Error"), _("Please select role"))
                return
            
            # Map role text to enum
            role_map = {
                _("Admin"): UserRole.ADMIN,
                _("Technician"): UserRole.TECHNICIAN,
                _("Doctor"): UserRole.DOCTOR,
                _("Receptionist"): UserRole.RECEPTIONIST
            }
            role = role_map.get(role_text, UserRole.RECEPTIONIST)
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Create user
            user = User(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                password_hash=password_hash,
                role=role,
                is_active=is_active
            )
            
            # In a real app, this would save to database
            messagebox.showinfo(_("Success"), _("User added successfully"))
            dialog.destroy()
            self.load_users_data()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text=_("Save"), command=save_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=_("Cancel"), 
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        username_entry.focus()
    
    def view_user_details(self):
        messagebox.showinfo(_("User Details"), _("User details would be shown here"))
    
    def edit_user(self):
        messagebox.showinfo(_("Edit User"), _("User editing functionality would be implemented here"))
    
    def disable_user(self):
        messagebox.showinfo(_("Disable User"), _("User disabling functionality would be implemented here"))
    
    def show_statistics(self):
        self.current_screen = self.show_statistics
        self.clear_content()
        
        # Statistics header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text=_("Reports and Statistics"), 
                 font=("Arial", 16)).pack(side=tk.LEFT)
        
        # Date range selector
        date_frame = ttk.Frame(header_frame)
        date_frame.pack(side=tk.RIGHT)
        
        ttk.Label(date_frame, text=_("From:")).pack(side=tk.LEFT)
        from_date_entry = ttk.Entry(date_frame, width=10)
        from_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(date_frame, text=_("To:")).pack(side=tk.LEFT)
        to_date_entry = ttk.Entry(date_frame, width=10)
        to_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(date_frame, text=_("Generate"), 
                  command=self.generate_statistics).pack(side=tk.LEFT, padx=5)
        
        # Statistics panels
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for different report types
        notebook = ttk.Notebook(stats_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Patient statistics tab
        patient_frame = ttk.Frame(notebook)
        notebook.add(patient_frame, text=_("Patient Statistics"))
        
        # Test statistics tab
        test_frame = ttk.Frame(notebook)
        notebook.add(test_frame, text=_("Test Statistics"))
        
        # Financial statistics tab
        financial_frame = ttk.Frame(notebook)
        notebook.add(financial_frame, text=_("Financial Statistics"))
        
        # Inventory statistics tab
        inventory_frame = ttk.Frame(notebook)
        notebook.add(inventory_frame, text=_("Inventory Statistics"))
        
        # Sample data for patient statistics
        ttk.Label(patient_frame, text=_("Total Patients: 125"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(patient_frame, text=_("New Patients (This Month): 15"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(patient_frame, text=_("Returning Patients: 85"), font=("Arial", 12)).pack(pady=5)
        
        # Sample data for test statistics
        ttk.Label(test_frame, text=_("Total Tests: 342"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(test_frame, text=_("Pending Tests: 24"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(test_frame, text=_("Completed Tests: 318"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(test_frame, text=_("Most Requested Test: Complete Blood Count"), font=("Arial", 12)).pack(pady=5)
        
        # Sample data for financial statistics
        ttk.Label(financial_frame, text=_("Total Revenue: $12,540"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(financial_frame, text=_("Outstanding Payments: $1,240"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(financial_frame, text=_("Average Test Price: $36.67"), font=("Arial", 12)).pack(pady=5)
        
        # Sample data for inventory statistics
        ttk.Label(inventory_frame, text=_("Total Inventory Items: 42"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(inventory_frame, text=_("Low Stock Items: 3"), font=("Arial", 12)).pack(pady=5)
        ttk.Label(inventory_frame, text=_("Expiring Soon: 2"), font=("Arial", 12)).pack(pady=5)
    
    def generate_statistics(self):
        messagebox.showinfo(_("Generate Statistics"), _("Statistics generation functionality would be implemented here"))
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = MedicalLabApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()