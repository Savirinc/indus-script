"""Round 63: decipherability threshold with replicates. See PROTOCOL.md (locked, sha256 e2a3ccb3...2a66df).
Run from this folder with ext/venv python: ../../ext/venv/bin/python run63.py. Requires numpy."""
import os
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS'): os.environ[v] = '1'
import sys, json, math, random, collections, csv, hashlib, unicodedata, statistics
from pathlib import Path
from multiprocessing import Pool
P = Path(__file__).resolve().parent; ROOT = P.parents[1]
LB = ROOT / 'ext/neurodecipher/data/linear_b-greek.cog'
IDS = ROOT / 'ext/lexibank_ids/cldf/forms.csv'
sys.path.insert(0, str(P.parent / 'round32'))
_argv = sys.argv; sys.argv = [_argv[0], str(LB)]
import benchmark as B                                  # round 32 v2 solver, unchanged
sys.argv = _argv

TARGETS = [120, 150, 170, 190, 210, 230, 250]
SEEDS = [63001, 63002, 63003, 63004, 63005]; EXTRA = [63006, 63007, 63008, 63009, 63010]
CHAIN_SEEDS = [63100, 63101, 63102, 63103]
PRIMARY, SECONDARY = 600_000, 150_000
INDUS_TOKENS, INDUS_RAW, INDUS_MERGED = 8726, 582, 541

# ---------- lexicons ----------
def syllabify(ph):                                     # round 32 to_lb loop, applied to an already-mapped string
    out = []; i = 0; n = len(ph)
    while i < n:
        c = ph[i]
        if c in B.VOW: out.append(c.upper()); i += 1; continue
        j = i
        while j < n and ph[j] not in B.VOW: j += 1
        if j == n: break
        cl = ph[i:j]; v = ph[j]
        if len(cl) > 1 and cl[0] in 'snrm' and i > 0: cl = cl[1:]
        for cc in cl: out.append((cc + v).upper())
        out[-1] = (cl[-1] + v).upper(); i = j + 1
    return out

FIN = {'æ': 'a', 'ü': 'u', 'ö': 'o', 'b': 'p', 'g': 'k', 'f': 'p', 'v': 'w', 'l': 'r', 'h': ''}
def fin_to_lb(form):
    s = form.lower().replace('æ', 'a')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    s = ''.join(FIN.get(c, c) for c in s)
    return syllabify(''.join(c for c in s if 'a' <= c <= 'z'))

def lexicon(name):
    if name == 'greek': return B.lex_cognate(range(len(B.words)))
    forms = [r['Form'] for r in csv.DictReader(IDS.open(encoding='utf-8')) if r['Language_ID'] == '128']
    return [w for w in map(fin_to_lb, forms) if w]

# ---------- cipher construction (sweep_exploratory homophone rule; seeded per protocol) ----------
def build(target, regime, seed):
    idx = list(range(len(B.words)))
    freq = collections.Counter(s for i in idx for s in B.words[i]); tot = sum(freq.values())
    so = {v: (max(1, min(11, round(target * freq[v] / tot))) if (freq[v] and target > 70) else 1) for v in B.VALUES}
    rng, rngh, rngg = random.Random(seed), random.Random(seed + 500), random.Random(seed + 900)
    ids = [(v, j) for v in B.VALUES for j in range(so[v])]; rng.shuffle(ids)
    sid = {x: n for n, x in enumerate(ids)}; truth = B.np.array([B.VI[v] for v, _ in ids])
    if regime == 'R2':
        rngg.shuffle(idx); texts = []
        while idx:
            k = rngg.choice([1, 2, 3]); texts.append([s for i in idx[:k] for s in B.words[i]]); idx = idx[k:]
    else:
        texts = [B.words[i] for i in idx]
    enc = [[sid[(s, rngh.randrange(so[s]))] for s in t] for t in texts]
    return collections.Counter(tuple(t) for t in enc), truth, len(ids)

_LEX = {}
def job(spec):
    lex_name, regime, target, seed, steps = spec
    if lex_name not in _LEX: _LEX[lex_name] = lexicon(lex_name)
    lex = _LEX[lex_name]
    types, truth, nsign = build(target, regime, seed)
    sc = B.Scorer(types, nsign, B.fit_lm(lex)); B.STEPS = steps
    chains = [B.anneal(sc, nsign, False, cs) for cs in CHAIN_SEEDS]
    best = max(chains, key=lambda x: x[0]); acc, tacc = B.accuracy(sc, best[1], truth)
    true_obj = B.objective(sc, truth)
    res = dict(lexicon=lex_name, regime=regime, target=target, seed=seed, steps=steps, sign_ids=nsign,
               tokens=int(sc.tokens), tokens_per_sign=sc.tokens / nsign, text_types=len(types), lexicon_forms=len(lex),
               share_signs_le2=float((sc.f <= 2).mean()), token_accuracy=acc, type_accuracy=tacc,
               freq_baseline=B.freq_baseline(sc, truth, lex), best_objective=best[0], true_key_objective=true_obj,
               true_ge_best=bool(true_obj >= best[0]), chain_accuracies=[B.accuracy(sc, c[1], truth)[0] for c in chains])
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()}), flush=True)
    return res

def med(rs): return statistics.median(r['token_accuracy'] for r in rs)

