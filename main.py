#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Concours de Belote
Application Windows complète en PyQt5
Version 2.0.0 - OPTIMISÉE
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont

# Ajouter le répertoire courant au chemin
sys.path.insert(0, str(Path(__file__).parent))

# Importer le logger avant tout
from utils.logger import logger

# Importer les styles
from ui.styles import AppStyles

# Importer la fenêtre principale
from ui.main_window import MainWindow

# Configuration
from config import APP_NAME, APP_VERSION


def show_splash_screen(app):
    """Affiche un écran de démarrage plein écran adaptatif"""
    from PyQt5.QtGui import QPainter, QColor, QPolygon
    from PyQt5.QtCore import QRect, QPoint
    from PyQt5.QtWidgets import QDesktopWidget

    # Adapter à l'écran
    screen = QDesktopWidget().screenGeometry()
    W = screen.width()
    H = screen.height()

    pixmap = QPixmap(W, H)
    pixmap.fill(QColor("#2c3e50"))

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Bandeaux dorés haut et bas
    bw = max(8, H // 80)
    painter.fillRect(0, 0, W, bw, QColor("#d4a017"))
    painter.fillRect(0, H - bw, W, bw, QColor("#d4a017"))

    # ── Deux grandes cartes ──
    # Les cartes occupent 55% de la hauteur
    CH = int(H * 0.52)
    CW = int(CH * 0.72)
    RAD = max(20, CW // 12)
    CX = W // 2
    card_top = int(H * 0.04)

    # Carte rouge (derrière, décalée droite)
    offset = int(CW * 0.25)
    painter.setBrush(QColor("#c0392b"))
    painter.setPen(QColor("#7b241c"))
    painter.drawRoundedRect(CX - CW//2 + offset, card_top + int(CH*0.05), CW, CH, RAD, RAD)
    # Coeur
    painter.setBrush(QColor("#ffffff"))
    painter.setPen(QColor("#ffffff"))
    hcx = CX + offset
    hy  = card_top + int(CH*0.05) + int(CH*0.20)
    hr  = int(CW * 0.18)
    painter.drawEllipse(hcx - int(hr*1.05), hy, int(hr*2), int(hr*2))
    painter.drawEllipse(hcx - int(hr*0.05), hy, int(hr*2), int(hr*2))
    heart = QPolygon([
        QPoint(hcx - int(hr*1.10), hy + int(hr*1.5)),
        QPoint(hcx + int(hr*1.10), hy + int(hr*1.5)),
        QPoint(hcx,                hy + int(hr*3.2)),
    ])
    painter.drawPolygon(heart)

    # Carte bleue (devant, décalée gauche)
    painter.setBrush(QColor("#1a5276"))
    painter.setPen(QColor("#0e3460"))
    painter.drawRoundedRect(CX - CW//2 - offset, card_top, CW, CH, RAD, RAD)
    # Pique
    painter.setBrush(QColor("#ffffff"))
    painter.setPen(QColor("#ffffff"))
    pcx = CX - offset
    py  = card_top + int(CH * 0.17)
    pr  = int(CW * 0.20)
    spade = QPolygon([
        QPoint(pcx,          py),
        QPoint(pcx - pr*2,   py + int(pr*2.8)),
        QPoint(pcx + pr*2,   py + int(pr*2.8)),
    ])
    painter.drawPolygon(spade)
    painter.drawEllipse(pcx - int(pr*1.1), py + int(pr*2.2), int(pr*1.2), int(pr*1.2))
    painter.drawEllipse(pcx - int(pr*0.1), py + int(pr*2.2), int(pr*1.2), int(pr*1.2))
    painter.fillRect(pcx - int(pr*0.22), py + int(pr*3.4), int(pr*0.44), int(pr*0.9), QColor("#ffffff"))

    # ── Titre ──
    title_y = int(H * 0.59)
    font_title = QFont("Segoe UI", max(40, W // 14), QFont.Bold)
    painter.setFont(font_title)
    painter.setPen(QColor("#ecf0f1"))
    painter.drawText(QRect(40, title_y, W - 80, int(H*0.13)), Qt.AlignCenter, "Belote Manager")

    # ── Sous-titre ──
    sub_y = int(H * 0.73)
    font_sub = QFont("Segoe UI", max(14, W // 55))
    painter.setFont(font_sub)
    painter.setPen(QColor("#bdc3c7"))
    painter.drawText(QRect(40, sub_y, W - 80, int(H*0.07)), Qt.AlignCenter,
                     "Gestionnaire de Concours de Belote")

    # ── Version ──
    ver_y = int(H * 0.80)
    font_ver = QFont("Segoe UI", max(12, W // 70))
    painter.setFont(font_ver)
    painter.setPen(QColor("#d4a017"))
    painter.drawText(QRect(40, ver_y, W - 80, int(H*0.06)), Qt.AlignCenter,
                     f"Version {APP_VERSION}")

    # ── Séparateur ──
    sep_y = int(H * 0.86)
    painter.setPen(QColor("#3d5166"))
    painter.drawLine(W//6, sep_y, W - W//6, sep_y)

    # ── Chargement ──
    font_load = QFont("Segoe UI", max(10, W // 90))
    painter.setFont(font_load)
    painter.setPen(QColor("#7f8c8d"))
    painter.drawText(QRect(40, sep_y + 10, W - 80, int(H*0.05)), Qt.AlignCenter,
                     "Chargement en cours\u2026")

    # ── Crédit ──
    credit_y = int(H * 0.91)
    font_credit = QFont("Segoe UI", max(10, W // 85), QFont.Bold)
    painter.setFont(font_credit)
    painter.setPen(QColor("#95a5a6"))
    painter.drawText(QRect(40, credit_y, W - 80, int(H*0.04)), Qt.AlignCenter,
                     "Cr\u00e9\u00e9 par Bayle Lo\u00efc")

    # ── Mentions légales ──
    legal_y = int(H * 0.955)
    font_legal = QFont("Segoe UI", max(8, W // 120))
    painter.setFont(font_legal)
    painter.setPen(QColor("#566573"))
    year = __import__("datetime").datetime.now().year
    painter.drawText(QRect(40, legal_y, W - 80, int(H*0.025)), Qt.AlignCenter,
        f"\u00a9 {year} Bayle Lo\u00efc  \u2014  Tous droits r\u00e9serv\u00e9s  "
        f"\u2014  Logiciel \u00e0 usage priv\u00e9  \u2014  Toute reproduction non autoris\u00e9e est interdite.")

    painter.end()

    splash = QSplashScreen(pixmap)
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    splash.move(screen.x(), screen.y())
    splash.show()
    app.processEvents()

    return splash

def main():
    """Point d'entrée principal de l'application"""
    try:
        logger.info("=" * 60)
        logger.info(f"Démarrage de {APP_NAME} v{APP_VERSION}")
        logger.info("=" * 60)
        
        # Créer l'application
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setApplicationVersion(APP_VERSION)
        
        # Appliquer le thème moderne
        logger.info("Application du thème moderne...")
        app.setStyleSheet(AppStyles.get_main_stylesheet())
        
        # Police par défaut
        app.setFont(QFont("Segoe UI", 10))
        
        # Afficher l'écran de démarrage
        logger.info("Affichage de l'écran de démarrage...")
        splash = show_splash_screen(app)
        
        # Simuler un chargement
        QTimer.singleShot(3500, splash.close)
        
        # Créer et afficher la fenêtre principale
        logger.info("Initialisation de la fenêtre principale...")
        window = MainWindow()
        
        # Fermer le splash et afficher la fenêtre
        def show_main_window():
            splash.finish(window)
            window.show()
            logger.info("Application démarrée avec succès")
        
        QTimer.singleShot(3500, show_main_window)
        
        # Lancer l'application
        exit_code = app.exec_()
        
        logger.info(f"Application fermée avec le code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.critical(f"Erreur fatale au démarrage: {e}", exc_info=True)
        
        # Afficher une boîte de dialogue d'erreur
        error_app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
        QMessageBox.critical(
            None,
            "Erreur fatale",
            f"Une erreur critique s'est produite au démarrage:\n\n{str(e)}\n\n"
            f"Consultez le fichier log pour plus de détails."
        )
        return 1


if __name__ == '__main__':
    sys.exit(main())