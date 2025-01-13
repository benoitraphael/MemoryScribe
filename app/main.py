from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import HiddenField
from .utils import get_user_files, save_user_file, get_user_directory
from . import db, csrf
from .note_cache import NoteCache
import os
from pathlib import Path

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("Erreur: Impossible d'importer google.generativeai")
    GEMINI_AVAILABLE = False

# Initialisation du cache
note_cache = NoteCache(os.path.join(os.path.dirname(__file__), 'cache'))

main = Blueprint('main', __name__)

class CSRFForm(FlaskForm):
    csrf_token = HiddenField()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    user_files = get_user_files(current_user.email)
    form = CSRFForm()
    return render_template('profile.html', files=user_files, form=form)

@main.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@main.route('/get_initial_context')
@login_required
def get_initial_context():
    try:
        user_files = get_user_files(current_user.email)
        context = {
            'prompt_systeme': user_files.get('prompt_systeme.md', ''),
            'memoire': user_files.get('memoire.md', ''),
            'essai': user_files.get('essai.md', '')
        }
        return jsonify({'success': True, 'context': context})
    except Exception as e:
        print(f"Erreur lors de la récupération du contexte: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/send_message', methods=['POST'])
@login_required
def send_message():
    try:
        print("\n=== RÉCEPTION D'UN MESSAGE ===")
        
        # Récupérer les données JSON
        data = request.get_json()
        message_content = data.get('message')
        history = data.get('history', [])
        
        if not message_content:
            return jsonify({
                "success": False,
                "error": "Message manquant"
            }), 400
        
        # Vérifier que l'utilisateur a une clé API configurée
        api_key = current_user.get_api_key()
        if not api_key:
            return jsonify({
                "success": False,
                "error": "Veuillez configurer votre clé API dans votre profil"
            }), 400
            
        print("Configuration de l'API Gemini")
        genai.configure(api_key=api_key)
        
        print("Création du modèle Gemini")
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Construire la conversation complète
        conversation = []
        
        # Ajouter l'historique des messages précédents
        print("\n=== AJOUT DE L'HISTORIQUE ===")
        for msg in history:
            conversation.append({
                "role": "user" if msg['sender'] == 'user' else "model",
                "parts": [{"text": msg['content']}]
            })
            
        # Ajouter le nouveau message
        conversation.append({
            "role": "user",
            "parts": [{"text": message_content}]
        })
        
        print("Envoi à Gemini")
        try:
            response = model.generate_content(
                contents=conversation,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    candidate_count=1,
                    max_output_tokens=8192
                )
            )
            
            # Récupérer la réponse
            assistant_response = response.text.strip()
            
            print("Réponse reçue de Gemini")
            return jsonify({
                "success": True,
                "response": assistant_response
            })
            
        except Exception as e:
            print(f"Erreur lors de l'appel à Gemini: {str(e)}")
            return jsonify({
                "success": False,
                "error": f"Erreur lors de l'appel à Gemini: {str(e)}"
            }), 500
            
    except Exception as e:
        print(f"Erreur lors du traitement du message: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@main.route('/append_to_memory', methods=['POST'])
@login_required
def append_to_memory():
    try:
        data = request.get_json()
        content = data.get('content')
        
        if not content:
            return jsonify({'success': False, 'error': 'Contenu manquant'}), 400
            
        # Récupérer le contenu actuel de memoire.md
        user_files = get_user_files(current_user.email)
        current_content = user_files.get('memoire.md', '')
        
        # Ajouter le nouveau contenu avec deux sauts de ligne pour la séparation
        new_content = current_content + ('\n\n' if current_content else '') + content
        
        # Sauvegarder le fichier mis à jour
        save_user_file(current_user.email, 'memoire.md', new_content)
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Erreur lors de l'ajout à la mémoire: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/save_file', methods=['POST'])
@login_required
@csrf.exempt
def save_file():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Données invalides"}), 400
            
        file_name = data.get('file_name')
        content = data.get('content')
        
        if not file_name or not content:
            return jsonify({"success": False, "error": "Nom de fichier ou contenu manquant"}), 400
        
        save_user_file(current_user.email, file_name, content)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@main.route('/save_api_key', methods=['POST'])
@login_required
def save_api_key():
    api_key = request.form.get('api_key')
    if not api_key:
        flash('La clé API ne peut pas être vide')
        return redirect(url_for('main.profile'))
    
    try:
        current_user.set_api_key(api_key)
        db.session.commit()
        flash('Clé API sauvegardée avec succès')
    except Exception as e:
        flash(f'Erreur lors de la sauvegarde de la clé API : {str(e)}')
    
    return redirect(url_for('main.profile'))

@main.route('/blog')
@main.route('/blog/page/<int:page>')
@login_required
def blog(page=1):
    print(f"DEBUG: Email de l'utilisateur: {current_user.email}")
    
    # Récupérer le chemin du fichier mémoire en utilisant get_user_directory
    user_dir = get_user_directory(current_user.email)
    memoire_path = os.path.join(user_dir, 'memoire.md')
    memoire_path = os.path.normpath(memoire_path)
    
    print(f"DEBUG: Chemin complet du fichier mémoire: {memoire_path}")
    print(f"DEBUG: Le fichier existe: {os.path.exists(memoire_path)}")
    
    if os.path.exists(memoire_path):
        with open(memoire_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"DEBUG: Contenu du fichier (premiers 200 caractères):\n{content[:200]}")
            print(f"DEBUG: Longueur totale du contenu: {len(content)} caractères")
    else:
        print(f"DEBUG: Le fichier n'existe pas!")
        # Lister le contenu du répertoire parent
        if os.path.exists(user_dir):
            print(f"DEBUG: Contenu du répertoire {user_dir}:")
            print(os.listdir(user_dir))
        else:
            print(f"DEBUG: Le répertoire utilisateur n'existe pas!")
    
    # Charger ou mettre à jour le cache si nécessaire
    cache_loaded = note_cache.load_cache(current_user.email)
    print(f"DEBUG: Cache chargé: {cache_loaded}")
    
    if not cache_loaded or note_cache.needs_update(Path(memoire_path)):
        print("DEBUG: Mise à jour du cache nécessaire")
        note_cache.update_from_file(Path(memoire_path))
        note_cache.save_cache(current_user.email)
    
    # Récupérer la page demandée
    notes, total_pages = note_cache.get_page(page)
    print(f"DEBUG: Nombre de notes trouvées: {len(notes) if notes else 0}")
    stats = note_cache.get_stats()
    print(f"DEBUG: Statistiques: {stats}")
    
    return render_template('blog.html', 
                         notes=notes,
                         page=page,
                         total_pages=total_pages,
                         stats=stats)
