"""Round 39: sound+meaning donor attribution. See PROTOCOL.md.
Usage: python3 semantic_attribution.py <kuiper_djvu.txt> <jambu_repo> <dravidian_db_dir> <lexibank_ids_repo>"""
import sys, csv, re, json, random, collections
from pathlib import Path
import numpy as np
from rapidfuzz.distance import Levenshtein
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round37'))
import fingerprint as F
csv.field_size_limit(10 ** 9)
FAMS = ['PDR', 'MUNDA', 'BUR', 'EUS', 'FIN']
STOP = set('a an the of to in on at and or with for by from as is be being used made etc esp e g i also sp species kind sort type part '
           'thing name names person man woman one small large big great little good bad very much many some any other certain particular'.split())


def stems(gloss):
    out = set()
    for t in re.findall(r'[a-z]+', (gloss or '').lower()):
        if t in STOP or len(t) < 3: continue
        for suf in ('ing', 'es', 'ed', 'ly', 's'):
            if t.endswith(suf) and len(t) - len(suf) >= 3: t = t[:-len(suf)]; break
        out.add(t)
    return out


def cvshape(w):
    return ''.join('V' if c in 'aeiou' else 'C' for c in w)


def cdial_glossed():
    """normalised OIA headword -> (raw, set of stems); plus rv flag."""
    g = collections.defaultdict(set); raw = {}; rv = {}
    for r in csv.reader(open(F.JAMBU / 'data/cdial/cdial.csv', encoding='utf-8')):
        if r[0] == 'Indo-Aryan' and r[8].endswith(':') and not r[2].startswith('*'):
            n = F.norm(r[2])
            if not n: continue
            g[n] |= stems(r[3]); raw.setdefault(n, r[2]); rv[n] = rv.get(n, False) or bool(re.search(r'\bRV\b', r[6] or ''))
    return g, raw, rv


def lexicons():
    L = {f: [] for f in FAMS}
    for r in csv.DictReader(open(F.DRDB / 'pdr_04.csv', encoding='utf-8')):
        f = (r['reconstruction'] or ''); m = r['meaning'] or ''
        if f and m and '[' not in f: L['PDR'].append((F.norm(re.split(r'\s*[~,/;]\s*', f)[0]), stems(m)))
    for r in csv.reader(open(F.JAMBU / 'data/munda/forms.csv', encoding='utf-8')):
        if len(r) > 3 and r[2] and r[2] != '—': L['MUNDA'].append((F.norm(r[2]), stems(r[3])))
    for r in csv.reader(open(F.JAMBU / 'data/other/forms/20220930-berger.csv', encoding='utf-8')):
        if len(r) > 3 and r[0] == 'Bur': L['BUR'].append((F.norm(r[2]), stems(r[3])))
    langs = {r['ID']: r['Name'] for r in csv.DictReader(open(F.IDS / 'cldf/languages.csv', encoding='utf-8')) if r['Name'] in ('Basque', 'Finnish')}
    pn = {r['ID']: r['Name'] for r in csv.DictReader(open(F.IDS / 'cldf/parameters.csv', encoding='utf-8'))}
    for r in csv.DictReader(open(F.IDS / 'cldf/forms.csv', encoding='utf-8')):
        if r['Language_ID'] in langs:
            L['EUS' if langs[r['Language_ID']] == 'Basque' else 'FIN'].append((F.norm(r['Form']), stems(pn.get(r['Parameter_ID'], ''))))
    for f in L:  # merge duplicates, drop empty
        m = collections.defaultdict(set)
        for w, s in L[f]:
            if w and s: m[w] |= s
        L[f] = list(m.items())
    return L


class Index:
    def __init__(self, lex):
        self.by = collections.defaultdict(set)
        for i, (w, s) in enumerate(lex):
            for t in s: self.by[t].add(i)
        self.lex = lex
    def best(self, w, st):
        cand = set().union(*[self.by.get(t, set()) for t in st]) if st else set()
        return max(((Levenshtein.normalized_similarity(w, self.lex[i][0]), self.lex[i][0]) for i in cand), default=(0.0, None))


