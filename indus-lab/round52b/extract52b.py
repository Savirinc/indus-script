"""Round 52b: extract the additional CDLI corpora named in PROTOCOL.md.
Usage: python3 extract52b.py DL_DIR   (DL_DIR holds cdliatf_unblocked.atf, cdli_cat.csv, osl.asl from round 52)
Writes controls/{OBL,OAL,SEAL,U4,U3,PE}.txt. Standard library only; only counts are printed."""
import sys, re, csv, collections
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round52'))
import extract52 as X   # tokeniser helpers (atf_to_osl, load_osl); importing does not run its extractors
D = Path(sys.argv[1]); X.D = D
OUT = P / 'controls'; OUT.mkdir(exist_ok=True)
csv.field_size_limit(10**9)

TEXT_UNIT = {'SEAL', 'U4', 'U3', 'PE'}   # one unit per object (Amendments 2-3)
SPECS = {   # code: (period prefixes, genres or None, languages or None, designation prefix or None, map through OSL?)
    'OBL': (('Old Babylonian (',), {'Letter'}, {'akk'}, None, True),
    'OAL': (('Old Assyrian',), {'Letter'}, {'akk'}, None, True),
    'SEAL': (('Ur III', 'Old Babylonian (', 'Early Old Babylonian'), None, {'sux', 'akk'}, 'CDLI Seals', True),
    'U4': (('Uruk IV',), {'Administrative'}, {'qpc'}, None, False),
    'U3': (('Uruk III',), {'Administrative'}, {'qpc'}, None, False),
    'PE': (('Proto-Elamite',), None, None, None, False),
}

def main():
    cat = {}
    with (D / 'cdli_cat.csv').open(encoding='utf-8', errors='replace') as f:
        for r in csv.DictReader(f):
            cat['P' + r['id_text'].zfill(6)] = (r.get('period', ''), r.get('genre', ''))
    v2s = X.load_osl()
    units = {k: [] for k in SPECS}; stats = {k: collections.Counter() for k in SPECS}
    active = []; lang = None; cur_seal = {}
    for line in (D / 'cdliatf_unblocked.atf').open(encoding='utf-8', errors='replace'):
        if line.startswith('&'):
            pid = line[1:8]; desig = line.split('=', 1)[1].strip() if '=' in line else ''
            per, gen = cat.get(pid, ('', '')); lang = None; cur_seal = {}
            active = [k for k, (pp, gg, ll, dd, _) in SPECS.items()
                      if per.startswith(pp) and (gg is None or gen in gg) and (dd is None or desig.startswith(dd))]
            continue
        if not active: continue
        if line.startswith('#atf: lang'):
            lang = line.split()[-1].strip(); continue
        if not re.match(r"^\d+'?\.", line): continue
        body = re.sub(r'\(\$.*?\$\)', ' ', line.split('.', 1)[1]).strip()
        if '...' in body or re.search(r'\bx\b', body) or re.search(r'\bn\b', body): continue
        for k in active:
            ll = SPECS[k][2]; use_osl = SPECS[k][4]
            if ll is not None and lang not in ll: continue
            toks = []
            for w in body.split():
                w = re.sub(r'[\[\]#!?*<>]', '', w)
                w = w.replace('_', '')                       # Akkadian ATF marks Sumerograms with _..._
                w = re.sub(r'\{([^}]*)\}', r'-\1-', w)
                for s in w.split('-'):
                    s = s.strip('-').strip()
                    if not s or not re.search(r'[A-Za-z0-9]', s): continue   # drop ',' case separators and other punctuation
                    if re.fullmatch(r'[\d/]+\([^)]*\)', s): toks.append(s); continue
                    if not use_osl: toks.append(s); continue
                    ms = re.fullmatch(r'[^()]+\(([^()]+)\)', s)
                    if ms: toks.append(ms.group(1)); stats[k]['mapped'] += 1; continue
                    s2 = X.atf_to_osl(s.lower())
                    if s2 in v2s: toks.append(v2s[s2]); stats[k]['mapped'] += 1
                    else: toks.append('v:' + s); stats[k]['unmapped'] += 1
            if toks:
                if k in TEXT_UNIT and units[k] and units[k][-1] is cur_seal.get(k):
                    units[k][-1].extend(toks)          # one unit per seal: all its lines
                else:
                    units[k].append(toks); cur_seal[k] = units[k][-1]
    for k in SPECS:
        print(k, dict(stats[k]))
        X.OUT = OUT; X.write(k, units[k])

if __name__ == '__main__': main()
