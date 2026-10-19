"""Round 52: writing-system signature test. See PROTOCOL.md (committed before this file).
Standard library only. Run from this folder: python3 run52.py"""
import sys, json, math, random, collections, time
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round30'))
import foreign_context as FC

SEED = 52001; B = 300; N = None   # N set to the actual Indus token count at run time (Amendment 2)
CORPORA = ['GRK', 'HEB', 'CHR', 'SUX', 'EGY', 'OBI', 'CHN']
CLASS = {'GRK': 'alphabet', 'HEB': 'alphabet', 'CHR': 'syllabary', 'SUX': 'logosyllabic', 'EGY': 'logosyllabic',
         'OBI': 'logographic', 'CHN': 'logographic'}
CLASSES = ['alphabet', 'syllabary', 'logosyllabic', 'logographic']
FEATS = ['V', 'hapax', 'top10', 'H1', 'H2H1', 'heaps', 'repeat', 'double']
ROBUST = ['top10', 'H1', 'H2H1', 'repeat', 'double']
CHI2_99_8 = 20.090

def log(*a):
    print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def H(counter):
    n = sum(counter.values()); return -sum(c / n * math.log2(c / n) for c in counter.values())

def features(texts, rng):
    toks = [s for t in texts for s in t]
    uni = collections.Counter(toks); V = len(uni)
    hapax = sum(1 for c in uni.values() if c == 1) / V
    top10 = sum(c for _, c in uni.most_common(10)) / len(toks)
    H1 = H(uni)
    pairs = collections.Counter((t[i], t[i + 1]) for t in texts for i in range(len(t) - 1))
    prev = collections.Counter(); [prev.update({a: c}) for (a, b), c in pairs.items()]
    H2 = H(pairs) - H(prev)
    order = toks[:]; rng.shuffle(order); seen = set(); vn = []
    grid = list(range(500, len(order), 100)) + [len(order)]
    gi = 0
    for i, s in enumerate(order, 1):
        seen.add(s)
        while gi < len(grid) and i == grid[gi]: vn.append((math.log(i), math.log(len(seen)))); gi += 1
    mx = sum(x for x, _ in vn) / len(vn); my = sum(y for _, y in vn) / len(vn)
    heaps = sum((x - mx) * (y - my) for x, y in vn) / sum((x - mx) ** 2 for x, _ in vn)
    long_ = [t for t in texts if len(t) >= 2]
    repeat = sum(1 for t in long_ if len(set(t)) < len(t)) / len(long_)
    double = sum(c for (a, b), c in pairs.items() if a == b) / sum(pairs.values())
    return dict(V=V, hapax=hapax, top10=top10, H1=H1, H2H1=H2 / H1, heaps=heaps, repeat=repeat, double=double)

def load_control(code):
    units = [l.split() for l in (P / 'controls' / f'{code}.txt').open(encoding='utf-8') if l.strip()]
    bylen = collections.defaultdict(list)
    for u in units: bylen[len(u)].append(u)
    return units, bylen

def indus_sample(units, maxlen_index, lengths, rng):
    """Indus-shaped sample: windows of Indus lengths from control units, never crossing a unit."""
    texts = []; total = 0
    while total < N:
        l = rng.choice(lengths)
        if total + l > N: l = N - total
        pool = maxlen_index[l]
        if not pool: raise SystemExit(f'no unit of length >= {l}')
        u = rng.choice(pool); st = rng.randrange(len(u) - l + 1)
        texts.append(u[st:st + l]); total += l
    return texts

def build_index(units, lengths):
    srt = sorted(units, key=len); idx = {}
    for l in range(1, max(lengths) + 1):
        idx[l] = [u for u in srt if len(u) >= l]
    return idx

# ---- linear algebra (8x8) ----
def inv(M):
    n = len(M); A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c])); A[c], A[p] = A[p], A[c]
        pv = A[c][c]; A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c]:
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]

def gaussian(vecs, ridge=0.05):
    n = len(vecs); d = len(vecs[0])
    mu = [sum(v[i] for v in vecs) / n for i in range(d)]
    cov = [[sum((v[i] - mu[i]) * (v[j] - mu[j]) for v in vecs) / (n - 1) + (ridge if i == j else 0) for j in range(d)] for i in range(d)]
    return mu, inv(cov)

def maha(x, g):
    mu, ci = g; d = [a - b for a, b in zip(x, mu)]
    return sum(d[i] * ci[i][j] * d[j] for i in range(len(d)) for j in range(len(d)))

