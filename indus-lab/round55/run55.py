"""Round 55: stroke signs as a numeral class (M1) and X7 with stroke signs removed (M2). See PROTOCOL.md (locked first).
Standard library only. Run from this folder: python3 -I run55.py"""
import sys, json, random, re, statistics, collections, time
from pathlib import Path
P = Path(__file__).resolve().parent
for d in ('round52', 'round58'): sys.path.insert(0, str(P.parent / d))
import run52 as R52
import run58 as R58          # load(), sample_block(), verdict(), CONDS, rep()

S = ['001', '002', '003', '004', '005', '013', '014', '015', '016', '017', '018', '031', '032', '033', '034', '035', '036']
COUNT = {'001': 1, '031': 1, '002': 2, '032': 2, '003': 3, '013': 3, '033': 3, '004': 4, '014': 4, '034': 4,
         '005': 5, '035': 5, '016': 6, '017': 7, '018': 8}
NUM_N01 = re.compile(r'^[1-9]\(N01\)$')

def log(*a):
    print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def frames(texts):
    fr = collections.defaultdict(collections.Counter); tok = []
    for t in texts:
        for i, s in enumerate(t):
            f = (t[i - 1] if i else '^', t[i + 1] if i + 1 < len(t) else '$')
            fr[f][s] += 1; tok.append((s, f))
    return fr, tok

def F(setS, fr, tok):
    setS = set(setS); n = hit = 0
    for s, f in tok:
        if s in setS:
            n += 1
            if any(o != s and o in setS for o in fr[f]): hit += 1
    return hit / n if n else 0.0

def bins_of(texts):
    c = collections.Counter(s for t in texts for s in t)
    ranked = sorted(c, key=lambda s: (-c[s], s))
    return {s: i // 20 for i, s in enumerate(ranked)}, ranked

def matched_set(members, binof, ranked, rng):
    """Replace each member by a random non-member from the same frequency bin (nearest bin if exhausted), no repeats."""
    mem = set(members); used = set(); out = []
    pool = collections.defaultdict(list)
    for s in ranked:
        if s not in mem: pool[binof[s]].append(s)
    nb = max(binof.values())
    for m in members:
        b = binof[m]
        for d in range(nb + 1):
            cands = [x for bb in (b - d, b + d) if 0 <= bb <= nb for x in pool[bb] if x not in used]
            if cands: break
        x = rng.choice(cands); used.add(x); out.append(x)
    return out

def percentile(real, null):
    return (sum(1 for x in null if x < real) + 0.5 * sum(1 for x in null if x == real)) / len(null)

def m1(texts, members, nsets, rng):
    fr, tok = frames(texts); binof, ranked = bins_of(texts)
    members = [m for m in members if m in binof]
    real = F(members, fr, tok)
    null = [F(matched_set(members, binof, ranked, rng), fr, tok) for _ in range(nsets)]
    return real, null, members

def spearman(xs, ys):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys); mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float('nan')

