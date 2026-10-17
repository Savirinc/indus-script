"""Round 29: exact conditional-order test. See PROTOCOL.md (written before execution).
Standard library only. Run from the folder containing indus-lab."""
from pathlib import Path
import sys, json, math, random, collections, statistics, hashlib
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round27'))
from cross_city import collect, fit, src

MAXLEN, K, BOOT = 9, 5.0, 2000
splits = json.loads((P.parent / 'round27/robustness.json').read_text())


def fit_pos(train, u):
    c = collections.defaultdict(collections.Counter)
    for s in train:
        for i, x in enumerate(s):
            c[len(s), i][x] += 1
    tot = {k: sum(v.values()) for k, v in c.items()}
    def lp(x, L, i):
        return math.log2((c[L, i][x] + K * u[x]) / (tot.get((L, i), 0) + K)) if (L, i) in tot else math.log2(u[x])
    return lp


def make_big(model):
    u, big, tot = model
    def lp(a, b):
        return math.log2((big.get(a, {}).get(b, 0) + 5 * u[b]) / (tot.get(a, 0) + 5))
    return lp


def seq_scores(seq, pos_lp, big_lp):
    L = len(seq)
    p = sum(pos_lp(x, L, i) for i, x in enumerate(seq))
    b = sum(big_lp(a, c) for a, c in zip(('BOS',) + seq, seq + ('EOS',)))
    return p, b


def distinct_perms(seq):
    """Multiset permutations without duplicates (lexicographic)."""
    items = sorted(seq); n = len(items); out = []
    used = [False] * n; cur = []
    def rec():
        if len(cur) == n:
            out.append(tuple(cur)); return
        prev = None
        for i in range(n):
            if used[i] or items[i] == prev: continue
            prev = items[i]; used[i] = True; cur.append(items[i]); rec(); cur.pop(); used[i] = False
    rec(); return out


def logsumexp2(v):
    m = max(v); return m + math.log2(sum(2 ** (x - m) for x in v))


def cond_bits(true, perms, scorer):
    vals = [scorer(p) for p in perms]
    return -(scorer(true) - logsumexp2(vals))


def sample_from(perms, scorer, rng):
    vals = [scorer(p) for p in perms]; m = max(vals)
    w = [2 ** (v - m) for v in vals]
    return rng.choices(perms, weights=w)[0]


def boot_ci(diffs, seed):
    rng = random.Random(seed); n = len(diffs)
    means = sorted(statistics.fmean(rng.choices(diffs, k=n)) for _ in range(BOOT))
    return means[int(0.025 * BOOT)], means[int(0.975 * BOOT) - 1]


def make_dp(seq, pos_lp, big_lp, use_pos, use_big):
    """Exact log2-sum over all distinct orderings of seq's multiset, via DP over (remaining counts, previous sign)."""
    L = len(seq); signs = sorted(set(seq)); cnt0 = tuple(seq.count(x) for x in signs)
    def step(prev, x, i):
        v = 0.0
        if use_pos: v += pos_lp(x, L, i)
        if use_big: v += big_lp(prev, x)
        return v
    memo = {}
    def V(cnt, prev):  # log2 sum of scores of all completions from this state
        key = (cnt, prev)
        if key in memo: return memo[key]
        i = L - sum(cnt)
        if i == L:
            r = big_lp(prev, 'EOS') if use_big else 0.0
        else:
            terms = []
            for j, x in enumerate(signs):
                if cnt[j]:
                    c2 = cnt[:j] + (cnt[j] - 1,) + cnt[j + 1:]
                    terms.append(step(prev, x, i) + V(c2, x))
            r = logsumexp2(terms)
        memo[key] = r; return r
    def score(t):
        v = step('BOS', t[0], 0)
        for i in range(1, L): v += step(t[i - 1], t[i], i)
        return v + (big_lp(t[-1], 'EOS') if use_big else 0.0)
    def sample(rng):
        cnt = cnt0; prev = 'BOS'; out = []
        for i in range(L):
            opts = []; ws = []
            for j, x in enumerate(signs):
                if cnt[j]:
                    c2 = cnt[:j] + (cnt[j] - 1,) + cnt[j + 1:]
                    opts.append((x, c2)); ws.append(step(prev, x, i) + V(c2, x))
            m = max(ws); x, cnt = rng.choices(opts, weights=[2 ** (w - m) for w in ws])[0]
            out.append(x); prev = x
        return tuple(out)
    return V(cnt0, 'BOS'), score, sample


