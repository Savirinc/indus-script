"""Round 53b: Dirichlet-process unigram word segmentation (Goldwater et al. 2009), Gibbs over boundaries.
See PROTOCOL.md (committed before this file). Standard library only. Run from this folder: python3 run53b.py"""
import sys, json, math, random, collections, time
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round53')); sys.path.insert(0, str(P.parent / 'round30'))
import run53 as R53          # load(), sample(), f1(), random_f1(), stats()
import foreign_context as FC
R53.P = P.parent / 'round53'  # controls live there

SEED = 53101; B = 30; ALPHA = 20.0; PSTOP = 0.5; SWEEPS = 150
MULTI = R53.MULTI; SINGLE = R53.SINGLE; OTHER = R53.OTHER

def log(*a):
    print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def dp_segment(texts, rng):
    """texts: list of (signs, gold). Returns list of boundary sets."""
    units = [s for s, _ in texts]
    tot = collections.Counter(x for u in units for x in u); T = sum(tot.values())
    lp = {s: math.log(c / T) for s, c in tot.items()}
    p0cache = {}
    def P0(w):
        v = p0cache.get(w)
        if v is None:
            v = PSTOP * (1 - PSTOP) ** (len(w) - 1) * math.exp(sum(lp[x] for x in w)); p0cache[w] = v
        return v
    # state
    bnd = [[rng.random() < 0.5 for _ in range(len(u) - 1)] for u in units]   # bnd[k][i-1] = boundary before sign i
    n = collections.Counter(); N = 0
    def words_of(k):
        u = units[k]; out = []; l = 0
        for i in range(1, len(u)):
            if bnd[k][i - 1]: out.append(tuple(u[l:i])); l = i
        out.append(tuple(u[l:])); return out
    for k in range(len(units)):
        for w in words_of(k): n[w] += 1; N += 1
    positions = [(k, i) for k, u in enumerate(units) for i in range(1, len(u))]
    for sweep in range(SWEEPS):
        temp = 2.0 - (sweep / (SWEEPS / 2)) if sweep < SWEEPS / 2 else 1.0
        rng.shuffle(positions)
        for k, i in positions:
            u = units[k]; b = bnd[k]
            l = i - 1
            while l > 0 and not b[l - 1]: l -= 1
            r = i + 1
            while r < len(u) and not b[r - 1]: r += 1
            w = tuple(u[l:r]); w1 = tuple(u[l:i]); w2 = tuple(u[i:r])
            if b[i - 1]: n[w1] -= 1; n[w2] -= 1; N -= 2
            else: n[w] -= 1; N -= 1
            p_no = (n[w] + ALPHA * P0(w)) / (N + ALPHA)
            p_yes = (n[w1] + ALPHA * P0(w1)) / (N + ALPHA) * (n[w2] + (1 if w1 == w2 else 0) + ALPHA * P0(w2)) / (N + 1 + ALPHA)
            if temp != 1.0: p_no **= 1 / temp; p_yes **= 1 / temp
            yes = rng.random() < p_yes / (p_yes + p_no)
            b[i - 1] = yes
            if yes: n[w1] += 1; n[w2] += 1; N += 2
            else: n[w] += 1; N += 1
    return [{i for i, x in enumerate(b, 1) if x} for b in bnd]

def prf(placed, texts):
    tp = fp = fn = 0
    for b, (_, gold) in zip(placed, texts):
        tp += len(b & gold); fp += len(b - gold); fn += len(gold - b)
    p = tp / (tp + fp) if tp + fp else 0; r = tp / (tp + fn) if tp + fn else 0
    return p, r, (2 * p * r / (p + r) if p + r else 0)

