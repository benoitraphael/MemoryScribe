# MemoryScribe

MemoryScribe est un assistant conversationnel intelligent et introspectif avec mémoire, utilisant l'API Gemini de Google.

## Fonctionnalités

- 🔐 **Gestion des utilisateurs**
  - Création de compte (email/mot de passe)
  - Configuration de la clé API Gemini
  - Connexion/Déconnexion
  - Modification des informations de compte

- 💬 **Interface de chat**
  - Conversation en temps réel avec Gemini
  - Affichage alterné des messages
  - Bouton de copie sur chaque message
  - Animation de chargement pendant les réponses

- 📝 **Gestion des documents**
  - 3 documents par utilisateur en Markdown :
    1. Mémoire (stockage des conversations importantes)
    2. Synthèse (points clés de notre conversation)
    3. Prompt système (personnalisation de l'assistant)
  - Éditeur Markdown avec sauvegarde automatique

- 📚 **Blog de notes**
  - Affichage des notes de conversation dans un format blog
  - Nettoyage automatique du formatage HTML pour une meilleure lisibilité
  - Affichage chronologique des notes
  - Indication du nombre total de notes

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-username/MemoryScribe.git
cd MemoryScribe
```

2. Créez un environnement virtuel et installez les dépendances :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurez votre clé API Gemini dans votre profil après inscription

4. Lancez l'application :
```bash
python run.py
```

5. Ouvrez votre navigateur à l'adresse : http://localhost:5001

## Technologies utilisées

- 🐍 Python avec Flask
- 🎨 Bootstrap pour l'interface
- 🧠 API Gemini de Google
- 🗄️ PostgreSQL pour la base de données
- 🔒 Flask-Login pour l'authentification
- ✨ Jinja2 pour les templates
- 📝 Support Markdown pour le formatage
