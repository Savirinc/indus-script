"""Round 65b: how many of the texts' own names must be known before the right-language word list decodes and stands out?
See PROTOCOL.md. Run from this folder with ext/venv python: ../../ext/venv/bin/python run65b.py. Requires numpy."""
import os
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS'): os.environ[v] = '1'
import sys, json, random, math, hashlib, statistics
from pathlib import Path
from multiprocessing import Pool
P = Path(__file__).resolve().parent; ROOT = P.parents[1]
sys.path.insert(0, str(P.parent / 'round65'))
import run65 as R65                                    # lexicons, spelling rule, order_info, decoy, cipher via run64 (unchanged)
R64, B = R65.R64, R65.B
NAMES = ROOT / 'ext/neurodecipher/data/linear_b-greek.names.cog'

FRACS = [0.05, 0.10, 0.25, 0.50]
SEEDS, EXTRA = R65.SEEDS, R65.EXTRA
CAND = ['G-IDS'] + R65.WRONG

def name_pool():
    rows = [l.split('\t') for l in NAMES.read_text(encoding='utf-8').splitlines()[1:]]
    pool = [[w for w in (B.to_lb(g) for g in gr.split('|')) if w] for _, gr in rows if gr != '_']
    order = list(range(len(pool))); random.Random(65950).shuffle(order)
    return pool, order

def known(f):
    pool, order = name_pool()
    return [w for i in order[:math.ceil(f * len(pool))] for w in pool[i]]

_LEX = {}
def job(spec):
    lang, f, seed, which = spec
    key = (lang, f)
    if key not in _LEX:
        names = known(f) if f else []
        lex = names if lang == 'NAMES' else R65.lexicon(lang) + names
        lm = B.fit_lm(lex); _LEX[key] = (lex, lm, R65.order_info(lex, lm), len(names))
    lex, lm, I, nn = _LEX[key]
    c = R64.build(R64.Q, 'R2', 70, seed, True)
    types = c['types'] if which == 'real' else R65.decoy(c['types'], seed)
    sc = B.Scorer(types, c['nsign'], lm); B.STEPS = R65.STEPS
    chains = [B.anneal(sc, c['nsign'], False, cs) for cs in R65.CHAIN_SEEDS]
    best = max(chains, key=lambda x: x[0]); mp = best[1]
    ll = float((sc.total(mp) * sc.cnt).sum()) / sc.tokens
    acc = sum(n for x, n in c['cnt'].items() if x < c['nsound'] and x not in c['opq'] and mp[x] == c['truth'][x]) / c['sound_tokens']
    res = dict(lang=lang, f=f, seed=seed, cipher=which, lexicon_words=len(lex), name_forms=nn, I=I, LL=ll,
               best_objective=best[0], accuracy=acc)
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()}), flush=True)
    return res

def main_jobs(fs, seeds):
    return [(L, f, s, w) for f in fs for s in seeds for L in CAND for w in ('real', 'decoy')]

def evaluate(out):
    g = {(r['lang'], r['f'], r['seed'], r['cipher']): r for r in out}
    def R(L, f, s): return (g[(L, f, s, 'real')]['LL'] - g[(L, f, s, 'decoy')]['LL']) / g[(L, f, s, 'real')]['I']
    ev = {}
    for f in FRACS:
        seeds = [s for s in SEEDS + EXTRA if ('G-IDS', f, s, 'real') in g and ('G-IDS', f, s, 'decoy') in g]
        accs = [g[('G-IDS', f, s, 'real')]['accuracy'] for s in SEEDS + EXTRA if ('G-IDS', f, s, 'real') in g]
        firsts = sum(all(R('G-IDS', f, s) > R(w, f, s) for w in R65.WRONG) for s in seeds)
        ev[f] = dict(layouts=len(seeds), G_IDS_first=firsts, acc_G_IDS=accs, acc_median=statistics.median(accs),
                     n_acc_ge_half=sum(a >= 0.5 for a in accs),
                     R={L: [R(L, f, s) for s in seeds] for L in CAND},
                     acc_names_only=[g[('NAMES', f, s, 'real')]['accuracy'] for s in SEEDS if ('NAMES', f, s, 'real') in g])
        five = len(seeds) == 5
        ev[f]['disc'] = firsts >= (4 if five else 7)
        ev[f]['dec'] = (ev[f]['acc_median'] >= 0.5) if len(accs) == 5 else (ev[f]['n_acc_ge_half'] >= 6)
    return ev

def threshold(ev, key):
    t = None
    for f in reversed(FRACS):
        if ev[f][key]: t = f
        else: break
    return t

def main():
    jobs = [('G-same', 0, s, 'real') for s in SEEDS] + main_jobs(FRACS, SEEDS) + [('NAMES', f, s, 'real') for f in FRACS for s in SEEDS]
    robustness = []
    with Pool(int(os.environ.get('R65B_PROCS', 8))) as pool:
        out = pool.map(job, jobs, chunksize=1)
        ev = evaluate(out)
        for key in ('disc', 'dec'):
            t = threshold(ev, key); k = FRACS.index(t) if t else len(FRACS)
            for f in {FRACS[i] for i in (k - 1, k) if 0 <= i < len(FRACS)}:
                if ev[f]['layouts'] > 5: continue
                if (key == 'disc' and ev[f]['G_IDS_first'] == 3) or (key == 'dec' and 0.45 <= ev[f]['acc_median'] <= 0.55):
                    out += pool.map(job, main_jobs([f], EXTRA), chunksize=1)
                    robustness.append(dict(trigger=key, f=f)); ev = evaluate(out)
    pos = statistics.median(r['accuracy'] for r in out if r['lang'] == 'G-same'); pos_ok = pos >= 0.70
    f_dec, f_disc = threshold(ev, 'dec'), threshold(ev, 'disc')
    npool = len(name_pool()[0]); words = lambda f: math.ceil(f * npool) if f else None
    verdict = 'VOID' if not pos_ok else ('NAMES CLOSE THE GAP' if f_disc else
              'NAMES DECODE, BUT DO NOT IDENTIFY THE LANGUAGE' if f_dec else 'NOT CLOSED AT 50%')
    res = dict(protocol_sha256=hashlib.sha256((P / 'PROTOCOL.md').read_bytes()).hexdigest(),
               positive_control=dict(median_accuracy=pos, passed=pos_ok, accuracies=[r['accuracy'] for r in out if r['lang'] == 'G-same']),
               name_pool=npool, f_dec=f_dec, f_disc=f_disc, names_at_f_dec=words(f_dec), names_at_f_disc=words(f_disc),
               robustness=robustness, by_fraction={str(f): ev[f] for f in FRACS}, verdict=verdict, runs=out)
    (P / 'results.json').write_text(json.dumps(res, indent=1, default=lambda o: o.item()))
    print('POSITIVE', round(pos, 3), pos_ok)
    for f in FRACS:
        e = ev[f]
        print(f, 'G-IDS first', e['G_IDS_first'], '/', e['layouts'], '| acc med', round(e['acc_median'], 3),
              '| names-only', [round(a, 2) for a in e['acc_names_only']],
              '| R med', {L: round(statistics.median(v), 3) for L, v in e['R'].items()})
    print('f_dec', f_dec, 'f_disc', f_disc, '| VERDICT', verdict)

if __name__ == '__main__':
    main()
