"""Round 58: syllabifiers (S1 akṣara, S2 phonological) and unit-file builder. See PROTOCOL.md.
  python3 -I extract58.py --check          syllabifier check (must be 40/40)
  python3 -I extract58.py RAWDIR           build controls/*.txt from fetch58.py output"""
import sys, re, csv, unicodedata, collections
from pathlib import Path
P = Path(__file__).resolve().parent

# ---------- Sanskrit (IAST) ----------
SK_V = ['ai', 'au', 'a', 'ā', 'i', 'ī', 'u', 'ū', 'ṛ', 'ṝ', 'ḷ', 'ḹ', 'e', 'o']
SK_C = ['kh', 'gh', 'ch', 'jh', 'ṭh', 'ḍh', 'th', 'dh', 'ph', 'bh',
        'k', 'g', 'ṅ', 'c', 'j', 'ñ', 'ṭ', 'ḍ', 'ṇ', 't', 'd', 'n', 'p', 'b', 'm', 'y', 'r', 'l', 'v', 'ś', 'ṣ', 's', 'h']
SK_M = ['ṃ', 'ḥ']
SK_TOK = sorted([(x, 'V') for x in SK_V] + [(x, 'C') for x in SK_C] + [(x, 'M') for x in SK_M], key=lambda t: -len(t[0]))

def sk_norm(w):
    w = unicodedata.normalize('NFC', w.lower()).replace('ṁ', 'ṃ').replace('ṝ', 'ṝ')
    return w

def sk_phon(w):
    """IAST word -> list of (segment, kind); unknown characters dropped and counted."""
    w = sk_norm(w); out = []; i = 0; drop = 0
    while i < len(w):
        for s, k in SK_TOK:
            if w.startswith(s, i): out.append((s, k)); i += len(s); break
        else: drop += 1; i += 1
    sk_phon.dropped += drop
    return out
sk_phon.dropped = 0

def ta_phon(w):
    """Tamil-script word -> (list of graphemes, list of (segment, kind) per grapheme)."""
    w = unicodedata.normalize('NFC', w); gs = []; i = 0
    while i < len(w):
        ch = w[i]
        if ch in TA_CONS:
            g = ch; i += 1
            if i < len(w) and (w[i] in TA_SIGN or w[i] == '்'): g += w[i]; i += 1
            gs.append(g)
        elif ch in TA_VOW or ch == 'ஃ': gs.append(ch); i += 1
        else: ta_phon.dropped += 1; i += 1
    segs = []
    for g in gs:
        if g == 'ஃ': segs.append([('ḵ', 'C')])
        elif g[0] in TA_VOW: segs.append([(TA_VOW[g[0]], 'V')])
        elif len(g) == 1: segs.append([(TA_CONS[g], 'C'), ('a', 'V')])
        elif g[1] == '்': segs.append([(TA_CONS[g[0]], 'C')])
        else: segs.append([(TA_CONS[g[0]], 'C'), (TA_SIGN[g[1]], 'V')])
    return gs, segs
ta_phon.dropped = 0
TA_CONS = dict(zip('கஙசஞடணதநபமயரலவழளறனஜஷஸஹஶ',
                   ['k', 'ṅ', 'c', 'ñ', 'ṭ', 'ṇ', 't', 'n', 'p', 'm', 'y', 'r', 'l', 'v', 'ḻ', 'ḷ', 'ṟ', 'ṉ', 'j', 'ṣ', 's', 'h', 'ś']))
