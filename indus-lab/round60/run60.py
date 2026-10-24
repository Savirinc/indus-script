"""Round 60: does sign order matter under the atlas key? Measurement, see PROTOCOL.md. Stdlib only.
Usage: python3 -I run60.py   (writes results.json and order_ledger.csv here)"""
import sys, json, csv, random, statistics
from pathlib import Path
P = Path(__file__).resolve().parent; LAB = P.parent
sys.path.insert(0, str(LAB / 'readings-atlas'))
import build_atlas as A
R = A.R
NP = 20

CACHE = {}
def cov_str(s):
    if s not in CACHE: CACHE[s] = A.gloss([s])[1]
    return CACHE[s]
def cov_tokens(toks): return A.gloss(A.reading(toks))[1] if '?' not in toks else None

def perms_for(texts, seed):
    rng = random.Random(seed)
    return [[rng.sample(range(len(t)), len(t)) for _ in range(NP)] for t in texts]

def arm(texts, score, perms):
    """score(seq) -> coverage. Returns T, Rev, P list (means over texts), G, Grev, pct, z, and per-text detail."""
    tr = [score(t) for t in texts]; rv = [score(t[::-1]) for t in texts]
    pj = [[score([t[i] for i in perms[k][j]]) for k, t in enumerate(texts)] for j in range(NP)]
    T = statistics.mean(tr); Rv = statistics.mean(rv); Pm = [statistics.mean(x) for x in pj]
    sd = statistics.stdev(Pm); G = T - statistics.mean(Pm)
    return dict(T=T, Rev=Rv, P=Pm, G=G, Grev=T - Rv, pct=sum(1 for x in Pm if x < T) / NP, z=G / sd if sd > 0 else float('inf')), (tr, rv, pj)

def key_score(key): return lambda seq: cov_tokens([key[s] for s in seq])
def unit_score(sub=None): return lambda seq: cov_str(''.join(sub[u] if sub else u for u in seq))

