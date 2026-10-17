#!/usr/bin/env python3
"""Build rebus_data word lists and Chinese control data. Run with python3 -I."""
import csv, json, re, sys, unicodedata, collections, os

csv.field_size_limit(10**9)
EXT = '/home/claude/ext'
SCR = '/tmp/claude-0/-home-claude/9c80a2c9-382f-522b-9621-b5cf62df3711/scratchpad'
OUT = SCR + '/rebus_data'
DRAV = SCR + '/indus/work/indus-lab/external/dravidian_db_v1.1'
UNIHAN = SCR + '/dl_unihan'
JAMBU = EXT + '/moli-mandala_data/data'

# ---------------- concepts: key -> (concepticon ids, english gloss keywords for raw dictionaries)
C = [
 ('fish', [227], ['fish']),
 ('man', [1554, 683, 1553], ['man', 'person', 'male', 'human being', 'human']),
 ('woman', [962], ['woman', 'female']),
 ('tree', [906], ['tree']),
 ('leaf', [628], ['leaf', 'leaves']),
 ('arrow', [977], ['arrow']),
 ('bow', [994, 3228], ['bow', 'bow (weapon)']),
 ('jar/pot', [4135, 1462, 2055, 3653], ['pot', 'jar', 'earthen pot', 'pitcher', 'cooking pot', 'water pot', 'pot (earthen)', 'water jar', 'earthenware pot']),
 ('mountain', [639, 2118], ['mountain', 'hill']),
 ('sun', [1343], ['sun']),
 ('moon', [1313], ['moon']),
 ('star', [1430], ['star']),
 ('water', [948], ['water']),
 ('river', [666, 3311], ['river']),
 ('fire', [221], ['fire']),
 ('house/roof', [1252, 769], ['house', 'roof', 'dwelling', 'hut']),
 ('field', [212], ['field', 'cultivated field', 'paddy field', 'rice field']),
 ('plough', [1921, 2154], ['plough', 'plow', 'plough (n)', 'plough (n.)']),
 ('boat', [1844], ['boat']),
 ('comb', [1475], ['comb', 'comb (n)']),
 ('bird', [937], ['bird']),
 ('bull/ox', [1008, 1169, 1153], ['bull', 'ox', 'bullock']),
 ('cow', [1007], ['cow']),
 ('goat', [1502], ['goat', 'she-goat', 'he-goat']),
 ('dog', [2009], ['dog']),
 ('elephant', [1290], ['elephant']),
 ('rhinoceros', [2591], ['rhinoceros', 'rhino']),
 ('tiger', [846], ['tiger']),
 ('snake', [730], ['snake', 'serpent']),
 ('crab', [2348], ['crab']),
 ('scorpion', [1538], ['scorpion']),
 ('frog', [503], ['frog']),
 ('turtle', [112, 895], ['turtle', 'tortoise']),
 ('knife', [1352], ['knife']),
 ('rope', [1218], ['rope', 'cord']),
 ('wheel', [710], ['wheel']),
 ('eye', [1248], ['eye']),
 ('hand', [1277], ['hand']),
 ('foot', [1301], ['foot']),
 ('head', [1256], ['head']),
 ('horn', [1393], ['horn']),
 ('mouth', [674], ['mouth']),
 ('tooth', [1380], ['tooth', 'teeth']),
 ('bone', [1394], ['bone']),
 ('egg', [744], ['egg']),
 ('grain/seed', [605, 714], ['grain', 'seed', 'seeds', 'corn']),
 ('plant', [653], ['plant']),
 ('flower', [239], ['flower', 'blossom']),
 ('fig tree', [322, 346], ['fig', 'fig tree', 'banyan', 'banyan tree', 'ficus', 'ficus religiosa', 'ficus indica', 'ficus bengalensis', 'pipal', 'peepal', 'pipal tree', 'sacred fig']),
 ('honey', [942], ['honey']),
 ('rain', [658, 2108], ['rain']),
 ('stone', [857, 2125], ['stone', 'rock']),
 ('gold', [1369], ['gold']),
 ('net', [2963, 2653, 388], ['net', 'fishing net', 'fishing-net']),
 ('drum', [908], ['drum']),
 ('one', [1493], ['one']), ('two', [1498], ['two']), ('three', [492], ['three']),
 ('four', [1500], ['four']), ('five', [493], ['five']), ('six', [1703], ['six']),
 ('seven', [1704], ['seven']), ('eight', [1705], ['eight']), ('nine', [1483], ['nine']),
 ('ten', [1515], ['ten']),
]
KEYS = [c[0] for c in C]
CID2KEY = {}
for k, ids, _ in C:
    for i in ids:
        CID2KEY[str(i)] = k
