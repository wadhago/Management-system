"""
Data models for the Medical Laboratory Management System
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass, field

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class TestStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class SampleStatus(Enum):
    VALID = "Valid"
    DAMAGED = "Damaged"
    INSUFFICIENT = "Insufficient"

class UserRole(Enum):
    ADMIN = "Admin"
    TECHNICIAN = "Technician"
    DOCTOR = "Doctor"
    RECEPTIONIST = "Receptionist"

class PaymentMethod(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    BANK_TRANSFER = "Bank Transfer"

class Permission(Enum):
    # Patient permissions
    VIEW_PATIENTS = "View Patients"
    ADD_PATIENT = "Add Patient"
    EDIT_PATIENT = "Edit Patient"
    DELETE_PATIENT = "Delete Patient"
    
    # Test permissions
    VIEW_TESTS = "View Tests"
    ADD_TEST = "Add Test"
    EDIT_TEST = "Edit Test"
    DELETE_TEST = "Delete Test"
    
    # Sample permissions
    VIEW_SAMPLES = "View Samples"
    ADD_SAMPLE = "Add Sample"
    EDIT_SAMPLE = "Edit Sample"
    DELETE_SAMPLE = "Delete Sample"
    
    # Report permissions
    VIEW_REPORTS = "View Reports"
    ADD_REPORT = "Add Report"
    EDIT_REPORT = "Edit Report"
    DELETE_REPORT = "Delete Report"
    SIGN_REPORT = "Sign Report"
    
    # Billing permissions
    VIEW_BILLING = "View Billing"
    ADD_INVOICE = "Add Invoice"
    EDIT_INVOICE = "Edit Invoice"
    DELETE_INVOICE = "Delete Invoice"
    
    # Inventory permissions
    VIEW_INVENTORY = "View Inventory"
    ADD_INVENTORY = "Add Inventory"
    EDIT_INVENTORY = "Edit Inventory"
    DELETE_INVENTORY = "Delete Inventory"
    
    # User permissions
    VIEW_USERS = "View Users"
    ADD_USER = "Add User"
    EDIT_USER = "Edit User"
    DELETE_USER = "Delete User"
    
    # Statistics permissions
    VIEW_STATISTICS = "View Statistics"
    GENERATE_REPORTS = "Generate Reports"

@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: Gender
    contact_info: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class TestType:
    id: str
    name: str
    description: str
    price: float
    category: str  # Blood, Urine, Stool, Radiology, etc.
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class TestRequest:
    id: str
    patient_id: str
    test_type_id: str
    status: TestStatus
    requested_by: str  # Doctor ID
    requested_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

@dataclass
class Sample:
    id: str
    test_request_id: str
    barcode: str
    collected_at: datetime
    status: SampleStatus
    notes: Optional[str] = None

@dataclass
class MedicalReport:
    id: str
    test_request_id: str
    content: str
    signed_by: str  # Doctor ID
    signed_at: datetime
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Invoice:
    id: str
    patient_id: str
    test_request_ids: List[str]
    total_amount: float
    paid_amount: float
    payment_method: Optional[PaymentMethod] = None
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: Optional[datetime] = None

@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    role: UserRole
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    permissions: List[Permission] = field(default_factory=list)

@dataclass
class UserPermission:
    id: str
    user_id: str
    permission: Permission
    granted_at: datetime = field(default_factory=datetime.now)

@dataclass
class InventoryItem:
    id: str
    name: str
    description: str
    quantity: int
    min_quantity: int  # Alert threshold
    supplier: str
    expiry_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class PurchaseOrder:
    id: str
    item_id: str
    quantity: int
    supplier: str
    ordered_at: datetime = field(default_factory=datetime.now)
    received_at: Optional[datetime] = None
    status: str = "Ordered"  # Ordered, Received, Cancelled

@dataclass
class TestTemplate:
    id: str
    test_type_id: str
    template_content: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)