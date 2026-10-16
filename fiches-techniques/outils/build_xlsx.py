# -*- coding: utf-8 -*-
import json, re, sys, copy
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink
sys.path.insert(0, '/tmp/claude-0/-home-user-concour-de-belotte/64d19263-231e-5d7c-a7b5-8e2986a86600/scratchpad/work')
from canon import CANON, IGNORE

IN = '/tmp/claude-0/-home-user-concour-de-belotte/64d19263-231e-5d7c-a7b5-8e2986a86600/scratchpad/in/'
TPL = IN + '2f16fdac-Fiche_techniques_CBT-.xlsx'
MENU = IN + '56eaa7fb-menu-2026-ehpad-fam.xlsx'
TCUIS = IN + '2e12933a-T_-Cuisson.xlsx'
fiches_path, out_path = sys.argv[1], sys.argv[2]
PORTIONS_DEFAULT = 100
BASE_PORTIONS = 70          # recette de base pour 70 personnes
EFFECTIF_EHPAD = 70         # hypothèse à confirmer par le chef
EFFECTIF_FAM = 40
CATALOGUE = json.load(open('/tmp/claude-0/-home-user-concour-de-belotte/64d19263-231e-5d7c-a7b5-8e2986a86600/scratchpad/work/catalogue.json', encoding='utf-8'))['produits']
ALIAS2CODE = {}
for _p in CATALOGUE:
    for _a in _p['aliases']: ALIAS2CODE[re.sub(r'\s+', ' ', _a).strip()] = _p['code']
PU_FORMULA = "=IFERROR(INDEX(Correspondance!$D$2:$D$3000,MATCH(A{r},Correspondance!$A$2:$A$3000,0)),0)"
PIECES_FORMULA = "=IFERROR(ROUNDUP(C{r}/INDEX(Correspondance!$E$2:$E$3000,MATCH(A{r},Correspondance!$A$2:$A$3000,0)),0),\"\")"
CODE2PROD = {_p['code']: _p for _p in CATALOGUE}
def is_piece(label):
    c = ALIAS2CODE.get(label)
    return bool(c) and CODE2PROD[c]['unite'] == 'Pièce'
def add_pieces_column(ws, rows, last_row):
    hdr = ws['H3']; hdr.value = 'Pièces à commander'
    hdr.font = copy.copy(ws['C3'].font); hdr.alignment = copy.copy(ws['C3'].alignment); hdr.border = copy.copy(ws['C3'].border)
    for r in rows:
        c = ws[f'H{r}']; c.value = PIECES_FORMULA.format(r=r)
        c.font = Font(name='Calibri', size=12, bold=True); c.alignment = Alignment(horizontal='center'); c.border = copy.copy(ws[f'C{r}'].border)
        c.number_format = '0'
    ws.column_dimensions['H'].width = 14
    ws.print_area = f'A1:H{last_row}'
used_products = set()

fiches = json.load(open(fiches_path, encoding='utf-8'))
if isinstance(fiches, dict): fiches = fiches['fiches']
by_name = {f['nom']: f for f in fiches}

# fiches originales du chef -> nom canonique (remplacent la version rédigée)
ORIG = {
    'Bourguignon': 'Bœuf bourguignon', 'Blanquette-Veau': 'Blanquette de veau', 'Pot au feu': 'Pot-au-feu',
    'Chili-CHR-Viande': 'Chili con carne', 'Haricots blancs': 'Haricots blancs', 'Lentilles': 'Lentilles',
    'Lentilles vinaig nuit': 'Salade de lentilles', 'Ratatouille': 'Ratatouille', 'Sauté Veau': 'Sauté de veau',
    'Echine de porc': 'Rôti de porc',
}
BONUS = ['Joue de boeuf', 'Haricots rouges', 'Chili-viande à part', 'COCO-Catalans', 'Pois Chiches']

wb = openpyxl.load_workbook(TPL)
tpl = wb['Haricots blancs']
orig_sheets = list(wb.sheetnames)

PREFIX = {'Entrée': 'E', 'Plat': 'P', 'Garniture': 'G', 'Dessert': 'D'}
used = set()
def sheet_name(cat, nom):
    base = f"{PREFIX[cat]}-{nom}"
    base = re.sub(r"[\[\]\:\*\?\/\\]", "-", base)[:31].rstrip()
    n, i = base, 2
    while n.lower() in used:
        suf = f"~{i}"; n = base[:31-len(suf)] + suf; i += 1
    used.add(n.lower()); return n