KW2KEY = {}
for k, _, kws in C:
    for w in kws:
        KW2KEY[w] = k

def gloss_key(gloss):
    """Exact-segment gloss match. Returns concept key or None. Only the first sense segment counts as primary."""
    g = gloss.lower()
    g = re.sub(r'<[^>]+>', '', g)
    segs = re.split(r'[;,/]|\s\|\s', g)
    hits = []
    for i, s in enumerate(segs):
        s = re.sub(r'\([^)]*\)', '', s).strip(' .\'"‘’“”:-')
        s = re.sub(r'^(a|an|the|to)\s+', '', s)
        s = re.sub(r'\s+\(?n\.?\)?$', '', s).strip()
        if s in KW2KEY:
            hits.append((i, KW2KEY[s]))
    return hits

# ---------------- simplifier
RETRO = {'ṭ': 'T', 'ḍ': 'D', 'ṇ': 'N', 'ḷ': 'L', 'ṛ': 'R', 'ṣ': 'S', 'ʈ': 'T', 'ɖ': 'D', 'ɳ': 'N', 'ɭ': 'L', 'ɽ': 'R', 'ʂ': 'S', 'ɻ': 'zh', 'ḻ': 'zh', 'ẓ': 'zh', 'ṟ': 'r', 'ṯ': 't', 'ṉ': 'n'}
OTHER = {'ñ': 'ny', 'ɲ': 'ny', 'ṅ': 'ng', 'ŋ': 'ng', 'ś': 'sh', 'ʃ': 'sh', 'š': 'sh', 'ž': 'zh', 'ʒ': 'zh', 'č': 'c', 'ʧ': 'c', 'ǰ': 'j', 'ʤ': 'j', 'ɟ': 'j',
         'ə': 'e', 'ɛ': 'e', 'ɔ': 'o', 'ɨ': 'i', 'ɯ': 'u', 'æ': 'ae', 'ɑ': 'a', 'ʌ': 'a', 'ɪ': 'i', 'ʊ': 'u', 'ʔ': '?', 'ˀ': '?', 'ʕ': '', 'ˤ': '', 'ɣ': 'gh', 'χ': 'x', 'ħ': 'h',
         'ɡ': 'g', 'ð': 'dh', 'θ': 'th', 'β': 'b', 'ɸ': 'f', 'ɬ': 'l', 'ɾ': 'r', 'ʁ': 'r', 'ʋ': 'v', 'ɦ': 'h', 'ç': 's', 'ʰ': 'h', 'ʷ': 'w', 'ʲ': 'y', 'ᵊ': 'e',
         'ḥ': 'h', 'ṃ': 'm', 'ṁ': 'm', 'ŕ': 'r', 'ł': 'l', 'ø': 'o', 'œ': 'oe', 'ü': 'u', 'ö': 'o', 'ä': 'a', 'ı': 'i', 'đ': 'd', 'ǯ': 'j', 'ʦ': 'ts', 'ʣ': 'dz', 'ć': 'c', 'ź': 'z', 'ɐ': 'a', 'γ': 'gh', 'ɒ': 'o', 'ɘ': 'e', 'ɵ': 'o', 'ʉ': 'u', 'ɤ': 'o', 'ɜ': 'e', 'ɞ': 'e', 'ʏ': 'u', 'ɮ': 'l', 'ʐ': 'zh', 'ɕ': 'sh', 'ʑ': 'zh', 'ɱ': 'm', 'ɴ': 'n', 'ʀ': 'r', 'ʎ': 'ly', 'ɥ': 'w', 'ɰ': 'w', 'ʝ': 'y', 'ɓ': 'b', 'ɗ': 'd', 'ʄ': 'j', 'ɠ': 'g', 'ɢ': 'g', 'ʡ': '?', 'ʢ': '', 'ⁿ': 'n', 'ᴀ': 'a', 'ɹ': 'r', 'ɺ': 'l', 'ʍ': 'w', 'ɧ': 'sh', 'ǝ': 'e', 'ɩ': 'i', 'ʸ': 'y', 'ᵐ': 'm', 'ᵑ': 'ng', 'ᵈ': 'd', 'ᵇ': 'b'}
