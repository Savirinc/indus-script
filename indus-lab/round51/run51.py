#!/usr/bin/env python
"""Round 51: sound+meaning attribution of proposed Meluhhan loanwords. See PROTOCOL.md.
Run: ../../ext/venv/bin/python run51.py   (needs numpy, rapidfuzz; ext/moli-mandala_data, ext/lexibank_ids, indus-lab/external/dravidian_db_v1.1)"""
import sys, csv, re, json, random, collections, pathlib
HERE = pathlib.Path(__file__).resolve().parent; LAB = HERE.parent; ROOT = LAB.parent
sys.argv = ['x', str(ROOT / 'data' / 'kuiper.txt'), str(ROOT / 'ext' / 'moli-mandala_data'), str(LAB / 'external' / 'dravidian_db_v1.1'), str(ROOT / 'ext' / 'lexibank_ids')]
sys.path.insert(0, str(LAB / 'round37')); sys.path.insert(0, str(LAB / 'round39'))
import numpy as np
from rapidfuzz.distance import Levenshtein
import fingerprint as F
import semantic_attribution as S
csv.field_size_limit(10 ** 9)
FAMS = ['PDR', 'IA', 'MUNDA', 'BUR', 'EUS', 'FIN']
SEED_BG, SEED_BOOT = 51001, 51002

MITANNI = [  # G1: Indo-Aryan words in Hittite/Hurrian texts (Mayrhofer 1966; Witzel 2001)
 ('aika', 'one'), ('tera', 'three'), ('panza', 'five'), ('satta', 'seven'), ('nawa', 'nine'), ('wartanna', 'turn round course'),
 ('babru', 'brown'), ('parita', 'grey'), ('pinkara', 'reddish red'), ('maryannu', 'chariot warrior young man'), ('assussanni', 'horse trainer')]

def load_candidates():
    rows = []
    for l in open(HERE / 'candidates.tsv', encoding='utf-8'):
        if not l.strip() or l.startswith('#'): continue
        p = l.rstrip('\n').split('\t'); rows.append(dict(form=p[0], lang=p[1], gloss=p[2], kind=p[3]))
    return rows

def sumerian_background(exclude):
    bg = []
    for l in open(HERE / 'epsd2_lemmas.tsv', encoding='utf-8'):
        cf, gw, pos = l.rstrip('\n').split('\t')
        if pos != 'N': continue
        w = F.norm(cf); st = S.stems(gw)
        if len(w) >= 2 and st and w not in exclude: bg.append((w, st))
    return bg

def lexicons_with_ia(exclude_ia=()):
    L = S.lexicons()
    g, raw, rv = S.cdial_glossed()
    L['IA'] = [(w, s) for w, s in g.items() if s and w not in exclude_ia]
    return L, g, rv

def attribution(targets, background, idx, label, fams=FAMS):
    rng = random.Random(SEED_BG); byshape = collections.defaultdict(list); bylen = collections.defaultdict(list)
    for w, s in background: byshape[S.cvshape(w)].append((w, s)); bylen[len(w)].append((w, s))
    d = {f: [] for f in fams}; pairs = {f: [] for f in fams}; cache = {}; per = []
    def m(f, w, s):
        k = (f, w)
        if k not in cache: cache[k] = idx[f].best(w, s)
        return cache[k]
    for w, s in targets:
        pool = [x for x in byshape.get(S.cvshape(w), []) if x[0] != w]
        if len(pool) < 5: pool = [x for x in bylen.get(len(w), []) if x[0] != w]
        bg = rng.sample(pool, min(5, len(pool))); row = {'target': w}
        for f in fams:
            sc, mw = m(f, w, s); base = float(np.mean([m(f, bw, bs)[0] for bw, bs in bg])) if bg else 0.0
            d[f].append(sc - base); row[f] = dict(best=mw, sim=round(sc, 3), baseline=round(base, 3))
            if mw: pairs[f].append((round(sc, 3), w, mw))
        per.append(row)
    d = {f: np.array(v) for f, v in d.items()}; A = {f: float(d[f].mean()) for f in fams}
    rb = np.random.default_rng(SEED_BOOT); n = len(targets); boots = []
    for _ in range(1000):
        ix = rb.integers(0, n, n); boots.append({f: d[f][ix].mean() for f in fams})
    p1 = {f: sum(max(fams, key=lambda k: b[k]) == f for b in boots) / 1000 for f in fams}
    pc = {f: sum(b[f] > b['EUS'] and b[f] > b['FIN'] for b in boots) / 1000 for f in fams}
    ci = {f: [float(np.percentile([b[f] for b in boots], q)) for q in (2.5, 97.5)] for f in fams}
    print(f'== {label}: {n} targets')
    for f in sorted(fams, key=lambda k: -A[k]): print(f'   {f:6s} A={A[f]:+.4f}  CI {ci[f][0]:+.4f}..{ci[f][1]:+.4f}  P(rank1)={p1[f]:.2f}  P(>both decoys)={pc[f]:.2f}')
    return dict(label=label, n=n, A=A, ci95=ci, p_rank1=p1, p_beats_decoys=pc, per_target=per, top_pairs={f: sorted(pairs[f], reverse=True)[:15] for f in fams})

