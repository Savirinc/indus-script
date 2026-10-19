"""Round 52b: writing-system signature with three classes. See PROTOCOL.md (committed before this file).
Standard library only. Run from this folder: python3 run52b.py"""
import sys, json, math, random, collections, time
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round52')); sys.path.insert(0, str(P.parent / 'round30'))
import run52 as R52          # features(), indus_sample(), build_index() unchanged
import foreign_context as FC

SEED = 52101; B = 300
FEATS = R52.FEATS; ROBUST = R52.ROBUST
CLASS = {'GRK': 'SMALL', 'HEB': 'SMALL', 'CHR': 'SMALL',
         'SUX': 'LARGE-PHON', 'OBL': 'LARGE-PHON', 'OAL': 'LARGE-PHON', 'SEAL': 'LARGE-PHON', 'EGY': 'LARGE-PHON', 'OBI': 'LARGE-PHON',
         'U4': 'ARCHAIC', 'U3': 'ARCHAIC', 'PE': 'ARCHAIC'}
REFERENCE = ['CHN']
NUMERALS = {'001','002','003','004','005','013','014','015','016','017','018','031','032','033','034','035','036'}

def log(*a):
    print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def control_path(code):
    for d in (P / 'controls', P.parent / 'round52' / 'controls'):
        if (d / f'{code}.txt').exists(): return d / f'{code}.txt'
    raise SystemExit(f'missing control {code}')

def load(code):
    return [l.split() for l in control_path(code).open(encoding='utf-8') if l.strip()]

def main():
    global LOG
    LOG = (P / 'run52b.log').open('w', encoding='utf-8'); t0 = time.time()
    indus = [list(t) for t in FC.TRAIN]; lengths = [len(t) for t in indus]; R52.N = sum(lengths)
    indus_f = R52.features(indus, random.Random(SEED))
    log('Indus', json.dumps({k: round(v, 4) for k, v in indus_f.items()}))
    # corpora: drop SEAL if too small
    codes = list(CLASS) + REFERENCE
    units = {}
    for c in codes:
        u = load(c); n = sum(len(x) for x in u)
        if c == 'SEAL' and n < 2 * R52.N:
            log('SEAL dropped: tokens', n); codes.remove('SEAL'); del CLASS['SEAL']; continue
        units[c] = u
    for cl in ('SMALL', 'LARGE-PHON', 'ARCHAIC'):
        if sum(1 for c in CLASS if CLASS[c] == cl) < 3: log('NOT RUN: class', cl, 'has fewer than 3 corpora'); return
    samples = {}
    for ci, c in enumerate(codes):
        idx = R52.build_index(units[c], lengths); samples[c] = []
        for b in range(B):
            r = random.Random(SEED + ci * 1000 + b)
            samples[c].append(R52.features(R52.indus_sample(units[c], idx, lengths, r), r))
        m = {f: sum(s[f] for s in samples[c]) / B for f in FEATS}
        log(c, CLASS.get(c, 'reference'), 'units', len(units[c]), 'tokens', sum(len(x) for x in units[c]),
            'mean', json.dumps({k: round(v, 4) for k, v in m.items()}))
    means = {c: {f: sum(s[f] for s in samples[c]) / B for f in FEATS} for c in codes}

    def sd_between(cs, feats):
        out = {}
        for f in feats:
            vals = [means[c][f] for c in cs]; m = sum(vals) / len(vals)
            out[f] = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1)) or 1e-9
        return out
    def dist(a, b, sd, feats): return math.sqrt(sum(((a[f] - b[f]) / sd[f]) ** 2 for f in feats))
    def nearest(x, cs, feats=FEATS):
        sd = sd_between(cs, feats)
        order = sorted(cs, key=lambda c: dist(x, means[c], sd, feats))
        return order, {c: dist(x, means[c], sd, feats) for c in cs}

    classified = [c for c in codes if c in CLASS]
    # positive control: LOCO
    loco = {}
    for c in classified:
        rest = [d for d in classified if d != c]
        hits = collections.Counter()
        for s in samples[c]:
            order, _ = nearest(s, rest); hits[CLASS[order[0]]] += 1
        loco[c] = dict(correct=hits[CLASS[c]] / B, assigned=dict(hits))
        log('LOCO', c, CLASS[c], 'correct', round(hits[CLASS[c]] / B, 3), dict(hits))
    worst = min(v['correct'] for v in loco.values())
    control = 'PASS' if worst >= 0.8 else 'WEAK' if worst >= 0.5 else 'METHOD-FAIL'
    log('positive control', control, 'worst', worst)

    # Indus verdict
    order, d = nearest(indus_f, classified)
    log('Indus nearest order', [(c, round(d[c], 2)) for c in order])
    near_class = CLASS[order[0]]
    flips = []
    for c in classified:
        rest = [x for x in classified if x != c]; o2, _ = nearest(indus_f, rest)
        if CLASS[o2[0]] != near_class: flips.append((c, CLASS[o2[0]]))
    if control == 'METHOD-FAIL': verdict = 'METHOD-FAIL'
    else:
        verdict = f'NEAREST-{near_class} (STABLE)' if not flips else f'NEAREST-{near_class} (UNSTABLE; flips to {flips})'
        if control == 'WEAK': verdict += ' (WEAK CONTROL)'
    log('VERDICT', verdict)
    # range check per class
    rng_check = {}
    for cl in ('SMALL', 'LARGE-PHON', 'ARCHAIC'):
        cs = [c for c in classified if CLASS[c] == cl]; k = 0; detail = {}
        for f in FEATS:
            lo = min(means[c][f] for c in cs); hi = max(means[c][f] for c in cs)
            inside = lo <= indus_f[f] <= hi; k += inside; detail[f] = inside
        rng_check[cl] = dict(count=k, detail=detail)
        log('range check', cl, k, '/ 8', [f for f in FEATS if detail[f]])
    # robustness: five features
    o5, d5 = nearest(indus_f, classified, ROBUST)
    log('robust 5-feature nearest', [(c, round(d5[c], 2)) for c in o5][:5])
    # robustness: numerals merged
    merged = [['NUM' if s in NUMERALS else s for s in t] for t in indus]
    fm = R52.features(merged, random.Random(SEED + 5)); om, dm = nearest(fm, classified)
    log('numerals merged Indus', json.dumps({k: round(v, 4) for k, v in fm.items()}), 'nearest', [(c, round(dm[c], 2)) for c in om][:5])
    # reference CHN distance
    sd_all = sd_between(classified, FEATS)
    log('CHN (reference) distance', round(dist(indus_f, means['CHN'], sd_all, FEATS), 2))
    json.dump(dict(seed=SEED, B=B, N=R52.N, indus=indus_f, classes=CLASS, means=means, loco=loco, control=control,
                   order=order, dist=d, verdict=verdict, flips=flips, range_check=rng_check,
                   robust5=dict(order=o5, dist=d5), numerals_merged=dict(features=fm, order=om, dist=dm),
                   samples=samples), (P / 'results.json').open('w'), indent=1)
    log('done', round(time.time() - t0, 1), 's')

if __name__ == '__main__': main()
