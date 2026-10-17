"""Round 37 substrate fingerprint. See PROTOCOL.md.
Usage: python3 fingerprint.py <kuiper_djvu.txt> <jambu_repo> <dravidian_db_dir> <lexibank_ids_repo>"""
import sys, csv, re, json, random, unicodedata, collections, math
from pathlib import Path
import numpy as np
csv.field_size_limit(10 ** 9)
P = Path(__file__).resolve().parent
KUIPER, JAMBU, DRDB, IDS = map(Path, sys.argv[1:5])
NBOOT = 500

# ---------------- normalisation (identical for all sets) ----------------
MAP = {'ǯ': 'j', 'ǰ': 'j', 'č': 'c', 'ć': 'c', 'ž': 's', 'ś': 's', 'ṣ': 's', 'ʃ': 's', 'ɕ': 's', 'š': 's', 'ʂ': 's', 'ŋ': 'n', 'ñ': 'n', 'ṅ': 'n', 'ɲ': 'n', 'ṇ': 'n', 'ɳ': 'n',
       'ɖ': 'd', 'ḍ': 'd', 'ʈ': 't', 'ṭ': 't', 'ɭ': 'l', 'ḷ': 'l', 'ɽ': 'r', 'ɾ': 'r', 'ṛ': 'r', 'ʀ': 'r', 'ə': 'a', 'ɐ': 'a',
       'æ': 'a', 'ä': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ö': 'o', 'ø': 'o', 'ɪ': 'i', 'ɨ': 'i', 'ʊ': 'u', 'ü': 'u', 'ɟ': 'j', 'ʤ': 'j',
       'ʧ': 'c', 'ɣ': 'g', 'ɡ': 'g', 'β': 'b', 'ɸ': 'p', 'ð': 'd', 'θ': 't', 'χ': 'k', 'x': 'k', 'q': 'k', 'w': 'v', 'z': 's',
       'ʒ': 's', 'ʐ': 's', 'ɦ': 'h', 'ʰ': '', 'ʔ': '', 'ˀ': '', "'": '', 'ʼ': '', 'ː': '', ':': '', 'ḥ': 'h', 'ṁ': 'n', 'ṃ': 'n',
       'y': 'y', 'f': 'p'}


def norm(s, blind=False):
    s = (s or '').lower()
    out = []
    for ch in s:
        if ch in MAP: out.append(MAP[ch]); continue
        d = unicodedata.normalize('NFD', ch)
        base = d[0]
        out.append(MAP.get(base, base))
    s = ''.join(out)
    s = re.sub(r'[^a-z]', '', s)
    s = re.sub(r'([kgcjtdpb])h', r'\1', s)
    if blind: s = s.translate(str.maketrans('bdgj', 'ptkc'))
    return s


# ---------------- data ----------------
def kuiper_words():
    lines = open(KUIPER, encoding='utf-8').read().split('\n')
    start = next(i for i, l in enumerate(lines) if l.strip().startswith('1. aks'))
    end = next(i for i, l in enumerate(lines) if i > start and 'EPILOGUE AND CONCLUSION' in l)
    block = ' '.join(l for l in lines[start:end] if not re.fullmatch(r'\s*\d+\s*', l))
    block = re.sub(r'\([^)]*\)', ' ', block)                       # verse refs / glosses
    block = block.replace('$', 'ś')
    chunks = re.split(r'\b\d{1,3}[a-z]?\.\s|\bS\.\s|\b1[0-9]S\.\s', block)
    words = []
    for c in chunks:
        for part in re.split(r'-\.\s|\.\s|,\s', c):
            part = part.strip().strip('.').strip(',')
            for tok in part.split():
                t = tok.strip('-.,;:!?')
                t = re.sub(r'(?<=[a-zA-Zāīūḱ])1(?=[a-zA-Z])', 'ī', t)      # OCR 1 for ī
                t = re.sub(r'(?<=[kstbp])f', 'ṛ', t)                       # OCR f for ṛ
                if len(re.sub(r'[^A-Za-zÀ-ɏḀ-ỿ]', '', t)) >= 2 and not t.isupper() and not re.search(r'\d', t):
                    words.append(t); break
    seen, out = set(), []
    for w in words:
        n = norm(w)
        if len(n) >= 2 and n not in seen and n not in ('etc', 'cf', 'see'): seen.add(n); out.append(w)
    return out