def threshold(rows, regime, recovered):
    """t* = tokens/sign of the sparsest level in the contiguous recovered run starting at the densest level."""
    levels = sorted({(r['tokens_per_sign'], r['target']) for r in rows if r['regime'] == regime}, reverse=True)
    t = None
    for tps, tg in levels:
        if recovered[(regime, tg)]: t = tps
        else: break
    return t, levels

def main():
    jobs = [('greek', rg, tg, s, st) for st in (PRIMARY, SECONDARY) for rg in ('R1', 'R2') for tg in TARGETS for s in SEEDS]
    jobs += [('finnish', 'R1', 120, s, PRIMARY) for s in SEEDS]
    with Pool(int(os.environ.get('R63_PROCS', 8))) as pool:
        out = pool.map(job, jobs, chunksize=1)
        prim = lambda rg, tg, extra=False: [r for r in out if r['lexicon'] == 'greek' and r['regime'] == rg
                                            and r['target'] == tg and r['steps'] == PRIMARY and (extra or r['seed'] in SEEDS)]
        recovered = {(rg, tg): med(prim(rg, tg)) >= 0.5 for rg in ('R1', 'R2') for tg in TARGETS}
        robustness = []
        for rg in ('R1', 'R2'):                        # rule 7: levels bracketing t* with median in [0.45, 0.55]
            t, levels = threshold([r for r in out if r['steps'] == PRIMARY and r['lexicon'] == 'greek'], rg, recovered)
            tgs = [tg for _, tg in levels]
            last = max([k for k, tg in enumerate(tgs) if recovered[(rg, tg)] and all(recovered[(rg, x)] for x in tgs[:k + 1])], default=-1)
            bracket = [tgs[k] for k in (last, last + 1) if 0 <= k < len(tgs)]
            for tg in bracket:
                m = med(prim(rg, tg))
                if 0.45 <= m <= 0.55:
                    out += pool.map(job, [('greek', rg, tg, s, PRIMARY) for s in EXTRA], chunksize=1)
                    ten = prim(rg, tg, extra=True)
                    recovered[(rg, tg)] = sum(r['token_accuracy'] >= 0.5 for r in ten) >= 6
                    robustness.append(dict(regime=rg, target=tg, median5=m, n_ge_half=sum(r['token_accuracy'] >= 0.5 for r in ten),
                                           recovered=recovered[(rg, tg)]))
    primary = [r for r in out if r['steps'] == PRIMARY and r['lexicon'] == 'greek']
    pos = [r for r in out if r['lexicon'] == 'greek' and r['regime'] == 'R1' and r['target'] == 170 and r['steps'] == SECONDARY and r['seed'] in SEEDS]
    neg = [r for r in out if r['lexicon'] == 'finnish']
    pos_ok, neg_ok = med(pos) >= 0.70, med(neg) <= 0.15
    merged = INDUS_TOKENS / INDUS_MERGED; raw = INDUS_TOKENS / INDUS_RAW
    th = {}
    for rg in ('R1', 'R2'):
        t, levels = threshold(primary, rg, recovered)
        densest = max(tps for tps, _ in levels)
        th[rg] = dict(t_star=t, N_star=(math.floor(INDUS_TOKENS / t) if t else None),
                      no_threshold_in_range=t is None, N_star_below=(None if t else INDUS_TOKENS / densest),
                      levels=[dict(target=tg, tokens_per_sign=tps, sign_ids=next(r['sign_ids'] for r in primary if r['regime'] == rg and r['target'] == tg),
                                   median_600k=med(prim(rg, tg)),
                                   median_150k=med([r for r in out if r['lexicon'] == 'greek' and r['regime'] == rg and r['target'] == tg and r['steps'] == SECONDARY]),
                                   true_ge_best=sum(r['true_ge_best'] for r in prim(rg, tg)), recovered=recovered[(rg, tg)])
                              for tps, tg in levels])
    if not (pos_ok and neg_ok): verdict = 'VOID'
    else:
        t1, t2 = th['R1']['t_star'], th['R2']['t_star']
        verdict = 'REACHABLE' if (t2 and merged >= t2) else 'KIND-ONLY' if (t1 and merged >= t1) else 'OUT OF REACH'
    near = [rg for rg in ('R1', 'R2') if th[rg]['t_star'] and abs(merged - th[rg]['t_star']) <= 0.5]
    res = dict(protocol_sha256=hashlib.sha256((P / 'PROTOCOL.md').read_bytes()).hexdigest(),
               source_sha256=hashlib.sha256(LB.read_bytes()).hexdigest(),
               indus=dict(tokens=INDUS_TOKENS, raw_signs=INDUS_RAW, raw_tps=raw, merged_signs=INDUS_MERGED, merged_tps=merged, share_le2=302 / 582),
               positive_control=dict(median=med(pos), passed=pos_ok), negative_control=dict(median=med(neg), passed=neg_ok),
               thresholds=th, robustness=robustness, verdict=verdict, at_threshold=near, runs=out)
    (P / 'results.json').write_text(json.dumps(res, indent=1))
    print('POSITIVE', round(med(pos), 3), pos_ok, '| NEGATIVE', round(med(neg), 3), neg_ok)
    for rg in ('R1', 'R2'):
        print(rg, 't*', th[rg]['t_star'], 'N*', th[rg]['N_star'], [(l['target'], round(l['tokens_per_sign'], 1), round(l['median_600k'], 3)) for l in th[rg]['levels']])
    print('VERDICT', verdict, ('at the threshold (' + ','.join(near) + ')') if near else '')

if __name__ == '__main__':
    main()
