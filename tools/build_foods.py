#!/usr/bin/env python3
"""Erzeugt foods.js aus dem Bundeslebensmittelschlüssel (BLS 4.0).

Aufruf:  python3 tools/build_foods.py PFAD/BLS_4_0_Daten_2025_DE.xlsx
Benötigt: openpyxl  (pip install openpyxl)

- tools/curated.json: die Lebensmittel mit Alltagsnamen und Portionsgrößen.
  Die Reihenfolge NICHT ändern und nichts löschen (nur hinten anfügen), weil
  Favoriten und "Zuletzt verwendet" über die Position gespeichert werden.
  "bls" ist der BLS-Code oder "MIX:CODE*Anteil+CODE*Anteil" für Mischungen.
- Alle übrigen BLS-Lebensmittel werden zusätzlich durchsuchbar.

Quelle: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0,
Deutsche Nährstoffdatenbank. Karlsruhe. DOI: 10.25826/Data20251217-134202-0
"""
import json, os, sys
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ['kcal','prot','fat','sfa','carb','sugar','fib','salt','ca','mg','fe','zn','k','vitA','vitC','vitD','vitE','b12','fol']
BLS_CODE = {'kcal':'ENERCC','prot':'PROT625','fat':'FAT','sfa':'FASAT','carb':'CHO','sugar':'SUGAR','fib':'FIBT','salt':'NACL',
            'ca':'CA','mg':'MG','fe':'FE','zn':'ZN','k':'K','vitA':'VITAA','vitC':'VITC','vitD':'VITD','vitE':'VITE','b12':'VITB12','fol':'FOL'}
GROUPS = {'B':'Brot & Brötchen','C':'Getreide & Flocken','D':'Kuchen, Kekse & Gebäck','E':'Nudeln & Eier','F':'Obst','G':'Gemüse',
          'H':'Hülsenfrüchte, Nüsse & Samen','K':'Kartoffeln & Pilze','M':'Milch & Käse','N':'Getränke','P':'Alkoholische Getränke',
          'Q':'Fette & Öle','R':'Würzmittel & Saucen','S':'Süßes','T':'Fisch','U':'Fleisch','V':'Fleisch, Geflügel & Innereien',
          'W':'Wurst & Schinken','X':'Gerichte & Beilagen','Y':'Gerichte'}
ZERO = {'TR','<LOD','<LOQ','<LOD or <LOQ'}          # Spuren / unter Nachweisgrenze -> 0
UNKNOWN = {None,'','-'}                              # kein Wert -> unbekannt

def num(v):
    if v in UNKNOWN: return None
    if isinstance(v,str):
        if v.strip() in ZERO: return 0
        try: return float(v.replace(',','.'))
        except ValueError: return None
    return float(v)

def rnd(v):
    if v is None: return None
    a = abs(v)
    r = round(v) if a >= 100 else round(v,1) if a >= 10 else round(v,2) if a >= 1 else round(v,3)
    return int(r) if r == int(r) else r

def main(xlsx):
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True))
    head, data = rows[0], rows[1:]
    col = {}
    for k,c in BLS_CODE.items():
        col[k] = next(i for i,h in enumerate(head) if h and h.startswith(c+' ') and 'Datenherkunft' not in h and 'Referenz' not in h)
    bls = {}
    for r in data:
        if not r[0]: continue
        bls[r[0]] = {'name':r[1], 'n':{k:num(r[i]) for k,i in col.items()}}

    curated = json.load(open(os.path.join(HERE,'curated.json'), encoding='utf8'))
    used = set(); base = []
    for c in curated:
        src = c['bls']
        if src.startswith('MIX:'):
            parts = [p.split('*') for p in src[4:].split('+')]
            n = {}
            for k in KEYS:
                vals = [(bls[code]['n'][k], float(f)) for code,f in parts]
                n[k] = None if any(v is None for v,_ in vals) else sum(v*f for v,f in vals)
            used.update(code for code,_ in parts)
        else:
            n = bls[src]['n']; used.add(src)
        por = ';'.join(f"{p['l']}={p['g']}" if isinstance(p,dict) else p for p in c['portions']) if isinstance(c['portions'],list) else c['portions']
        base.append([c['name'], c['cat'], [rnd(n[k]) for k in KEYS], por, src])

    extra = []
    for code,f in sorted(bls.items(), key=lambda x:x[1]['name']):
        if code in used: continue
        extra.append([code, f['name'], [rnd(f['n'][k]) for k in KEYS]])

    out = os.path.join(HERE, '..', 'foods.js')
    with open(out,'w',encoding='utf8') as fh:
        fh.write('/* Nährwerte je 100 g essbarer Anteil.\n'
                 '   Quelle: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0,\n'
                 '   Deutsche Nährstoffdatenbank. Karlsruhe. DOI: 10.25826/Data20251217-134202-0\n'
                 '   Erzeugt mit tools/build_foods.py – nicht von Hand bearbeiten.\n'
                 '   null = Wert im BLS nicht vorhanden. Reihenfolge: ' + ', '.join(KEYS) + ' */\n')
        fh.write('window.FOOD_KEYS=' + json.dumps(KEYS) + ';\n')
        fh.write('window.BLS_GROUPS=' + json.dumps(GROUPS, ensure_ascii=False, separators=(',',':')) + ';\n')
        fh.write('window.BASE_FOODS=[\n' + ',\n'.join(json.dumps(b, ensure_ascii=False, separators=(',',':')) for b in base) + '\n];\n')
        fh.write('window.BLS_FOODS=[\n' + ',\n'.join(json.dumps(e, ensure_ascii=False, separators=(',',':')) for e in extra) + '\n];\n')
    print(f'{len(base)} Alltags-Lebensmittel + {len(extra)} weitere BLS-Lebensmittel -> {os.path.getsize(out)/1024:.0f} KB')

if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