def decide(r, fams=FAMS):
    cand = [f for f in fams if f not in ('EUS', 'FIN')]
    best = [f for f in cand if r['p_rank1'][f] >= 0.9 and r['ci95'][f][0] > 0 and r['p_beats_decoys'][f] >= 0.95]
    sec = [f for f in cand if f not in best and r['ci95'][f][0] > 0 and r['p_beats_decoys'][f] >= 0.95]
    return (f'BEST-SUPPORTED DONOR: {best[0]}' if best else 'NO FAMILY ATTRIBUTABLE') + (f'; secondary: {sec}' if sec else '')

def main():
    out = {'protocol': 'PROTOCOL.md', 'seeds': [SEED_BG, SEED_BOOT]}
    cands = load_candidates(); words = [(F.norm(c['form']), S.stems(c['gloss'])) for c in cands if c['kind'] == 'word']
    topo = [(F.norm(c['form']), S.stems(c['gloss'])) for c in cands if c['kind'] == 'toponym']
    g1 = [(F.norm(w), S.stems(gl)) for w, gl in MITANNI]
    # G2 targets as in round 39
    hw = F.cdial_headwords(); dl = F.dravloans(hw); D = sorted({F.norm(w) for w in dl} - {''})
    L, g, rv = lexicons_with_ia(exclude_ia=set(D))
    Dg = [(w, g[w]) for w in D if g.get(w)]
    out['counts'] = dict(candidates=len(words), toponyms=len(topo), g1=len(g1), g2=len(Dg), lexicons={f: len(L[f]) for f in FAMS})
    print('lexicons', out['counts']['lexicons'])
    idx = {f: S.Index(L[f]) for f in FAMS}
    excl = {w for w, _ in words} | {w for w, _ in topo} | {w for w, _ in g1}
    bg_sum = sumerian_background(excl); out['counts']['sumerian_background'] = len(bg_sum)
    bg_cdial = [(w, s) for w, s in g.items() if rv.get(w) and s and w not in set(D)]
    out['G1'] = attribution(g1, bg_sum, idx, 'G1 Mitanni Indo-Aryan words (Sumerian background)')
    out['G1_pass'] = out['G1']['p_rank1']['IA'] >= 0.9 and out['G1']['ci95']['IA'][0] > 0
    out['G2'] = attribution(Dg, bg_cdial, idx, 'G2 Dravidian loans in Sanskrit (CDIAL background, IA lexicon minus the loans)')
    out['G2_pass'] = out['G2']['p_rank1']['PDR'] >= 0.9 and out['G2']['ci95']['PDR'][0] > 0
    fams39 = ['PDR', 'MUNDA', 'BUR', 'EUS', 'FIN']
    out['G2_round39_families'] = attribution(Dg, bg_cdial, {f: idx[f] for f in fams39}, 'G2 as round 39 (no IA family)', fams39)
    print('G1', 'PASS' if out['G1_pass'] else 'FAIL', '| G2', 'PASS' if out['G2_pass'] else 'FAIL')
    out['candidates'] = attribution(words, bg_sum, idx, 'MELUHHAN CANDIDATE WORDS')
    out['toponyms'] = attribution(topo, bg_sum, idx, 'toponyms (not verdict-bearing)')
    if not (out['G1_pass'] and out['G2_pass']): dec = 'UNINTERPRETABLE (gate failed)'
    else: dec = decide(out['candidates'])
    out['decision'] = dec; print('DECISION', dec)
    json.dump(out, open(HERE / 'results.json', 'w'), indent=1, ensure_ascii=False, default=list)

if __name__ == '__main__': main()
