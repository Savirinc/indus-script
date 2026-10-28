"""Round 64: sound-sign recovery when Linear B is made logosyllabic at the Indus word-sign share. See PROTOCOL.md.
Run from this folder with ext/venv python: ../../ext/venv/bin/python run64.py. Requires numpy."""
import os
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS'): os.environ[v] = '1'
import sys, json, random, collections, hashlib, statistics
from pathlib import Path
from multiprocessing import Pool
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round63'))
import run63 as R63                                    # lexicons (Greek cognate, Finnish IDS) and round 32 solver, unchanged
B = R63.B

S_LEVELS = [70, 100, 130, 160]; Q = 0.42
SEEDS = [64001, 64002, 64003, 64004, 64005]; EXTRA = [64006, 64007, 64008, 64009, 64010]
CHAIN_SEEDS = [64300, 64301, 64302, 64303]; STEPS = 600_000; OPAQUE_MAX = 2

def build(q, regime, S, seed, opaque):
    idx = list(range(len(B.words)))
    logo = set(random.Random(seed + 300).sample(idx, round(q * len(idx))))
    freq = collections.Counter(s for i in idx if i not in logo for s in B.words[i]); tot = sum(freq.values())
    so = {v: (max(1, min(11, round(S * freq[v] / tot))) if (freq[v] and S > 70) else 1) for v in B.VALUES}
    rng, rngh, rngg = random.Random(seed), random.Random(seed + 500), random.Random(seed + 900)
    ids = [(v, j) for v in B.VALUES for j in range(so[v])]; rng.shuffle(ids)
    sid = {x: n for n, x in enumerate(ids)}; nsound = len(ids)
    logo_id = {i: nsound + k for k, i in enumerate(sorted(logo))}; nsign = nsound + len(logo)
    truth = B.np.array([B.VI[v] for v, _ in ids] + [-1] * len(logo))
    rngg.shuffle(idx)
    groups = []
    if regime == 'R2':
        while idx:
            k = rngg.choice([1, 2, 3]); groups.append(idx[:k]); idx = idx[k:]
    else:
        groups = [[i] for i in idx]
    texts = [[t for i in g for t in ([logo_id[i]] if i in logo else [sid[(s, rngh.randrange(so[s]))] for s in B.words[i]])]
             for g in groups]
    cnt = collections.Counter(x for t in texts for x in t)
    opq = {x for x, c in cnt.items() if c <= OPAQUE_MAX} if opaque else set()
    segs = []
    for t in texts:
        cur = []
        for x in t:
            if x in opq:
                if cur: segs.append(tuple(cur)); cur = []
            else: cur.append(x)
        if cur: segs.append(tuple(cur))
    sound_tokens = sum(c for x, c in cnt.items() if x < nsound)
    used_sound = sum(1 for x in cnt if x < nsound)
    return dict(types=collections.Counter(segs), truth=truth, nsign=nsign, nsound=nsound, cnt=cnt, opq=opq,
                sound_tokens=sound_tokens, used_sound=used_sound, logo_tokens=sum(c for x, c in cnt.items() if x >= nsound),
                logo_types=len(logo), opaque_sound_ids=sum(1 for x in opq if x < nsound),
                opaque_logo_ids=sum(1 for x in opq if x >= nsound))

_LEX = {}
def job(spec):
    name, lex_name, q, regime, S, seed, opaque = spec
    if lex_name not in _LEX: _LEX[lex_name] = R63.lexicon(lex_name)
    lex = _LEX[lex_name]
    c = build(q, regime, S, seed, opaque)
    sc = B.Scorer(c['types'], c['nsign'], B.fit_lm(lex)); B.STEPS = STEPS
    chains = [B.anneal(sc, c['nsign'], False, cs) for cs in CHAIN_SEEDS]
    best = max(chains, key=lambda x: x[0]); mp = best[1]
    def acc(m): return sum(n for x, n in c['cnt'].items() if x < c['nsound'] and x not in c['opq'] and m[x] == c['truth'][x]) / c['sound_tokens']
    true_mp = c['truth'].copy(); true_mp[true_mp < 0] = 0
    res = dict(set=name, lexicon=lex_name, q=q, regime=regime, S=S, seed=seed, opaque=opaque, sign_ids=c['nsign'],
               sound_ids_used=c['used_sound'], sound_tokens=c['sound_tokens'], u=c['sound_tokens'] / c['used_sound'],
               logo_tokens=c['logo_tokens'], logo_share=c['logo_tokens'] / (c['logo_tokens'] + c['sound_tokens']),
               opaque_sound_ids=c['opaque_sound_ids'], opaque_logo_ids=c['opaque_logo_ids'], segment_types=len(c['types']),
               sound_accuracy=acc(mp), chain_accuracies=[acc(ch[1]) for ch in chains], best_objective=best[0])
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()}), flush=True)
    return res

