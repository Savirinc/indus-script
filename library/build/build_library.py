"""Build the library: copy the raw sources, write the clean inscriptions table, render the PDFs.
Run from the repo root: python3 library/build/build_library.py. Needs Google Chrome (headless) for the PDFs.
Never edits indus-lab/raw or indus-lab/external; it only copies from them."""
import csv, hashlib, html, re, shutil, subprocess, sys, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]; LIB = ROOT / 'library'; BUILD = LIB / 'build'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
FONTS = ROOT / 'ext' / 'fonts'                       # local only (git-ignored); the Indus font is unlicensed
BUILT = '29 October 2026'

SOURCES = {                                          # folder -> files copied unchanged
    '01-icit-lipi': ['indus-lab/raw/inscriptions.csv', 'indus-lab/raw/LICENSE', 'indus-lab/raw/README.md'],
    '02-bourdeau-cyphersolver': ['indus-lab/raw/corpus.tsv', 'indus-lab/raw/corpus_m77_added.tsv', 'indus-lab/raw/glyphs.tsv',
                                 'indus-lab/raw/icit_m77_map.tsv', 'indus-lab/raw/population-script.sql',
                                 'indus-lab/LICENSE-DATA-GPL-3.txt'],
    '03-mayig-cisi': ['indus-lab/raw/cisi_mayig.tsv', 'indus-lab/raw/cisi_signs.tsv'],
    '04-explorer-snapshot': ['indus-lab/round46-brahmi-coverage/texts.js'],
    '05-dravidian-db-v1.1': ['indus-lab/external/dravidian_db_v1.1'],
    '06-cdli-dilmun-meluhha': ['data/derived/dil.txt', 'data/derived/dilmeta.txt', 'data/derived/dilp.txt',
                               'data/derived/ctx.txt', 'data/derived/hits.txt'],
    '07-kuiper-1991-words': ['data/derived/kuiper1991_ch5_words.txt'],
}

def copy_sources():
    for folder, items in SOURCES.items():
        dst = LIB / 'raw' / folder; dst.mkdir(parents=True, exist_ok=True)
        for it in items:
            src = ROOT / it
            if src.is_dir(): shutil.copytree(src, dst / src.name, dirs_exist_ok=True)
            else: shutil.copy2(src, dst / src.name)
    lines = []
    for p in sorted((LIB / 'raw').rglob('*')):
        if p.is_file() and p.name != 'SHA256SUMS' and p.name != '.DS_Store':
            lines.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(LIB / "raw")}')
    (LIB / 'raw' / 'SHA256SUMS').write_text('\n'.join(lines) + '\n')

def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]

def records():
    rows = list(csv.DictReader((ROOT / 'indus-lab/raw/inscriptions.csv').open(encoding='utf-8')))
    out = []
    for r in rows:
        out.append(dict(icit_id=r['id'], cisi=r['cisi'].strip(), site=r['site'].strip(), region=r['region'].strip(),
                        object_type=r['type'].strip(), material=r['material'].strip(), shape=r['shape'].strip(),
                        direction=r['dir.'].strip().upper(), complete=r['complete'].strip(), sign_count=r['text length'].strip(),
                        text=r['text'].strip(), notes=(r['notes'] or '').strip()))
    out.sort(key=lambda x: (x['site'], natkey(x['cisi']), natkey(x['icit_id'])))
    for i, x in enumerate(out, 1): x['no'] = i
    return out

