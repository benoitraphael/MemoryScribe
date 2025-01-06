import os
from dotenv import load_dotenv

# Charger les variables d'environnement
print("Loading environment variables...")
load_dotenv()

class Config:
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-à-changer'
    
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
    
    # Configuration du stockage des fichiers
    # En production (Render), utiliser /opt/render/project/src/
    # En local, utiliser le dossier instance/
    IS_PRODUCTION = os.environ.get('RENDER') is not None
    if IS_PRODUCTION:
        USER_DATA_PATH = '/opt/render/project/src/user_data'
    else:
        USER_DATA_PATH = os.path.join('instance', 'users')
