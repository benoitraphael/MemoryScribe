from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os
from base64 import b64encode, b64decode
from pathlib import Path
from datetime import datetime

# Clé de chiffrement pour les clés API
def get_or_create_key():
    # En production, utiliser la variable d'environnement
    env_key = os.getenv('ENCRYPTION_KEY')
    if env_key:
        return env_key.encode()
        
    # En développement, utiliser un fichier
    key_file = Path('instance/encryption.key')
    if key_file.exists():
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        key_file.parent.mkdir(parents=True, exist_ok=True)
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

ENCRYPTION_KEY = get_or_create_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))  
    api_key_encrypted = db.Column(db.String(512))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_api_key(self, api_key):
        if api_key:
            encrypted_data = cipher_suite.encrypt(api_key.encode())
            self.api_key_encrypted = b64encode(encrypted_data).decode()
        else:
            self.api_key_encrypted = None
            
    def get_api_key(self):
        if self.api_key_encrypted:
            try:
                encrypted_data = b64decode(self.api_key_encrypted)
                return cipher_suite.decrypt(encrypted_data).decode()
            except:
                return None
        return None
        
    def __repr__(self):
        return f'<User {self.email}>'
