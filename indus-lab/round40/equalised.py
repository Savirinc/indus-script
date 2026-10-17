"""Round 40: size-equalised rerun of round 39. See PROTOCOL.md."""
import sys, json, random, collections
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round39')); sys.path.insert(0, str(P.parent / 'round37'))
import fingerprint as F
import semantic_attribution as S

FAMS = ['PDR', 'MUNDA', 'EUS', 'FIN']


def A_values(targets, background, idx):
    rng = random.Random(39001); byshape = collections.defaultdict(list); bylen = collections.defaultdict(list)
    for w, s in background: byshape[S.cvshape(w)].append((w, s)); bylen[len(w)].append((w, s))
    cache = {}; d = {f: [] for f in FAMS}
    def m(f, w, s):
        if (f, w) not in cache: cache[(f, w)] = idx[f].best(w, s)[0]
        return cache[(f, w)]
    for w, s in targets:
        pool = [x for x in byshape.get(S.cvshape(w), []) if x[0] != w]
        if len(pool) < 5: pool = [x for x in bylen.get(len(w), []) if x[0] != w]
        bg = rng.sample(pool, min(5, len(pool)))
        for f in FAMS: d[f].append(m(f, w, s) - np.mean([m(f, bw, bs) for bw, bs in bg]))
    return {f: float(np.mean(v)) for f, v in d.items()}


def main():
    g, raw, rv = S.cdial_glossed()
    hw = F.cdial_headwords(); kw = F.kuiper_words(); dl = F.dravloans(hw)
    K = sorted({F.norm(w) for w in kw} - {''}); D = sorted({F.norm(w) for w in dl} - {''})
    Kg = [(w, g[w]) for w in K if g.get(w)]; Dg = [(w, g[w]) for w in D if g.get(w)]
    excl = set(K) | set(D); B = [(w, s) for w, s in g.items() if rv.get(w) and s and w not in excl]
    L = S.lexicons(); n = len(L['MUNDA'])
    print('targets', len(Kg), len(Dg), 'size', n, {f: len(L[f]) for f in FAMS})
    runs = []
    for k in range(100):
        rng = random.Random(40000 + k)
        sub = {f: (L[f] if f == 'MUNDA' else rng.sample(L[f], n)) for f in FAMS}
        idx = {f: S.Index(sub[f]) for f in FAMS}
        runs.append({'control': A_values(Dg, B, idx), 'kuiper': A_values(Kg, B, idx)})
    ctrl = sum(max(FAMS, key=lambda f: r['control'][f]) == 'PDR' for r in runs) / 100
    pm = sum(r['kuiper']['PDR'] > r['kuiper']['MUNDA'] for r in runs) / 100
    pc = sum(r['kuiper']['PDR'] > max(r['kuiper']['EUS'], r['kuiper']['FIN']) for r in runs) / 100
    mean = {t: {f: float(np.mean([r[t][f] for r in runs])) for f in FAMS} for t in ('control', 'kuiper')}
    dec = ('INCONCLUSIVE (control lacks power at equal size)' if ctrl < 0.9 else
           'PREMISE HOLDS' if pm >= 0.9 and pc >= 0.9 else 'PREMISE FAILS (size artefact)' if pm <= 0.6 else 'WEAKENED')
    out = dict(subsamples=100, size=n, control_PDR_first=ctrl, kuiper_PDR_gt_MUNDA=pm, kuiper_PDR_gt_controls=pc, mean_A=mean, decision=dec, runs=runs)
    print(json.dumps({k: v for k, v in out.items() if k != 'runs'}, indent=1)); print('DECISION', dec)
    (P / 'results.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
