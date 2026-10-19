"""Round 52: turn the raw control downloads into sign-token sequences.
Usage: python3 extract52.py DL_DIR   (writes controls/*.txt: one unit per line, signs space-separated)
Standard library only. No statistics are computed here beyond counts of units, tokens and types."""
import sys, re, json, csv, unicodedata, collections, html
from pathlib import Path
D = Path(sys.argv[1]); OUT = Path(__file__).resolve().parent / 'controls'; OUT.mkdir(exist_ok=True)
csv.field_size_limit(10**9)

def write(name, units):
    units = [u for u in units if len(u) >= 1]
    with (OUT / f'{name}.txt').open('w', encoding='utf-8') as f:
        for u in units: f.write(' '.join(u) + '\n')
    toks = sum(len(u) for u in units); types = len(set(s for u in units for s in u))
    print(f'{name}: units {len(units)}, tokens {toks}, types {types}, units>=2 {sum(len(u)>=2 for u in units)}', flush=True)

# ---- GRK: Homer, letters, diacritics stripped, final sigma merged, scriptio continua per line
def grk():
    units = []
    for fn in ('iliad.xml', 'odyssey.xml'):
        txt = (D / fn).read_text(encoding='utf-8')
        for m in re.finditer(r'<l\b[^>]*>(.*?)</l>', txt, re.S):
            s = re.sub(r'<[^>]+>', '', m.group(1)); s = html.unescape(s)
            s = unicodedata.normalize('NFD', s).lower()
            s = ''.join(c for c in s if unicodedata.category(c)[0] == 'L' and 'GREEK' in unicodedata.name(c, ''))
            s = unicodedata.normalize('NFC', s).replace('ς', 'σ')
            if s: units.append(list(s))
    write('GRK', units)

# ---- HEB: WLC consonants, finals merged, per verse
FIN = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}
def heb():
    units = []
    for b in ('Gen', 'Exod', 'Lev', 'Num', 'Deut'):
        txt = (D / f'wlc_{b}.xml').read_text(encoding='utf-8')
        for v in re.finditer(r'<verse\b[^>]*>(.*?)</verse>', txt, re.S):
            ws = re.findall(r'<w\b[^>]*>(.*?)</w>', v.group(1), re.S)
            s = ''.join(ws).replace('/', '')
            s = ''.join(FIN.get(c, c) for c in s if 'א' <= c <= 'ת')
            if s: units.append(list(s))
    write('HEB', units)

# ---- CHR: Cherokee syllabary characters per verse
def chr_():
    txt = (D / 'Cherokee-NT.xml').read_text(encoding='utf-8')
    units = []
    for m in re.finditer(r'<seg\b[^>]*type="verse"[^>]*>(.*?)</seg>', txt, re.S):
        s = ''.join(c for c in html.unescape(m.group(1)) if 'Ꭰ' <= c <= 'Ᏽ')
        if s: units.append(list(s))
    write('CHR', units)

# ---- SUX: CDLI Ur III administrative Sumerian, ATF signs mapped through OSL
SUB = str.maketrans('0123456789x', '₀₁₂₃₄₅₆₇₈₉ₓ')
def atf_to_osl(v):
    v = v.replace('sz', 'š').replace('s,', 'ṣ').replace('t,', 'ṭ').replace('j', 'ŋ')   # OSL writes h, not ḫ
    m = re.fullmatch(r'([^\d]+?)(\d+|x)?', v)
    if not m: return v
    base, num = m.group(1), m.group(2)
    return base + (num.translate(SUB) if num else '')
def load_osl():
    val2sign = {}; sign = None
    for line in (D / 'osl.asl').open(encoding='utf-8'):
        if line.startswith('@sign '): sign = line.split(None, 1)[1].strip()
        elif line.startswith('@end sign'): sign = None
        elif line.startswith('@v') and sign:
            parts = line.split('\t')
            if len(parts) < 2: continue
            v = parts[1].strip().rstrip('?').lstrip('%')
            v = re.sub(r'^\w+:', '', v)            # language prefixes like akk:
            if v and v not in val2sign: val2sign[v] = sign
    return val2sign
