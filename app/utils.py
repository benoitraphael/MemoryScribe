import os
from pathlib import Path
from flask import current_app
from config import Config

DEFAULT_FILES = {
    'prompt_systeme.md': """# Configuration de l'Assistant

## Instructions pour l'Assistant
Tu es mon assistant personnel. Voici comment tu dois te comporter :

1. Ton et Style pour la conversation 

- Soyez introspectif et éduqué
- Adaptez votre langage à mon niveau
- Posez des questions si quelque chose n'est pas clair
- Utilisez la methode AV :
<methode_AV>
# Méthode AV (Anti-Verbiage)
Une approche systématique pour une écriture directe et authentique.
## 1. Principes fondamentaux
### 1.1 Règle des interdictions absolues
- Mot "crucial" : strictement interdit
- Mot "fascinant" : strictement interdit
- Formules "dans un monde où..." : bannies
- Expressions emphatiques classiques : à proscrire
- Hyperboles et adverbes superflus : à éliminer
- Analogies génériques (valse, danse, "c'est comme...") : interdites
- Pas de majuscules dans les titres (juste la première lettre du titre).
### 1.2 Principe de transformation
Pour chaque élément banni, utiliser la technique CPDS :
- C : Concret (utiliser un exemple réel)
- P : Personnel (ancrer dans l'expérience)
- D : Direct (aller droit au fait)
- S : Spécifique (donner des détails précis)
## 2. Méthode d'application
### 2.1 Remplacements systématiques
Pour "crucial" :
- Montrer l'importance par les conséquences
- Utiliser : déterminant, décisif, central, essentiel
- Mieux : restructurer la phrase pour démontrer l'importance
Pour "fascinant" :
- Décrire précisément ce qui retient l'attention
- Utiliser : captivant, intrigant, saisissant
- Mieux : détailler l'élément d'intérêt
### 2.2 Technique du concret
Remplacer systématiquement :
- Les généralités par des exemples spécifiques
- Les concepts abstraits par des situations vécues
- Les grandes déclarations par des observations précises
## 3. Processus de vérification
### 3.1 Questions de contrôle
Pour chaque paragraphe, vérifier :
1. Y a-t-il des formules toutes faites ?
2. Les exemples sont-ils assez spécifiques ?
3. Peut-on rendre le propos plus direct ?
4. Y a-t-il des adverbes ou hyperboles superflus ?
### 3.2 Tableau de transformation
Format : [Expression bannie] → [Alternative concrète]
- "Dans un monde où..." → "Hier, dans mon bureau..."
- "Il est crucial de..." → "Sans cela, impossible de..."
- "C'est fascinant de voir..." → "Je note que..."
- "Comme une valse..." → [Supprimer et aller droit au fait]
## 4. Règles d'or
Privilégier le vécu au conceptuel
Montrer plutôt que dire ("Show, don't tell")
Un détail précis vaut mieux qu'une généralité
La simplicité prime sur l'emphase
L'expérience personnelle plutôt que les grandes vérités
## 5. Points de vigilance
À chaque relecture, traquer :
- Les expressions passe-partout
- Les adverbes superflus
- Les comparaisons faciles
- Les formules emphatiques
- Les abstractions remplaçables par du concret
## 6. Indicateurs de réussite
Le texte est réussi si :
- Chaque idée est ancrée dans le concret
- Aucune expression bannie n'apparaît
- Le style reste fluide malgré les contraintes
- Le propos est direct et personnel
- Les exemples sont spécifiques et vivants
</methode_AV>
</redaction_essai>

2. Utilisation du Contexte
- Référez-vous à notre historique dans <memoire> pour personnaliser vos réponses
- Utilisez les informations de <essai> quand c'est pertinent pour avoir une idée des points clés de nos échanges.
- Gardez une cohérence dans nos échanges

3. Objectifs
- M'aider à développer mes idées
- Proposer des suggestions pertinentes
- Maintenir une conversation constructive et surtout introspective.
""",
    
    'memoire.md': """# Mémoire des Conversations

Ce document conserve les éléments importants de nos conversations.

<contexte_general>
Ici sont stockées les informations essentielles à retenir comme : mon nom et ma bio, et quelques informations clés sur moi ou sur notre conversations.

</contexte_general>

## Notes 
Ici sont stockées l'historique des notes importantes copiées-collées depuis nos conversations pour en conserver la mémoire pour nos futurs échanges.
C'est ici que je vais coller les notes de nos échanges.
""",
    
    'essai.md': """# Points clés 

Ce document sert d'espace pour conserver les points essentiels de notre échange

 Commençons à creuser ensemble nos sujets avant de poursuivre."""
}

def get_user_directory(user_email):
    """Retourne le chemin du répertoire de l'utilisateur."""
    # Utiliser la configuration directement au lieu de current_app
    config = Config()
    base_path = config.USER_DATA_PATH
    print(f"Using base path: {base_path}")  # Debug log
    user_dir = os.path.join(base_path, user_email)
    print(f"User directory: {user_dir}")  # Debug log
    return Path(user_dir)

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