def main():
    # ---- inscriptions ----
    recs = [c for c in A.CAND if A.signs_of(c)]
    for c in recs: c['signs'] = A.signs_of(c)
    alltexts = [[s for s in c['signs'] if s in A.KEY] for c in recs]
    signs = sorted({s for t in alltexts for s in t}); bins = R.freq_bins(alltexts, signs)
    base = {s: A.KEY[s] for s in signs}
    shuf = {sd: R.shuffle_key(base, bins, random.Random(sd)) for sd in range(46901, 46941)}
    seen, texts, ids = set(), [], []
    for c in recs:
        t = tuple(c['signs'])
        if len(t) >= 3 and all(s in A.KEY for s in t) and t not in seen:
            seen.add(t); texts.append(list(t)); ids.append(c['id'])
    lens = [len(t) for t in texts]
    print(f'inscriptions: {len(texts)} distinct, fully assigned, length >= 3; mean length {statistics.mean(lens):.2f}', flush=True)
    out = dict(n_inscriptions=len(texts), mean_length=statistics.mean(lens))

    # ---- positive control: Ramayana windows ----
    lines = [l.split() for l in open(LAB / 'round58' / 'controls' / 'RAM_S1.txt', encoding='utf-8') if l.split()]
    rng = random.Random(60201); win = []
    for n in lens:
        cand = [l for l in lines if len(l) >= n]
        l = rng.choice(cand); i = rng.randrange(len(l) - n + 1); win.append(l[i:i + n])
    cperm = perms_for(win, 60202)
    pc, _ = arm(win, unit_score(), cperm)
    ut = sorted({u for w in win for u in w}); ubins = R.freq_bins(win, ut); ident = {u: u for u in ut}
    pc_sub = [arm(win, unit_score(R.shuffle_key(ident, ubins, random.Random(sd))), cperm)[0]['G'] for sd in range(60401, 60421)]
    pc_pass = pc['pct'] == 1.0 and pc['z'] >= 3 and all(pc['G'] > g for g in pc_sub)
    out['positive_control'] = dict(pc, G_substitutions=pc_sub, passed=pc_pass)
    print(f"positive control (Ramayana): T {pc['T']:.3f} perm-mean {statistics.mean(pc['P']):.3f} rev {pc['Rev']:.3f} G {pc['G']:.4f} z {pc['z']:.2f} pct {pc['pct']:.2f}; "
          f"substitution G max {max(pc_sub):.4f} mean {statistics.mean(pc_sub):.4f} -> {'PASS' if pc_pass else 'FAIL'}", flush=True)

    # ---- negative control: order-free strings ----
    freq = {}
    for l in lines:
        for u in l: freq[u] = freq.get(u, 0) + 1
    us, ws = list(freq), list(freq.values()); rng = random.Random(60301)
    iid = [rng.choices(us, ws, k=n) for n in lens]
    nc, _ = arm(iid, unit_score(), perms_for(iid, 60302))
    nc_pass = abs(nc['z']) < 3
    out['negative_control'] = dict(nc, passed=nc_pass)
    print(f"negative control (order-free): G {nc['G']:.4f} z {nc['z']:.2f} pct {nc['pct']:.2f} -> {'PASS' if nc_pass else 'FAIL'}", flush=True)

    # ---- Indus ----
    iperm = perms_for(texts, 60101)
    at, (tr, rv, pj) = arm(texts, key_score(A.KEY), iperm)
    sk = {sd: arm(texts, key_score(shuf[sd]), iperm)[0] for sd in range(46901, 46921)}
    print(f"atlas key: T {at['T']:.4f} perm-mean {statistics.mean(at['P']):.4f} rev {at['Rev']:.4f} G {at['G']:.4f} Grev {at['Grev']:.4f} z {at['z']:.2f} pct {at['pct']:.2f}", flush=True)
    for sd, a in sk.items():
        print(f"  scrambled {sd}: T {a['T']:.4f} G {a['G']:.4f} Grev {a['Grev']:.4f} z {a['z']:.2f} pct {a['pct']:.2f}", flush=True)
    ge = sum(1 for a in sk.values() if a['G'] >= at['G'])
    out['atlas'] = at; out['scrambled'] = {str(k): v for k, v in sk.items()}; out['scrambled_G_at_or_above'] = ge
    robust = {}
    if ge == 1:
        sk2 = {sd: arm(texts, key_score(shuf[sd]), iperm)[0] for sd in range(46921, 46941)}
        ge40 = ge + sum(1 for a in sk2.values() if a['G'] >= at['G'])
        robust['extra_keys'] = {str(k): v for k, v in sk2.items()}; robust['at_or_above_of_40'] = ge40
        print(f'robustness: {ge40} of 40 scrambled keys at or above', flush=True)
    key_ok = ge == 0 or (ge == 1 and robust['at_or_above_of_40'] <= 2)

    def verdict(a, key_ok):
        if a['pct'] == 1.0 and a['z'] >= 3: return 'ORDER SIGNAL' if key_ok else 'ORDER, NOT KEY'
        return 'NO ORDER EFFECT'
    v = verdict(at, key_ok)
    if 2.5 <= at['z'] <= 3.5:
        reps = [verdict(arm(texts, key_score(A.KEY), perms_for(texts, sd))[0], key_ok) for sd in range(60111, 60121)]
        robust['perm_redraws'] = reps
        if sum(1 for x in reps if x == v) < 8: v = 'NO ORDER EFFECT (not robust)'
        print(f'robustness redraws: {reps}', flush=True)
    out['robustness'] = robust
    out['verdict'] = v if (pc_pass and nc_pass) else 'VOID'
    print('VERDICT:', out['verdict'], '' if out['verdict'] != 'VOID' else f'(descriptive verdict would be {v})', flush=True)
    json.dump(out, open(P / 'results.json', 'w'), indent=1)

    # ---- per-inscription ledger ----
    with open(P / 'order_ledger.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['record_id', 'signs_reading_order', 'reading_true', 'coverage_true', 'reading_reversed', 'coverage_reversed',
                    'coverage_permutations_mean', 'share_permutations_at_or_above_true'])
        for k, t in enumerate(texts):
            ps = [pj[j][k] for j in range(NP)]
            w.writerow([ids[k], ' '.join(t), ' '.join(A.reading([A.KEY[s] for s in t])), f'{tr[k]:.2f}',
                        ' '.join(A.reading([A.KEY[s] for s in t[::-1]])), f'{rv[k]:.2f}', f'{statistics.mean(ps):.2f}',
                        f'{sum(1 for x in ps if x >= tr[k]) / NP:.2f}'])

if __name__ == '__main__':
    main()