def main():
    global LOG
    LOG = (P / 'run52.log').open('w', encoding='utf-8')
    t0 = time.time()
    indus = [list(t) for t in FC.TRAIN]
    lengths = [len(t) for t in indus]
    log('Indus texts', len(indus), 'tokens', sum(lengths), 'types', len({s for t in indus for s in t}))
    global N; N = sum(lengths)
    rng = random.Random(SEED)
    indus_f = features(indus, rng)
    log('Indus features', json.dumps({k: round(v, 4) for k, v in indus_f.items()}))

    # control samples
    samples = {}
    for ci, code in enumerate(CORPORA):
        units, _ = load_control(code); idx = build_index(units, lengths)
        samples[code] = []
        for b in range(B):
            r = random.Random(SEED + ci * 1000 + b)
            texts = indus_sample(units, idx, lengths, r)
            samples[code].append(features(texts, r))
        m = {f: sum(s[f] for s in samples[code]) / B for f in FEATS}
        log(code, CLASS[code], 'units', len(units), 'tokens', sum(len(u) for u in units),
            'mean', json.dumps({k: round(v, 4) for k, v in m.items()}))
    # standardisation: pooled within-corpus sd
    sd = {}
    for f in FEATS:
        ss = 0; dfree = 0
        for code in CORPORA:
            vals = [s[f] for s in samples[code]]; m = sum(vals) / B
            ss += sum((v - m) ** 2 for v in vals); dfree += B - 1
        sd[f] = math.sqrt(ss / dfree) or 1e-9
    def vec(s, feats=FEATS): return [s[f] / sd[f] for f in feats]

    def fit_classes(exclude=None, feats=FEATS):
        g = {}
        for cl in CLASSES:
            vs = [vec(s, feats) for code in CORPORA if CLASS[code] == cl and code != exclude for s in samples[code]]
            if vs: g[cl] = gaussian(vs)
        return g
    def nearest(x, g): return min(g, key=lambda cl: maha(x, g[cl]))

    # positive control: leave-one-corpus-out at class level
    loco = {}
    for code in CORPORA:
        if sum(1 for c in CORPORA if CLASS[c] == CLASS[code]) < 2: continue
        g = fit_classes(exclude=code)
        hits = sum(1 for s in samples[code] if nearest(vec(s), g) == CLASS[code]) / B
        assigned = collections.Counter(nearest(vec(s), g) for s in samples[code])
        loco[code] = dict(correct=hits, assigned=dict(assigned))
        log('LOCO', code, 'true', CLASS[code], 'correct', round(hits, 3), dict(assigned))
    g_all = fit_classes()
    chr_self = sum(1 for s in samples['CHR'] if nearest(vec(s), g_all) == 'syllabary') / B
    log('CHR self-consistency (not a test)', chr_self)
    worst = min(v['correct'] for v in loco.values())
    control = 'PASS' if worst >= 0.8 else 'WEAK' if worst >= 0.5 else 'METHOD-FAIL'
    log('positive control', control, 'worst', worst)

    # Indus
    x = vec(indus_f)
    dist = {cl: maha(x, g_all[cl]) for cl in CLASSES}
    inside = [cl for cl in CLASSES if dist[cl] <= CHI2_99_8]
    near = min(dist, key=dist.get)
    if control == 'METHOD-FAIL': verdict = 'METHOD-FAIL'
    elif len(inside) == 1: verdict = f'MATCH-{inside[0]}'
    elif len(inside) > 1: verdict = 'AMBIGUOUS'
    else: verdict = f'OUTSIDE-ALL, nearest {near}'
    if control == 'WEAK' and verdict != 'METHOD-FAIL': verdict += ' (WEAK CONTROL)'
    log('Indus Mahalanobis', {k: round(v, 2) for k, v in dist.items()}, 'inside', inside, 'VERDICT', verdict)

    # robustness: features without inventory splitting
    g_rob = fit_classes(feats=ROBUST); xr = vec(indus_f, ROBUST)
    dist_r = {cl: maha(xr, g_rob[cl]) for cl in CLASSES}
    log('Robust (5 features) Mahalanobis', {k: round(v, 2) for k, v in dist_r.items()}, 'nearest', min(dist_r, key=dist_r.get))

    # shuffled-Indus diagnostics
    r = random.Random(SEED + 99)
    sh_within = [t[:] for t in indus]; [r.shuffle(t) for t in sh_within]
    flat = [s for t in indus for s in t]; r.shuffle(flat); sh_across = []; i = 0
    for l in lengths: sh_across.append(flat[i:i + l]); i += l
    diag = {}
    for name, tx in (('within', sh_within), ('across', sh_across)):
        f = features(tx, random.Random(SEED + 100)); xv = vec(f)
        dd = {cl: maha(xv, g_all[cl]) for cl in CLASSES}
        diag[name] = dict(features=f, dist=dd, nearest=min(dd, key=dd.get))
        log('Indus shuffled', name, json.dumps({k: round(v, 4) for k, v in f.items()}), {k: round(v, 2) for k, v in dd.items()})
    # diagnostic's own control on one SUX sample
    units, _ = load_control('SUX'); idx = build_index(units, lengths); rs = random.Random(SEED + 7)
    sx = indus_sample(units, idx, lengths, rs); f0 = features(sx, random.Random(1))
    sw = [t[:] for t in sx]; [rs.shuffle(t) for t in sw]; f1 = features(sw, random.Random(1))
    log('SUX sample H2/H1 real', round(f0['H2H1'], 4), 'within-shuffled', round(f1['H2H1'], 4))
    diag['sux_check'] = dict(real=f0['H2H1'], shuffled=f1['H2H1'])

    # within-class spread: per-corpus means
    per = {code: {f: sum(s[f] for s in samples[code]) / B for f in FEATS} for code in CORPORA}
    json.dump(dict(seed=SEED, B=B, N=N, indus=indus_f, per_corpus_mean=per, sd=sd, loco=loco, control=control,
                   indus_dist=dist, inside=inside, verdict=verdict, robust_dist=dist_r, diagnostics=diag,
                   samples={c: samples[c] for c in CORPORA}),
              (P / 'results.json').open('w'), indent=1)
    log('done', round(time.time() - t0, 1), 's')

if __name__ == '__main__': main()
