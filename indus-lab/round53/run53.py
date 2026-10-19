"""Round 53: multi-sign words vs one sign per word. See PROTOCOL.md (committed before this file).
Standard library only. Run from this folder: python3 run53.py"""
import sys, json, math, random, collections, time
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round30'))
import foreign_context as FC

SEED = 53001; B = 100
MULTI = ['SEAL', 'SUX', 'OBL', 'OAL']; SINGLE = ['CHN']; OTHER = ['OBI']
TAUS = [x / 4 for x in range(-8, 25)]   # -2 .. 6 step 0.25

def log(*a):
    print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def load(code):
    units = []
    for l in (P / 'controls' / f'{code}.txt').open(encoding='utf-8'):
        if not l.strip(): continue
        words = [w.split() for w in l.strip().split(' | ')]
        signs = [s for w in words for s in w]
        gold = set(); i = 0
        for w in words[:-1]: i += len(w); gold.add(i)        # boundary after sign index i-1
        units.append((signs, gold))
    return units

def sample(units, N, rng):
    out = []; total = 0
    while total < N:
        signs, gold = rng.choice(units)
        if total + len(signs) > N:
            k = N - total; signs = signs[:k]; gold = {g for g in gold if g < k}
        out.append((signs, gold)); total += len(signs)
    return out

def pmi_table(texts):
    pair = collections.Counter(); left = collections.Counter(); right = collections.Counter()
    for signs, _ in texts:
        for a, b in zip(signs, signs[1:]): pair[(a, b)] += 1; left[a] += 1; right[b] += 1
    T = sum(pair.values())
    return {ab: (math.log2(c * T / (left[ab[0]] * right[ab[1]])) if c >= 2 else -math.inf) for ab, c in pair.items()}

def segment(texts, pmi, tau):
    """returns per text the set of placed boundaries"""
    return [{i + 1 for i, (a, b) in enumerate(zip(s, s[1:])) if pmi[(a, b)] < tau} for s, _ in texts]

def f1(placed, texts):
    tp = fp = fn = 0
    for b, (_, gold) in zip(placed, texts):
        tp += len(b & gold); fp += len(b - gold); fn += len(gold - b)
    p = tp / (tp + fp) if tp + fp else 0; r = tp / (tp + fn) if tp + fn else 0
    return 2 * p * r / (p + r) if p + r else 0

def random_f1(placed, texts, rng, reps=100):
    rate = sum(len(b) for b in placed) / max(1, sum(len(s) - 1 for s, _ in texts))
    acc = 0
    for _ in range(reps):
        rb = [{i + 1 for i in range(len(s) - 1) if rng.random() < rate} for s, _ in texts]
        acc += f1(rb, texts)
    return acc / reps

def stats(placed, texts, pmi=None, minc=None, sample_counts=None):
    seg_lengths = []; multi_units = 0; n_units = 0
    for b, (s, _) in zip(placed, texts):
        if minc and any(sample_counts[x] < minc for x in s): continue
        n_units += 1; cuts = sorted(b); prev = 0; lens = []
        for c in cuts + [len(s)]: lens.append(c - prev); prev = c
        seg_lengths += lens
        if any(l >= 2 for l in lens): multi_units += 1
    return (sum(seg_lengths) / len(seg_lengths) if seg_lengths else 0), (multi_units / n_units if n_units else 0), n_units