def med(rs): return statistics.median(r['sound_accuracy'] for r in rs)

def indus_topn():
    sys.path.insert(0, str(P.parent / 'round30'))
    import foreign_context as FC
    v = [n for _, n in collections.Counter(s for t in FC.TRAIN for s in t).most_common()]
    return v

def main():
    sets = {'P': ('greek', Q, 'R2', True), 'K': ('greek', Q, 'R1', True), 'B': ('greek', 0.0, 'R2', True), 'V': ('greek', Q, 'R2', False)}
    jobs = [(nm, lx, q, rg, S, s, op) for nm, (lx, q, rg, op) in sets.items() for S in S_LEVELS for s in SEEDS]
    jobs += [('POS', 'greek', 0.0, 'R1', 70, s, True) for s in SEEDS] + [('NEG', 'finnish', Q, 'R2', 70, s, True) for s in SEEDS]
    with Pool(int(os.environ.get('R64_PROCS', 8))) as pool:
        out = pool.map(job, jobs, chunksize=1)
        get = lambda nm, S, extra=False: [r for r in out if r['set'] == nm and r['S'] == S and (extra or r['seed'] in SEEDS)]
        recovered = {(nm, S): med(get(nm, S)) >= 0.5 for nm in sets for S in S_LEVELS}
        robustness = []
        last = max([k for k in range(len(S_LEVELS)) if all(recovered[('P', S)] for S in S_LEVELS[:k + 1])], default=-1)
        for k in (last, last + 1):
            if 0 <= k < len(S_LEVELS) and 0.45 <= med(get('P', S_LEVELS[k])) <= 0.55:
                S = S_LEVELS[k]
                out += pool.map(job, [('P', 'greek', Q, 'R2', S, s, True) for s in EXTRA], chunksize=1)
                ten = get('P', S, extra=True); n = sum(r['sound_accuracy'] >= 0.5 for r in ten)
                recovered[('P', S)] = n >= 6
                robustness.append(dict(S=S, median5=med(get('P', S)), n_ge_half=n, recovered=recovered[('P', S)]))
    pos, neg = [r for r in out if r['set'] == 'POS'], [r for r in out if r['set'] == 'NEG']
    pos_ok, neg_ok = med(pos) >= 0.70, med(neg) <= 0.15
    summary = {nm: [dict(S=S, u=statistics.mean(r['u'] for r in get(nm, S)), logo_share=statistics.mean(r['logo_share'] for r in get(nm, S)),
                         median=med(get(nm, S)), accuracies=sorted(r['sound_accuracy'] for r in get(nm, S)), recovered=recovered[(nm, S)])
                    for S in S_LEVELS] for nm in sets}
    u_star = None
    for row in summary['P']:
        if row['recovered']: u_star = row['u']
        else: break
    v = indus_topn()
    n_star = max([n for n in range(1, len(v) + 1) if sum(v[:n]) / n >= u_star], default=0) if u_star else None
    verdict = 'VOID' if not (pos_ok and neg_ok) else ('SOUND PART RECOVERABLE' if u_star else 'NOT RECOVERED IN RANGE')
    res = dict(protocol_sha256=hashlib.sha256((P / 'PROTOCOL.md').read_bytes()).hexdigest(),
               positive_control=dict(median=med(pos), passed=pos_ok), negative_control=dict(median=med(neg), passed=neg_ok),
               summary=summary, robustness=robustness, u_star=u_star, indus_N_star=n_star,
               indus_opaque_rule=dict(signs=len(v), opaque=sum(1 for n in v if n <= OPAQUE_MAX), kept=sum(1 for n in v if n > OPAQUE_MAX),
                                      kept_tokens=sum(n for n in v if n > OPAQUE_MAX), tokens=sum(v)),
               verdict=verdict, runs=out)
    (P / 'results.json').write_text(json.dumps(res, indent=1, default=lambda o: o.item()))
    print('POSITIVE', round(med(pos), 3), pos_ok, '| NEGATIVE', round(med(neg), 3), neg_ok)
    for nm in sets: print(nm, [(r['S'], round(r['u'], 1), round(r['median'], 3)) for r in summary[nm]])
    print('u*', u_star, 'Indus N*', n_star, '| VERDICT', verdict)

if __name__ == '__main__':
    main()