MODE_LABEL = {'CBT_NUIT': 'CBT – cuisson de nuit', 'SOUS_VIDE_BT': 'Sous vide basse température', 'NORMAL': 'Cuisson traditionnelle', 'FROID': 'Préparation froide', 'CHEF': 'CBT – fiche originale du chef'}

index = []  # (cat, nom, sheet, mode, titre)
order = ['Entrée', 'Plat', 'Garniture', 'Dessert']
names_by_cat = {c: [n for n, (cat, _) in CANON.items() if cat == c] for c in order}
orig_by_canon = {v: k for k, v in ORIG.items()}

def link_chef_sheet(ws):
    sumrow = next(r for r in range(4, 40) if isinstance(ws[f'F{r}'].value, str) and 'SUM' in ws[f'F{r}'].value.upper())
    pu_row = next(r for r in range(sumrow, sumrow + 4) if ws[f'A{r}'].value and 'Prix unitaire' in str(ws[f'A{r}'].value))
    # recette de base ramenée à BASE_PORTIONS
    tot_cell = ws[f'B{pu_row + 1}'].value   # 'Poids total ou ingrédient principal' : formule SUM ou valeur saisie par le chef
    if isinstance(tot_cell, (int, float)):
        total = tot_cell
    else:
        total = sum(ws[f'B{r}'].value for r in range(4, sumrow) if isinstance(ws[f'B{r}'].value, (int, float)))
    pn = ws[f'B{pu_row + 3}'].value
    k = (BASE_PORTIONS * pn / total) if (total and isinstance(pn, (int, float)) and pn) else 1
    if isinstance(tot_cell, (int, float)):
        ws[f'B{pu_row + 1}'] = round(tot_cell * k, 2)
    for r in range(4, sumrow):
        v = ws[f'A{r}'].value
        if v is not None and str(v).strip():
            ws[f'A{r}'] = re.sub(r'\s+', ' ', str(v)).strip()
            used_products.add(ws[f'A{r}'].value)
            ws[f'E{r}'] = PU_FORMULA.format(r=r)
        q = ws[f'B{r}'].value
        if isinstance(q, (int, float)):
            q = q * k
            ws[f'B{r}'] = round(q, 2) if q >= 1 else round(q, 3)
    ws[f'B{pu_row + 4}'] = '=Paramètres!$B$5'
    ws[f'C{pu_row + 4}'] = 'Effectif EHPAD + FAM (feuille Paramètres) – possibilité de saisir un autre nombre'
    ws[f'C{pu_row + 3}'] = 'Possibilité de saisir le grammage'
    for rr in (pu_row + 3, pu_row + 4):
        ws[f'C{rr}'].alignment = Alignment(horizontal='left'); ws[f'C{rr}'].font = Font(name='Calibri', size=10, italic=True)
    g = ws['G4'].value
    if isinstance(g, str):
        g = g.replace('(voir colonne B quantité pour un bac)', '(colonne B = recette de base 70 portions, à répartir en bacs 1/1 H10 : environ 1,5 kg de légumineuses sèches par bac)')
        g = g.replace('(voir colonne C quantité production)', '(colonne C = quantité de production)')
        ws['G4'] = g
    ws.page_setup.orientation = 'landscape'
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = f'A1:G{pu_row + 4}'
    piece_rows = [r for r in range(4, sumrow) if ws[f'A{r}'].value and is_piece(ws[f'A{r}'].value)]
    if piece_rows: add_pieces_column(ws, piece_rows, pu_row + 4)

def clear_row(ws, r):
    for col in 'ABDE':
        ws[f'{col}{r}'].value = None

