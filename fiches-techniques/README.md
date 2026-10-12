# Fiches techniques – menu annuel 2026 EHPAD / FAM

**Fichier principal : `Fiches_techniques_menu_2026.xlsx`** (282 feuilles).

## Contenu du classeur
| Feuille | Rôle |
|---|---|
| `Sommaire` | Liste des 279 fiches (catégorie, mode de cuisson, nombre de passages au menu 2026), liens cliquables vers chaque fiche, filtres. |
| `Menu → fiches` | Les 53 semaines du menu, jour par jour et service par service (midi / soir), avec pour chaque entrée, plat, garniture et dessert la fiche correspondante (lien cliquable). |
| `T° cuisson de nuit` | Copie du tableau de températures du chef (cuissons longues 12 h – 18 h). |
| `E-…` (83) | Fiches entrées. |
| `P-…` (122) | Fiches plats. |
| `G-…` (59) | Fiches garnitures. |
| `D-…` (10) | Fiches desserts. |
| `X-…` (5) | Fiches originales du chef non présentes au menu (joue de bœuf, haricots rouges, chili viande à part, coco catalans, pois chiches) conservées telles quelles. |

Les fiches déjà rédigées par le chef dans `Fiche_techniques_CBT.xlsx` (bourguignon, blanquette de veau, pot-au-feu, chili con carne, haricots blancs, lentilles, lentilles vinaigrette, ratatouille, sauté de veau, rôti de porc/échine) ont été reprises **telles quelles** à la place d'une version réécrite.

## Modèle de fiche (identique à l'exemple CBT)
- A1 titre · E2 valeur pasteurisatrice théorique minimum · G1 mode / température de cuisson.
- Lignes 4 à 18 : produit, quantité recette de base, **quantité de production (formule)**, unité, prix unitaire (à saisir), total € (formule).
- G4 mode opératoire.
- B23 poids net d'une portion (modifiable) · B24 **nombre de portions à produire (à saisir, 100 par défaut)**. Les colonnes C et F ainsi que le prix unitaire portion se recalculent.

## Répartition des modes de cuisson
| Mode | Nb de fiches | Titre |
|---|---|---|
| CBT – cuisson de nuit (four vapeur ou sauteuse, 12 h – 18 h) | 64 + 10 fiches du chef | « … cuisson de nuit » |
| Sous vide basse température (thermoplongeur ou four vapeur) | 41 | « … sous vide basse température » |
| Cuisson traditionnelle | 123 | nom du plat |
| Préparation froide (liaison froide) | 46 | nom du plat |

Règle appliquée : dès qu'une préparation se prête à la basse température / au sous vide / à la cuisson de nuit (viandes braisées, rôtis, volailles, abats, légumineuses, légumes racines, potages, ratatouille…), la fiche est rédigée en CBT en respectant la table de températures du chef ; sinon elle est rédigée en cuisson normale.

## Sous-dossiers
- `sources/` : les trois fichiers d'origine (menu 2026, fiche technique CBT modèle, températures de cuisson).
- `fiches_techniques_2026.json` : les 274 fiches rédigées, sous forme de données (réutilisables pour regénérer ou modifier le classeur).
- `outils/` : `canon.py` (regroupement des intitulés du menu : fautes de frappe et variantes → nom de fiche), `build_xlsx.py` (assemblage du classeur à partir du modèle), `brief.md` (consignes de rédaction).

Regénérer le classeur : `python3 outils/build_xlsx.py fiches_techniques_2026.json Fiches_techniques_menu_2026.xlsx` (adapter les chemins des sources en tête de script).