LONGV = set('āēīōūȳĀĒĪŌŪ')

def simplify(s):
    if not s:
        return ''
    s = unicodedata.normalize('NFC', s).strip().lstrip('*').strip()
    s = re.split(r'[;,/~]', s)[0].strip().lstrip('*')
    s = re.sub(r'\([^)]*\)', '', s).strip()
    out = []
    for ch in s:
        if ch == '\u0323':
            if out and out[-1] and out[-1][-1].lower() in 'tdnlrscjz':
                out[-1] = out[-1][:-1] + out[-1][-1].upper()
            continue
        if unicodedata.combining(ch):
            if ch == '\u0304' and out and out[-1] and out[-1][-1] in 'aeiouy':
                out.append(out[-1][-1])
            continue
        if ch in RETRO or ch.lower() in RETRO:
            out.append(RETRO.get(ch) or RETRO[ch.lower()]); continue
        low = ch.lower()
        if low in OTHER:
            out.append(OTHER[low]); continue
        d = unicodedata.normalize('NFD', ch)
        base = d[0]
        if base in RETRO:
            out.append(RETRO[base]); continue
        if base.lower() in OTHER:
            out.append(OTHER[base.lower()]); continue
        if '̄' in d and base.lower() in 'aeiouy':   # macron
            out.append(base.lower() * 2); continue
        if '̣' in d:  # dot below on other letters
            out.append(base.upper() if base.lower() in 'tdnlrs' else base.lower()); continue
        if ch in 'ː:':
            if out and out[-1] and out[-1][-1] in 'aeiou':
                out.append(out[-1][-1])
            continue
        if base.isascii() and (base.isalpha()):
            out.append(base.lower()); continue
        if base in "?-":
            out.append(base); continue
        # drop everything else (combining marks, brackets, digits, etc.)
    r = ''.join(out).replace('-', '')
    return r

def write_tsv(path, rows):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept', 'form', 'form_ipa_or_simplified', 'source', 'notes'])
        order = {k: i for i, k in enumerate(KEYS)}
        rows = sorted(rows, key=lambda r: (order[r[0]], r[5] if len(r) > 5 else 0))
        seen = set()
        for r in rows:
            sig = (r[0], r[1], r[3])
            if sig in seen:
                continue
            seen.add(sig)
            w.writerow(r[:5])
    return rows

COVER = collections.OrderedDict()

def record(code, rows):
    COVER[code] = collections.Counter(r[0] for r in rows)

# ---------------- generic CLDF (lexibank) loader
def cldf_rows(repo, lang_ids, src_label, form_field='Form', seg_simplify=False, max_per=4):
    params = {}
    for p in csv.DictReader(open(f'{EXT}/{repo}/cldf/parameters.csv')):
        params[p['ID']] = (p.get('Concepticon_ID') or '', p.get('Name', ''))
    rows = []
    cnt = collections.Counter()
    for r in csv.DictReader(open(f'{EXT}/{repo}/cldf/forms.csv')):
        if r['Language_ID'] not in lang_ids:
            continue
        cid, pname = params.get(r['Parameter_ID'], ('', ''))
        k = CID2KEY.get(cid)
        via = f'concepticon {cid}'
        if not k and not cid:
            h = gloss_key(re.sub(r'^the ', '', pname))
            if h and h[0][0] == 0:
                k = h[0][1]; via = 'no Concepticon ID; matched on dataset gloss'
        if not k:
            continue
        cnt[k] += 1
        form = r.get(form_field) or r.get('Value')
        if seg_simplify:
            toks = [t.split('/')[0].rstrip('.') for t in (r.get('Segments') or '').split() if t != '+']
            simp = simplify(''.join(toks))
        else:
            simp = simplify(form)
        note = f'{via} ({pname}); lang {r["Language_ID"]}'
        if r.get('Loan', '').lower() == 'true':
            note += '; flagged loan'
        if cnt[k] > 1:
            note += '; alternative form'
        if cnt[k] > max_per:
            continue
        if repo == 'lexibank_sagartst':
            form = r['Value']; simp = simplify(form)
        rows.append([k, form, simp, f'{src_label} form {r["ID"]}', note, cnt[k]])
    return rows

