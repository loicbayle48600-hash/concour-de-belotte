# 🧑‍🍳 HACCP Cuisine — Registre d'hygiène pour tablette Android

Application de gestion HACCP conçue pour être utilisée sur une **tablette Android**, directement en cuisine.
C'est une **application web progressive (PWA)** : elle s'installe comme une vraie application (icône sur
l'écran d'accueil, plein écran) et fonctionne **100 % hors-ligne** — aucune connexion internet n'est
nécessaire au quotidien. Toutes les données restent stockées **sur la tablette**.

## ✨ Fonctionnalités

| Module | Description |
|---|---|
| 🏠 **Accueil** | Tableau de bord du jour : alertes (relevés manquants, nettoyages à faire, DLC imminentes, non-conformités ouvertes) |
| 🌡️ **Températures** | Relevés des frigos/congélateurs avec contrôle automatique de conformité et action corrective obligatoire |
| 📦 **Réception** | Contrôle des livraisons (fournisseur, température, état) avec photo du bon de livraison |
| 🏷️ **Traçabilité** | Enregistrement des étiquettes produits avec **photo via la caméra de la tablette**, n° de lot et DLC |
| 🧽 **Nettoyage** | Plan de nettoyage (quotidien / hebdomadaire / mensuel) avec validation par employé |
| 🍟 **Huiles de friture** | Suivi des contrôles, filtrations et changements d'huile |
| ❄️ **Refroidissement** | Suivi du refroidissement rapide (63 °C → 10 °C en moins de 2 h) avec calcul automatique |
| ⚠️ **Non-conformités** | Créées automatiquement en cas d'anomalie + déclaration manuelle, suivi jusqu'à clôture |
| 📊 **Historique** | Consultation par module et période, **export CSV** (Excel) et **impression / PDF** |
| ⚙️ **Paramètres** | Établissement, employés, équipements froids, zones de nettoyage, friteuses, **sauvegarde / restauration** |

## 📲 Installation sur la tablette Android

L'application doit être ouverte une première fois depuis une adresse web (HTTPS). Le plus simple :
**GitHub Pages** (gratuit).

### 1. Activer GitHub Pages (une seule fois, depuis un ordinateur)

1. Ouvrez le dépôt sur GitHub → **Settings** → **Pages**.
2. Dans « Build and deployment », choisissez **Deploy from a branch**.
3. Sélectionnez la branche `main` et le dossier `/ (root)`, puis **Save**.
4. Après 1 à 2 minutes, l'application est disponible à l'adresse :
   `https://<votre-compte>.github.io/<nom-du-depot>/haccp-app/`

### 2. Installer sur la tablette

1. Sur la tablette, ouvrez **Chrome** et allez à l'adresse ci-dessus.
2. Menu ⋮ (en haut à droite) → **« Ajouter à l'écran d'accueil »** (ou « Installer l'application »).
3. Validez : l'icône ✅ HACCP apparaît sur l'écran d'accueil.
4. Ouvrez l'application depuis cette icône : elle se lance en plein écran et
   **fonctionne ensuite sans internet**.

### 3. Premier démarrage

1. Allez dans **⚙️ Paramètres**.
2. Renseignez le nom de l'établissement, vos employés, vos frigos/congélateurs
   (avec leurs températures min/max), vos zones de nettoyage et vos friteuses.
3. C'est prêt ! Les alertes du tableau de bord se mettent à jour automatiquement.

## 💾 Sauvegarde des données

Les données sont stockées uniquement sur la tablette (IndexedDB). Pensez à faire régulièrement
**Paramètres → Exporter toutes les données** : un fichier `sauvegarde_haccp_<date>.json` est téléchargé,
à conserver (Drive, e-mail, clé USB). Il peut être restauré à tout moment, y compris sur une autre tablette.

> ⚠️ Réglementation : les enregistrements HACCP doivent être conservés (généralement 6 mois à 1 an minimum
> selon les documents). Utilisez l'export CSV/PDF mensuel pour archiver.

## 🖥️ Utilisation sans GitHub Pages (avancé)

Sur un réseau local, n'importe quel petit serveur web fait l'affaire, par exemple :

```bash
cd haccp-app
python3 -m http.server 8080
```

puis ouvrez `http://<ip-du-pc>:8080` sur la tablette. (Le mode hors-ligne complet — service worker —
nécessite HTTPS ou localhost, mais l'application reste utilisable tant que la page est ouverte.)

## 🔧 Technique

- Une seule page `index.html` (HTML/CSS/JavaScript, sans dépendance externe).
- Données : IndexedDB (`records` + `settings`), demande de stockage persistant à Android.
- Photos : capturées via `<input capture="environment">`, recompressées en JPEG (max 900 px).
- Hors-ligne : service worker (`sw.js`) avec pré-cache de l'application.
- Interface optimisée tablette : cibles tactiles ≥ 48 px, mode portrait et paysage.