def main():
    global LOG
    LOG = (P / 'run53.log').open('w', encoding='utf-8'); t0 = time.time()
    indus = [(list(t), set()) for t in FC.TRAIN]; N = sum(len(s) for s, _ in indus)
    corpora = {c: load(c) for c in MULTI + SINGLE + OTHER}
    for c, u in corpora.items(): log(c, 'units', len(u), 'tokens', sum(len(s) for s, _ in u), 'mean unit len', round(sum(len(s) for s, _ in u) / len(u), 2))
    samples = {c: [sample(corpora[c], N, random.Random(SEED + ci * 1000 + b)) for b in range(B)] for ci, c in enumerate(corpora)}
    pmis = {c: [pmi_table(t) for t in samples[c]] for c in corpora}
    # calibrate tau on MULTI only
    best = None
    for tau in TAUS:
        m = sum(sum(f1(segment(t, p, tau), t) for t, p in zip(samples[c], pmis[c])) / B for c in MULTI) / len(MULTI)
        if best is None or m > best[1]: best = (tau, m)
    tau = best[0]; log('tau*', tau, 'mean MULTI F1', round(best[1], 3))
    # positive control
    passed = []; ctrl = {}
    for c in MULTI:
        rng = random.Random(SEED + 77)
        fs = []; rs = []
        for t, p in zip(samples[c], pmis[c]):
            pl = segment(t, p, tau); fs.append(f1(pl, t)); rs.append(random_f1(pl, t, rng, 20))
        mf = sum(fs) / B; mr = sum(rs) / B; ctrl[c] = dict(f1=mf, random_f1=mr, margin=mf - mr)
        if mf - mr >= 0.15: passed.append(c)
        log('control', c, 'F1', round(mf, 3), 'random', round(mr, 3), 'margin', round(mf - mr, 3))
    control = 'PASS' if len(passed) >= 3 else 'METHOD-FAIL'
    log('positive control', control, 'passed', passed)
    # statistics
    res = {}
    for c in corpora:
        Ss = []; Ms = []; S5 = []
        for t, p in zip(samples[c], pmis[c]):
            pl = segment(t, p, tau); cnt = collections.Counter(x for s, _ in t for x in s)
            S, M, _ = stats(pl, t); s5, _, n5 = stats(pl, t, p, 5, cnt); Ss.append(S); Ms.append(M); S5.append(s5)
        mean = lambda v: sum(v) / len(v); sd = lambda v: math.sqrt(sum((x - mean(v)) ** 2 for x in v) / (len(v) - 1))
        res[c] = dict(S=mean(Ss), S_sd=sd(Ss), M=mean(Ms), M_sd=sd(Ms), S_min5=mean(S5))
        log(c, 'S', round(mean(Ss), 3), '±', round(sd(Ss), 3), 'M', round(mean(Ms), 3), '±', round(sd(Ms), 3), 'S(min count 5)', round(mean(S5), 3))
    p_ind = pmi_table(indus); pl = segment(indus, p_ind, tau); cnt = collections.Counter(x for s, _ in indus for x in s)
    S_i, M_i, _ = stats(pl, indus); S5_i, _, n5 = stats(pl, indus, p_ind, 5, cnt)
    seg_hist = collections.Counter()
    for b, (s, _) in zip(pl, indus):
        prev = 0
        for c_ in sorted(b) + [len(s)]: seg_hist[c_ - prev] += 1; prev = c_
    log('Indus S', round(S_i, 3), 'M', round(M_i, 3), 'S(min count 5)', round(S5_i, 3), 'units kept', n5, 'segment length histogram', dict(sorted(seg_hist.items())))
    # verdict
    def near(x, c, key): return abs(x - res[c][key]) <= 2 * res[c][key + '_sd']
    def verdict_on(x, key):
        if control != 'PASS': return 'METHOD-FAIL'
        multi_vals = [res[c][key] for c in passed]; s_multi = min(multi_vals); s_single = res['CHN'][key]
        above_single = x > s_single + 2 * res['CHN'][key + '_sd']; below_multi = x < s_multi - 2 * max(res[c][key + '_sd'] for c in passed)
        if (any(near(x, c, key) for c in passed) or x >= s_multi) and above_single: return 'MULTI-SIGN-WORDS'
        if (near(x, 'CHN', key) or x <= s_single) and below_multi: return 'SINGLE-SIGN-WORDS'
        return 'BETWEEN'
    vS = verdict_on(S_i, 'S'); vM = verdict_on(M_i, 'M')
    verdict = vS if vS == vM else ('METHOD-FAIL' if control != 'PASS' else 'BETWEEN')
    log('verdict on S', vS, 'on M', vM, 'VERDICT', verdict)
    # negative-control diagnostic
    r = random.Random(SEED + 9); sh = []
    for s, _ in indus: s2 = s[:]; r.shuffle(s2); sh.append((s2, set()))
    p_sh = pmi_table(sh); S_sh, M_sh, _ = stats(segment(sh, p_sh, tau), sh)
    log('Indus shuffled within texts: S', round(S_sh, 3), 'M', round(M_sh, 3))
    # top cohesive pairs for the report
    top = sorted(((v, ab) for ab, v in p_ind.items() if v > -math.inf), reverse=True)[:15]
    pair_c = collections.Counter((a, b) for s, _ in indus for a, b in zip(s, s[1:]))
    log('top Indus cohesive pairs (PMI, pair, count):', [(round(v, 2), '-'.join(ab), pair_c[ab]) for v, ab in top])
    json.dump(dict(seed=SEED, B=B, N=N, tau=tau, calib_f1=best[1], control=control, passed=passed, controls=ctrl, corpora=res,
                   indus=dict(S=S_i, M=M_i, S_min5=S5_i, seg_hist=dict(seg_hist)), shuffled=dict(S=S_sh, M=M_sh),
                   verdict=verdict, verdict_S=vS, verdict_M=vM, top_pairs=[(v, list(ab), pair_c[ab]) for v, ab in top]),
              (P / 'results.json').open('w'), indent=1)
    log('done', round(time.time() - t0, 1), 's')

if __name__ == '__main__': main()
