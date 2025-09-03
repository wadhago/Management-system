"""
Database management for the Medical Laboratory Management System
"""
import sqlite3
import os
from typing import List, Optional
from datetime import datetime
import uuid
from models import (
    Patient, TestType, TestRequest, Sample, MedicalReport, 
    Invoice, User, InventoryItem, PurchaseOrder, TestTemplate, Gender, 
    TestStatus, SampleStatus, UserRole, PaymentMethod, Permission, UserPermission
)

class DatabaseManager:
    def __init__(self, db_path: str = "medical_lab.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_types (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_requests (
                id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                test_type_id TEXT NOT NULL,
                status TEXT NOT NULL,
                requested_by TEXT NOT NULL,
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (test_type_id) REFERENCES test_types (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS samples (
                id TEXT PRIMARY KEY,
                test_request_id TEXT NOT NULL,
                barcode TEXT UNIQUE NOT NULL,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (test_request_id) REFERENCES test_requests (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_reports (
                id TEXT PRIMARY KEY,
                test_request_id TEXT NOT NULL,
                content TEXT,
                signed_by TEXT NOT NULL,
                signed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (test_request_id) REFERENCES test_requests (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                total_amount REAL NOT NULL,
                paid_amount REAL DEFAULT 0,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid_at TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoice_test_requests (
                invoice_id TEXT NOT NULL,
                test_request_id TEXT NOT NULL,
                PRIMARY KEY (invoice_id, test_request_id),
                FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                FOREIGN KEY (test_request_id) REFERENCES test_requests (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_items (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                quantity INTEGER NOT NULL,
                min_quantity INTEGER NOT NULL,
                supplier TEXT,
                expiry_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id TEXT PRIMARY KEY,
                item_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                supplier TEXT NOT NULL,
                ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                received_at TIMESTAMP,
                status TEXT DEFAULT 'Ordered',
                FOREIGN KEY (item_id) REFERENCES inventory_items (id)
            )
        ''')
        
        # New table for test result templates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_templates (
                id TEXT PRIMARY KEY,
                test_type_id TEXT NOT NULL,
                template_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (test_type_id) REFERENCES test_types (id)
            )
        ''')
        
        # New table for user permissions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_permissions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                permission TEXT NOT NULL,
                granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()
    
    # Patient methods
    def create_patient(self, patient: Patient) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO patients (id, name, age, gender, contact_info, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient.id, patient.name, patient.age, patient.gender.value, 
                patient.contact_info, patient.created_at, patient.updated_at
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def generate_patient_id(self) -> str:
        """Generate a unique 8-digit patient ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        while True:
            # Generate a random 8-digit number
            import random
            patient_id = f"{random.randint(10000000, 99999999)}"
            
            # Check if this ID already exists
            cursor.execute('SELECT id FROM patients WHERE id = ?', (patient_id,))
            if not cursor.fetchone():
                conn.close()
                return patient_id
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Patient(
                id=row[0],
                name=row[1],
                age=row[2],
                gender=Gender(row[3]),
                contact_info=row[4],
                created_at=datetime.fromisoformat(row[5]),
                updated_at=datetime.fromisoformat(row[6])
            )
        return None
    
    def update_patient(self, patient: Patient) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE patients 
                SET name = ?, age = ?, gender = ?, contact_info = ?, updated_at = ?
                WHERE id = ?
            ''', (
                patient.name, patient.age, patient.gender.value, 
                patient.contact_info, patient.updated_at, patient.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_patient(self, patient_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def get_all_patients(self) -> List[Patient]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients')
        rows = cursor.fetchall()
        conn.close()
        
        patients = []
        for row in rows:
            patients.append(Patient(
                id=row[0],
                name=row[1],
                age=row[2],
                gender=Gender(row[3]),
                contact_info=row[4],
                created_at=datetime.fromisoformat(row[5]),
                updated_at=datetime.fromisoformat(row[6])
            ))
        return patients
    
    def get_patients_by_registration_date_range(self, start_date: datetime, end_date: datetime) -> List[Patient]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            WHERE created_at >= ? AND created_at <= ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        rows = cursor.fetchall()
        conn.close()
        
        patients = []
        for row in rows:
            patients.append(Patient(
                id=row[0],
                name=row[1],
                age=row[2],
                gender=Gender(row[3]),
                contact_info=row[4],
                created_at=datetime.fromisoformat(row[5]),
                updated_at=datetime.fromisoformat(row[6])
            ))
        return patients

    # Test Type methods
    def create_test_type(self, test_type: TestType) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO test_types (id, name, description, price, category, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                test_type.id, test_type.name, test_type.description, 
                test_type.price, test_type.category, test_type.created_at
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_test_types(self) -> List[TestType]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_types')
        rows = cursor.fetchall()
        conn.close()
        
        test_types = []
        for row in rows:
            test_types.append(TestType(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                category=row[4],
                created_at=datetime.fromisoformat(row[5])
            ))
        return test_types
    
    def get_test_type(self, test_type_id: str) -> Optional[TestType]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_types WHERE id = ?', (test_type_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return TestType(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                category=row[4],
                created_at=datetime.fromisoformat(row[5])
            )
        return None
    
    def update_test_type(self, test_type: TestType) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE test_types 
                SET name = ?, description = ?, price = ?, category = ?
                WHERE id = ?
            ''', (
                test_type.name, test_type.description, 
                test_type.price, test_type.category, test_type.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_test_type(self, test_type_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM test_types WHERE id = ?', (test_type_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def get_next_test_id(self) -> str:
        """Generate the next sequential three-digit test ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get the highest existing test ID from the test_types table
        cursor.execute('''
            SELECT id FROM test_types 
            WHERE id GLOB '[0-9][0-9][0-9]' 
            ORDER BY CAST(id AS INTEGER) DESC 
            LIMIT 1
        ''')
        row = cursor.fetchone()
        
        if row:
            # Extract the numeric part and increment
            current_id = int(row[0])
            next_id = current_id + 1
        else:
            # Start from 1 if no existing sequential IDs
            next_id = 1
        
        conn.close()
        
        # Format as three-digit number with leading zeros
        return f"{next_id:03d}"
    
    # Test Request methods
    def create_test_request(self, test_request: TestRequest) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO test_requests 
                (id, patient_id, test_type_id, status, requested_by, requested_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                test_request.id, test_request.patient_id, test_request.test_type_id,
                test_request.status.value, test_request.requested_by, 
                test_request.requested_at, test_request.completed_at
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_test_request(self, test_request_id: str) -> Optional[TestRequest]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_requests WHERE id = ?', (test_request_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return TestRequest(
                id=row[0],
                patient_id=row[1],
                test_type_id=row[2],
                status=TestStatus(row[3]),
                requested_by=row[4],
                requested_at=datetime.fromisoformat(row[5]),
                completed_at=datetime.fromisoformat(row[6]) if row[6] else None
            )
        return None
    
    def get_all_test_requests(self) -> List[TestRequest]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_requests')
        rows = cursor.fetchall()
        conn.close()
        
        test_requests = []
        for row in rows:
            test_requests.append(TestRequest(
                id=row[0],
                patient_id=row[1],
                test_type_id=row[2],
                status=TestStatus(row[3]),
                requested_by=row[4],
                requested_at=datetime.fromisoformat(row[5]),
                completed_at=datetime.fromisoformat(row[6]) if row[6] else None
            ))
        return test_requests
    
    def update_test_request_status(self, test_request_id: str, status: TestStatus) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        completed_at = datetime.now() if status == TestStatus.COMPLETED else None
        
        try:
            cursor.execute('''
                UPDATE test_requests 
                SET status = ?, completed_at = ?
                WHERE id = ?
            ''', (status.value, completed_at, test_request_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def update_test_request(self, test_request: TestRequest) -> bool:
        """Update all fields of a test request"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        completed_at = test_request.completed_at.isoformat() if test_request.completed_at else None
        
        try:
            cursor.execute('''
                UPDATE test_requests 
                SET patient_id = ?, test_type_id = ?, status = ?, requested_by = ?, 
                    requested_at = ?, completed_at = ?
                WHERE id = ?
            ''', (
                test_request.patient_id, test_request.test_type_id, test_request.status.value,
                test_request.requested_by, test_request.requested_at.isoformat(), completed_at,
                test_request.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    
    def get_test_requests_by_patient(self, patient_id: str) -> List[TestRequest]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_requests WHERE patient_id = ?', (patient_id,))
        rows = cursor.fetchall()
        conn.close()
        
        test_requests = []
        for row in rows:
            test_requests.append(TestRequest(
                id=row[0],
                patient_id=row[1],
                test_type_id=row[2],
                status=TestStatus(row[3]),
                requested_by=row[4],
                requested_at=datetime.fromisoformat(row[5]),
                completed_at=datetime.fromisoformat(row[6]) if row[6] else None
            ))
        return test_requests
    
    def get_test_requests_by_date_range(self, start_date: datetime, end_date: datetime) -> List[TestRequest]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM test_requests 
            WHERE requested_at >= ? AND requested_at <= ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        rows = cursor.fetchall()
        conn.close()
        
        test_requests = []
        for row in rows:
            test_requests.append(TestRequest(
                id=row[0],
                patient_id=row[1],
                test_type_id=row[2],
                status=TestStatus(row[3]),
                requested_by=row[4],
                requested_at=datetime.fromisoformat(row[5]),
                completed_at=datetime.fromisoformat(row[6]) if row[6] else None
            ))
        return test_requests

    def delete_test_request(self, test_request_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM test_requests WHERE id = ?', (test_request_id,))
            conn.commit()
            success = cursor.rowcount > 0
            return success
        except sqlite3.Error:
            return False
        finally:
            conn.close()
    
    # Sample methods
    def create_sample(self, sample: Sample) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO samples 
                (id, test_request_id, barcode, collected_at, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                sample.id, sample.test_request_id, sample.barcode,
                sample.collected_at, sample.status.value, sample.notes
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_sample(self, sample_id: str) -> Optional[Sample]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM samples WHERE id = ?', (sample_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Sample(
                id=row[0],
                test_request_id=row[1],
                barcode=row[2],
                collected_at=datetime.fromisoformat(row[3]),
                status=SampleStatus(row[4]),
                notes=row[5]
            )
        return None
    
    def get_sample_by_barcode(self, barcode: str) -> Optional[Sample]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM samples WHERE barcode = ?', (barcode,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Sample(
                id=row[0],
                test_request_id=row[1],
                barcode=row[2],
                collected_at=datetime.fromisoformat(row[3]),
                status=SampleStatus(row[4]),
                notes=row[5]
            )
        return None
    
    def get_all_samples(self) -> List[Sample]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM samples')
        rows = cursor.fetchall()
        conn.close()
        
        samples = []
        for row in rows:
            samples.append(Sample(
                id=row[0],
                test_request_id=row[1],
                barcode=row[2],
                collected_at=datetime.fromisoformat(row[3]),
                status=SampleStatus(row[4]),
                notes=row[5]
            ))
        return samples
    
    # Medical Report methods
    def create_medical_report(self, report: MedicalReport) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO medical_reports 
                (id, test_request_id, content, signed_by, signed_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                report.id, report.test_request_id, report.content,
                report.signed_by, report.signed_at, report.created_at
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_medical_report(self, report_id: str) -> Optional[MedicalReport]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM medical_reports WHERE id = ?', (report_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return MedicalReport(
                id=row[0],
                test_request_id=row[1],
                content=row[2],
                signed_by=row[3],
                signed_at=datetime.fromisoformat(row[4]),
                created_at=datetime.fromisoformat(row[5])
            )
        return None
    
    def get_medical_reports_by_test_request(self, test_request_id: str) -> List[MedicalReport]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM medical_reports WHERE test_request_id = ?', (test_request_id,))
        rows = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in rows:
            reports.append(MedicalReport(
                id=row[0],
                test_request_id=row[1],
                content=row[2],
                signed_by=row[3],
                signed_at=datetime.fromisoformat(row[4]),
                created_at=datetime.fromisoformat(row[5])
            ))
        return reports
    
    def get_all_medical_reports(self) -> List[MedicalReport]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM medical_reports')
        rows = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in rows:
            reports.append(MedicalReport(
                id=row[0],
                test_request_id=row[1],
                content=row[2],
                signed_by=row[3],
                signed_at=datetime.fromisoformat(row[4]),
                created_at=datetime.fromisoformat(row[5])
            ))
        return reports
    
    def update_medical_report(self, report: MedicalReport) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE medical_reports 
                SET content = ?, signed_by = ?, signed_at = ?
                WHERE id = ?
            ''', (
                report.content, report.signed_by, report.signed_at,
                report.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_medical_report(self, report_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM medical_reports WHERE id = ?', (report_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    # User methods
    def create_user(self, user: User) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (id, username, email, password_hash, role, is_active, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user.id, user.username, user.email, user.password_hash, 
                user.role.value, user.is_active, user.created_at, user.last_login
            ))
            conn.commit()
            
            # Save user permissions
            for permission in user.permissions:
                user_permission = UserPermission(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    permission=permission
                )
                self.create_user_permission(user_permission)
            
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user(self, user_id: str) -> Optional[User]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                role=UserRole(row[4]),
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]),
                last_login=datetime.fromisoformat(row[7]) if row[7] else None,
                permissions=[]  # Will be populated below
            )
            
            # Load user permissions
            user.permissions = [perm.permission for perm in self.get_user_permissions(user_id)]
            
            return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                role=UserRole(row[4]),
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]),
                last_login=datetime.fromisoformat(row[7]) if row[7] else None,
                permissions=[]  # Will be populated below
            )
            
            # Load user permissions
            user.permissions = [perm.permission for perm in self.get_user_permissions(user.id)]
            
            return user
        return None
    
    def authenticate_user(self, username: str, password_hash: str) -> Optional[User]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Update last login
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE username = ?
            ''', (username,))
            conn.commit()
            conn.close()
            
            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                role=UserRole(row[4]),
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]),
                last_login=datetime.fromisoformat(row[7]) if row[7] else None,
                permissions=[]  # Will be populated below
            )
            
            # Load user permissions
            user.permissions = [perm.permission for perm in self.get_user_permissions(user.id)]
            
            return user
        return None
    
    def update_user(self, user: User) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET username = ?, email = ?, role = ?, is_active = ?
                WHERE id = ?
            ''', (
                user.username, user.email, user.role.value, user.is_active, user.id
            ))
            
            # Update user permissions
            # First delete all existing permissions for this user
            self.delete_user_permissions(user.id)
            
            # Then add the new permissions
            for permission in user.permissions:
                user_permission = UserPermission(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    permission=permission
                )
                self.create_user_permission(user_permission)
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    # Inventory methods
    def create_inventory_item(self, item: InventoryItem) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO inventory_items 
                (id, name, description, quantity, min_quantity, supplier, expiry_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.id, item.name, item.description, item.quantity, 
                item.min_quantity, item.supplier, item.expiry_date, 
                item.created_at, item.updated_at
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_inventory_item(self, item_id: str) -> Optional[InventoryItem]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM inventory_items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return InventoryItem(
                id=row[0],
                name=row[1],
                description=row[2],
                quantity=row[3],
                min_quantity=row[4],
                supplier=row[5],
                expiry_date=datetime.fromisoformat(row[6]) if row[6] else None,
                created_at=datetime.fromisoformat(row[7]),
                updated_at=datetime.fromisoformat(row[8])
            )
        return None
    
    def get_all_inventory_items(self) -> List[InventoryItem]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM inventory_items')
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append(InventoryItem(
                id=row[0],
                name=row[1],
                description=row[2],
                quantity=row[3],
                min_quantity=row[4],
                supplier=row[5],
                expiry_date=datetime.fromisoformat(row[6]) if row[6] else None,
                created_at=datetime.fromisoformat(row[7]),
                updated_at=datetime.fromisoformat(row[8])
            ))
        return items
    
    def get_low_stock_items(self) -> List[InventoryItem]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM inventory_items 
            WHERE quantity <= min_quantity
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append(InventoryItem(
                id=row[0],
                name=row[1],
                description=row[2],
                quantity=row[3],
                min_quantity=row[4],
                supplier=row[5],
                expiry_date=datetime.fromisoformat(row[6]) if row[6] else None,
                created_at=datetime.fromisoformat(row[7]),
                updated_at=datetime.fromisoformat(row[8])
            ))
        return items
    
    def get_inventory_items_by_expiry_date_range(self, start_date: datetime, end_date: datetime) -> List[InventoryItem]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM inventory_items 
            WHERE expiry_date >= ? AND expiry_date <= ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append(InventoryItem(
                id=row[0],
                name=row[1],
                description=row[2],
                quantity=row[3],
                min_quantity=row[4],
                supplier=row[5],
                expiry_date=datetime.fromisoformat(row[6]) if row[6] else None,
                created_at=datetime.fromisoformat(row[7]),
                updated_at=datetime.fromisoformat(row[8])
            ))
        return items

    def update_inventory_quantity(self, item_id: str, quantity: int) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE inventory_items 
                SET quantity = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (quantity, item_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    # Test Template methods
    def create_test_template(self, template: TestTemplate) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO test_templates 
                (id, test_type_id, template_content, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                template.id, template.test_type_id, template.template_content,
                template.created_at, template.updated_at
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_test_template(self, template_id: str) -> Optional[TestTemplate]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_templates WHERE id = ?', (template_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return TestTemplate(
                id=row[0],
                test_type_id=row[1],
                template_content=row[2],
                created_at=datetime.fromisoformat(row[3]),
                updated_at=datetime.fromisoformat(row[4])
            )
        return None
    
    def get_test_template_by_test_type(self, test_type_id: str) -> Optional[TestTemplate]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_templates WHERE test_type_id = ?', (test_type_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return TestTemplate(
                id=row[0],
                test_type_id=row[1],
                template_content=row[2],
                created_at=datetime.fromisoformat(row[3]),
                updated_at=datetime.fromisoformat(row[4])
            )
        return None
    
    def get_all_test_templates(self) -> List[TestTemplate]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM test_templates')
        rows = cursor.fetchall()
        conn.close()
        
        templates = []
        for row in rows:
            templates.append(TestTemplate(
                id=row[0],
                test_type_id=row[1],
                template_content=row[2],
                created_at=datetime.fromisoformat(row[3]),
                updated_at=datetime.fromisoformat(row[4])
            ))
        return templates
    
    def update_test_template(self, template: TestTemplate) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE test_templates 
                SET template_content = ?, updated_at = ?
                WHERE id = ?
            ''', (
                template.template_content, template.updated_at, template.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_test_template(self, template_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM test_templates WHERE id = ?', (template_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    # User Permission methods
    def create_user_permission(self, user_permission: UserPermission) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_permissions 
                (id, user_id, permission, granted_at)
                VALUES (?, ?, ?, ?)
            ''', (
                user_permission.id, user_permission.user_id, user_permission.permission.value,
                user_permission.granted_at
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user_permissions(self, user_id: str) -> List[UserPermission]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_permissions WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        permissions = []
        for row in rows:
            permissions.append(UserPermission(
                id=row[0],
                user_id=row[1],
                permission=Permission(row[2]),
                granted_at=datetime.fromisoformat(row[3])
            ))
        return permissions
    
    def get_all_user_permissions(self) -> List[UserPermission]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_permissions')
        rows = cursor.fetchall()
        conn.close()
        
        permissions = []
        for row in rows:
            permissions.append(UserPermission(
                id=row[0],
                user_id=row[1],
                permission=Permission(row[2]),
                granted_at=datetime.fromisoformat(row[3])
            ))
        return permissions
    
    def get_all_invoices(self) -> List[Invoice]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM invoices')
        rows = cursor.fetchall()
        conn.close()
        
        invoices = []
        for row in rows:
            # Get associated test request IDs
            test_request_ids = []
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT test_request_id FROM invoice_test_requests WHERE invoice_id = ?', (row[0],))
            test_request_rows = cursor.fetchall()
            conn.close()
            
            for tr_row in test_request_rows:
                test_request_ids.append(tr_row[0])
            
            invoices.append(Invoice(
                id=row[0],
                patient_id=row[1],
                test_request_ids=test_request_ids,
                total_amount=row[2],
                paid_amount=row[3],
                payment_method=PaymentMethod(row[4]) if row[4] else None,
                created_at=datetime.fromisoformat(row[5]),
                paid_at=datetime.fromisoformat(row[6]) if row[6] else None
            ))
        return invoices
    
    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Get associated test request IDs
            test_request_ids = []
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT test_request_id FROM invoice_test_requests WHERE invoice_id = ?', (invoice_id,))
            test_request_rows = cursor.fetchall()
            conn.close()
            
            for tr_row in test_request_rows:
                test_request_ids.append(tr_row[0])
            
            return Invoice(
                id=row[0],
                patient_id=row[1],
                test_request_ids=test_request_ids,
                total_amount=row[2],
                paid_amount=row[3],
                payment_method=PaymentMethod(row[4]) if row[4] else None,
                created_at=datetime.fromisoformat(row[5]),
                paid_at=datetime.fromisoformat(row[6]) if row[6] else None
            )
        return None
    
    def get_invoices_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Invoice]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM invoices 
            WHERE created_at >= ? AND created_at <= ?
        ''', (start_date.isoformat(), end_date.isoformat()))
        rows = cursor.fetchall()
        conn.close()
        
        invoices = []
        for row in rows:
            # Get associated test request IDs
            test_request_ids = []
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT test_request_id FROM invoice_test_requests WHERE invoice_id = ?', (row[0],))
            test_request_rows = cursor.fetchall()
            conn.close()
            
            for tr_row in test_request_rows:
                test_request_ids.append(tr_row[0])
            
            invoices.append(Invoice(
                id=row[0],
                patient_id=row[1],
                test_request_ids=test_request_ids,
                total_amount=row[2],
                paid_amount=row[3],
                payment_method=PaymentMethod(row[4]) if row[4] else None,
                created_at=datetime.fromisoformat(row[5]),
                paid_at=datetime.fromisoformat(row[6]) if row[6] else None
            ))
        return invoices

    def delete_user_permission(self, permission_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM user_permissions WHERE id = ?', (permission_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def delete_user_permissions(self, user_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM user_permissions WHERE user_id = ?', (user_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    def update_user_password(self, user_id: str, new_password_hash: str) -> bool:
        """
        Update a user's password hash in the database.
        
        Args:
            user_id (str): The ID of the user to update
            new_password_hash (str): The new password hash
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET password_hash = ?
                WHERE id = ?
            ''', (new_password_hash, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False
        finally:
            conn.close()
