from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from os import path

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    # Création de l'application Flask
    app = Flask(__name__)
    
    # Configuration de base
    app.config['SECRET_KEY'] = 'votre_clé_secrète_temporaire'  # À changer en production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['WTF_CSRF_ENABLED'] = False  # Désactive CSRF temporairement
    
    # Initialisation des extensions avec l'app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)  # Initialise CSRF même s'il est désactivé
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
    
    return app