def write_table(recs):
    d = LIB / 'inscriptions'; d.mkdir(parents=True, exist_ok=True)
    cols = ['no', 'cisi', 'icit_id', 'site', 'region', 'object_type', 'material', 'shape', 'direction', 'complete', 'sign_count', 'text', 'notes']
    with (d / 'inscriptions.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(recs)

GLYPH = {}
for l in (ROOT / 'indus-lab/raw/glyphs.tsv').open(encoding='utf-8'):
    a = l.rstrip('\n').split('\t')
    if len(a) == 2 and a[0].isdigit() and a[1]: GLYPH[a[0].zfill(3)] = a[1].split()[0]

KIND = {'SEAL': 'seal', 'TAB': 'tablet', 'POT': 'pottery', 'TAG': 'tag/sealing', 'MISC': 'other', 'BNGL': 'bangle', 'ROD': 'rod',
        'IMPL': 'implement', 'BEAD': 'bead', 'MDLN': 'medallion'}

def text_html(t, glyphs):
    e = html.escape
    if not glyphs: return '<span class="num">' + e(t).replace('/', ' / ') + '</span>'
    parts = re.split(r'(\d{3})', t); out = []
    for p in parts:
        if re.fullmatch(r'\d{3}', p):
            out.append(f'<span class="g" title="{p}">&#x{GLYPH[p]};</span>' if p in GLYPH and p != '000' else '<span class="miss">?</span>')
        elif '/' in p: out.append('<span class="br">/</span>')
    return '<span class="ind">' + ''.join(out) + '</span><br><span class="num sm">' + e(t).replace('/', ' / ') + '</span>'

def catalogue_html(recs, glyphs):
    e = html.escape; by_site = collections.OrderedDict()
    for x in recs: by_site.setdefault(x['site'], []).append(x)
    idx = ''.join(f'<tr><td>{e(s)}</td><td class="r">{len(v):,}</td><td class="r">{v[0]["no"]:,}–{v[-1]["no"]:,}</td></tr>' for s, v in by_site.items())
    body = []
    for s, v in by_site.items():
        rows = ''.join(
            f'<tr><td class="r">{x["no"]}</td><td><b>{e(x["cisi"])}</b></td><td class="mut">{e(x["icit_id"])}</td>'
            f'<td>{e(KIND.get(x["object_type"].split(":")[0], x["object_type"]))}<span class="mut"> {e(x["object_type"])}</span></td>'
            f'<td>{e(x["material"] if x["material"] != "-" else "")}</td><td>{e(x["direction"] if x["direction"] != "-" else "")}</td>'
            f'<td class="txt">{text_html(x["text"], glyphs)}</td></tr>' for x in v)
        body.append(f'<h2>{e(s)} <span class="mut">({len(v):,} records, nos. {v[0]["no"]:,}–{v[-1]["no"]:,})</span></h2>'
                    f'<table class="cat"><thead><tr><th>No.</th><th>Seal / object no. (CISI)</th><th>ICIT</th><th>Object</th>'
                    f'<th>Material</th><th>Dir.</th><th>Signs {"(drawn, then numbers)" if glyphs else "(sign numbers)"}</th></tr></thead><tbody>{rows}</tbody></table>')
    n_obj = len({x['cisi'] for x in recs}); title = 'Indus inscriptions: complete catalogue' + (' with signs' if glyphs else '')
    licence = ('<p class="warn"><b>Local copy, not for distribution.</b> The sign drawings use the lipi Indus webfont, which has no licence. '
               'The public edition (sign numbers only) is <code>library/pdf/Indus-Inscriptions-Catalogue.pdf</code>.</p>' if glyphs else '')
    front = f'''<section class="front"><h1>{title}</h1>
<p class="sub">Every record in the Interactive Corpus of Indus Texts export used by this project: {len(recs):,} records (inscribed sides or faces) from {n_obj:,} catalogue numbers at {len(by_site)} sites. Built {BUILT} for Arham Partap Jain, from <code>indus-lab/raw/inscriptions.csv</code> (sha256 c22d39c3…3429) by <code>library/build/build_library.py</code>.</p>{licence}
<h3>How to read a row</h3><ul>
<li><b>No.</b> is this catalogue's running number, 1 to {len(recs):,}, sorted by site and then catalogue number. The same numbers are in <code>library/inscriptions/inscriptions.csv</code>.</li>
<li><b>Seal / object no.</b> is the CISI number (<i>Corpus of Indus Seals and Inscriptions</i>, Joshi &amp; Parpola 1987; Shah &amp; Parpola 1991; Parpola, Pande &amp; Koskikallio 2010). Its prefix names the site: M = Mohenjo-daro, H = Harappa, L = Lothal, K = Kalibangan, and so on. One object with writing on several sides has one CISI number and several records. A dash (–) means the object has no CISI number; use its ICIT number.</li>
<li><b>ICIT</b> is the record number in the Interactive Corpus of Indus Texts (Wells &amp; Fuls). The part after the dot is the side.</li>
<li><b>Object</b> is the ICIT type code: SEAL (S square, R rectangular, C cylinder…), TAB tablet, POT inscribed pottery, TAG sealing or tag, and so on.</li>
<li><b>Dir.</b> is the writing direction recorded by ICIT. R/L is right to left, the usual direction of the script; L/R is left to right; NR means not recorded; T/B is top to bottom.</li>
<li><b>Signs</b> are ICIT sign numbers, in the order the corpus stores them. <code>+</code> at an end means the text is complete there; <code>[</code> or <code>]</code> means the object is broken there; <code>/</code> is a new line; <b>000</b> is a sign that cannot be read or identified.</li></ul>
<p><b>Left out on purpose:</b> the upstream "sanskrit" and "translation" columns. They are one researcher's proposed readings, not facts about the texts. Rounds 46–47 of this project tested that key and found its output no more language-like than its own shuffles. No photographs are reproduced, because the CISI plates are under copyright.</p>
<p><b>Duplicates.</b> Records are not independent texts. Many tablets were pressed from one mould, and many seals repeat the same text.</p>
<h3>Sites</h3><table class="idx"><tr><th>Site</th><th>Records</th><th>Nos.</th></tr>{idx}</table>
<p class="mut">Data: yajnadevam/lipi export of ICIT and Mahadevan data, MIT licence (Copyright 2024 Michael Carlson); see <code>library/raw/01-icit-lipi/</code>.</p></section>'''
    face = (f'@font-face{{font-family:IndusW;src:url("{(FONTS / "sk_indus_script-webfont.ttf").as_uri()}")}}'
            f'@font-face{{font-family:Indus;src:url("{(FONTS / "indus-font.ttf").as_uri()}")}}' if glyphs else '')
    css = face + '''@page{size:A4;margin:12mm 11mm 14mm 11mm;@bottom-center{content:counter(page) " / " counter(pages);font:7.5pt "Helvetica Neue",Arial,sans-serif;color:#666}}
body{font-family:"Helvetica Neue",Arial,sans-serif;font-size:8pt;color:#111;margin:0}
h1{font-size:18pt;margin:0 0 3mm} h2{font-size:11pt;margin:5mm 0 1.5mm;break-after:avoid} h3{font-size:10pt;margin:4mm 0 1mm}
.front{break-after:page} .sub{font-size:9pt;color:#333} ul{padding-left:5mm} li{margin:0 0 1mm}
.warn{border:1.2pt solid #b33;background:#fdf3f2;padding:2.5mm}
code{font-size:7.5pt;background:#f3f3f3;padding:0 .8mm}
table{border-collapse:collapse;width:100%} th{background:#eee;text-align:left;font-size:7.4pt}
td,th{border-bottom:.4pt solid #ccc;padding:.7mm 1.2mm;vertical-align:top} tr{break-inside:avoid}
.idx{width:auto} .idx td,.idx th{padding:.4mm 3mm} .r{text-align:right} .mut{color:#777;font-weight:normal}
.cat thead{display:table-header-group} .num{font-family:Menlo,monospace;font-size:7.6pt} .sm{font-size:6.6pt;color:#555}
.ind{font-family:IndusW,Indus;font-size:17pt;line-height:1.15} .miss{font-size:9pt;color:#b33;padding:0 1mm} .br{color:#999;padding:0 1.5mm}
.txt{width:''' + ('46%' if glyphs else '36%') + '}'
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{css}</style></head><body>{front}{"".join(body)}</body></html>'

def print_pdf(src, pdf):
    pdf.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--allow-file-access-from-files',
                    f'--print-to-pdf={pdf}', src.as_uri()], check=True, capture_output=True, timeout=900)
    print('wrote', pdf.relative_to(ROOT), f'{pdf.stat().st_size / 1e6:.1f} MB')

def main():
    copy_sources(); recs = records(); write_table(recs)
    (LIB / 'local').mkdir(exist_ok=True)
    tmp = LIB / 'local' / 'catalogue.html'; tmp.write_text(catalogue_html(recs, False), encoding='utf-8')
    print_pdf(tmp, LIB / 'pdf' / 'Indus-Inscriptions-Catalogue.pdf')
    if (FONTS / 'indus-font.ttf').exists():
        loc = LIB / 'local'; loc.mkdir(exist_ok=True); t2 = loc / 'catalogue-signs.html'
        t2.write_text(catalogue_html(recs, True), encoding='utf-8')
        print_pdf(t2, loc / 'Indus-Inscriptions-Catalogue-with-signs.pdf')
    print_pdf(BUILD / 'language-and-history.html', LIB / 'pdf' / 'Indus-Language-and-History.pdf')

if __name__ == '__main__':
    main()
