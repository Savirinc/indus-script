"""Round 58: Sanskrit/Tamil syllable repetition at Indus lengths. See PROTOCOL.md (locked before this file).
Standard library only. Run from this folder after extract58.py: python3 -I run58.py"""
import sys, json, math, random, statistics, time
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round52')); sys.path.insert(0, str(P.parent / 'round47')); sys.path.insert(0, str(P))
import run52 as R52          # features(), indus_sample(), build_index() unchanged; imports round30 FC
import run47 as R47          # read_v (descriptive item 2)
import extract58 as X

SOURCES = ['RV', 'RAM', 'SKW', 'SKN', 'PUR', 'TMW', 'TMN']
SHORT = {'SKW': 'words', 'TMW': 'words', 'SKN': 'names', 'TMN': 'names'}
CONDS = [(s, m) for s in SOURCES for m in ('S1', 'S2')]
B = 300; KS = [2, 3, 4, 6, 8, 12]; I_MERGED = 0.177

def log(*a):
    print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def load(code, mode):
    lines = [l.rstrip('\n') for l in (P / 'controls' / f'{code}_{mode}.txt').open(encoding='utf-8') if l.strip()]
    if code in ('SKW', 'TMW'): return [[w.split() for w in l.split(' | ') if w.split()] for l in lines]
    return [l.split() for l in lines]

def short_prep(data, kind, lengths):
    flat = [(si, wi) for si, s in enumerate(data) for wi in range(len(s))] if kind == 'words' else None
    units = [data[si][wi] for si, wi in flat] if kind == 'words' else data
    return flat, units, R52.build_index(units, lengths)

def short_sample(data, kind, prep, lengths, rng, N):
    """Indus-shaped sample from words (grouped by sentence) or names; concatenation fallback (PROTOCOL.md)."""
    flat, units, idx = prep
    texts = []; total = 0; ext = 0
    while total < N:
        l = rng.choice(lengths)
        if total + l > N: l = N - total
        if idx[l]:
            u = rng.choice(idx[l])
        else:
            ext += 1
            if kind == 'words':
                while True:
                    si, wi = rng.choice(flat); u = []
                    for w in data[si][wi:]:
                        u = u + w
                        if len(u) >= l: break
                    if len(u) >= l: break
            else:
                u = list(rng.choice(units))
                while len(u) < l: u += rng.choice(units)
        st = rng.randrange(len(u) - l + 1); texts.append(u[st:st + l]); total += l
    return texts, ext

def rep(texts):
    long_ = [t for t in texts if len(t) >= 2]
    return sum(1 for t in long_ if len(set(t)) < len(t)) / len(long_)

def homophone(texts, k, rng): return [[(u, rng.randrange(k)) for u in t] for t in texts]

def sample_block(code, mode, data, lengths, seeds):
    reps = []; exts = 0; ntexts = 0; homo = {k: [] for k in KS}
    if code not in SHORT: idx = R52.build_index(data, lengths)
    else: prep = short_prep(data, SHORT[code], lengths)
    for sd in seeds:
        r = random.Random(sd)
        if code in SHORT: texts, e = short_sample(data, SHORT[code], prep, lengths, r, R52.N)
        else: texts = R52.indus_sample(data, idx, lengths, r); e = 0
        reps.append(R52.features(texts, r)['repeat']); exts += e; ntexts += len(texts)
        hr = random.Random(sd + 500000)
        for k in KS: homo[k].append(rep(homophone(texts, k, hr)))
    return reps, exts / ntexts, homo

def verdict(reps, I):
    m = statistics.mean(reps); s = statistics.stdev(reps); k = sum(1 for x in reps if x <= I)
    z = (m - I) / s if s else float('inf')
    v = 'EXCLUDED' if k == 0 and z >= 5 else ('NOT EXCLUDED' if k >= 3 else 'BORDERLINE')
    return dict(mean=m, sd=s, min=min(reps), max=max(reps), k_le_I=k, z=z, verdict=v)