TA_VOW = dict(zip('அஆஇஈஉஊஎஏஐஒஓஔ', ['a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'ē', 'ai', 'o', 'ō', 'au']))
TA_SIGN = dict(zip('ாிீுூெேைொோௌ',
                   ['ā', 'i', 'ī', 'u', 'ū', 'e', 'ē', 'ai', 'o', 'ō', 'au']))

def s1_from_phon(ph):
    """Akṣara: cluster + vowel, ṃ/ḥ attach left, word-final consonant cluster one unit."""
    units = []; onset = ''
    for s, k in ph:
        if k == 'C': onset += s
        elif k == 'V': units.append(onset + s); onset = ''
        else:  # M
            if onset: units.append(onset); onset = ''
            if units: units[-1] += s
            else: units.append(s)
    if onset: units.append(onset)
    return units

def s2_from_phon(ph):
    """Phonological syllable: first consonant of a medial cluster is a coda; ṃ/ḥ and final consonants are codas."""
    nuc = [i for i, (s, k) in enumerate(ph) if k == 'V']
    if not nuc: return [''.join(s for s, _ in ph)] if ph else []
    cuts = []  # index where each syllable after the first starts
    for a, b in zip(nuc, nuc[1:]):
        mids = [j for j in range(a + 1, b) if ph[j][1] == 'C']
        cuts.append(mids[1] if len(mids) >= 2 else (mids[0] if mids else b))
    bounds = [0] + cuts + [len(ph)]
    return [''.join(s for s, _ in ph[x:y]) for x, y in zip(bounds, bounds[1:])]

def sk_syl(word, mode):
    ph = sk_phon(word)
    return s1_from_phon(ph) if mode == 'S1' else s2_from_phon(ph)

def ta_syl(word, mode):
    gs, segs = ta_phon(word)
    if mode == 'S1': return [''.join(s for s, _ in g) for g in segs]   # one unit per written grapheme
    return s2_from_phon([x for g in segs for x in g])

# ---------- check (PROTOCOL.md, 40 words) ----------
SK_CHECK = """agnim a·gni·m ag·nim; yajñasya ya·jña·sya yaj·ñas·ya; purohitam pu·ro·hi·ta·m pu·ro·hi·tam; indraḥ i·ndraḥ in·draḥ;
kṛṣṇa kṛ·ṣṇa kṛṣ·ṇa; rāmāyaṇam rā·mā·ya·ṇa·m rā·mā·ya·ṇam; saṃskṛtam saṃ·skṛ·ta·m saṃs·kṛ·tam; aśvaḥ a·śvaḥ aś·vaḥ;
devam de·va·m de·vam; vāk vā·k vāk; hotāram ho·tā·ra·m ho·tā·ram; ṛtvijam ṛ·tvi·ja·m ṛt·vi·jam; bhaktiḥ bha·ktiḥ bhak·tiḥ;
vaiśvānaraḥ vai·śvā·na·raḥ vaiś·vā·na·raḥ; auṣadhī au·ṣa·dhī au·ṣa·dhī; sūktam sū·kta·m sūk·tam; jyotiḥ jyo·tiḥ jyo·tiḥ;
mitrāvaruṇā mi·trā·va·ru·ṇā mit·rā·va·ru·ṇā; gāyatrī gā·ya·trī gā·yat·rī; brahman bra·hma·n brah·man"""
TA_CHECK = """அறம் a·ṟa·m a·ṟam; பொருள் po·ru·ḷ po·ruḷ; இன்பம் i·ṉ·pa·m iṉ·pam; தமிழ் ta·mi·ḻ ta·miḻ; கண்ணி ka·ṇ·ṇi kaṇ·ṇi;
கொன்றை ko·ṉ·ṟai koṉ·ṟai; வேந்தன் vē·n·ta·ṉ vēn·taṉ; பாடல் pā·ṭa·l pā·ṭal; சேரமான் cē·ra·mā·ṉ cē·ra·māṉ;
ஔவையார் au·vai·yā·r au·vai·yār; நிலம் ni·la·m ni·lam; விசும்பு vi·cu·m·pu vi·cum·pu; தீ tī tī; நீரும் nī·ru·m nī·rum;
ஐம்பெரும் ai·m·pe·ru·m aim·pe·rum; ஞாயிறு ñā·yi·ṟu ñā·yi·ṟu; பெருஞ்சோற்று pe·ru·ñ·cō·ṟ·ṟu pe·ruñ·cōṟ·ṟu;
உதியன் u·ti·ya·ṉ u·ti·yaṉ; பாஅல் pā·a·l pā·al; முடிநாகராயர் mu·ṭi·nā·ka·rā·ya·r mu·ṭi·nā·ka·rā·yar"""

def check():
    ok = 0; n = 0
    for spec, f in [(SK_CHECK, sk_syl), (TA_CHECK, ta_syl)]:
        for item in spec.replace('\n', ' ').split(';'):
            w, e1, e2 = item.split()
            for mode, exp in [('S1', e1), ('S2', e2)]:
                got = '·'.join(f(w, mode)); good = got == unicodedata.normalize('NFC', exp)
                print(('ok  ' if good else 'FAIL'), mode, w, got, '' if good else f'(expected {exp})')
            n += 1; ok += all('·'.join(f(w, m)) == unicodedata.normalize('NFC', e) for m, e in [('S1', e1), ('S2', e2)])
    print(f'syllabifier check: {ok}/{n} words correct in both modes')
    return ok == n

# ---------- builders ----------
IAST_OK = re.compile(r"[^a-zāīūṛṝḷḹṃḥṅñṭḍṇśṣṁ]")
TA_OK = re.compile(r'[^஀-௿ ]')

def dcs_sentences(folder):
    for f in sorted(folder.glob('*.conllu')):
        sent = []
        for line in f.open(encoding='utf-8'):
            line = line.rstrip('\n')
            if not line.strip():
                if sent: yield sent; sent = []
                continue
            if line.startswith('#'): continue
            c = line.split('\t')
            if len(c) < 6 or not c[0].isdigit(): continue     # skip multi-word ranges and empty nodes
            form = IAST_OK.sub('', unicodedata.normalize('NFC', c[1].lower()))
            if form: sent.append((form, 'Case=Cpd' in c[5]))
        if sent: yield sent

def words_of(sent):
    """Re-join compound members (Case=Cpd) with the next token."""
    out = []; buf = ''
    for form, cpd in sent:
        buf += form
        if not cpd: out.append(buf); buf = ''
    if buf: out.append(buf)
    return out

NAME_EXCL = ['work', 'metre', 'meter', 'plant', 'sāman', 'hymn', 'chapter', 'section', 'treatise', 'commentary',
             'verse', 'letter', 'particular', 'text']

def wiki_clean(s):
    s = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', s)
    s = re.sub(r'\{\{[^}]*\}\}', ' ', s); s = re.sub(r'<[^>]*>', ' ', s)
    s = re.sub(r'\([^)]*\)', ' ', s); s = re.sub(r'\[[^\]]*\]', ' ', s)
    return s

def build(raw):
    raw = Path(raw); out = P / 'controls'; out.mkdir(exist_ok=True)
    stats = {}
    def write(code, mode, lines):
        with (out / f'{code}_{mode}.txt').open('w', encoding='utf-8') as fh:
            for l in lines: fh.write(l + '\n')
        stats[f'{code}_{mode}'] = len(lines)
    sk_sents = {}
    for code, folder in [('RV', 'Ṛgveda'), ('RAM', 'Rāmāyaṇa')]:
        sk_sents[code] = [words_of(s) for s in dcs_sentences(raw / folder)]
    names = []
    rows = csv.reader((raw / 'dictionary.csv').open(encoding='utf-8'), delimiter='\t')
    next(rows)
    for r in rows:
        if len(r) < 5: continue
        first = r[4].split(';')[0].strip().lower()
        if first.startswith('name of') and not any(x in first for x in NAME_EXCL):
            w = IAST_OK.sub('', unicodedata.normalize('NFC', r[1].lower()))
            if w: names.append(w)
    names = sorted(set(names))
    lines_ta = []; names_ta = []
    marks = ['பாடியவர்', 'பாடப்பட்டோன்', 'பாடப்பட்டோர்', 'பாடப்பெற்றோர்']
    meta = marks + ['திணை', 'துறை']
    for f in sorted((raw / 'puram').glob('*.wiki')):
        if f.stem in ('புறநானூறு__1', 'புறநானூறு__2', 'புறநானூறு__3'): continue   # Amendment 1: duplicates of poems 1-3
        inpoem = False
        for line in f.open(encoding='utf-8'):
            if '<poem>' in line: inpoem = True; line = line.split('<poem>', 1)[1]
            closing = '</poem>' in line
            if closing: line = line.split('</poem>', 1)[0]
            if any(m in line for m in marks):
                body = wiki_clean(line).split(':', 1)[-1]
                for part in re.split(r'[,،]', body):
                    t = TA_OK.sub('', part).replace(' ', '')
                    if t and not any(m in t for m in marks): names_ta.append(t)
            elif any(m in line for m in meta): pass
            elif inpoem or (line.startswith('#') and not line.upper().startswith('#REDIRECT') and not line.startswith('#வழிமாற்று')):
                body = line[1:] if line.startswith('#') else line
                for seg in re.split(r'<br\s*/?>', body):
                    words = TA_OK.sub(' ', wiki_clean(seg)).split()
                    if words: lines_ta.append(words)
            if closing: inpoem = False
    names_ta = sorted(set(names_ta))
    for mode in ['S1', 'S2']:
        for code in ['RV', 'RAM']:
            write(code, mode, [' '.join(u for w in s for u in sk_syl(w, mode)) for s in sk_sents[code] if s])
        write('SKW', mode, [' | '.join(' '.join(sk_syl(w, mode)) for w in s) for c in ['RV', 'RAM'] for s in sk_sents[c] if s])
        write('SKN', mode, [' '.join(sk_syl(w, mode)) for w in names])
        write('PUR', mode, [' '.join(u for w in l for u in ta_syl(w, mode)) for l in lines_ta])
        write('TMW', mode, [' | '.join(' '.join(ta_syl(w, mode)) for w in l) for l in lines_ta])
        write('TMN', mode, [' '.join(ta_syl(w, mode)) for w in names_ta])
    print('unit counts', stats)
    print('dropped characters: sanskrit', sk_phon.dropped, 'tamil', ta_phon.dropped)
    print('Tamil names sample:', names_ta[:12]); print('Sanskrit names sample:', names[:12], len(names))

if __name__ == '__main__':
    if sys.argv[1] == '--check': sys.exit(0 if check() else 1)
    if not check(): sys.exit('syllabifier check failed; amend before building')
    build(sys.argv[1])
