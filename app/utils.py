import os
from pathlib import Path
from flask import current_app

DEFAULT_FILES = {
    'prompt_systeme.md': """# Configuration de l'Assistant

## Instructions pour l'Assistant
Je suis votre assistant personnel. Voici comment je dois me comporter :

1. Ton et Style
- Soyez professionnel mais amical
- Adaptez votre langage à mon niveau
- Posez des questions si quelque chose n'est pas clair

2. Utilisation du Contexte
- Référez-vous à notre historique dans <memoire> pour personnaliser vos réponses
- Utilisez les informations de <essai> quand c'est pertinent
- Gardez une cohérence dans nos échanges

3. Objectifs
- M'aider à développer mes idées
- Proposer des suggestions pertinentes
- Maintenir une conversation constructive""",
    
    'memoire.md': """# Mémoire des Conversations

Ce document conserve les éléments importants de nos conversations.

## Points Clés
- [À venir]

## Préférences Notées
- [À venir]""",
    
    'essai.md': """# Espace de Travail

Ce document sert d'espace de travail pour développer vos idées.

## Notes et Idées
- [À venir]

## Développements
- [À venir]"""
}

def get_user_directory(user_email):
    """Retourne le chemin du répertoire de l'utilisateur."""
    base_path = current_app.config['USER_DATA_PATH']
    user_dir = os.path.join(base_path, user_email)
    return user_dir

def init_user_files(user_email):
    """Crée les fichiers nécessaires pour un nouvel utilisateur."""
    user_dir = get_user_directory(user_email)
    
    # Créer le répertoire utilisateur s'il n'existe pas
    os.makedirs(user_dir, exist_ok=True)
    
    # Créer les fichiers par défaut
    for filename, content in DEFAULT_FILES.items():
        file_path = os.path.join(user_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

def get_user_files(user_email):
    """Récupère le contenu des fichiers d'un utilisateur."""
    user_dir = get_user_directory(user_email)
    files_content = {}
    
    for filename in DEFAULT_FILES.keys():
        file_path = os.path.join(user_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                files_content[filename] = f.read()
        except FileNotFoundError:
            files_content[filename] = DEFAULT_FILES[filename]
    
    return files_content

def save_user_file(user_email, file_type, content):
    """Sauvegarde le contenu d'un fichier utilisateur."""
    user_dir = get_user_directory(user_email)
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs(user_dir, exist_ok=True)
    
    file_path = os.path.join(user_dir, file_type)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