# ---------------- 1. Proto-Dravidian
def build_pdr():
    rows = []
    pdr = list(csv.DictReader(open(f'{DRAV}/pdr_04.csv')))
    found = collections.defaultdict(list)
    for x in pdr:
        if x['source_classification'] != 'Proto-Dravidian':
            continue
        hits = gloss_key(x['meaning'])
        if not hits:
            continue
        pos, k = hits[0]
        rank = (0 if x['reference'].startswith('Krishnamurti') else 1, pos, int(x['number'] or 0))
        found[k].append((rank, x))
    for k, lst in found.items():
        lst.sort(key=lambda t: t[0])
        for i, (rank, x) in enumerate(lst[:4]):
            note = f'DEDR {x["number"]}; meaning "{x["meaning"][:60]}"; {x["reference"]}'
            note += '; PRIMARY (standard reconstruction)' if i == 0 else '; alternative PDr candidate'
            if rank[1] > 0:
                note += '; concept matched a non-first gloss sense'
            rows.append([k, x['reconstruction'], simplify(x['reconstruction']), f'dravidian_db_v1.1 pdr_04.csv id_pdr={x["id_pdr"]}', note, i])
    # Tamil fallback from DEDR
    missing = [k for k in KEYS if k not in found]
    tam = collections.defaultdict(list)
    for x in csv.DictReader(open(f'{DRAV}/dedr_entry_v11.csv')):
        if x['lang_str'] != 'Tamil':
            continue
        hits = gloss_key(x['entry_meaning'])
        if hits and hits[0][1] in missing and hits[0][0] == 0:
            tam[hits[0][1]].append(x)
    for k in missing:
        for i, x in enumerate(tam.get(k, [])[:3]):
            rows.append([k, x['entry_str'], simplify(x['entry_str']), f'dravidian_db_v1.1 dedr_entry_v11.csv entry_id={x["entry_id"]}',
                         f'FLAG: no PDr reconstruction matched; Tamil (DEDR {x["dedr_index_id"]}) "{x["entry_meaning"][:60]}"' + ('; alternative' if i else ''), 10 + i])
    rows = write_tsv(f'{OUT}/lang_pdr.tsv', rows)
    record('pdr', rows)

# ---------------- JAMBU raw source loader (gloss-matched)
def jambu_raw(files, langs, label_fn, primary_only=True):
    out = collections.defaultdict(list)
    for fn in files:
        for r in csv.reader(open(fn)):
            if len(r) < 4 or r[0] not in langs:
                continue
            hits = gloss_key(r[3])
            if not hits:
                continue
            pos, k = hits[0]
            if primary_only and pos != 0:
                continue
            src = r[7] if len(r) > 7 else ''
            out[r[0]].append((k, r[2], r[3], src, os.path.basename(fn), r[1]))
    return out

def build_munda():
    # Proto-Munda (Rau 2019) and daughters
    files = [f'{JAMBU}/munda/forms.csv'] + [f'{JAMBU}/other/forms/{f}.csv' for f in
             ['20260828-pinnow-munda', '20260828-munda-proto-kherwarian', '20260828-zide-sora-juray', '20260911-kharia-living']]
    got = jambu_raw(files, {'PMu', 'sa', 'mu', 'so', 'kh', 'PKher'}, None)
    asjp_map = {'sa': {'SANTALI'}, 'so': {'SORA'}, 'mu': {'MUNDARI'}, 'kh': {'KHARIA'}}
    names = {'PMu': 'pmu', 'sa': 'sat', 'mu': 'unr', 'so': 'srb', 'kh': 'khr', 'PKher': 'pkher'}
    for lang, code in names.items():
        rows = []
        cnt = collections.Counter()
        for (k, form, gloss, src, fn, pid) in got.get(lang, []):
            cnt[k] += 1
            if cnt[k] > 4:
                continue
            note = f'gloss "{gloss[:50]}" (exact-segment gloss match)'
            if lang == 'PMu':
                note = 'Rau 2019 Proto-Munda (via JAMBU); ' + note
            rows.append([k, form, simplify(form), f'JAMBU data/{"munda" if fn=="forms.csv" else "other/forms"}/{fn} [{src[:60]}] {pid}', note + ('' if cnt[k] == 1 else '; alternative'), cnt[k]])
        if lang in asjp_map:
            rows += [r[:4] + [r[4] + '; ASJP supplement'] + [100 + r[5]] for r in cldf_rows('lexibank_asjp', asjp_map[lang], 'lexibank/asjp', seg_simplify=True, max_per=2)]
        rows = write_tsv(f'{OUT}/lang_{code}.tsv', rows)
        record(code, rows)

