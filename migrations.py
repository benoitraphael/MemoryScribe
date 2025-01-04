from app import db, create_app
from app.models import User

def init_db():
    app = create_app()
    with app.app_context():
        # Supprime toutes les tables existantes
        db.drop_all()
        # Crée les tables avec le nouveau schéma
        db.create_all()
        print("Base de données réinitialisée avec succès!")

if __name__ == '__main__':
    init_db()