for cat in order:
    for nom in names_by_cat[cat]:
        sname = sheet_name(cat, nom)
        if nom in orig_by_canon:
            src = wb[orig_by_canon[nom]]
            ws = wb.copy_worksheet(src); ws.title = sname
            link_chef_sheet(ws)
            title = str(src['A1'].value or '').strip()
            index.append((cat, nom, sname, 'CHEF', title)); continue
        f = by_name.get(nom)
        if f is None:
            print('MANQUANTE:', nom); continue
        ws = wb.copy_worksheet(tpl); ws.title = sname
        ws['A1'] = f['titre']
        ws['E2'] = f['vp']
        ws['G1'] = f['cuisson']
        ings = f['ingredients'][:15]
        tot = sum(i['qte'] for i in ings if i['qte'])
        k = (BASE_PORTIONS * f['poids_portion'] / tot) if tot else 1
        for i in range(15):
            r = 4 + i
            clear_row(ws, r)
            if i < len(ings):
                ing = ings[i]
                ws[f'A{r}'] = ing['produit'] if ing['qte'] is not None else (ing['produit'] if 'PM' in ing['produit'] else ing['produit'] + ' PM')
                q = ing['qte']
                if q is not None:
                    q = q * k
                    q = round(q, 2) if q >= 1 else round(q, 3)
                ws[f'B{r}'] = q
                ws[f'D{r}'] = ing['unite']
                ws[f'A{r}'] = re.sub(r'\s+', ' ', str(ws[f'A{r}'].value)).strip()
                used_products.add(ws[f'A{r}'].value)
            ws[f'E{r}'] = PU_FORMULA.format(r=r)
        ws['G4'] = f['mode_operatoire']
        piece_rows = [4 + i for i, ing in enumerate(ings) if is_piece(re.sub(r'\s+', ' ', ing['produit']).strip())]
        if piece_rows: add_pieces_column(ws, piece_rows, 24)
        ws['B23'] = f['poids_portion']
        ws['B24'] = '=Paramètres!$B$5'
        ws['C23'] = 'Possibilité de saisir le grammage'
        ws['C24'] = 'Effectif EHPAD + FAM (feuille Paramètres) – possibilité de saisir un autre nombre'
        # un peu plus de hauteur pour le mode opératoire long
        nlines = f['mode_operatoire'].count('\n') + 1
        if nlines > 14:
            for r in range(5, 19): ws.row_dimensions[r].height = 22
        ws.page_setup.orientation = 'landscape'
        ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 1
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_area = 'A1:G24'
        index.append((cat, nom, sname, f['mode'], f['titre']))

# fiches bonus du chef (non présentes au menu)
for s in BONUS:
    src = wb[s]; ws = wb.copy_worksheet(src); ws.title = ('X-' + s)[:31]
    link_chef_sheet(ws)
    index.append(('Autres fiches du chef', s, ws.title, 'CHEF', str(src['A1'].value or '').strip()))

# supprimer les feuilles d'origine
for s in orig_sheets:
    del wb[s]

# ---------- Sommaire ----------
som = wb.create_sheet('Sommaire', 0)
hdr_font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
hdr_fill = PatternFill('solid', fgColor='1F4E78')
thin = Side(style='thin', color='999999'); bd = Border(left=thin, right=thin, top=thin, bottom=thin)
som['A1'] = 'FICHES TECHNIQUES – MENU ANNUEL EHPAD / FAM'
som['A1'].font = Font(name='Calibri', size=18, bold=True)
som['A2'] = "Cliquer sur le nom d'une fiche pour l'ouvrir. Modes : CBT – cuisson de nuit (four vapeur 12-18 h) ; Sous vide basse température ; Cuisson traditionnelle ; Préparation froide."
som['A3'] = "Sur chaque fiche : saisir le nombre de portions à produire (B24) et, si besoin, le grammage (B23) et les prix unitaires (colonne E) ; les quantités de production (colonne C) et les coûts se recalculent."
heads = ['Catégorie', 'Fiche', 'Mode de cuisson', 'Titre de la fiche', 'Nb de fois au menu 2026']
for j, h in enumerate(heads, 1):
    c = som.cell(row=5, column=j, value=h); c.font = hdr_font; c.fill = hdr_fill; c.border = bd; c.alignment = Alignment(horizontal='center', vertical='center')
# occurrences
items = json.load(open('/tmp/claude-0/-home-user-concour-de-belotte/64d19263-231e-5d7c-a7b5-8e2986a86600/scratchpad/work/items.json', encoding='utf-8'))
alias = {a: n for n, (c, als) in CANON.items() for a in als}
occ = {}
for role, d in items.items():
    for k, n in d.items():
        if k in alias: occ[alias[k]] = occ.get(alias[k], 0) + n