def attribution(targets, background, idx, label):
    """targets/background: list of (norm word, stems)."""
    rng = random.Random(39001); byshape = collections.defaultdict(list); bylen = collections.defaultdict(list)
    for w, s in background: byshape[cvshape(w)].append((w, s)); bylen[len(w)].append((w, s))
    d = {f: [] for f in FAMS}; pairs = {f: [] for f in FAMS}; cache = {}
    def m(f, w, s):
        k = (f, w)
        if k not in cache: cache[k] = idx[f].best(w, s)
        return cache[k]
    for w, s in targets:
        pool = [x for x in byshape.get(cvshape(w), []) if x[0] != w]
        if len(pool) < 5: pool = [x for x in bylen.get(len(w), []) if x[0] != w]
        bg = rng.sample(pool, min(5, len(pool)))
        for f in FAMS:
            sc, mw = m(f, w, s)
            d[f].append(sc - np.mean([m(f, bw, bs)[0] for bw, bs in bg]))
            if mw: pairs[f].append((round(sc, 3), w, mw))
    d = {f: np.array(v) for f, v in d.items()}
    A = {f: float(d[f].mean()) for f in FAMS}
    rb = np.random.default_rng(39002); n = len(targets); boots = []
    for _ in range(1000):
        ix = rb.integers(0, n, n); boots.append({f: d[f][ix].mean() for f in FAMS})
    p1 = {f: sum(max(FAMS, key=lambda k: b[k]) == f for b in boots) / 1000 for f in FAMS}
    pc = {f: sum(b[f] > b['EUS'] and b[f] > b['FIN'] for b in boots) / 1000 for f in FAMS}
    ci = {f: [float(np.percentile([b[f] for b in boots], q)) for q in (2.5, 97.5)] for f in FAMS}
    print(f'== {label}: {n} glossed target words')
    for f in sorted(FAMS, key=lambda k: -A[k]):
        print(f'   {f:6s} A={A[f]:+.4f}  CI {ci[f][0]:+.4f}..{ci[f][1]:+.4f}  P(rank1)={p1[f]:.2f}  P(>both controls)={pc[f]:.2f}')
    return dict(label=label, n=n, A=A, ci95=ci, p_rank1=p1, p_beats_controls=pc,
                top_pairs={f: sorted(pairs[f], reverse=True)[:30] for f in FAMS})


def main():
    g, raw, rv = cdial_glossed()
    hw = F.cdial_headwords(); kw = F.kuiper_words(); dl = F.dravloans(hw)
    K = sorted({F.norm(w) for w in kw} - {''}); D = sorted({F.norm(w) for w in dl} - {''})
    Kg = [(w, g[w]) for w in K if g.get(w)]; Dg = [(w, g[w]) for w in D if g.get(w)]
    excl = set(K) | set(D)
    B = [(w, s) for w, s in g.items() if rv.get(w) and s and w not in excl]
    L = lexicons(); idx = {f: Index(L[f]) for f in FAMS}
    print('glossed: kuiper', len(Kg), 'of', len(K), '| dravloans', len(Dg), 'of', len(D), '| background', len(B), '| lexicons', {f: len(v) for f, v in L.items()})
    out = {'counts': dict(kuiper_glossed=len(Kg), kuiper_total=len(K), drav_glossed=len(Dg), background=len(B), lex={f: len(v) for f, v in L.items()})}
    out['control'] = attribution(Dg, B, idx, 'POSITIVE CONTROL: Dravidian loans')
    c = out['control']; out['control_PASS'] = c['p_rank1']['PDR'] >= 0.9 and c['ci95']['PDR'][0] > 0
    print('CONTROL', 'PASS' if out['control_PASS'] else 'FAIL')
    out['kuiper'] = attribution(Kg, B, idx, 'KUIPER foreign words')
    k = out['kuiper']
    if not out['control_PASS']: dec = 'UNINTERPRETABLE (control failed)'
    else:
        best = [f for f in FAMS if k['p_rank1'][f] >= 0.9 and k['ci95'][f][0] > 0 and k['p_beats_controls'][f] >= 0.95]
        sec = [f for f in FAMS if f not in best and k['ci95'][f][0] > 0 and k['p_beats_controls'][f] >= 0.95]
        dec = (f'BEST-SUPPORTED DONOR: {best[0]}' if best else 'NO FAMILY ATTRIBUTABLE') + (f'; secondary: {sec}' if sec else '')
    out['decision'] = dec; print('DECISION', dec)
    (P / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False, default=list))


if __name__ == '__main__':
    main()
