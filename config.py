#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration de l'application
"""

from pathlib import Path

# Informations de l'application
APP_NAME = "Gestionnaire de Concours de Belote"
APP_VERSION = "2.0.0"

# Chemins
BASE_DIR = Path(__file__).parent
SAVE_FILE = BASE_DIR / "data" / "competition.json"
BACKUP_DIR = BASE_DIR / "data" / "backups"

# Configuration des points
TOTAL_POINTS = 162  # Points totaux par donne

# Règles de la belote
BELOTE_RULES = {
    'belote_rebelote': 20,
    'carre': 100,
    'suite': 50,
    'capot': 90,  # Bonus capot (tous les plis)
    'litige': 0    # Points en cas de litige
}

# Valeurs des cartes à l'atout
CARD_VALUES_ATOUT = {
    'Valet': 20,
    'Neuf': 14,
    'As': 11,
    'Dix': 10,
    'Roi': 4,
    'Dame': 3,
    'Huit': 0,
    'Sept': 0
}

# Valeurs des cartes sans atout
CARD_VALUES_SANS_ATOUT = {
    'As': 11,
    'Dix': 10,
    'Roi': 4,
    'Dame': 3,
    'Valet': 2,
    'Neuf': 0,
    'Huit': 0,
    'Sept': 0
}

# Règles configurables
BELOTE_GAME_RULES = {
    'titre': 'Règles de la Belote',
    'sections': [
        {
            'titre': '🎯 Valeur des cartes À L\'ATOUT',
            'contenu': [
                'Valet : 20 points',
                'Neuf : 14 points',
                'As : 11 points',
                'Dix : 10 points',
                'Roi : 4 points',
                'Dame : 3 points',
                'Huit et Sept : 0 point'
            ]
        },
        {
            'titre': '🃏 Valeur des cartes SANS ATOUT',
            'contenu': [
                'As : 11 points',
                'Dix : 10 points',
                'Roi : 4 points',
                'Dame : 3 points',
                'Valet : 2 points',
                'Neuf, Huit, Sept : 0 point'
            ]
        },
        {
            'titre': '⭐ Points bonus',
            'contenu': [
                'Belote/Rebelote : 20 points',
                'Carré de Valets : 200 points',
                'Carré de Neuf : 150 points',
                'Carré d\'As, Dix, Roi, Dame : 100 points',
                'Suite de 5 cartes : 100 points',
                'Suite de 4 cartes : 50 points',
                'Suite de 3 cartes : 20 points',
                'Capot (tous les plis) : 90 points bonus'
            ]
        },
        {
            'titre': '📏 Règles importantes',
            'contenu': [
                '• Total par donne : 162 points',
                '• On ne pisse pas à l\'atout',
                '• Obligation de monter sur l\'atout du partenaire',
                '• Obligation de couper si on ne peut fournir',
                '• La belote annule le capot',
                '• En cas de litige : 81 points partout'
            ]
        },
        {
            'titre': '🎲 Comptage des points',
            'contenu': [
                '• Le dernier pli vaut 10 points (dix de der)',
                '• L\'équipe qui fait les 8 plis : capot (162 + 90 = 252 points)',
                '• Si une équipe ne fait pas son contrat : l\'adversaire marque tous les points'
            ]
        }
    ]
}

# Configuration de l'auto-sauvegarde
AUTO_SAVE_INTERVAL = 30  # secondes (modifié de 60 à 30 pour plus de sécurité)

# Configuration des exports
EXPORT_DIR = BASE_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)