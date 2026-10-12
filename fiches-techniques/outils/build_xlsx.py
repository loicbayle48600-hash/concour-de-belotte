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

def clear_row(ws, r):
    for col in 'ABDE':
        ws[f'{col}{r}'].value = None

for cat in order:
    for nom in names_by_cat[cat]:
        sname = sheet_name(cat, nom)
        if nom in orig_by_canon:
            src = wb[orig_by_canon[nom]]
            ws = wb.copy_worksheet(src); ws.title = sname
            title = str(src['A1'].value or '').strip()
            index.append((cat, nom, sname, 'CHEF', title))
            continue
        f = by_name.get(nom)
        if f is None:
            print('MANQUANTE:', nom); continue
        ws = wb.copy_worksheet(tpl); ws.title = sname
        ws['A1'] = f['titre']
        ws['E2'] = f['vp']
        ws['G1'] = f['cuisson']
        ings = f['ingredients'][:15]
        for i in range(15):
            r = 4 + i
            clear_row(ws, r)
            if i < len(ings):
                ing = ings[i]
                ws[f'A{r}'] = ing['produit'] if ing['qte'] is not None else (ing['produit'] if 'PM' in ing['produit'] else ing['produit'] + ' PM')
                ws[f'B{r}'] = ing['qte']
                ws[f'D{r}'] = ing['unite']
        ws['G4'] = f['mode_operatoire']
        ws['B23'] = f['poids_portion']
        ws['B24'] = PORTIONS_DEFAULT
        ws['C23'] = 'Possibilité de saisir le grammage'
        ws['C24'] = 'Possibilité de saisir le nombre de portions'
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

wb.active = 0
wb.save(out_path)
print('feuilles:', len(wb.sheetnames), 'fiches index:', len(index))
