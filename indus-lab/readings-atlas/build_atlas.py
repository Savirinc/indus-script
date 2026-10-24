"""Readings atlas: every inscribed object in the Tejesh Raut / ICIT corpus read with the expanded Yajnadevam (atlas) mapping,
rendered in Brahmi, with a machine Sanskrit dictionary match and the same method under a scrambled key.
DESCRIPTIVE PRODUCT, NOT A TEST AND NOT A DECIPHERMENT. Stdlib only.
Usage: python3 -I build_atlas.py OUT_DIR     (writes atlas.html and ledger.csv; the PDF is printed from atlas.html)
Needs ../../ext/dcs/dictionary.csv (DCS, CC BY 4.0) and ../../ext/fonts (Noto Sans Brahmi; lipi Indus webfont sk_indus_script-webfont.ttf restored from the owner's archive, unlicensed: local use only)."""
import sys, json, csv, re, html, random, statistics, unicodedata, collections
from pathlib import Path
P = Path(__file__).resolve().parent; LAB = P.parent; ROOT = LAB.parent
sys.path.insert(0, str(LAB / 'round47')); sys.path.insert(0, str(LAB / 'round58'))
import run47 as R          # read_v (Yajnadevam's vowel rule), shuffle_key
import extract58 as X      # sk_phon (IAST segmenter)
R46 = LAB / 'round46-brahmi-coverage'
SHUF_SEED = 46901; N_SHUF = 20

# ---------- data ----------
KEY = json.load(open(R46 / 'expanded-map.json'))
s = open(R46 / 'texts.js', encoding='utf-8').read(); J = json.loads(s[s.index('{'):s.rindex('}') + 1])
COLS = J['columns']; OBJ = {r[0]: dict(zip(COLS, r)) for r in J['rows']}
CAND = json.load(open(R46 / 'candidate-readings.json'))
GLYPH = {}
for l in open(R46 / 'glyphs.tsv', encoding='utf-8'):
    a = l.rstrip('\n').split('\t')
    if len(a) == 2 and a[0].isdigit() and a[1]: GLYPH[a[0].zfill(3)] = a[1].split()[0]

def signs_of(c):
    t = c['text_code'] or ''
    seq = re.findall(r'\d{3}', t)
    return seq[::-1] if c['direction'] == 'R/L' else seq

# ---------- reading and Brahmi ----------
def iast(v): return v.replace('aa', 'ā').replace('A', 'ā').replace('ii', 'ī')
def reading(tokens):
    """Yajnadevam's rule (round 47 read_v) on each run of assigned tokens; unknown signs shown as '?'."""
    out, run = [], []
    for t in tokens + [None]:
        if t is None or t == '?':
            if run: out.append(iast(R.read_v(run)))
            run = []
            if t == '?': out.append('?')
        else: run.append(t)
    return out