def main():
    global LOG
    LOG = (P / 'run58.log').open('w', encoding='utf-8'); t0 = time.time()
    out = dict(protocol='PROTOCOL.md', B=B)
    # ---- control 3: syllabifier ----
    ok = X.check(); out['syllabifier_check'] = ok
    if not ok: log('VOID: syllabifier check failed'); return
    # ---- control 1: pipeline ----
    indus = [list(t) for t in R52.FC.TRAIN]; lengths = [len(t) for t in indus]; R52.N = sum(lengths)
    I = R52.features(indus, random.Random(58000))['repeat']
    log('Indus texts', len(indus), 'tokens', R52.N, 'repeat', round(I, 6))
    seal = [l.split() for l in (P.parent / 'round52b' / 'controls' / 'SEAL.txt').open(encoding='utf-8') if l.strip()]
    r = random.Random(52101 + 6 * 1000 + 0)
    seal0 = R52.features(R52.indus_sample(seal, R52.build_index(seal, lengths), lengths, r), r)['repeat']
    stored = json.load((P.parent / 'round52b' / 'results.json').open())['samples']['SEAL'][0]['repeat']
    pc1 = round(I, 4) == 0.0351 and seal0 == stored
    out['control_pipeline'] = dict(indus_repeat=I, seal_sample0=seal0, seal_stored=stored, passed=pc1)
    log('control 1 (pipeline):', 'PASS' if pc1 else 'FAIL', out['control_pipeline'])
    # ---- control 2: sampler on Indus itself ----
    iidx = R52.build_index(indus, lengths); sr = []
    for b in range(B):
        rr = random.Random(58901 + b); sr.append(R52.features(R52.indus_sample(indus, iidx, lengths, rr), rr)['repeat'])
    pc2 = abs(statistics.mean(sr) - I) <= 0.01
    out['control_sampler'] = dict(mean=statistics.mean(sr), sd=statistics.stdev(sr), passed=pc2)
    log('control 2 (sampler on Indus):', 'PASS' if pc2 else 'FAIL', out['control_sampler'])
    if not (pc1 and pc2): log('VOID: control failed'); out['verdict'] = 'VOID'; json.dump(out, (P / 'results.json').open('w'), indent=1); return
    # ---- conditions ----
    out['conditions'] = {}
    for ci, (code, mode) in enumerate(CONDS):
        data = load(code, mode)
        types = len({u for x in data for w in (x if code in ('SKW', 'TMW') else [x]) for u in w})
        reps, extshare, homo = sample_block(code, mode, data, lengths, [58001 + ci * 1000 + b for b in range(B)])
        res = verdict(reps, I); res.update(units=len(data), syllable_types=types, extended_share=extshare)
        if res['verdict'] == 'BORDERLINE':
            blocks = []
            for blk in range(10):
                rb, _, _ = sample_block(code, mode, data, lengths, [59001 + ci * 1000 + blk * 300 + b for b in range(B)])
                blocks.append(verdict(rb, I)['verdict'] == 'EXCLUDED')
            res['replicate_blocks_excluded'] = sum(blocks)
            res['verdict'] = 'EXCLUDED' if sum(blocks) >= 8 else 'NOT EXCLUDED'
        hm = {k: statistics.mean(v) for k, v in homo.items()}
        need = next((k for k in KS if hm[k] <= I), None)
        res['homophony'] = dict(mean_by_k=hm, k_needed=need if need else '>12',
                                implied_inventory=(need * types) if need else f'>{12 * types}')
        res['vs_merged_0177'] = dict(k_le=sum(1 for x in reps if x <= I_MERGED), mean_minus=statistics.mean(reps) - I_MERGED)
        out['conditions'][f'{code}_{mode}'] = res
        log(f'{code}_{mode}: units {len(data)} types {types} mean {res["mean"]:.4f} sd {res["sd"]:.4f} min {res["min"]:.4f} '
            f'k<=I {res["k_le_I"]} z {res["z"]:.1f} ext {extshare:.3f} -> {res["verdict"]}'
            + (f' (replicates {res["replicate_blocks_excluded"]}/10)' if 'replicate_blocks_excluded' in res else '')
            + f' | homophony k needed {res["homophony"]["k_needed"]} | samples <= 0.177: {res["vs_merged_0177"]["k_le"]}')
    # ---- descriptive 2: Yajnadevam's readings in reading space ----
    key = json.load((P.parent / 'round46-brahmi-coverage' / 'expanded-map.json').open())
    kept = [t for t in indus if all(s in key for s in t)]
    def iast(s): return s.replace('aa', 'ā').replace('A', 'ā').replace('ii', 'ī')
    rd = [X.sk_syl(iast(R47.read_v([key[s] for s in t])), 'S1') for t in kept]
    out['yajnadevam'] = dict(texts=len(kept), repeat_S1=rep(rd), repeat_signs=rep(kept))
    log('Yajnadevam readings: texts', len(kept), 'reading-space repeat (S1)', round(rep(rd), 4), 'sign-space repeat', round(rep(kept), 4))
    v = [c['verdict'] for c in out['conditions'].values()]
    out['summary'] = dict(excluded=v.count('EXCLUDED'), not_excluded=v.count('NOT EXCLUDED'))
    log('SUMMARY', out['summary'], f'time {time.time() - t0:.0f}s')
    json.dump(out, (P / 'results.json').open('w', encoding='utf-8'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