r = 6
fill_cat = {'Entrée': 'E2EFDA', 'Plat': 'FCE4D6', 'Garniture': 'DDEBF7', 'Dessert': 'FFF2CC', 'Autres fiches du chef': 'EDEDED'}
for cat, nom, sname, mode, title in index:
    vals = [cat, nom, MODE_LABEL[mode], title.replace('\n', ' '), occ.get(nom, '')]
    for j, v in enumerate(vals, 1):
        c = som.cell(row=r, column=j, value=v); c.border = bd; c.font = Font(name='Calibri', size=11)
        c.fill = PatternFill('solid', fgColor=fill_cat[cat])
    link = som.cell(row=r, column=2); link.hyperlink = Hyperlink(ref=link.coordinate, location=f"'{sname}'!A1", display=nom); link.font = Font(name='Calibri', size=11, color='0563C1', underline='single')
    r += 1
for col, w in zip('ABCDE', [22, 42, 30, 52, 22]): som.column_dimensions[col].width = w
som.freeze_panes = 'A6'
som.auto_filter.ref = f"A5:E{r-1}"

# ---------- Menu -> fiches ----------
mw = openpyxl.load_workbook(MENU, data_only=False)
mp = wb.create_sheet('Menu → fiches', 1)
heads = ['Semaine', 'Jour', 'Service', 'Entrée (menu)', 'Fiche entrée', 'Plat (menu)', 'Fiche plat', 'Garniture (menu)', 'Fiche garniture', 'Dessert (menu)', 'Fiche dessert']
for j, h in enumerate(heads, 1):
    c = mp.cell(row=1, column=j, value=h); c.font = hdr_font; c.fill = hdr_fill; c.border = bd; c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
sheet_of = {nom: sname for cat, nom, sname, mode, title in index}
days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
def canon_of(v):
    if v is None: return None, ''
    s = re.sub(r'\s+', ' ', str(v)).strip()
    if not s: return None, ''
    k = s.lower()
    return alias.get(k), s
r = 2
for ws in mw.worksheets:
    for d in range(7):
        base = 3 + 5 * d
        for col, svc in (('B', 'Midi'), ('D', 'Soir')):
            row = [ws.title, days[d], svc]
            for off in (0, 1, 2, 4):
                cn, raw = canon_of(ws[f'{col}{base+off}'].value)
                row += [raw, cn or '']
            if not any(row[3::2]): continue
            for j, v in enumerate(row, 1):
                c = mp.cell(row=r, column=j, value=v); c.border = bd; c.font = Font(name='Calibri', size=10)
            for j in (5, 7, 9, 11):
                cn = row[j-1]
                if cn and cn in sheet_of:
                    c = mp.cell(row=r, column=j); c.hyperlink = Hyperlink(ref=c.coordinate, location=f"'{sheet_of[cn]}'!A1", display=cn); c.font = Font(name='Calibri', size=10, color='0563C1', underline='single')
            r += 1
for col, w in zip('ABCDEFGHIJK', [14, 10, 8, 26, 26, 26, 28, 24, 26, 18, 24]): mp.column_dimensions[col].width = w
mp.freeze_panes = 'A2'; mp.auto_filter.ref = f"A1:K{r-1}"

# ---------- T° cuisson (copie) ----------
tw = openpyxl.load_workbook(TCUIS)['Feuil1']
tc = wb.create_sheet('T° cuisson de nuit', 2)
for row in tw.iter_rows():
    for c in row:
        if c.value is not None:
            n = tc.cell(row=c.row, column=c.column, value=c.value)
            n.font = copy.copy(c.font); n.alignment = copy.copy(c.alignment); n.border = copy.copy(c.border); n.fill = copy.copy(c.fill)
for k, v in tw.column_dimensions.items(): tc.column_dimensions[k].width = v.width
for m in tw.merged_cells.ranges: tc.merge_cells(str(m))

# ---------- Paramètres ----------
pa = wb.create_sheet('Paramètres', 1)
pa['A1'] = 'PARAMÈTRES DE PRODUCTION'; pa['A1'].font = Font(name='Calibri', size=16, bold=True)
rows = [('Nombre de portions de la recette de base', BASE_PORTIONS, 'Les quantités de la colonne B de chaque fiche sont calculées pour ce nombre de portions.'),
        ('Effectif maison de retraite (EHPAD)', EFFECTIF_EHPAD, 'À CONFIRMER – valeur provisoire, à saisir.'),
        ('Effectif FAM', EFFECTIF_FAM, 'Saisi d\'après les indications du chef.'),
        ('Nombre de portions à produire (total)', '=B3+B4', 'Utilisé par défaut en B24 de chaque fiche (modifiable fiche par fiche).')]
