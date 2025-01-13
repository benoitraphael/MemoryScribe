import re
from datetime import datetime
from pathlib import Path
import json
import pickle
from typing import List, Dict, Optional

class Note:
    def __init__(self, date: datetime, sender: str, content: str):
        self.date = date
        self.sender = sender
        self.content = content

    def to_dict(self) -> dict:
        return {
            'date': self.date.isoformat(),
            'sender': self.sender,
            'content': self.content
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
        return cls(
            date=datetime.fromisoformat(data['date']),
            sender=data['sender'],
            content=data['content']
        )

class NoteCache:
    # Simplification du pattern pour ne chercher que le début des notes
    NOTE_PATTERN = r"# NOTE DE CONVERSATION DU ([^\n]+) PAR ([^\n]+)\n(.*?)(?=\n# NOTE DE CONVERSATION DU|\Z)"
    
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.notes: List[Note] = []
        self.last_modified: Optional[float] = None
        self.metadata: Dict = {
            'total_notes': 0,
            'authors': set(),
            'date_range': {'start': None, 'end': None}
        }

    def _get_cache_path(self, user_email: str) -> Path:
        """Retourne le chemin du fichier cache pour un utilisateur."""
        safe_email = user_email.replace('@', '_at_').replace('.', '_dot_')
        return self.cache_dir / f"{safe_email}_cache.pkl"

    def needs_update(self, memoire_path: Path) -> bool:
        """Vérifie si le cache doit être mis à jour."""
        if not memoire_path.exists():
            return False
        return self.last_modified != memoire_path.stat().st_mtime

    def parse_notes(self, content: str) -> List[Note]:
        """Parse le contenu du fichier mémoire pour extraire les notes."""
        notes = []
        matches = re.finditer(self.NOTE_PATTERN, content, re.DOTALL)
        print(f"DEBUG: Début du parsing des notes")
        
        for match in matches:
            date_str, sender, content = match.groups()
            print(f"DEBUG: Note trouvée - Date: {date_str}, Sender: {sender}")
            try:
                # On stocke simplement la date comme une chaîne pour l'instant
                date = datetime.now()  # Date par défaut
                notes.append(Note(date, sender.strip(), content.strip()))
                print(f"DEBUG: Note ajoutée avec succès")
            except Exception as e:
                print(f"DEBUG: Erreur lors du parsing de la note: {e}")
                continue

        print(f"DEBUG: Nombre total de notes parsées: {len(notes)}")
        return sorted(notes, key=lambda x: x.date, reverse=True)

    def update_from_file(self, memoire_path: Path) -> None:
        """Met à jour le cache à partir du fichier mémoire."""
        if not memoire_path.exists():
            return

        with open(memoire_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.notes = self.parse_notes(content)
        self.last_modified = memoire_path.stat().st_mtime
        
        # Mise à jour des métadonnées
        self.metadata['total_notes'] = len(self.notes)
        self.metadata['authors'] = {note.sender for note in self.notes}
        if self.notes:
            self.metadata['date_range'] = {
                'start': min(note.date for note in self.notes),
                'end': max(note.date for note in self.notes)
            }

    def save_cache(self, user_email: str) -> None:
        """Sauvegarde le cache sur le disque."""
        cache_path = self._get_cache_path(user_email)
        with open(cache_path, 'wb') as f:
            pickle.dump({
                'notes': [note.to_dict() for note in self.notes],
                'last_modified': self.last_modified,
                'metadata': self.metadata
            }, f)

    def load_cache(self, user_email: str) -> bool:
        """Charge le cache depuis le disque."""
        cache_path = self._get_cache_path(user_email)
        if not cache_path.exists():
            return False

        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
                self.notes = [Note.from_dict(note_dict) for note_dict in data['notes']]
                self.last_modified = data['last_modified']
                self.metadata = data['metadata']
            return True
        except Exception as e:
            print(f"Erreur lors du chargement du cache: {e}")
            return False

    def get_page(self, page: int, per_page: int = 20) -> tuple:
        """Retourne une page de notes et le nombre total de pages."""
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(self.notes) + per_page - 1) // per_page
        return self.notes[start:end], total_pages

    def search(self, query: str) -> List[Note]:
        """Recherche dans les notes."""
        query = query.lower()
        return [
            note for note in self.notes
            if query in note.content.lower() or
               query in note.sender.lower()
        ]

    def get_stats(self) -> Dict:
        """Retourne des statistiques sur les notes."""
        return {
            'total_notes': self.metadata['total_notes'],
            'authors': list(self.metadata['authors']),
            'date_range': self.metadata['date_range']
        }