def main():
    global LOG
    LOG = (P / 'run55.log').open('w', encoding='utf-8'); t0 = time.time(); out = dict(protocol='PROTOCOL.md')
    indus = [list(t) for t in R52.FC.TRAIN]; lengths = [len(t) for t in indus]; R52.N = sum(lengths)
    log('Indus texts', len(indus), 'tokens', R52.N)

    # ---------- M1 positive controls ----------
    ctl = {}
    pe = [l.split() for l in (P.parent / 'round52b' / 'controls' / 'PE.txt').open(encoding='utf-8') if l.strip()]
    u = [l.split() for c in ('U4', 'U3') for l in (P.parent / 'round52b' / 'controls' / f'{c}.txt').open(encoding='utf-8') if l.strip()]
    for name, units in (('PE', pe), ('U4+U3', u)):
        idx = R52.build_index(units, lengths); pcts = []
        for j in range(20):
            r = random.Random(55101 + j)
            smp = R52.indus_sample(units, idx, lengths, r)
            mem = sorted({s for t in smp for s in t if NUM_N01.match(s)})
            real, null, mem = m1(smp, mem, 200, random.Random(55301 + j))
            pcts.append(percentile(real, null))
        med = statistics.median(pcts)
        ctl[name] = dict(median_percentile=med, percentiles=pcts, passed=med >= 0.95)
        log(f'M1 control {name}: median percentile {med:.3f} -> {"PASS" if med >= 0.95 else "FAIL"}')
    out['m1_controls'] = ctl
    m1_void = not all(c['passed'] for c in ctl.values())

    # ---------- M1 on Indus ----------
    real, null, mem = m1(indus, S, 1000, random.Random(55001))
    pct = percentile(real, null)
    reading = 'VOID (control failed)' if m1_void else ('class' if pct >= 0.99 else ('no class behaviour detected' if pct < 0.95 else 'weak'))
    out['m1'] = dict(F=real, null_mean=statistics.mean(null), null_sd=statistics.stdev(null), percentile=pct,
                     members_present=mem, reading=reading)
    log(f'M1 Indus: F {real:.4f} null {statistics.mean(null):.4f} ({statistics.stdev(null):.4f}) percentile {pct:.3f} -> {reading}')

    # ---------- M2 pipeline check ----------
    data = R58.load('RV', 'S1')
    reps, _, _ = R58.sample_block('RV', 'S1', data, lengths, [58001 + b for b in range(300)])
    st = json.load((P.parent / 'round58' / 'results.json').open(encoding='utf-8'))['conditions']['RV_S1']
    pc = (statistics.mean(reps), min(reps), max(reps)) == (st['mean'], st['min'], st['max'])
    out['m2_pipeline'] = dict(mean=statistics.mean(reps), min=min(reps), max=max(reps), stored=[st['mean'], st['min'], st['max']], passed=pc)
    log('M2 pipeline check (round 58 RV_S1 reproduced):', 'PASS' if pc else 'FAIL')
    if not pc:
        log('VOID: M2 pipeline check failed'); out['m2'] = 'VOID'
    else:
        stripped = [[s for s in t if s not in set(S)] for t in indus]; stripped = [t for t in stripped if t]
        sl = [len(t) for t in stripped]; R52.N = sum(sl)
        In = R58.rep(stripped)
        out['m2_indus'] = dict(texts=len(stripped), tokens=R52.N, repeat=In)
        log(f'M2 stripped Indus: texts {len(stripped)} tokens {R52.N} repeat {In:.4f}')
        conds = {}
        for ci, (code, mode) in enumerate(R58.CONDS):
            data = R58.load(code, mode)
            reps, ext, homo = R58.sample_block(code, mode, data, sl, [56001 + ci * 1000 + b for b in range(300)])
            res = R58.verdict(reps, In); res['extended_share'] = ext
            if res['verdict'] == 'BORDERLINE':
                blocks = []
                for blk in range(10):
                    rb, _, _ = R58.sample_block(code, mode, data, sl, [70001 + ci * 1000 + blk * 300 + b for b in range(300)])
                    blocks.append(R58.verdict(rb, In)['verdict'] == 'EXCLUDED')
                res['replicate_blocks_excluded'] = sum(blocks); res['verdict'] = 'EXCLUDED' if sum(blocks) >= 8 else 'NOT EXCLUDED'
            hm = {k: statistics.mean(v) for k, v in homo.items()}
            res['homophony_k_needed'] = next((k for k in R58.KS if hm[k] <= In), '>12')
            conds[f'{code}_{mode}'] = res
            log(f'{code}_{mode}: mean {res["mean"]:.4f} sd {res["sd"]:.4f} min {res["min"]:.4f} k<=I {res["k_le_I"]} z {res["z"]:.1f} -> {res["verdict"]}'
                + (f' (replicates {res["replicate_blocks_excluded"]}/10)' if 'replicate_blocks_excluded' in res else '')
                + f' | homophony k {res["homophony_k_needed"]}')
        out['m2'] = conds
        v = [c['verdict'] for c in conds.values()]
        out['m2_summary'] = dict(excluded=v.count('EXCLUDED'), not_excluded=v.count('NOT EXCLUDED'))
        log('M2 SUMMARY', out['m2_summary'])

    # ---------- descriptive ----------
    c = collections.Counter(s for t in indus for s in t)
    byk = collections.Counter(); [byk.update({COUNT[s]: c[s]}) for s in COUNT]
    ks = list(range(1, 9)); d1 = dict(indus_by_count={k: byk[k] for k in ks}, indus_rho=spearman(ks, [byk[k] for k in ks]))
    for name, units in (('PE', pe), ('U4+U3', u)):
        cc = collections.Counter(s for t in units for s in t if NUM_N01.match(s))
        k9 = list(range(1, 10)); f = [cc[f'{k}(N01)'] for k in k9]
        d1[name] = dict(by_count=dict(zip(k9, f)), rho=spearman(k9, f))
    out['d1'] = d1; log('D1', json.dumps(d1))
    Sset = set(S); d2 = collections.Counter()
    for t in indus:
        if len(t) >= 2 and len(set(t)) < len(t):
            rep = {s for s, n in collections.Counter(t).items() if n > 1}
            d2['stroke only' if rep <= Sset else ('non-stroke only' if not rep & Sset else 'both')] += 1
    out['d2'] = dict(d2); log('D2 repeated-sign texts', dict(d2))
    pos = {'S': collections.Counter(), 'all': collections.Counter()}
    for t in indus:
        if len(t) < 2: continue
        for i, s in enumerate(t):
            p = 'initial' if i == 0 else ('final' if i == len(t) - 1 else 'medial')
            pos['all'][p] += 1
            if s in Sset: pos['S'][p] += 1
    d3 = {k: {p: v[p] / sum(v.values()) for p in ('initial', 'medial', 'final')} for k, v in pos.items()}
    out['d3'] = d3; log('D3 position shares', json.dumps(d3))
    log(f'time {time.time() - t0:.0f}s')
    json.dump(out, (P / 'results.json').open('w', encoding='utf-8'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
