"""Round 65: does a truth-free statistic rank the right language first in the round 64 logosyllabic setting? See PROTOCOL.md.
Run from this folder with ext/venv python: ../../ext/venv/bin/python run65.py. Requires numpy."""
import os
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS'): os.environ[v] = '1'
import sys, json, random, collections, hashlib, statistics, csv, re, unicodedata
from pathlib import Path
from multiprocessing import Pool
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round63')); sys.path.insert(0, str(P.parent / 'round64'))
import run63 as R63                                    # Greek cognate lexicon, syllabify
import run64 as R64                                    # cipher construction (set P), unchanged
B = R63.B; np = B.np

SEEDS = [65001, 65002, 65003, 65004, 65005]; EXTRA = [65006, 65007, 65008, 65009, 65010]
CHAIN_SEEDS = [65300, 65301, 65302, 65303]; STEPS = 600_000; NMAX = 1500
IDS_LANGS = {'G-IDS': '167', 'G-mod': '168', 'Finnish': '128', 'Basque': '219', 'Hungarian': '131', 'Hawaiian': '235',
             'Maori': '236', 'Spanish': '176', 'Latin': '169', 'Sanskrit': '211', 'Persian': '214'}
WRONG = ['Finnish', 'Basque', 'Hungarian', 'Hawaiian', 'Maori', 'Spanish', 'Latin', 'Sanskrit', 'Persian']
LANGS = ['G-same', 'G-IDS', 'G-mod'] + WRONG

# ---------- lexicons (protocol spelling rule) ----------
CMAP = {'æ': 'a', 'ɑ': 'a', 'ə': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ø': 'o', 'b': 'p', 'g': 'k', 'f': 'p', 'v': 'w', 'l': 'r', 'h': '',
        'c': 'k', 'q': 'k', 'x': 'ks', 'y': 'j', 'ŋ': 'n', 'ɲ': 'n', 'ð': 'd', 'θ': 't', 'ɣ': 'k', 'ʃ': 's', 'ʒ': 'z'}
def spell(piece):
    s = piece.lower()
    for ch in ('ʰ', "'", 'ʔ'): s = s.replace(ch, '')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    s = ''.join(CMAP.get(c, c) for c in s)
    return R63.syllabify(''.join(c for c in s if 'a' <= c <= 'z'))

def lexicon(name):
    if name == 'G-same': return R63.lexicon('greek')
    forms = [r['Form'] for r in csv.DictReader(R63.IDS.open(encoding='utf-8')) if r['Language_ID'] == IDS_LANGS[name]]
    words = sorted({tuple(w) for f in forms for p in re.split(r'[\s\-.]+', f) if p for w in [spell(p)] if w})
    if len(words) > NMAX: words = sorted(random.Random(65900).sample(words, NMAX))
    return [list(w) for w in words]

def seq_ll(lm, segs):
    """Bigram LM log-likelihood per token of syllable segments (round 32 conventions: BOS/EOS, OOV)."""
    tot = tok = 0.0
    for s in segs:
        q = [B.BOS] + [B.VI.get(x, B.OOV) for x in s] + [B.EOS]
        tot += sum(lm[a, b] for a, b in zip(q, q[1:])); tok += len(s)
    return tot / tok

def order_info(lex, lm):
    rng = random.Random(65800); idx = list(range(len(lex))); rng.shuffle(idx); segs = []
    while idx:
        k = rng.choice([1, 2, 3]); segs.append([x for i in idx[:k] for x in lex[i]]); idx = idx[k:]
    rs = random.Random(65801); shuf = []
    for s in segs:
        t = list(s); rs.shuffle(t); shuf.append(t)
    return seq_ll(lm, segs) - seq_ll(lm, shuf)

def decoy(types, seed):
    rng = random.Random(seed + 700); out = collections.Counter()
    for seg, n in types.items():
        for _ in range(n):
            t = list(seg); rng.shuffle(t); out[tuple(t)] += 1
    return out