def build_bur():
    got = jambu_raw([f'{JAMBU}/other/forms/20260726-yoshioka-eastern-burushaski.csv'], {'Bur'}, None)
    rows = []
    cnt = collections.Counter()
    for (k, form, gloss, src, fn, pid) in got.get('Bur', []):
        cnt[k] += 1
        if cnt[k] > 4:
            continue
        rows.append([k, form, simplify(form), f'JAMBU data/other/forms/{fn} [{src[:70]}]', f'Yoshioka 2012 Eastern Burushaski; gloss "{gloss[:50]}" (exact-segment gloss match)' + ('' if cnt[k] == 1 else '; alternative'), cnt[k]])
    rows += [r[:4] + [r[4] + '; ASJP supplement'] + [100 + r[5]] for r in cldf_rows('lexibank_asjp', {'BURUSHASKI'}, 'lexibank/asjp', seg_simplify=True, max_per=2)]
    rows = write_tsv(f'{OUT}/lang_bsk.tsv', rows)
    record('bsk', rows)

def build_cldf_langs():
    specs = [
        ('san', [('lexibank_ids', {'211'}, 'lexibank/ids', False)]),
        ('elx', [('lexibank_ids', {'216'}, 'lexibank/ids', False), ('lexibank_asjp', {'ELAMITE'}, 'lexibank/asjp', True)]),
        ('sux', [('lexibank_asjp', {'SUMERIAN'}, 'lexibank/asjp', True)]),
        ('eus', [('lexibank_ids', {'219'}, 'lexibank/ids', False)]),
        ('fin', [('lexibank_ids', {'128'}, 'lexibank/ids', False)]),
        ('jpn', [('lexibank_wold', {'Japanese'}, 'lexibank/wold', False)]),
        ('och', [('lexibank_sagartst', {'OldChinese'}, 'lexibank/sagartst (Baxter & Sagart 2014 via Sagart et al. 2019)', False),
                 ('lexibank_asjp', {'OLD_CHINESE'}, 'lexibank/asjp', True)]),
    ]
    for code, srcs in specs:
        rows = []
        for j, (repo, ids, label, seg) in enumerate(srcs):
            rs = cldf_rows(repo, ids, label, seg_simplify=seg)
            if j > 0:
                rs = [r[:4] + [r[4] + '; ASJP supplement'] + [100 + r[5]] for r in rs]
            rows += rs
        if code == 'och':
            # attach characters from sagartst raw
            hz = {}
            for r in csv.DictReader(open(f'{EXT}/lexibank_sagartst/raw/sino-tibetan-raw.tsv'), delimiter='\t'):
                if r['DOCULECT'] == 'Old_Chinese':
                    hz[r['ENTRY_IN_SOURCE'].strip()] = r['HANZI']
            for r in rows:
                if r[1] in hz:
                    r[4] += f'; hanzi {hz[r[1]]}'
            for r in rows:
                if r[1].startswith('*'):
                    pass
        rows = write_tsv(f'{OUT}/lang_{code}.tsv', rows)
        record(code, rows)

# ---------------- Chinese
def load_unihan():
    U = collections.defaultdict(dict)
    for fn in ['Unihan_Readings.txt', 'Unihan_DictionaryLikeData.txt', 'Unihan_Variants.txt', 'Unihan_IRGSources.txt']:
        for line in open(f'{UNIHAN}/{fn}', encoding='utf-8'):
            if line.startswith('#') or not line.strip():
                continue
            cp, field, val = line.rstrip('\n').split('\t', 2)
            if field in ('kMandarin', 'kTang', 'kCantonese', 'kDefinition', 'kHanyuPinlu', 'kGradeLevel', 'kPhonetic', 'kTraditionalVariant', 'kSimplifiedVariant', 'kTotalStrokes', 'kFanqie'):
                U[chr(int(cp[2:], 16))][field] = val
    return U

