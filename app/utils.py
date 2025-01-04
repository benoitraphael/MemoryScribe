import os
from pathlib import Path

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
- Rédiger et améliorer du contenu
- Garder une trace de nos échanges importants

Modifiez ces instructions selon vos besoins !
""",

    'memoire.md': """# Mémoire des Conversations

Ce document contient les notes importantes de nos conversations.
Elles permettent à l'assistant de se souvenir de nos échanges précédents
et de mieux personnaliser ses réponses.

## Comment l'utiliser
1. Copiez les messages importants depuis le chat (bouton de copie)
2. Collez-les ici en les organisant par date
3. L'assistant utilisera ces informations dans vos prochaines conversations

---
# Vos notes apparaîtront ici
""",

    'essai.md': """# Livre en Cours de Rédaction

Ce document contient le texte en cours de rédaction, basé sur nos conversations.
L'assistant s'en servira comme référence pour maintenir la cohérence
dans la génération de contenu.

## Structure Suggérée
1. Introduction
2. Développement
3. Conclusion

---
Votre texte apparaîtra ici...
"""
}

def init_user_files(user_email):
    """Crée les fichiers nécessaires pour un nouvel utilisateur."""
    # Créer le dossier utilisateur
    user_dir = Path("instance/users") / user_email
    user_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer les fichiers avec leur contenu initial
    for filename, content in DEFAULT_FILES.items():
        file_path = user_dir / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
def get_user_files(user_email):
    """Récupère le contenu des fichiers d'un utilisateur."""
    user_dir = Path("instance/users") / user_email
    files = {}
    
    for filename in ["memoire.md", "essai.md", "prompt_systeme.md"]:
        file_path = user_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                files[filename] = f.read()
        else:
            files[filename] = ""
            
    return files

def save_user_file(user_email, file_type, content):
    """Sauvegarde le contenu d'un fichier utilisateur."""
    if file_type not in ["memoire.md", "essai.md", "prompt_systeme.md"]:
        raise ValueError("Type de fichier invalide")
        
    user_dir = Path("instance/users") / user_email
    file_path = user_dir / file_type
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True
