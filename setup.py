#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création automatique du projet BeloteManager
Lance ce script pour créer toute la structure complète
"""

import os
import sys
from pathlib import Path

def create_structure():
    """Crée toute la structure du projet"""
    
    # Dossier racine
    base_dir = Path("BeloteManager")
    base_dir.mkdir(exist_ok=True)
    
    # Créer les sous-dossiers
    folders = [
        "models",
        "database", 
        "utils",
        "ui",
        "backups"
    ]
    
    for folder in folders:
        (base_dir / folder).mkdir(exist_ok=True)
    
    print(f"✓ Dossiers créés dans {base_dir}")
    
    # Fichiers à créer
    files = {
        "config.py": '''# Configuration générale - Gestionnaire de Concours de Belote
import os
from pathlib import Path
from enum import Enum

# Chemins
APP_NAME = "Gestionnaire de Concours de Belote"
APP_VERSION = "2.0.0"
BASE_DIR = Path(__file__).resolve().parent

# Base de données
DB_FILE = BASE_DIR / "concours_belote.db"
SAVE_FILE = BASE_DIR / "concours_belote.json"
BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

# Points
POINTS_PER_GAME = 162
GAMES_PER_ROUND = 12
TOTAL_POINTS = POINTS_PER_GAME * GAMES_PER_ROUND  # 1944 points

# Types d'équipes
TEAM_TYPES = {
    'mixte': 'Mixte',
    'femmes': 'Femmes',
    'hommes': 'Hommes'
}

# Règles spéciales belote
BELOTE_RULES = {
    'belote': 20,
    'rebelote': 20,
    'carré_valet': 200,
    'carré_dame': 200,
    'carré_roi': 200,
    'carré_as': 200,
    'tierce': 20,
    'quarte': 50,
    'quinte': 100,
    'sixième': 150,
    'septième': 200,
    'huitième': 250
}

# Sauvegarde automatique
AUTOSAVE_INTERVAL_MS = 60000  # 1 minute

# Interface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PROJECTOR_WIDTH = 1920
PROJECTOR_HEIGHT = 1080

# Couleurs
COLOR_PRIMARY = "#2c3e50"
COLOR_SECONDARY = "#3498db"
COLOR_SUCCESS = "#27ae60"
COLOR_WARNING = "#e74c3c"
COLOR_LIGHT = "#ecf0f1"
COLOR_DARK = "#2c3e50"
COLOR_LOCKED = "#95a5a6"

# Polices
FONT_SIZE_NORMAL = 11
FONT_SIZE_LARGE = 14
FONT_SIZE_TITLE = 18
FONT_SIZE_PROJECTOR = 48
FONT_SIZE_PROJECTOR_LARGE = 56
''',
        
        "requirements.txt": '''PyQt5==5.15.9
reportlab==4.0.9
Pillow==10.0.0
''',
        
        "install.bat": '''@echo off
chcp 65001 >nul
echo Installation des dependances...
echo.
pip install -r requirements.txt
echo.
echo Installation terminée!
pause
''',
        
        "run.bat": '''@echo off
chcp 65001 >nul
cd /d %~dp0
python main.py
pause
''',
    }
    
    # Créer les fichiers
    for filename, content in files.items():
        filepath = base_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {filename}")
    
    print("\n✓ Tous les fichiers de configuration créés!")
    print("\nPour créer les autres fichiers Python, utilise le ZIP complet.")
    print(f"\nLe dossier {base_dir} a été créé!")

if __name__ == '__main__':
    try:
        create_structure()
        print("\n✓ Succès! Dossier BeloteManager créé.")
    except Exception as e:
        print(f"✗ Erreur: {e}")
        sys.exit(1)