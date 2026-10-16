# BRIEF – Rédaction de fiches techniques de cuisine collective (EHPAD / FAM)

Vous rédigez des fiches techniques pour une cuisine de collectivité (EHPAD + foyer d'accueil médicalisé, ~100 à 250 couverts).
Chaque fiche doit suivre EXACTEMENT le modèle "Fiche technique CBT" du chef (voir exemples ci-dessous).
Le chef dispose d'un four mixte vapeur programmable (cuisson de nuit), d'une sauteuse, d'une cellule de refroidissement, d'une machine sous vide et d'un thermoplongeur.
Règle du chef : **si le plat peut se faire en cuisson basse température / sous vide / cuisson de nuit (CBT), la fiche est rédigée en CBT. Sinon, la fiche est rédigée en cuisson normale (traditionnelle).** Toujours sur le même modèle.

## Structure d'une fiche (champs à renseigner)
- `nom` : nom canonique fourni (recopier à l'identique).
- `categorie` : fourni (Entrée / Plat / Garniture / Dessert) – recopier.
- `mode` : `CBT_NUIT` (cuisson longue de nuit 12h-18h au four vapeur ou sauteuse), `SOUS_VIDE_BT` (sous vide basse température, thermoplongeur ou four vapeur, quelques heures), `NORMAL` (cuisson traditionnelle), `FROID` (préparation froide sans cuisson ou assemblage).
- `titre` : titre de la fiche (cellule A1). Convention : CBT_NUIT → "<Nom> cuisson de nuit" ; SOUS_VIDE_BT → "<Nom> sous vide basse température" ; NORMAL → "<Nom>" ; FROID → "<Nom>".
- `vp` : valeur pasteurisatrice théorique minimum (cellule E2). CBT à ≥ 85°C → "> à 10 000" ; CBT à 70-80°C → "> à 1200" ; CBT/sous vide à 60-68°C → "> à 150" ; sous vide ≤ 58°C (rosbif, saumon…) → "> à 70" (préciser consommation rapide) ; NORMAL → "63°C à cœur" ; FROID → "Liaison froide 0/+3°C".
- `cuisson` : texte court de la cellule G1 (en-tête droite, 2 à 4 lignes séparées par \n). Exemples : "Cuisson 85°C four vapeur\nBac gastro avec couvercles ou sauteuse" ; "Cuisson 65°C four vapeur\nBac gastro ou grilles" ; "Sous vide 64°C thermoplongeur ou four vapeur\nPoches sous vide" ; "Four mixte 180°C\nPlaques gastro" ; "Préparation froide\nBac gastro + film, 0/+3°C".
- `ingredients` : 6 à 15 lignes {produit, qte, unite}. Quantités de la RECETTE DE BASE pour environ 50 à 80 portions, avec l'ingrédient principal autour de 10 kg (viande/poisson 10 kg ; légumineuses sèches 1,5 kg + 4,5 L d'eau pour un bac comme dans les exemples ; légumes 8-10 kg). Unité : "Kg", "L" ou "Pièce". Les produits "PM" (pour mémoire : herbes, épices en quantité minime) ont qte = null. Privilégier les produits de collectivité : surgelés 4ème/5ème gamme, cubes d'oignons surgelés, brunoise surgelée, ail surgelé, fond déshydraté, etc.
- `poids_portion` : poids net d'une portion en kg (ex. 0.12 pour 120 g de viande en sauce ; 0.10 pour un rôti ; 0.15 pour un plat complet ; 0.15 à 0.20 pour une garniture ; 0.08 à 0.10 pour une entrée). Cohérent avec la quantité totale (le tableur calcule nb portions = somme des quantités / poids portion).
- `mode_operatoire` : texte de la cellule G4. Commence par "Mode opératoire :" puis une étape par ligne (\n). 6 à 14 lignes. Style télégraphique du chef (voir exemples). Pour les CBT : préciser le programme four (température vapeur, durée mini/maxi, phases éventuelles), le conditionnement (bac gastro 1/1 avec couvercle sans trou, grilles, poche sous vide), puis le lendemain : refroidissement en cellule (63°C à 10°C en moins de 2 heures) pour remise en température différée (≥ 63°C à cœur) ou maintien en étuve pour liaison chaude. Pour le sous vide : conditionner, cuire, refroidir en cellule, DLC 5 jours max (J+5) sauf précision. Pour le NORMAL : étapes de préparation, cuisson (T° four et temps), contrôle 63°C à cœur, maintien ≥ 63°C ou refroidissement rapide. Pour le FROID : préparation en liaison froide, assaisonnement, conditionnement, conservation 0/+3°C, service dans les 24h-48h.

## Table de températures du chef (cuissons longues 12h-18h, vapeur ou thermoplongeur) – À RESPECTER
| T° | Produits | Remarques |
|---|---|---|
| 95°C | Agrumes (sirop à 15 : 1 kg sucre / 0,5 L eau, 5h à 18h sous vide), Légumineuses (haricots secs, lentilles, pois chiches, flageolets) | |
| 88°C | Tête de veau, Langue de bœuf, Pied de porc / veau | |
| 85°C | Sauté de bœuf, Sauté de mouton, Ratatouille, Légumes tajine, Aubergines, Cuisse de poule, Paleron de bœuf | |
| 74°C | Osso bucco, Blanquette de veau | Débuter la cuisson à 85°C pendant 2h00 |
| 72°C | Souris d'agneau, Cuisses de canard entières, Sauté d'agneau | Possibilité à 68°C |
| 70°C | Paleron de veau | |
| 65°C | Rôti de veau bas carré, Échine de porc | Débuter la cuisson par un pic (80°C ambiance jusqu'à 72°C à cœur) puis 65°C jusqu'au matin |
| 62°C | Ballotines de canard, Ballotines d'épaule d'agneau | À 65°C si un peu ferme |
Autres repères basse température / sous vide admis (hors table) : rôti de bœuf/rosbif sous vide 56-58°C (2h30-4h selon diamètre, saisir avant ou après), rôti de dinde / suprême de volaille / escalope sous vide 64-66°C (1h30-3h), filet mignon de porc sous vide 62-64°C (2h), magret 57°C puis saisir, pavé de saumon sous vide 52-55°C (consommation rapide) ou 63°C pour public fragile, poisson blanc sous vide 58-62°C, légumes racines (carottes, salsifis, panais, PDT) sous vide 85-90°C (45 min à 1h30), jambon braisé 68-70°C, cuisses de poulet 85°C 3h puis 72°C ou 75°C à cœur, gigot 62-65°C (ou 72°C à cœur pour public fragile), sauté de veau (phase 1 85°C 3h puis 72°C continue, 66°C si épaule/bas carré), rôti de porc comme échine (pic 80°C jusqu'à 72°C à cœur puis 65°C).
Public fragile (personnes âgées) : les viandes hachées, volailles et poissons doivent atteindre une sécurité équivalente à 63°C à cœur ou une pasteurisation sous vide suffisante (temps/température). Œufs : utiliser des ovoproduits pasteurisés pour les préparations froides (mayonnaise, mousse).

## Exemples du chef (style à imiter)

### Exemple 1 – Bourguignon cuisson de nuit  (G1 : "Cuisson 85°C four vapeur\nBac gastro avec couvercles ou sauteuse" ; VP "> à 10 000" ; portion 0.13)
Ingrédients : Sauté de bœuf de préférence gélatineux 40/60g 10 Kg ; Vin rouge 4 L ; Eau 4 L ; Oignons cubes surgelés 1 Kg ; Carottes rondelles surgelées 1 Kg ; Concentré de tomates 0.2 L ; Fécule de pomme de terre 0.55 Kg ; Sel 0.07 Kg ; Poivre 0.006 Kg ; Ail 0.1 Kg ; Laurier, thym, baies de genièvre PM ; Huile cuisson 0.2 L ; Bouillon de bœuf PM.
Mode opératoire :
Peser tous les ingrédients d'épicerie
Mettre le vin à ébullition avec thym, laurier et baies
Faire revenir le sauté avec les oignons à feu vif pour obtenir une belle coloration sans ébullition
Ajouter les carottes, l'ail, le concentré, sel, poivre et singer avec la fécule, mouiller avec le vin.
Le mélange doit devenir un peu épais
Appliquer le programme de cuisson : Sauté de Bœuf Cuisson de nuit CHPV (85°C vapeur 12h à 18h)
Le lendemain : refroidir en cellule (63°C à 10°C en moins de deux heures) pour une remise en T° différée ou maintenir en étuve pour un service en liaison chaude.

### Exemple 2 – Blanquette de veau - CBT Nuit (G1 : "Cuisson 74°C four vapeur\nBac gastro avec couvercles" ; VP "> à 1200" ; portion 0.12)
Ingrédients : Sauté de veau blanquette 12 Kg ; Brunoise de légumes surgelée crue 1.25 Kg ; Champignons surgelés 2.5 Kg ; Oignons ciselés 0.8 Kg ; Lait ou bouillon 3 L ; Crème 35% 2 Kg ; Sel 0.084 Kg ; Fécule de PDT 0.27 Kg ; Beurre 0.05 Kg ; Vin blanc 0.5 L.
Mode opératoire :
Blanchir la blanquette et décanter
Suer les oignons et la garniture, déglacer au vin blanc. Stopper la chauffe, ajouter le liant délayé dans le bouillon et la crème. Ajouter la viande.
Conditionner en poche. Refroidir. Conditionner sous vide.
Cuire à 74°C vapeur entre 12H00 et 18H00 (débuter 2h00 à 85°C)
Refroidir en cellule (63°C à 10°C en moins de deux heures) pour une remise en T° différée

### Exemple 3 – Haricots blancs cuisson de nuit (G1 : "Cuisson 95°C four vapeur\nBac gastro avec couvercles\nOu cuisson sauteuse (compatible cuisson de nuit)" ; VP "> à 10 000" ; portion 0.25)
Ingrédients (pour 1 bac) : Haricots blancs secs 1.5 Kg ; Sel 0.05 Kg ; Moutarde 0.5 Kg ; Eau 4.5 L ; Lardons facultatifs 0.8 Kg ; Laurier - Thym PM ; Brunoise surgelée 1 Kg ; Beurre 0.18 Kg.
Mode opératoire :
Four : Dans des bacs 1/1 (H10 ou 15) mettre tous les ingrédients (voir colonne B quantité pour un bac)
Mélanger et ajouter un couvercle
Cuisson : 95°C vapeur 12H00 minimum et 18h00 au maximum
Le lendemain : Refroidir en cellule (63°C à 10°C en moins de deux heures) pour une remise en T° différée ou maintenir en étuve pour un service en liaison chaude.
Sauteuse ou marmite (compatible cuisson de nuit) : mettre tous les ingrédients, couvrir, 95°C fonction mijotage 12H00 à 18H00. Le lendemain transférer en bacs, couvrir, refroidir en cellule.

### Exemple 4 – Rôti Échine cuisson de nuit (G1 : "Cuisson nuit vapeur\nBac gastro ou grilles ou sauteuse" ; VP "> à 150" ; portion 0.10)
Ingrédients : Rôti de porc échine 10 Kg ; Sel 0.12 Kg ; Poivre PM ; Huile cuisson 0.1 L.
Mode opératoire :
Plaquer les échines en bacs ou sur grilles
Si cuisson en bac mouiller à mi-hauteur des rôtis et ne pas ajouter de couvercle. Pour une cuisson en sauteuse mouiller à hauteur
Phase 1 : Four 80°C ambiance vapeur jusqu'à 72°C à cœur (sauteuse : idem)
Phase 2 : Four 65°C ambiance vapeur jusqu'au lendemain matin (sauteuse : 65°C jusqu'au lendemain matin)
Le lendemain : trancher, refroidir en cellule ou maintenir en étuve ≥ 63°C

### Exemple 5 – Ratatouille de nuit (G1 : "Programme ratatouille cuisson de nuit\nBac gastro avec couvercles" ; VP "> à 10 000" ; portion 0.22)
Ingrédients : Aubergines 3 Kg ; Courgettes 3 Kg ; Poivrons rouges et verts 1 Kg ; Tomates 1 Kg ; Oignons 0.8 Kg ; Ail 0.05 Kg ; Huile d'olive 0.3 L ; Sel 0.055 Kg ; Piment d'Espelette 0.06 Kg ; Colombo 0.02 Kg ; Herbes de Provence PM ; Fécule pomme de terre 0.12 Kg.
Mode opératoire : Peser tous les ingrédients d'épicerie / Laver, tailler les légumes et les disposer dans un bac pour assaisonnement / Ajouter tous les ingrédients et mélanger / Répartir dans les bacs cuisson, ajouter un couvercle sans trou / Cuisson vapeur 83°C pendant 14H00 à 18H00.

## Consignes de qualité
- Produits de collectivité réalistes, quantités cohérentes (ratios sel ≈ 8-10 g/kg, liant fécule ≈ 50 g/L de sauce).
- Pour les produits achetés prêts à l'emploi (jambon blanc, rosette, pâté, cordon bleu, poisson pané, nuggets, pizza surgelée, quenelles, bouchée à la reine, mortadelle, melon…) : fiche courte en mode NORMAL ou FROID avec la mise en œuvre réelle (déconditionnement, cuisson/remise en température, grammage, dressage) et une sauce ou un accompagnement maison si pertinent (ex. cordon bleu : four 180°C 20 min, 63°C à cœur).
- Garnitures de légumes racines, légumineuses, ratatouille, purées : si pertinent, proposer CBT_NUIT ou SOUS_VIDE_BT (légumes sous vide 85-90°C). Légumes verts (haricots verts, brocolis, petits pois) : NORMAL (vapeur 100°C quelques minutes, refroidissement, remise en T°).
- Viandes en sauce, braisés, rôtis, volailles entières, abats : CBT_NUIT ou SOUS_VIDE_BT en priorité, conformément à la table.
- Grillades (steak, escalope poêlée, merguez, chipolatas, boudin) : NORMAL (ou sous vide puis saisie si c'est un vrai avantage en collectivité, ex. steak de bœuf sous vide 56°C puis marquage).
- Textes en français, sans fautes, ton professionnel et concis.