for i, (lab, val, note) in enumerate(rows, start=2):
    pa.cell(row=i, column=1, value=lab).font = Font(name='Calibri', size=12, bold=(i == 5))
    c = pa.cell(row=i, column=2, value=val); c.font = Font(name='Calibri', size=14, bold=True, color=('0000FF' if i < 5 else '000000'))
    c.fill = PatternFill('solid', fgColor=('FFFF00' if i in (3, 4) else 'DDEBF7')); c.border = bd; c.alignment = Alignment(horizontal='center')
    pa.cell(row=i, column=3, value=note).font = Font(name='Calibri', size=10, italic=True)
pa['A7'] = 'Cellules jaunes = à saisir. Le total se recalcule automatiquement.'; pa['A7'].font = Font(name='Calibri', size=10, italic=True)
pa.column_dimensions['A'].width = 44; pa.column_dimensions['B'].width = 14; pa.column_dimensions['C'].width = 80

# ---------- Cadencier ----------
ca = wb.create_sheet('Cadencier', 2)
ca['A1'] = 'CADENCIER – CATALOGUE DES PRODUITS'; ca['A1'].font = Font(name='Calibri', size=16, bold=True)
ca['A2'] = "Prix moyen collectivité = prix moyen grossiste restauration collective 2026 (HT, par unité d'achat), utilisé tant qu'aucun prix facture n'est saisi. Saisir le prix facture (colonne G, jaune), la date et le fournisseur : le prix retenu (J) bascule automatiquement sur le prix facture et met à jour toutes les fiches."
ca['A2'].font = Font(name='Calibri', size=10, italic=True)
heads = ['Code', 'Famille', 'Produit', "Unité d'achat", 'Poids moyen par pièce (kg)', 'Conditionnement', 'Prix moyen collectivité HT (€/unité)', 'Prix facture HT (€/unité)', 'Date facture', 'Fournisseur', 'Prix retenu (€/unité)', 'Prix retenu ramené au kg ou au L', 'Nb de fiches', 'Observations']
for j, h in enumerate(heads, 1):
    c = ca.cell(row=4, column=j, value=h); c.font = hdr_font; c.fill = hdr_fill; c.border = bd; c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
ca.row_dimensions[4].height = 42
fam_order = ['Viandes', 'Volailles', 'Charcuterie', 'Poissons et produits de la mer', 'Produits laitiers et œufs (BOF)', 'Fruits et légumes frais', 'Surgelés', 'Épicerie sèche', 'Conserves et sauces', 'Épices, herbes et condiments', 'Vins, alcools et boissons', 'Produits élaborés (prêts à l\'emploi)', 'Pain, pâtisserie et desserts', 'Divers']
cat_sorted = sorted(CATALOGUE, key=lambda p: (fam_order.index(p['famille']) if p['famille'] in fam_order else 99, p['code']))
# nb de fiches par produit
fiche_count = {}
for f in fiches:
    codes = set(ALIAS2CODE.get(re.sub(r'\s+', ' ', i['produit']).strip()) for i in f['ingredients'])
    for cde in codes:
        if cde: fiche_count[cde] = fiche_count.get(cde, 0) + 1