RVTAG = {}
def cdial_headwords():
    hw = {}
    for r in csv.reader(open(JAMBU / 'data/cdial/cdial.csv', encoding='utf-8')):
        if r[0] == 'Indo-Aryan' and r[8].endswith(':') and r[1] not in hw:
            hw[r[1]] = r[2]; RVTAG[r[1]] = bool(re.search(r'\bRV\b', r[6] or ''))
    return hw


def inherited(hw, exclude):
    # DEVIATION (before scoring): JAMBU etymologies.csv has PIE etymologies for only 2 entries, so INHERITED =
    # Rigveda-attested CDIAL OIA headwords minus Kuiper words and Dravidian loans (background Vedic vocabulary).
    ex = {norm(w) for w in exclude}
    return [w for k, w in hw.items() if RVTAG.get(k) and not w.startswith('*') and norm(w) not in ex]


def dravloans(hw):
    out = []
    for r in csv.DictReader(open(JAMBU / 'data/cross-family-comparisons.csv', encoding='utf-8')):
        if r['Relation'] == 'loan' and r['Direction'] == 'entry-from-compared' and r['Compared_Entry_ID'].startswith('d'):
            k = r['Entry_ID']
            if k in hw and not hw[k].startswith('*'): out.append(hw[k])
    return out


def lex_pdr():
    out = []
    for r in csv.DictReader(open(DRDB / 'pdr_04.csv', encoding='utf-8')):
        f = r['reconstruction'] or ''
        if not f or '[' in f: continue
        out.append(re.split(r'\s*[~,/;]\s*', f)[0])
    return out


def lex_munda():
    return [r[2] for r in csv.reader(open(JAMBU / 'data/munda/forms.csv', encoding='utf-8')) if len(r) > 2 and r[2] and r[2] != '—']


def ids_lang(names):
    langs = {r['ID'] for r in csv.DictReader(open(IDS / 'cldf/languages.csv', encoding='utf-8')) if r['Name'] in names}
    return [r['Form'] for r in csv.DictReader(open(IDS / 'cldf/forms.csv', encoding='utf-8')) if r['Language_ID'] in langs]


def lex_bur():
    b = [r[2] for r in csv.reader(open(JAMBU / 'data/other/forms/20220930-berger.csv', encoding='utf-8')) if len(r) > 2 and r[0] == 'Bur']
    return b + ids_lang({'Burushaski'})


# ---------------- model ----------------
def feats(w):
    s = '^' + w + '$'
    f = [s[i] for i in range(len(s))] + [s[i:i + 2] for i in range(len(s) - 1)]
    L = len(w); f.append('L<=3' if L <= 3 else 'L4-5' if L <= 5 else 'L6-7' if L <= 7 else 'L>=8')
    return f


class Model:
    def __init__(self, pos, neg):
        voc = collections.Counter(x for w in pos + neg for x in set(feats(w)))
        self.voc = {x: i for i, x in enumerate(sorted(k for k, c in voc.items() if c >= 2))}
        X = self.mat(pos + neg); y = np.array([1.0] * len(pos) + [0.0] * len(neg))
        wts = np.where(y == 1, len(y) / (2 * len(pos)), len(y) / (2 * len(neg)))
        b = np.zeros(X.shape[1]); c = 0.0; lam = 1.0
        for _ in range(400):
            p = 1 / (1 + np.exp(-(X @ b + c)))
            g = X.T @ ((p - y) * wts) / len(y) + lam * b / len(y)
            gc = ((p - y) * wts).mean()
            b -= 0.5 * g; c -= 0.5 * gc
        self.b, self.c = b, c
    def mat(self, ws):
        X = np.zeros((len(ws), len(self.voc)))
        for r, w in enumerate(ws):
            for x in feats(w):
                if x in self.voc: X[r, self.voc[x]] += 1
        return X
    def logodds(self, ws):
        return self.mat(ws) @ self.b + self.c