def main():
    global LOG
    LOG = (P / 'run53b.log').open('w', encoding='utf-8'); t0 = time.time()
    indus = [(list(t), set()) for t in FC.TRAIN]; N = sum(len(s) for s, _ in indus)
    corpora = {c: R53.load(c) for c in MULTI + SINGLE + OTHER}
    res = {}; ctrl = {}
    for ci, c in enumerate(corpora):
        Ss = []; Ms = []; S5 = []; Fs = []; Rs = []; Ps = []; Rc = []
        for b in range(B):
            rng = random.Random(SEED + ci * 1000 + b)
            texts = R53.sample(corpora[c], N, rng)
            pl = dp_segment(texts, rng)
            cnt = collections.Counter(x for s, _ in texts for x in s)
            S, M, _ = R53.stats(pl, texts); s5, _, _ = R53.stats(pl, texts, None, 5, cnt)
            Ss.append(S); Ms.append(M); S5.append(s5)
            if c in MULTI:
                p_, r_, f_ = prf(pl, texts); Ps.append(p_); Rc.append(r_); Fs.append(f_); Rs.append(R53.random_f1(pl, texts, rng, 20))
            if b % 10 == 9: log(c, 'sample', b + 1, 'S so far', round(sum(Ss) / len(Ss), 3), round(time.time() - t0), 's')
        mean = lambda v: sum(v) / len(v); sd = lambda v: math.sqrt(sum((x - mean(v)) ** 2 for x in v) / (len(v) - 1))
        res[c] = dict(S=mean(Ss), S_sd=sd(Ss), M=mean(Ms), M_sd=sd(Ms), S_min5=mean(S5))
        if c in MULTI:
            ctrl[c] = dict(precision=mean(Ps), recall=mean(Rc), f1=mean(Fs), random_f1=mean(Rs), margin=mean(Fs) - mean(Rs))
            log('control', c, 'P', round(mean(Ps), 3), 'R', round(mean(Rc), 3), 'F1', round(mean(Fs), 3), 'random', round(mean(Rs), 3), 'margin', round(mean(Fs) - mean(Rs), 3))
        log(c, 'S', round(res[c]['S'], 3), '±', round(res[c]['S_sd'], 3), 'M', round(res[c]['M'], 3), '±', round(res[c]['M_sd'], 3), 'S(min count 5)', round(res[c]['S_min5'], 3))
    passed = [c for c in MULTI if ctrl[c]['margin'] >= 0.15]
    control = 'PASS' if len(passed) >= 3 else 'METHOD-FAIL'
    log('positive control', control, 'passed', passed)
    # Indus
    rng = random.Random(SEED + 999); pl = dp_segment(indus, rng)
    cnt = collections.Counter(x for s, _ in indus for x in s)
    S_i, M_i, _ = R53.stats(pl, indus); S5_i, _, n5 = R53.stats(pl, indus, None, 5, cnt)
    lex = collections.Counter(); seg_hist = collections.Counter()
    for b, (s, _) in zip(pl, indus):
        prev = 0
        for c_ in sorted(b) + [len(s)]:
            seg = tuple(s[prev:c_]); seg_hist[len(seg)] += 1
            if len(seg) >= 2: lex[seg] += 1
            prev = c_
    multi_tokens = sum(len(w) * c for w, c in lex.items())
    log('Indus S', round(S_i, 3), 'M', round(M_i, 3), 'S(min count 5)', round(S5_i, 3), 'segments', dict(sorted(seg_hist.items())), 'multi-sign token share', round(multi_tokens / N, 3))
    log('Indus induced lexicon (top 20 multi-sign):', [('-'.join(w), c) for w, c in lex.most_common(20)])
    def near(x, c, key): return abs(x - res[c][key]) <= 2 * res[c][key + '_sd']
    def verdict_on(x, key):
        if control != 'PASS': return 'METHOD-FAIL'
        s_multi = min(res[c][key] for c in passed); s_single = res['CHN'][key]
        above_single = x > s_single + 2 * res['CHN'][key + '_sd']; below_multi = x < s_multi - 2 * max(res[c][key + '_sd'] for c in passed)
        if (any(near(x, c, key) for c in passed) or x >= s_multi) and above_single: return 'MULTI-SIGN-WORDS'
        if (near(x, 'CHN', key) or x <= s_single) and below_multi: return 'SINGLE-SIGN-WORDS'
        return 'BETWEEN'
    vS = verdict_on(S_i, 'S'); vM = verdict_on(M_i, 'M')
    verdict = vS if vS == vM else ('METHOD-FAIL' if control != 'PASS' else 'BETWEEN')
    log('verdict on S', vS, 'on M', vM, 'VERDICT', verdict)
    r = random.Random(SEED + 9); sh = []
    for s, _ in indus: s2 = s[:]; r.shuffle(s2); sh.append((s2, set()))
    S_sh, M_sh, _ = R53.stats(dp_segment(sh, r), sh)
    log('Indus shuffled within texts: S', round(S_sh, 3), 'M', round(M_sh, 3))
    json.dump(dict(seed=SEED, B=B, alpha=ALPHA, pstop=PSTOP, sweeps=SWEEPS, N=N, control=control, passed=passed, controls=ctrl, corpora=res,
                   indus=dict(S=S_i, M=M_i, S_min5=S5_i, seg_hist=dict(seg_hist), multi_token_share=multi_tokens / N,
                              lexicon=[(list(w), c) for w, c in lex.most_common(50)]),
                   shuffled=dict(S=S_sh, M=M_sh), verdict=verdict, verdict_S=vS, verdict_M=vM),
              (P / 'results.json').open('w'), indent=1)
    log('done', round(time.time() - t0, 1), 's')

if __name__ == '__main__': main()
