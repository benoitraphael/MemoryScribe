import os
from dotenv import load_dotenv

# Charger les variables d'environnement
print("Loading environment variables...")
load_dotenv()

class Config:
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-à-changer'
    
    # Configuration CSRF
    WTF_CSRF_CHECK_DEFAULT = False  # Désactive la vérification CSRF par défaut
    
    # Configuration Base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'
    
    # Debug: afficher l'URL de la base de données et les variables d'environnement
    print(f"Environment variables:")
    print(f"DATABASE_URL = {os.environ.get('DATABASE_URL')}")
    print(f"Using database: {SQLALCHEMY_DATABASE_URI}")
    
    # Si l'URL commence par postgres://, la convertir en postgresql://
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration API
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    # Configuration du stockage des fichiers utilisateurs
    IS_PRODUCTION = os.environ.get('RENDER') is not None
    USER_DATA_PATH = '/app/instance/users' if IS_PRODUCTION else 'instance/users'
    print(f"User data path: {USER_DATA_PATH}")