def load_phonoml():
    P = {}
    for r in csv.DictReader(open(f'{EXT}/alxdrdelaporte_yunpy/src/yunpy/sources/phonoML_characters.csv')):
        P[r['Character']] = r['Transcriptions']
    return P

def load_oc():
    oc = collections.defaultdict(list)
    for r in csv.DictReader(open(f'{EXT}/lexibank_sagartst/raw/sino-tibetan-raw.tsv'), delimiter='\t'):
        if r['DOCULECT'] == 'Old_Chinese' and r['HANZI'].strip():
            v = r['ENTRY_IN_SOURCE'].strip()
            for h in r['HANZI'].strip():
                if v not in oc[h]:
                    oc[h].append(v)
    return oc

def is_cjk(ch):
    o = ord(ch)
    return 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0x20000 <= o <= 0x3134F or 0xF900 <= o <= 0xFAFF

def build_chinese():
    U = load_unihan(); P = load_phonoml(); OC = load_oc()
    # corpus
    CP = f'{EXT}/chinese-poetry_chinese-poetry'
    lines, idx = [], []
    for r in json.load(open(f'{CP}/诗经/shijing.json')):
        t = ''.join(c for c in ''.join(r['content']) if is_cjk(c))
        lines.append(t); idx.append(('shijing', f'{r["chapter"]}/{r["section"]}/{r["title"]}', 'simplified (as published in chinese-poetry)'))
    for r in json.load(open(f'{CP}/论语/lunyu.json')):
        for i, p in enumerate(r['paragraphs']):
            t = ''.join(c for c in p if is_cjk(c))
            if t:
                lines.append(t); idx.append(('lunyu', f'{r["chapter"]}#{i+1}', 'simplified (as published in chinese-poetry)'))
    for name, fn in [('mengzi', 'mengzi'), ('daxue', 'daxue'), ('zhongyong', 'zhongyong')]:
        d = json.load(open(f'{CP}/四书五经/{fn}.json'))
        d = d if isinstance(d, list) else [d]
        for r in d:
            for i, p in enumerate(r['paragraphs']):
                t = ''.join(c for c in p if is_cjk(c))
                if t:
                    lines.append(t); idx.append((name, f'{r["chapter"]}#{i+1}', 'traditional'))
    # simplified -> traditional where Unihan gives a unique traditional variant
    amb = collections.Counter(); conv_lines = []
    for t, (src, _, script) in zip(lines, idx):
        if script.startswith('simplified'):
            o = []
            for c in t:
                tv = U.get(c, {}).get('kTraditionalVariant')
                if tv:
                    vs = [chr(int(x[2:], 16)) for x in tv.split()]
                    if len(vs) == 1:
                        o.append(vs[0])
                    else:
                        o.append(c if c in vs else vs[0]); amb[c] += 1
                else:
                    o.append(c)
            conv_lines.append(''.join(o))
        else:
            conv_lines.append(t)
    open(f'{OUT}/chinese_corpus.txt', 'w').write('\n'.join(lines) + '\n')
    open(f'{OUT}/chinese_corpus_trad.txt', 'w').write('\n'.join(conv_lines) + '\n')
    with open(f'{OUT}/chinese_corpus_index.tsv', 'w') as f:
        f.write('line\ttext\tlocator\tscript\tn_chars\n')
        for i, ((s, loc, sc), t) in enumerate(zip(idx, lines), 1):
            f.write(f'{i}\t{s}\t{loc}\t{sc}\t{len(t)}\n')
    with open(f'{OUT}/chinese_corpus_trad_ambiguous.tsv', 'w') as f:
        f.write('simplified\tcount\ttraditional_candidates(Unihan kTraditionalVariant)\n')
        for c, n in amb.most_common():
            f.write(f'{c}\t{n}\t{U[c]["kTraditionalVariant"]}\n')
    corpus_freq = collections.Counter(''.join(conv_lines))
    # character table: kGradeLevel (HK primary-school list) U kHanyuPinlu (frequency) U corpus chars (trad)
    chars = set(c for c, v in U.items() if 'kGradeLevel' in v or 'kHanyuPinlu' in v) | set(corpus_freq)
    def pinlu(c):
        v = U[c].get('kHanyuPinlu', '')
        return sum(int(x) for x in re.findall(r'\((\d+)\)', v))
    with open(f'{OUT}/chinese_chars.tsv', 'w') as f:
        f.write('char\tcodepoint\tmandarin\tcantonese\ttang\tmc_baxter_phonoml\tmc_fanqie_unihan\toc_baxter_sagart\tphonetic_kPhonetic\tgrade_level\thanyupinlu_freq\tcorpus_freq\tdefinition\n')
        for c in sorted(chars, key=lambda c: (-corpus_freq.get(c, 0), -pinlu(c), ord(c))):
            u = U.get(c, {})
            f.write('\t'.join([c, f'U+{ord(c):04X}', u.get('kMandarin', ''), u.get('kCantonese', ''), u.get('kTang', ''), P.get(c, ''), u.get('kFanqie', ''),
                               ' ; '.join(OC.get(c, [])), u.get('kPhonetic', ''), u.get('kGradeLevel', ''), str(pinlu(c)), str(corpus_freq.get(c, 0)),
                               u.get('kDefinition', '').replace('\t', ' ')]) + '\n')
    # phonetic series (kPhonetic, Casey 1980 classes) for all chars having it
    ser = collections.defaultdict(list)
    for c, u in U.items():
        for cls in u.get('kPhonetic', '').split():
            ser[cls].append(c)
    with open(f'{OUT}/chinese_phonetic_series.tsv', 'w') as f:
        f.write('kPhonetic_class\tn\tmembers\n')
        for cls in sorted(ser, key=lambda x: (int(re.match(r'\d+', x).group()), x)):
            f.write(f'{cls}\t{len(ser[cls])}\t{"".join(sorted(ser[cls], key=ord))}\n')
    # pictographs
    PIC = [
        ('fish', '魚', 'fish', ''), ('man', '人', 'person (side view)', ''), ('woman', '女', 'kneeling woman', ''),
        ('tree', '木', 'tree', ''), ('arrow', '矢', 'arrow', ''), ('bow', '弓', 'bow', ''),
        ('jar/pot', '缶', 'earthen jar', ''), ('jar/pot', '鬲', 'tripod cauldron', ''),
        ('mountain', '山', 'mountain (three peaks)', ''), ('sun', '日', 'sun', ''), ('moon', '月', 'crescent moon', ''),
        ('star', '晶', 'stars (original graph of 星)', '星 itself is phono-semantic (日/晶 + 生)'),
        ('water', '水', 'flowing water', ''), ('river', '川', 'river', ''), ('fire', '火', 'flames', ''),
        ('house/roof', '宀', 'roof/house', 'bound radical'), ('field', '田', 'field', ''),
        ('plough', '力', 'plough/digging stick', 'interpretation of 力 as plough is disputed'),
        ('boat', '舟', 'boat', ''), ('bird', '鳥', 'bird', ''), ('bird', '隹', 'short-tailed bird', ''),
        ('bull/ox', '牛', 'ox head', ''), ('goat', '羊', 'sheep/goat head', 'OC *ɢaŋ = sheep/goat'),
        ('dog', '犬', 'dog', ''), ('elephant', '象', 'elephant', ''), ('rhinoceros', '兕', 'rhinoceros/wild buffalo', 'identification debated'),
        ('tiger', '虎', 'tiger', ''), ('snake', '它', 'snake (original graph of 蛇)', ''), ('snake', '巳', 'snake/foetus', 'disputed'),
        ('scorpion', '萬', 'scorpion (original sense; borrowed for "ten thousand")', ''),
        ('frog', '黽', 'frog/toad', ''), ('turtle', '龜', 'turtle', ''), ('knife', '刀', 'knife', ''),
        ('wheel', '車', 'chariot (wheels+axle)', 'depicts chariot, not wheel alone'),
        ('eye', '目', 'eye', ''), ('hand', '手', 'hand', ''), ('hand', '又', 'right hand', ''),
        ('foot', '足', 'foot/leg', ''), ('foot', '止', 'foot(print)', ''), ('head', '首', 'head', ''), ('head', '頁', 'head on body', ''),
        ('horn', '角', 'horn', ''), ('mouth', '口', 'mouth', ''), ('tooth', '齒', 'teeth in mouth', 'later adds phonetic 止'),
        ('tooth', '牙', 'molar/tusk', ''), ('bone', '骨', 'bone (冎 + 肉)', 'core 冎 is the pictograph'),
        ('egg', '卵', 'egg/ovary', 'interpretation debated'), ('grain/seed', '禾', 'grain plant with ear', ''), ('grain/seed', '米', 'grains of rice', ''),
        ('plant', '屮', 'sprout/plant', ''), ('plant', '生', 'plant emerging from ground', 'compound pictograph'),
        ('flower', '華', 'flowering plant (original sense of 華)', ''), ('rain', '雨', 'rain from sky', ''),
        ('stone', '石', 'stone under cliff', ''), ('gold', '金', 'metal', 'graph origin debated; partly phonetic 今'),
        ('net', '网', 'net', ''), ('drum', '壴', 'drum on stand (original graph of 鼓)', ''), ('drum', '鼓', 'hand beating drum', 'compound'),
        ('one', '一', 'one stroke', 'indicative (指事), not pictograph'), ('two', '二', 'two strokes', 'indicative'), ('three', '三', 'three strokes', 'indicative'),
        ('four', '四', '', 'loan graph; original 亖'), ('five', '五', '', 'abstract/loan'), ('six', '六', '', 'loan graph'),
        ('seven', '七', '', 'loan graph'), ('eight', '八', '', 'loan graph (divide)'), ('nine', '九', '', 'loan graph'), ('ten', '十', '', 'indicative'),
        ('leaf', '', '', 'no standard pictograph (葉 is phono-semantic)'), ('cow', '', '', 'covered by 牛'), ('crab', '', '', 'no pictograph (蟹 phono-semantic)'),
        ('comb', '', '', 'no common pictograph (梳/櫛 phono-semantic)'), ('rope', '', '', 'no clear pictograph (糸 = silk thread)'),
        ('fig tree', '', '', 'none'), ('honey', '', '', 'none (蜜 phono-semantic)'),
    ]
    with open(f'{OUT}/chinese_pictographs.tsv', 'w') as f:
        f.write('concept\tchar\tdepicts\toc_baxter_sagart\tmc_baxter_phonoml\tmandarin\ttang\tnotes\n')
        for k, ch, dep, note in PIC:
            u = U.get(ch, {}) if ch else {}
            oc = ' ; '.join(OC.get(ch, [])) if ch else ''
            n = note
            if ch and not oc:
                n = (n + '; ' if n else '') + 'OC not in available BS-derived source (sagartst); use MC'
            f.write('\t'.join([k, ch, dep, oc, P.get(ch, '') if ch else '', u.get('kMandarin', ''), u.get('kTang', ''), n]) + '\n')
    print('corpus lines', len(lines), 'chars', sum(map(len, lines)), 'ambiguous simplified chars', sum(amb.values()), 'distinct', len(amb))
    print('char table', len(chars), 'with OC', sum(1 for c in chars if c in OC), 'with MC', sum(1 for c in chars if c in P))
    print('pictographs with OC', sum(1 for k, ch, _, _ in PIC if ch and ch in OC), 'of', sum(1 for p in PIC if p[1]))

def coverage():
    codes = list(COVER)
    with open(f'{OUT}/COVERAGE.md', 'w') as f:
        f.write('# Coverage matrix (number of forms per concept per language; blank = missing)\n\n')
        f.write('| concept | ' + ' | '.join(codes) + ' |\n|' + '---|' * (len(codes) + 1) + '\n')
        for k in KEYS:
            f.write(f'| {k} | ' + ' | '.join(str(COVER[c].get(k, '')) for c in codes) + ' |\n')
        f.write('| **concepts covered (of %d)** | ' % len(KEYS) + ' | '.join(str(len(COVER[c])) for c in codes) + ' |\n')
    for c in codes:
        print(c, len(COVER[c]), 'missing:', ','.join(k for k in KEYS if k not in COVER[c]))

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    build_pdr(); build_munda(); build_bur(); build_cldf_langs()
    build_chinese()
    coverage()