BV = dict(zip(['a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'e', 'ai', 'o', 'au'], range(0x11005, 0x11013)))
BS = {'ā': 0x11038, 'i': 0x1103A, 'ī': 0x1103B, 'u': 0x1103C, 'ū': 0x1103D, 'ṛ': 0x1103E, 'ṝ': 0x1103F, 'ḷ': 0x11040,
      'ḹ': 0x11041, 'e': 0x11042, 'ai': 0x11043, 'o': 0x11044, 'au': 0x11045}
BC = dict(zip(['k', 'kh', 'g', 'gh', 'ṅ', 'c', 'ch', 'j', 'jh', 'ñ', 'ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ', 't', 'th', 'd', 'dh', 'n',
               'p', 'ph', 'b', 'bh', 'm', 'y', 'r', 'l', 'v', 'ś', 'ṣ', 's', 'h'], range(0x11013, 0x11034)))
VIRAMA, ANUSVARA, VISARGA = 0x11046, 0x11001, 0x11002
def brahmi(word):
    ph = X.sk_phon(word); out = []; i = 0
    while i < len(ph):
        sgm, k = ph[i]
        if k == 'C':
            out.append(chr(BC[sgm]))
            if i + 1 < len(ph) and ph[i + 1][1] == 'V':
                v = ph[i + 1][0]; i += 1
                if v != 'a': out.append(chr(BS[v]))
            else: out.append(chr(VIRAMA))
        elif k == 'V': out.append(chr(BV[sgm]))
        else: out.append(chr(ANUSVARA if sgm == 'ṃ' else VISARGA))
        i += 1
    return ''.join(out)

# ---------- dictionary match ----------
def norm(w):
    """The author groups sounds: compare without length, retroflexion, sibilant or nasal distinctions, or aspiration."""
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if not unicodedata.combining(c))
    w = re.sub(r'([kgcjtdpb])h', r'\1', w)
    return re.sub(r'[^a-z]', '', w)
DICT = {}
rd = csv.reader(open(ROOT / 'ext' / 'dcs' / 'dictionary.csv', encoding='utf-8'), delimiter='\t'); next(rd)
for r in rd:
    if len(r) >= 5 and r[1].strip() and r[4].strip():
        n = norm(r[1])
        if len(n) >= 3 and n not in DICT: DICT[n] = (r[1], r[4].split(';')[0].strip())
MAXW = 16
def segment(word):
    """Cover as many letters as possible with dictionary words (≥ 3 letters); ties: fewer words."""
    n = norm(word); L = len(n); best = [(0, 0, None)] * (L + 1)
    for i in range(1, L + 1):
        cand = [(best[i - 1][0], best[i - 1][1], None)]
        for j in range(max(0, i - MAXW), i - 2):
            if n[j:i] in DICT: cand.append((best[j][0] + i - j, best[j][1] - 1, (j, n[j:i])))
        best[i] = max(cand, key=lambda x: (x[0], x[1]))
    words, i = [], L
    while i > 0:
        if best[i][2]: j, w = best[i][2]; words.append(DICT[w]); i = j
        else: i -= 1
    return words[::-1], best[L][0], L
def gloss(parts):
    ws, cov, tot = [], 0, 0
    for p in parts:
        if p == '?': continue
        w, c, t = segment(p); ws += w; cov += c; tot += t
    return ws, (cov / tot if tot else 0.0)

# ---------- labels ----------
TYPE = {'SEAL:S': 'square seal', 'SEAL:R': 'rectangular seal', 'SEAL': 'seal', 'TAB:B': 'moulded tablet', 'TAB:I': 'incised tablet',
        'TAB:C': 'copper tablet', 'POT:T:g': 'pottery graffito', 'TAG': 'tag / sealing', 'SLG': 'sealing'}
MOTIF = {'Bull1': 'unicorn', 'Bult': 'short-horned bull', 'Gaur': 'gaur (bison)', 'Swas': 'swastika', 'Elep': 'elephant',
         'Rhin': 'rhinoceros', 'Tigr': 'tiger', 'Buff': 'water buffalo', 'Goat': 'goat', 'None': 'no motif'}
def motif(m):
    if not m: return '—'
    base = m.split(':')[0]; return MOTIF.get(base, m)

def main(outdir):
    outdir = Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    recs = [c for c in CAND if signs_of(c)]
    for c in recs: c['signs'] = signs_of(c)
    # scrambled keys: round 47 structure-preserving shuffle, frequency bins over all records
    texts = [[s for s in c['signs'] if s in KEY] for c in recs]
    signs = sorted({s for t in texts for s in t}); bins = R.freq_bins(texts, signs)
    shuf = [R.shuffle_key({s: KEY[s] for s in signs}, bins, random.Random(SHUF_SEED + i)) for i in range(N_SHUF)]
    rows = []; cov_real = []; cov_shuf = [[] for _ in range(N_SHUF)]
    for c in recs:
        toks = [KEY.get(s, '?') for s in c['signs']]
        parts = reading(toks); ws, cov = gloss(parts); cov_real.append(cov)
        sparts0 = reading([shuf[0].get(s, '?') for s in c['signs']]); sws, scov = gloss(sparts0)
        for i in range(N_SHUF):
            cov_shuf[i].append(cov if False else gloss(reading([shuf[i].get(s, '?') for s in c['signs']]))[1])
        o = OBJ.get(c['id'], {})
        rows.append(dict(id=c['id'], cisi=(c['cisi'] or '').strip(' <>'), site=c['site'], type=TYPE.get(o.get('type', ''), o.get('type', '') or '—'),
                         motif=motif(o.get('symbol', '')), material=o.get('material', '') or '', direction=c['direction'] or 'unknown',
                         complete=o.get('complete', ''), signs=c['signs'], values=toks, reading=' '.join(parts),
                         brahmi=' '.join(brahmi(p) if p != '?' else '?' for p in parts),
                         words=[f'{w} — {g}' for w, g in ws], coverage=cov,
                         s_reading=' '.join(sparts0), s_words=[f'{w} — {g}' for w, g in sws], s_coverage=scov,
                         unknown=toks.count('?')))
    rows.sort(key=lambda r: (r['site'], r['cisi'], r['id']))
    m_real = statistics.mean(cov_real); m_sh = [statistics.mean(x) for x in cov_shuf]
    summary = dict(records=len(rows), fully_assigned=sum(1 for r in rows if r['unknown'] == 0),
                   coverage_real=m_real, coverage_shuffled_mean=statistics.mean(m_sh), coverage_shuffled_sd=statistics.stdev(m_sh),
                   coverage_shuffled_min=min(m_sh), coverage_shuffled_max=max(m_sh),
                   shuffles_at_or_above_real=sum(1 for x in m_sh if x >= m_real), dictionary_entries=len(DICT))
    json.dump(summary, open(outdir / 'summary.json', 'w'), indent=1)
    print(json.dumps(summary, indent=1))
    with open(outdir / 'ledger.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['record_id', 'cisi', 'site', 'object', 'motif', 'material', 'direction', 'signs_reading_order', 'values', 'reading_iast',
                    'reading_brahmi', 'dictionary_words', 'dictionary_coverage', 'scrambled_key_reading', 'scrambled_key_words',
                    'scrambled_key_coverage', 'unassigned_signs'])
        for r in rows:
            w.writerow([r['id'], r['cisi'], r['site'], r['type'], r['motif'], r['material'], r['direction'], ' '.join(r['signs']),
                        ' '.join(r['values']), r['reading'], r['brahmi'], ' | '.join(r['words']), f"{r['coverage']:.2f}",
                        r['s_reading'], ' | '.join(r['s_words']), f"{r['s_coverage']:.2f}", r['unknown']])
    write_html(outdir / 'atlas.html', rows, summary)

def write_html(path, rows, S):
    e = html.escape; fonts = (ROOT / 'ext' / 'fonts').resolve()
    def card(r):
        gl = ''.join(f'<span title="{s}">&#x{GLYPH[s]};</span>' if s in GLYPH else f'<span class="nog">[{s}]</span>' for s in r['signs'])
        words = '<br>'.join(e(x) for x in r['words']) or '<i>no dictionary word found</i>'
        swords = '; '.join(e(x) for x in r['s_words'][:3]) or '<i>no word</i>'
        flag = f'<span class="flag">{r["unknown"]} sign(s) without a value</span>' if r['unknown'] else ''
        return f'''<div class="card"><div class="hd"><b>{e(r["cisi"] or "#" + str(r["id"]))}</b> · {e(r["site"])} · {e(r["type"])} · motif: {e(r["motif"])}<span class="rid">record {r["id"]} · {e(r["direction"])}</span></div>
<div class="row"><div class="ind">{gl}</div><div class="codes">{e(" · ".join(r["signs"]))}<br>values: {e(" · ".join(r["values"]))} {flag}</div></div>
<div class="row"><div class="bra">{e(r["brahmi"])}</div><div class="rom">{e(r["reading"])}</div></div>
<div class="gl"><span class="lab">Dictionary match (machine, DCS; not a translation) · {r["coverage"]:.0%} of letters:</span><br>{words}</div>
<div class="sc"><span class="lab">Same method, scrambled key:</span> {e(r["s_reading"])} · {r["s_coverage"]:.0%} · {swords}</div></div>'''
    cards = '\n'.join(card(r) for r in rows)
    front = f'''<section class="front"><h1>Indus inscriptions read with the Indus–Brahmi atlas mapping</h1>
<p class="sub">Every inscribed object with a sign sequence in the Tejesh Raut / ICIT corpus ({S["records"]:,} records), read with the expanded Yajnadevam mapping (714 signs) of <i>Indus-Brahmi-Full-Mapping-Atlas.pdf</i>. Built 24 October 2026 for Arham Partap Jain. Local document, not for distribution: the sign drawings use an unlicensed font.</p>
<div class="warn"><b>Status: this is not a decipherment.</b> It shows what the atlas mapping produces when applied to every inscription, nothing more. The mapping has failed every controlled test run on it (rounds 47, 57 and 59 of the Indus lab: its readings fit Sanskrit no better than readings from shuffled versions of the same key). The English lines are machine dictionary matches, not meanings.</div>
<h2>The check printed on every card</h2>
<p>Each card also shows what the <b>same method</b> produces with a <b>scrambled key</b>: the same sign values, randomly reassigned among signs of similar frequency. If the atlas mapping were right, its readings should contain far more real Sanskrit words than scrambled readings do.</p>
<table><tr><th></th><th>Share of letters covered by dictionary words (average over all records)</th></tr>
<tr><td>Atlas mapping</td><td><b>{S["coverage_real"]:.1%}</b></td></tr>
<tr><td>20 scrambled keys</td><td>mean <b>{S["coverage_shuffled_mean"]:.1%}</b> (range {S["coverage_shuffled_min"]:.1%}–{S["coverage_shuffled_max"]:.1%}); {S["shuffles_at_or_above_real"]} of 20 at or above the atlas mapping</td></tr></table>
<p>Dictionary: Digital Corpus of Sanskrit (Hellwig, CC BY 4.0), {S["dictionary_entries"]:,} headwords of three or more letters, compared the way the mapping's author groups sounds (no vowel length, retroflexion, sibilant or nasal distinctions, or aspiration). The reading splits into words covering as many letters as possible.</p>
<h2>How to read a card</h2><ol>
<li><b>Header:</b> CISI catalogue number, site, kind of object, animal motif, record number and writing direction.</li>
<li><b>Signs</b> as drawn in the lipi Indus font, in reading order (left to right here; most originals run right to left), with ICIT sign numbers and the atlas values. <b>No photographs:</b> the CISI photographs are copyrighted and are not reproduced.</li>
<li><b>Brahmi</b> rendering of the reading (Noto Sans Brahmi) and its romanisation, built with the mapping author's own vowel rule.</li>
<li><b>Dictionary match:</b> Sanskrit headwords found inside the reading, with the first English sense.</li>
<li><b>Scrambled key:</b> the same steps with values shuffled. Compare the two.</li></ol>
<p>{S["fully_assigned"]:,} of {S["records"]:,} records have a value for every sign; the rest show “?” for damaged or unassigned signs. Records are not independent texts: duplicates (for example, moulded tablets from one mould) appear separately. Sorted by site, then CISI number. The same data is in <code>ledger.csv</code>.</p></section>'''
    css = f'''@font-face{{font-family:IndusW;src:url("{(fonts / 'sk_indus_script-webfont.ttf').as_uri()}")}}
@font-face{{font-family:Indus;src:url("{(fonts / 'indus-font.ttf').as_uri()}")}}
@font-face{{font-family:Brahmi;src:url("{(fonts / 'NotoSansBrahmi-Regular.ttf').as_uri()}")}}
@font-face{{font-family:NS;src:url("{(fonts / 'NotoSans[wdth,wght].ttf').as_uri()}")}}
@page{{size:A4;margin:12mm 12mm 14mm 12mm;@bottom-center{{content:counter(page);font:8pt NS}}}}
body{{font-family:NS,sans-serif;font-size:8.6pt;color:#1a1a1a;margin:0}}
.front{{page-break-after:always}} h1{{font-size:17pt;margin:0 0 4mm}} h2{{font-size:11pt;margin:5mm 0 2mm}} .sub{{color:#444}}
.warn{{border:1.5pt solid #b33;background:#fdf3f2;padding:3mm;margin:4mm 0}} table{{border-collapse:collapse}} td,th{{border:.5pt solid #999;padding:1.5mm 2.5mm;text-align:left}}
.card{{border:.6pt solid #888;border-radius:2mm;padding:2.2mm 3mm;margin:0 0 2.6mm;height:58mm;overflow:hidden;page-break-inside:avoid;box-sizing:border-box}}
.hd{{font-size:8.4pt;border-bottom:.4pt solid #ccc;padding-bottom:1mm;margin-bottom:1.2mm}} .rid{{float:right;color:#777}}
.row{{display:flex;align-items:center;gap:5mm;margin:1mm 0}} .ind{{font-family:IndusW,Indus;font-size:25pt;line-height:1.1;min-width:60mm}}
.codes{{font-size:7.6pt;color:#555}} .bra{{font-family:Brahmi;font-size:20pt;min-width:60mm}} .rom{{font-size:11pt;font-style:italic}}
.gl{{font-size:7.8pt;margin-top:1mm;max-height:13mm;overflow:hidden}} .sc{{font-size:7.2pt;color:#666;margin-top:1mm;border-top:.4pt dashed #ccc;padding-top:.8mm;max-height:7mm;overflow:hidden}}
.lab{{color:#777}} .flag{{color:#b33;margin-left:2mm}} .nog{{font-size:8pt;font-family:NS}}'''
    path.write_text(f'<!doctype html><html><head><meta charset="utf-8"><title>Indus readings atlas</title><style>{css}</style></head><body>{front}{cards}</body></html>', encoding='utf-8')

if __name__ == '__main__':
    main(sys.argv[1])
