"""Round 54: Akkadian extracts with per-token phonetic/logographic flags. Usage: python3 extract54.py DL_DIR
Writes controls/{OBL,OAL,SEAL}.txt: one unit per line, tokens SIGN/p (syllabic), SIGN/l (Sumerogram, determinative, numeral).
Standard library only; prints counts."""
import sys, re, csv, collections
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round52'))
import extract52 as X
D = Path(sys.argv[1]); X.D = D
OUT = P / 'controls'; OUT.mkdir(exist_ok=True)
csv.field_size_limit(10**9)
SPECS = {'OBL': (('Old Babylonian (',), {'Letter'}, None, False),
         'OAL': (('Old Assyrian',), {'Letter'}, None, False),
         'SEAL': (('Ur III', 'Old Babylonian (', 'Early Old Babylonian'), None, 'CDLI Seals', True)}

def main():
    cat = {}
    with (D / 'cdli_cat.csv').open(encoding='utf-8', errors='replace') as f:
        for r in csv.DictReader(f): cat['P' + r['id_text'].zfill(6)] = (r.get('period', ''), r.get('genre', ''))
    v2s = X.load_osl(); units = {k: [] for k in SPECS}; stats = {k: collections.Counter() for k in SPECS}
    active = []; lang = None; cur = {}
    for line in (D / 'cdliatf_unblocked.atf').open(encoding='utf-8', errors='replace'):
        if line.startswith('&'):
            pid = line[1:8]; desig = line.split('=', 1)[1].strip() if '=' in line else ''
            per, gen = cat.get(pid, ('', '')); lang = None; cur = {}
            active = [k for k, (pp, gg, dd, _) in SPECS.items() if per.startswith(pp) and (gg is None or gen in gg) and (dd is None or desig.startswith(dd))]
            continue
        if not active: continue
        if line.startswith('#atf: lang'): lang = line.split()[-1].strip(); continue
        if lang != 'akk' or not re.match(r"^\d+'?\.", line): continue
        body = re.sub(r'\(\$.*?\$\)', ' ', line.split('.', 1)[1]).strip()
        if '...' in body or re.search(r'\bx\b', body) or re.search(r'\bn\b', body): continue
        toks = []; in_log = False
        for w in body.split():
            w = re.sub(r'[\[\]#!?*<>]', '', w)
            starts = w.startswith('_'); ends = w.endswith('_') and len(w) > 1
            w = w.strip('_')
            word_log = in_log or starts
            if starts and not ends: in_log = True
            if ends: in_log = False
            parts = re.split(r'(\{[^}]*\})', w)
            for part in parts:
                if not part: continue
                det = part.startswith('{')
                for s in part.strip('{}').split('-'):
                    s = s.strip('-').strip()
                    if not s or not re.search(r'[A-Za-z0-9]', s): continue
                    if re.fullmatch(r'[\d/]+\([^)]*\)', s): toks.append(s + '/l'); continue
                    ms = re.fullmatch(r'[^()]+\(([^()]+)\)', s)
                    name = ms.group(1) if ms else v2s.get(X.atf_to_osl(s.lower()), 'v:' + s)
                    flag = 'l' if (word_log or det or (s.isupper() and not ms)) else 'p'
                    toks.append(name + '/' + flag)
        if not toks: continue
        for k in active:
            if SPECS[k][3] and units[k] and units[k][-1] is cur.get(k): units[k][-1].extend(toks)
            else: units[k].append(list(toks)); cur[k] = units[k][-1]
    for k in SPECS:
        us = units[k]
        with (OUT / f'{k}.txt').open('w', encoding='utf-8') as f:
            for u in us: f.write(' '.join(u) + '\n')
        c = collections.Counter(t[-1] for u in us for t in u)
        print(f'{k}: units {len(us)}, tokens {sum(len(u) for u in us)}, syllabic {c["p"]}, logographic {c["l"]}', flush=True)

if __name__ == '__main__': main()