_LEX = {}
def job(spec):
    lang, seed, which = spec
    if lang not in _LEX:
        lex = lexicon(lang); lm = B.fit_lm(lex); _LEX[lang] = (lex, lm, order_info(lex, lm))
    lex, lm, I = _LEX[lang]
    c = R64.build(R64.Q, 'R2', 70, seed, True)
    types = c['types'] if which == 'real' else decoy(c['types'], seed)
    sc = B.Scorer(types, c['nsign'], lm); B.STEPS = STEPS
    chains = [B.anneal(sc, c['nsign'], False, cs) for cs in CHAIN_SEEDS]
    best = max(chains, key=lambda x: x[0]); mp = best[1]
    ll = float((sc.total(mp) * sc.cnt).sum()) / sc.tokens
    acc = sum(n for x, n in c['cnt'].items() if x < c['nsound'] and x not in c['opq'] and mp[x] == c['truth'][x]) / c['sound_tokens']
    res = dict(lang=lang, seed=seed, cipher=which, lexicon_words=len(lex), I=I, LL=ll, best_objective=best[0],
               tokens=int(sc.tokens), accuracy=acc)
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()}), flush=True)
    return res

def table(out, seeds):
    get = {(r['lang'], r['seed'], r['cipher']): r for r in out}
    rows = {}
    for s in seeds:
        for L in LANGS:
            re_, de = get[(L, s, 'real')], get[(L, s, 'decoy')]
            D = re_['LL'] - de['LL']
            rows[(L, s)] = dict(D=D, I=re_['I'], R=D / re_['I'], LL_real=re_['LL'], obj_real=re_['best_objective'], accuracy=re_['accuracy'])
    return rows

def firsts(rows, seeds, cand):
    return sum(all(rows[(cand, s)]['R'] > rows[(w, s)]['R'] for w in WRONG) for s in seeds)

def main():
    jobs = [(L, s, w) for s in SEEDS for L in LANGS for w in ('real', 'decoy')]
    with Pool(int(os.environ.get('R65_PROCS', 8))) as pool:
        out = pool.map(job, jobs, chunksize=1)
        rows = table(out, SEEDS); seeds = list(SEEDS)
        f_ids, f_same = firsts(rows, seeds, 'G-IDS'), firsts(rows, seeds, 'G-same')
        robust = f_ids == 3 or f_same == 3
        if robust:
            out += pool.map(job, [(L, s, w) for s in EXTRA for L in LANGS for w in ('real', 'decoy')], chunksize=1)
            seeds = SEEDS + EXTRA; rows = table(out, seeds)
            f_ids, f_same = firsts(rows, seeds, 'G-IDS'), firsts(rows, seeds, 'G-same')
    n = len(seeds); hi, lo = (4, 2) if n == 5 else (7, 5)
    pos = statistics.median(rows[('G-same', s)]['accuracy'] for s in SEEDS); pos_ok = pos >= 0.70
    if not pos_ok: verdict = 'VOID'
    elif f_same < hi: verdict = 'CANNOT DISCRIMINATE'
    elif f_ids >= hi: verdict = 'DISCRIMINATES'
    elif f_ids <= lo: verdict = 'ONLY WITH THE TEXT\'S OWN WORDS'
    else: verdict = 'IN BETWEEN'
    rank = {}
    for s in seeds:
        order = sorted(['G-IDS'] + WRONG, key=lambda L: -rows[(L, s)]['R'])
        rank[s] = order
    summary = {L: dict(R=[rows[(L, s)]['R'] for s in seeds], D=[rows[(L, s)]['D'] for s in seeds], I=rows[(L, seeds[0])]['I'],
                       LL_real=[rows[(L, s)]['LL_real'] for s in seeds], accuracy=[rows[(L, s)]['accuracy'] for s in seeds],
                       R_median=statistics.median(rows[(L, s)]['R'] for s in seeds)) for L in LANGS}
    res = dict(protocol_sha256=hashlib.sha256((P / 'PROTOCOL.md').read_bytes()).hexdigest(), seeds=seeds, robustness_run=robust,
               positive_control=dict(median_accuracy=pos, passed=pos_ok), G_IDS_first=f_ids, G_same_first=f_same, of=n,
               ranking_by_layout={str(s): rank[s] for s in seeds}, summary=summary, verdict=verdict, runs=out)
    (P / 'results.json').write_text(json.dumps(res, indent=1, default=lambda o: o.item()))
    print('POSITIVE', round(pos, 3), pos_ok, '| G-IDS first', f_ids, '/', n, '| G-same first', f_same, '/', n)
    for L in LANGS: print(f"{L:10s} I {summary[L]['I']:.3f} R med {summary[L]['R_median']:.3f}", [round(x, 3) for x in summary[L]['R']])
    print('VERDICT', verdict)

if __name__ == '__main__':
    main()