r = 5
code_row = {}
for p in cat_sorted:
    vals = [p['code'], p['famille'], p['produit'], p['unite'], p.get('poids_piece'), p.get('conditionnement', ''), p['prix_base'], None, None, None,
            f'=IF(H{r}<>"",H{r},G{r})', f'=IF(AND(D{r}="Pièce",E{r}>0),K{r}/E{r},K{r})', fiche_count.get(p['code'], 0), p.get('observations', '')]
    for j, v in enumerate(vals, 1):
        c = ca.cell(row=r, column=j, value=v); c.border = bd; c.font = Font(name='Calibri', size=11)
    ca.cell(row=r, column=5).number_format = '0.000'; ca.cell(row=r, column=5).font = Font(name='Calibri', size=11, color='0000FF')
    ca.cell(row=r, column=7).number_format = '#,##0.00 "€"'; ca.cell(row=r, column=7).font = Font(name='Calibri', size=11, color='0000FF')
    ca.cell(row=r, column=8).number_format = '#,##0.00 "€"'; ca.cell(row=r, column=8).fill = PatternFill('solid', fgColor='FFFF00'); ca.cell(row=r, column=8).font = Font(name='Calibri', size=11, color='0000FF')
    ca.cell(row=r, column=9).number_format = 'DD/MM/YYYY'; ca.cell(row=r, column=9).fill = PatternFill('solid', fgColor='FFFF00')
    ca.cell(row=r, column=10).fill = PatternFill('solid', fgColor='FFFF00')
    ca.cell(row=r, column=11).number_format = '#,##0.00 "€"'; ca.cell(row=r, column=11).font = Font(name='Calibri', size=11, bold=True)
    ca.cell(row=r, column=12).number_format = '#,##0.00 "€"'
    if p['unite'] == 'Pièce':
        for j in (4, 5): ca.cell(row=r, column=j).fill = PatternFill('solid', fgColor='E2EFDA')
    code_row[p['code']] = r
    r += 1
LAST_CAT = r - 1
for col, w in zip('ABCDEFGHIJKLMN', [10, 30, 44, 9, 11, 22, 16, 16, 12, 18, 14, 16, 10, 40]): ca.column_dimensions[col].width = w
ca.freeze_panes = 'A5'; ca.auto_filter.ref = f"A4:N{LAST_CAT}"

# ---------- Correspondance (intitulé de fiche -> produit du cadencier) ----------
co = wb.create_sheet('Correspondance', 3)
co['A1'] = "Correspondance entre les intitulés utilisés dans les fiches et les produits du cadencier (le prix est repris du cadencier par formule). Modifier le code (colonne B) pour rattacher un intitulé à un autre produit."
co['A1'].font = Font(name='Calibri', size=10, italic=True)
# la ligne 1 est une note ; le tableau commence ligne 2 (en-têtes) pour rester dans $A$2:$A$3000
heads = ['Intitulé dans les fiches', 'Code produit', 'Produit du cadencier', 'Prix retenu ramené au kg ou L', 'Poids moyen par pièce (kg)', "Unité d'achat"]
for j, h in enumerate(heads, 1):
    c = co.cell(row=2, column=j, value=h); c.font = hdr_font; c.fill = hdr_fill; c.border = bd
r = 3
missing_alias = []
for raw in sorted(used_products, key=lambda x: x.lower()):
    code = ALIAS2CODE.get(raw)
    if code is None: missing_alias.append(raw); continue
    co.cell(row=r, column=1, value=raw).border = bd
    co.cell(row=r, column=2, value=code).border = bd
    co.cell(row=r, column=3, value=f'=IFERROR(INDEX(Cadencier!$C$5:$C${LAST_CAT},MATCH(B{r},Cadencier!$A$5:$A${LAST_CAT},0)),"code inconnu")').border = bd
    c = co.cell(row=r, column=4, value=f'=IFERROR(INDEX(Cadencier!$L$5:$L${LAST_CAT},MATCH(B{r},Cadencier!$A$5:$A${LAST_CAT},0)),0)'); c.border = bd; c.number_format = '#,##0.00 "€"'
    c = co.cell(row=r, column=5, value=f'=IFERROR(INDEX(Cadencier!$E$5:$E${LAST_CAT},MATCH(B{r},Cadencier!$A$5:$A${LAST_CAT},0)),"")'); c.border = bd; c.number_format = '0.000'
    c = co.cell(row=r, column=6, value=f'=IFERROR(INDEX(Cadencier!$D$5:$D${LAST_CAT},MATCH(B{r},Cadencier!$A$5:$A${LAST_CAT},0)),"")'); c.border = bd
    r += 1
if missing_alias: print('PRODUITS SANS CORRESPONDANCE:', missing_alias)
for col, w in zip('ABCDEF', [60, 12, 44, 16, 12, 10]): co.column_dimensions[col].width = w
co.freeze_panes = 'A3'; co.auto_filter.ref = f"A2:F{r-1}"
# PU_FORMULA utilise la colonne D de Correspondance, lignes 2..3000 : OK

wb.active = 0
wb.save(out_path)
print('feuilles:', len(wb.sheetnames), 'fiches index:', len(index))
