"""
Utility functions for the Medical Laboratory Management System
"""
import barcode
from barcode.writer import ImageWriter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
import os

def generate_barcode(data: str, filename: str = "barcode") -> str:
    """
    Generate a barcode image for the given data
    Returns the path to the generated barcode image
    """
    try:
        # Generate barcode
        code128 = barcode.get_barcode_class('code128')
        barcode_obj = code128(data, writer=ImageWriter())
        
        # Save barcode
        barcode_path = f"{filename}.png"
        barcode_obj.save(filename)
        
        return barcode_path
    except Exception as e:
        print(f"Error generating barcode: {e}")
        return None

def send_email(to_email: str, subject: str, body: str, 
               smtp_server: str = "smtp.gmail.com", 
               smtp_port: int = 587,
               username: str = None, 
               password: str = None) -> bool:
    """
    Send an email
    Returns True if successful, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Create server connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(username, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_encryption_key() -> bytes:
    """
    Generate a new encryption key
    """
    return Fernet.generate_key()

def encrypt_data(data: str, key: bytes) -> bytes:
    """
    Encrypt data using the provided key
    """
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
    """
    Decrypt data using the provided key
    """
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()