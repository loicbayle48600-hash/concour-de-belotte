#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer automatiquement tous les fichiers manquants
"""

from pathlib import Path

# Contenu des fichiers
FILES_CONTENT = {
    "utils/__init__.py": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module utilitaires"""
try:
    from .logger import logger, Logger
except ImportError:
    logger = None
    Logger = None
''',
    
    "ui/__init__.py": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module interface utilisateur"""
''',
}

def create_missing_files():
    """Crée tous les fichiers manquants"""
    
    # Créer les dossiers
    for folder in ["utils", "ui", "logs"]:
        Path(folder).mkdir(exist_ok=True)
        print(f"✓ Dossier '{folder}' créé/vérifié")
    
    # Créer les fichiers __init__.py
    for filepath, content in FILES_CONTENT.items():
        file_path = Path(filepath)
        if not file_path.exists():
            file_path.write_text(content, encoding='utf-8')
            print(f"✓ Fichier '{filepath}' créé")
        else:
            print(f"→ Fichier '{filepath}' existe déjà")
    
    print("\n✅ Tous les fichiers sont créés !")
    print("Vous pouvez maintenant lancer: python main.py")

if __name__ == "__main__":
    create_missing_files()