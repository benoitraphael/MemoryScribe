from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from os import path
from config import Config
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
print("Loading environment variables...")

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    # Chargement des variables d'environnement
    load_dotenv()
    print("Loading environment variables...")
    
    # Création de l'application Flask
    app = Flask(__name__)
    
    # Chargement de la configuration depuis config.py
    app.config.from_object(Config)
    
    # Configuration de la base de données
    database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/memoryline')
    print("Environment variables:")
    print(f"DATABASE_URL = {database_url}")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    
    # Chemin pour les données utilisateur
    user_data_path = os.getenv('USER_DATA_PATH', 'instance/users')
    print(f"User data path: {user_data_path}")
    app.config['USER_DATA_PATH'] = user_data_path
    
    # Initialisation des extensions avec l'app
    db.init_app(app)
    migrate = Migrate(app, db)  # Création de l'instance Migrate ici
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import et enregistrement des blueprints
    from .auth import auth
    from .main import main
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    
    # Configuration du login manager
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Création de la base de données si elle n'existe pas
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")  # Log pour debug
        
        # Initialisation de la base de données
        print("Using database:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    return app

# Création de l'instance de l'application
app = create_app()