def run(target, inh_train, lexicons, blind, label, seed):
    T = sorted({norm(w, blind) for w in target} - {''}); I = sorted({norm(w, blind) for w in inh_train} - {''})
    L = {k: sorted({norm(w, blind) for w in v} - {''}) for k, v in lexicons.items()}
    def delta(m):
        base = m.logodds(L['IA-HELDOUT']).mean()
        return {k: float(m.logodds(v).mean() - base) for k, v in L.items() if k != 'IA-HELDOUT'}
    obs = delta(Model(T, I))
    rng = random.Random(seed); ranks = collections.Counter(); beats = collections.Counter(); boots = []
    fams = ['PDR', 'MUNDA', 'BUR', 'EUS', 'FIN']
    for _ in range(NBOOT):
        d = delta(Model([rng.choice(T) for _ in T], [rng.choice(I) for _ in I])); boots.append(d)
        top = max(fams, key=lambda k: d[k]); ranks[top] += 1
        for k in fams:
            if d[k] > d['EUS'] and d[k] > d['FIN']: beats[k] += 1
    res = dict(label=label, blind=blind, n_target=len(T), n_inherited_train=len(I), n_lex={k: len(v) for k, v in L.items()},
               delta_observed=obs, p_rank1={k: ranks[k] / NBOOT for k in fams}, p_beats_controls={k: beats[k] / NBOOT for k in fams},
               ci95={k: [float(np.percentile([b[k] for b in boots], q)) for q in (2.5, 97.5)] for k in fams})
    print(f"== {label} ({'criterion-blind' if blind else 'primary'}): target {len(T)} words, inherited-train {len(I)}")
    for k in sorted(fams, key=lambda k: -obs[k]):
        print(f"   {k:6s} dF={obs[k]:+.3f}  CI{res['ci95'][k][0]:+.2f}..{res['ci95'][k][1]:+.2f}  P(rank1)={res['p_rank1'][k]:.2f}  P(>controls)={res['p_beats_controls'][k]:.2f}")
    return res


def main():
    hw = cdial_headwords(); kw = kuiper_words(); dl = dravloans(hw)
    inh = inherited(hw, kw + dl); rng = random.Random(37001); rng.shuffle(inh)
    inh_train, inh_held = inh[:len(inh) // 2], inh[len(inh) // 2:]
    lex = {'PDR': lex_pdr(), 'MUNDA': lex_munda(), 'BUR': lex_bur(), 'EUS': ids_lang({'Basque'}), 'FIN': ids_lang({'Finnish'}), 'IA-HELDOUT': inh_held}
    (P / 'kuiper_parsed.txt').write_text('\n'.join(f'{w}\t{norm(w)}' for w in kw), encoding='utf-8')
    (P / 'dravloans.txt').write_text('\n'.join(f'{w}\t{norm(w)}' for w in dl), encoding='utf-8')
    print('kuiper', len(kw), '| dravloans', len(dl), '| inherited', len(inh), '| lexicons', {k: len(v) for k, v in lex.items()})
    out = {}
    out['control_primary'] = run(dl, inh_train, lex, False, 'POSITIVE CONTROL: Dravidian loans', 37100)
    out['control_blind'] = run(dl, inh_train, lex, True, 'POSITIVE CONTROL: Dravidian loans', 37101)
    c = out['control_primary']['p_rank1']; out['control_PASS'] = c['PDR'] >= 0.9
    print('CONTROL', 'PASS' if out['control_PASS'] else 'FAIL')
    out['foreign_primary'] = run(kw, inh_train, lex, False, 'KUIPER foreign words', 37200)
    out['foreign_blind'] = run(kw, inh_train, lex, True, 'KUIPER foreign words', 37201)
    def verdict(r):
        for k in ['PDR', 'MUNDA', 'BUR', 'EUS', 'FIN']:
            if r['p_rank1'][k] >= 0.9 and r['p_beats_controls'][k] >= 0.95: return k
        return None
    m, mb = verdict(out['foreign_primary']), verdict(out['foreign_blind'])
    out['decision'] = ('UNINTERPRETABLE (control failed)' if not out['control_PASS'] else
                       f'MATCH {m}' + (' (criterion-robust)' if mb == m else ' (not criterion-robust)') if m else 'NO SINGLE FAMILY MATCHES')
    print('DECISION', out['decision'])
    (P / 'results.json').write_text(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
