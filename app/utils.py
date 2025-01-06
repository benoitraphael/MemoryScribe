import os
from pathlib import Path
from flask import current_app
from config import Config

DEFAULT_FILES = {
    'prompt_systeme.md': """# Configuration de l'Assistant

## Instructions pour l'Assistant
Tu es mon assistant personnel. Voici comment tu dois te comporter :

1. Ton et Style
- Soyez professionnel mais amical
- Adaptez votre langage à mon niveau
- Posez des questions si quelque chose n'est pas clair

2. Utilisation du Contexte
- Référez-vous à notre historique dans <memoire> pour personnaliser vos réponses
- Utilisez les informations de <essai> quand c'est pertinent pour avoir une idée de l'état de l'avancée de notre livre.
- Gardez une cohérence dans nos échanges

3. Objectifs
- M'aider à développer mes idées
- Proposer des suggestions pertinentes
- Maintenir une conversation constructive""",
    
    'memoire.md': """# Mémoire des Conversations

Ce document conserve les éléments importants de nos conversations.

<contexte_general>
Ici sont stockées les informations essentielles à retenir comme : mon nom et ma bio, et quelques informations clés sur moi ou sur notre conversations.

</contexte_general>

<notes>
Ici sont stockées l'historique des notes importantes copiées-collées depuis nos conversations pour en conserver la mémoire pour nos futurs échanges.
C'est ici que je vais coller les notes de nos échanges.

</notes>""",
    
    'essai.md': """# Écriture de notre livre

Ce document sert d'espace pour conserver la rédaction de notre livre

## État de l'écriture

Pour l'instant, rien n'a été écrit ! Commençons à creuser ensemble nos sujets avant de commencer l'écriture."""
}

def get_user_directory(user_email):
    """Retourne le chemin du répertoire de l'utilisateur."""
    # Utiliser la configuration directement au lieu de current_app
    config = Config()
    base_path = config.USER_DATA_PATH
    print(f"Using base path: {base_path}")  # Debug log
    user_dir = os.path.join(base_path, user_email)
    print(f"User directory: {user_dir}")  # Debug log
    return user_dir

def init_user_files(user_email):
    """Crée les fichiers nécessaires pour un nouvel utilisateur."""
    user_dir = get_user_directory(user_email)
    print(f"Creating user directory: {user_dir}")  # Debug log
    
    # Créer le répertoire utilisateur s'il n'existe pas
    os.makedirs(user_dir, exist_ok=True)
    
    # Créer les fichiers par défaut
    for filename, content in DEFAULT_FILES.items():
        file_path = os.path.join(user_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                print(f"Created file: {file_path}")  # Debug log

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
