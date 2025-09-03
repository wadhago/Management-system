"""
Web version of the Medical Laboratory Management System
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_lab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models (simplified versions of the original models)
class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='RECEPTIONIST')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_info = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestType(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestRequest(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    test_type_id = db.Column(db.String(36), db.ForeignKey('test_type.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='PENDING')
    requested_by = db.Column(db.String(100), nullable=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_patients = Patient.query.count()
    pending_tests = TestRequest.query.filter_by(status='PENDING').count()
    
    return render_template('dashboard.html', 
                         total_patients=total_patients,
                         pending_tests=pending_tests)

@app.route('/patients')
@login_required
def patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@app.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        patient = Patient(
            id=str(uuid.uuid4()),
            name=request.form['name'],
            age=int(request.form['age']),
            gender=request.form['gender'],
            contact_info=request.form['contact_info']
        )
        
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully')
        return redirect(url_for('patients'))
    
    return render_template('add_patient.html')

@app.route('/tests')
@login_required
def tests():
    tests = TestType.query.all()
    return render_template('tests.html', tests=tests)

@app.route('/request_test/<patient_id>', methods=['GET', 'POST'])
@login_required
def request_test(patient_id):
    patient = Patient.query.get(patient_id)
    test_types = TestType.query.all()
    
    if request.method == 'POST':
        selected_tests = request.form.getlist('tests')
        
        for test_type_id in selected_tests:
            test_request = TestRequest(
                id=str(uuid.uuid4()),
                patient_id=patient_id,
                test_type_id=test_type_id,
                requested_by=current_user.username,
                status='PENDING'
            )
            db.session.add(test_request)
        
        db.session.commit()
        flash('Test requests submitted successfully')
        return redirect(url_for('patients'))
    
    return render_template('request_test.html', patient=patient, test_types=test_types)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                id=str(uuid.uuid4()),
                username='admin',
                email='admin@lab.com',
                password_hash=generate_password_hash('admin123'),
                role='ADMIN'
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True)