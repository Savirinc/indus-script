"""Round 53: extracts with word boundaries. Usage: python3 extract53.py DL_DIR
Writes controls/{SEAL,SUX,OBL,OAL,CHN,OBI}.txt: one unit per line, signs space-separated, words separated by ' | '.
Only units of 2-13 signs are written (PROTOCOL). Standard library only; prints counts."""
import sys, re, csv, json, collections, unicodedata
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round52'))
import extract52 as X
D = Path(sys.argv[1]); X.D = D
OUT = P / 'controls'; OUT.mkdir(exist_ok=True)
csv.field_size_limit(10**9)

SPECS = {  # code: (period prefixes, genres or None, langs, designation prefix, whole-object unit?)
    'SUX': (('Ur III',), {'Administrative'}, {'sux'}, None, False),
    'OBL': (('Old Babylonian (',), {'Letter'}, {'akk'}, None, False),
    'OAL': (('Old Assyrian',), {'Letter'}, {'akk'}, None, False),
    'SEAL': (('Ur III', 'Old Babylonian (', 'Early Old Babylonian'), None, {'sux', 'akk'}, 'CDLI Seals', True),
}

def write(name, units):
    units = [u for u in units if 2 <= sum(len(w) for w in u) <= 13]
    with (OUT / f'{name}.txt').open('w', encoding='utf-8') as f:
        for u in units: f.write(' | '.join(' '.join(w) for w in u) + '\n')
    toks = sum(len(w) for u in units for w in u); words = sum(len(u) for u in units)
    print(f'{name}: units {len(units)}, tokens {toks}, words {words}, signs/word {toks/max(words,1):.2f}', flush=True)

def cdli():
    cat = {}
    with (D / 'cdli_cat.csv').open(encoding='utf-8', errors='replace') as f:
        for r in csv.DictReader(f): cat['P' + r['id_text'].zfill(6)] = (r.get('period', ''), r.get('genre', ''))
    v2s = X.load_osl()
    units = {k: [] for k in SPECS}; active = []; lang = None; cur = {}
    for line in (D / 'cdliatf_unblocked.atf').open(encoding='utf-8', errors='replace'):
        if line.startswith('&'):
            pid = line[1:8]; desig = line.split('=', 1)[1].strip() if '=' in line else ''
            per, gen = cat.get(pid, ('', '')); lang = None; cur = {}
            active = [k for k, (pp, gg, ll, dd, _) in SPECS.items() if per.startswith(pp) and (gg is None or gen in gg) and (dd is None or desig.startswith(dd))]
            continue
        if not active: continue
        if line.startswith('#atf: lang'): lang = line.split()[-1].strip(); continue
        if not re.match(r"^\d+'?\.", line): continue
        body = re.sub(r'\(\$.*?\$\)', ' ', line.split('.', 1)[1]).strip()
        if '...' in body or re.search(r'\bx\b', body) or re.search(r'\bn\b', body): continue
        for k in active:
            if lang not in SPECS[k][2]: continue
            words = []
            for w in body.split():
                w = re.sub(r'[\[\]#!?*<>]', '', w).replace('_', '')
                w = re.sub(r'\{([^}]*)\}', r'-\1-', w)
                toks = []
                for s in w.split('-'):
                    s = s.strip('-').strip()
                    if not s or not re.search(r'[A-Za-z0-9]', s): continue
                    if re.fullmatch(r'[\d/]+\([^)]*\)', s): toks.append(s); continue
                    ms = re.fullmatch(r'[^()]+\(([^()]+)\)', s)
                    if ms: toks.append(ms.group(1)); continue
                    s2 = X.atf_to_osl(s.lower()); toks.append(v2s.get(s2, 'v:' + s))
                if toks: words.append(toks)
            if not words: continue
            if SPECS[k][4] and units[k] and units[k][-1] is cur.get(k): units[k][-1].extend(words)
            else: units[k].append(words); cur[k] = units[k][-1]
    for k in SPECS: write(k, units[k])

def chn():
    j = json.load((D / 'shijing.json').open(encoding='utf-8')); units = []
    for poem in j:
        for line in poem['content']:
            for clause in re.split(r'[，。！？、；：]', line):
                s = [c for c in clause if unicodedata.category(c).startswith('L')]
                if s: units.append([[c] for c in s])      # approximate gold: one character per word
    write('CHN', units)

def obi():
    j = json.load((D / 'obimd_data.json').open(encoding='utf-8')); units = []
    for rec in j:
        for g in rec.get('RecordUtilSentenceGroupVoList', []):
            if not str(g.get('GroupCategory', '')).startswith('InscriptionSentence'): continue
            chars = g.get('RecordUtilOracleCharVoList', [])
            if not chars or any(c.get('SeatFont', 0) != 0 or not c.get('Label') for c in chars): continue
            units.append([[c['Label']] for c in sorted(chars, key=lambda c: c['OrderNumber'])])   # no gold: each sign its own word
    write('OBI', units)

cdli(); chn(); obi()