def sux():
    cat = {}
    with (D / 'cdli_cat.csv').open(encoding='utf-8', errors='replace') as f:
        for r in csv.DictReader(f):
            if r.get('period', '').startswith('Ur III') and r.get('genre', '') == 'Administrative':
                cat['P' + r['id_text'].zfill(6)] = 1
    v2s = load_osl(); print('osl values', len(v2s), 'Ur III admin ids', len(cat), flush=True)
    units = []; mapped = unmapped = 0; keep = False; bad = set('[]#!?*<>')
    unmapped_c = collections.Counter()
    for line in (D / 'cdliatf_unblocked.atf').open(encoding='utf-8', errors='replace'):
        if line.startswith('&'):
            pid = line[1:8]; keep = pid in cat; lang_ok = True; continue
        if not keep: continue
        if line.startswith('#atf: lang'):
            lang_ok = line.strip().endswith('sux'); continue
        if not lang_ok or not re.match(r"^\d+'?\.", line): continue
        body = re.sub(r'\(\$.*?\$\)', ' ', line.split('.', 1)[1]).strip()   # drop ($ blank space $) notes
        if '...' in body or re.search(r'\bx\b', body) or re.search(r'\bn\b', body): continue   # damaged line
        toks = []
        ok = True
        for w in body.split():
            w = re.sub(r'[\[\]#!?*<>]', '', w)
            w = re.sub(r'\{([^}]*)\}', r'-\1-', w)       # determinatives become signs
            for s in w.split('-'):
                s = s.strip('-').strip()
                if not s: continue
                if re.fullmatch(r'[\d/]+\([^)]*\)', s) or re.fullmatch(r'\d+\([^)]*\)', s):
                    toks.append(s); continue             # numeral token stays one sign
                ms = re.fullmatch(r'[^()]+\(([^()]+)\)', s)        # value(SIGN): take the sign name
                if ms: toks.append(ms.group(1)); mapped += 1; continue
                s2 = atf_to_osl(s.lower())
                if s2 in v2s: toks.append(v2s[s2]); mapped += 1
                else: toks.append('v:' + s); unmapped += 1; unmapped_c[s] += 1
        if toks: units.append(toks)
    print('SUX mapped', mapped, 'unmapped', unmapped, 'top unmapped', unmapped_c.most_common(15), flush=True)
    write('SUX', units)

# ---- EGY: AES, Gardiner codes from MdC in reading order, fully encoded sentences only
def egy():
    units = []
    for fn in ('_aes_bbawgrabinschriften.json', '_aes_smaek.json'):
        j = json.load((D / fn).open(encoding='utf-8'))
        for s in (j.values() if isinstance(j, dict) else j):
            ts = s.get('token', [])
            if not ts or any(not t.get('hiero') for t in ts): continue
            toks = []
            for t in ts:
                for code in re.split(r'[-:*&()<>\s]+', t['hiero']):
                    code = re.sub(r'[\\/].*$', '', code).strip()   # rotation/shading suffixes
                    if code: toks.append(code)
            if toks: units.append(toks)
    write('EGY', units)

# ---- OBI: OBIMD inscription sentences, main-character labels in reading order, no placeholders
def obi():
    j = json.load((D / 'obimd_data.json').open(encoding='utf-8'))
    units = []; dropped = 0
    for rec in j:
        for g in rec.get('RecordUtilSentenceGroupVoList', []):
            if not str(g.get('GroupCategory', '')).startswith('InscriptionSentence'): continue
            chars = g.get('RecordUtilOracleCharVoList', [])
            if any(c.get('SeatFont', 0) != 0 or not c.get('Label') for c in chars) or not chars: dropped += 1; continue
            chars = sorted(chars, key=lambda c: c['OrderNumber'])
            units.append([c['Label'] for c in chars])
    print('OBI groups dropped for placeholders', dropped, flush=True)
    write('OBI', units)

# ---- CHN: Shijing characters per line (comma/period-separated clauses kept as one unit per stanza line)
def chn():
    j = json.load((D / 'shijing.json').open(encoding='utf-8'))
    units = []
    for poem in j:
        for line in poem['content']:
            s = [c for c in line if unicodedata.category(c).startswith('L')]
            if s: units.append(s)
    write('CHN', units)

ALL = dict(GRK=grk, HEB=heb, CHR=chr_, SUX=sux, EGY=egy, OBI=obi, CHN=chn)
if __name__ == '__main__':
    for k in (sys.argv[2:] or ALL): ALL[k]()