def n_perms(seq):
    n = math.factorial(len(seq))
    for c in collections.Counter(seq).values(): n //= math.factorial(c)
    return n


def evaluate(texts, pos_lp, big_lp, tag):
    rows = []
    for t in texts:
        r = dict(text=t, perms=n_perms(t), U=math.log2(n_perms(t)))
        for name, up, ub in [('POS', 1, 0), ('BIG', 0, 1), ('POSBIG', 1, 1)]:
            Z, score, _ = make_dp(t, pos_lp, big_lp, up, ub); r[name] = Z - score(t)
        rows.append(r)
    d = [r['POS'] - r['POSBIG'] for r in rows]
    lo, hi = boot_ci(d, f'round29boot:{tag}')
    return dict(n=len(rows), mean_bits={m: statistics.fmean(r[m] for r in rows) for m in ['U', 'POS', 'BIG', 'POSBIG']},
                pos_minus_posbig=statistics.fmean(d), ci95=[lo, hi],
                verdict='above0' if lo > 0 else 'below0' if hi < 0 else 'includes0'), rows


def main():
    out = []
    for spec in splits:
        source, subset = spec['source'], spec['subset']
        train = sorted(collect(source, subset)); model = fit(train); u = model[0]; vocab = set(u)
        pos_lp = fit_pos(train, u); big_lp = make_big(model)
        raw = [tuple(x['text']) for x in spec['predictions']]
        mapped = [tuple(x if x in vocab else 'UNK' for x in s) for s in raw]
        too_long = [s for s in mapped if len(s) > MAXLEN]
        single = [s for s in mapped if len(s) <= MAXLEN and len(set(s)) == 1]
        elig = [s for s in mapped if len(s) <= MAXLEN and len(set(s)) > 1]
        tag = f'{subset}:{source}'
        primary, rows = evaluate(elig, pos_lp, big_lp, tag)
        rng = random.Random(f'round29neg:{tag}')
        neg_txt = [make_dp(s, pos_lp, big_lp, 1, 0)[2](rng) for s in elig]
        neg, _ = evaluate(neg_txt, pos_lp, big_lp, tag + ':neg')
        rng = random.Random(f'round29pos:{tag}')
        pos_txt = [make_dp(s, pos_lp, big_lp, 0, 1)[2](rng) for s in elig]
        posc, _ = evaluate(pos_txt, pos_lp, big_lp, tag + ':pos')
        item = dict(subset=subset, source=source, target=spec['target'], test_types=len(mapped),
                    excluded_too_long=len(too_long), excluded_single_ordering=len(single),
                    primary=primary, negative_control=neg, positive_control=posc)
        out.append(item); rows_out = rows
        print(json.dumps({k: v for k, v in item.items()}, indent=1), flush=True)
        (P / f'per_text_{subset.replace(":", "")}_{source}.json').write_text(json.dumps(rows, indent=1))
    v = [c['primary']['verdict'] for c in out]
    neg_bad = any(c['negative_control']['verdict'] == 'above0' for c in out)
    pos_ok = sum(c['positive_control']['verdict'] == 'above0' for c in out)
    if neg_bad: decision = 'VOID (negative control failed)'
    elif v.count('above0') >= 3 and 'below0' not in v: decision = 'SUPPORT H_adj'
    elif v.count('above0') + 0 <= 1: decision = 'SUPPORT H_joint' + ('' if pos_ok >= 3 else ' (but positive control weak: low power)')
    else: decision = 'MIXED'
    res = dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(), decision=decision,
               positive_controls_detected=pos_ok, conditions=out)
    (P / 'results.json').write_text(json.dumps(res, indent=2))
    print('DECISION:', decision)


if __name__ == '__main__':
    main()
