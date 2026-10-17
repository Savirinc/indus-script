"""Round 32: Linear B decipherability ladder under Indus-like degradation. See PROTOCOL.md.
Input: NeuroDecipher data/linear_b-greek.cog (path as argv[1]). Requires numpy."""
import sys, json, math, random, unicodedata, collections, hashlib
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parent
SRC = Path(sys.argv[1])
STEPS, CHAINS, T0, T1, K_SMOOTH = 150_000, 4, 3.0, 0.05, 0.1

rows = [l.rstrip('\n').split('\t') for l in SRC.open(encoding='utf-8')][1:]
words = [[unicodedata.name(c).split()[-1] for c in lb] for lb, _ in rows]
greek = [g.split('|') if g != '_' else [] for _, g in rows]
VALUES = sorted({s for w in words for s in w}); VI = {v: i for i, v in enumerate(VALUES)}
NV = len(VALUES); BOS, EOS, OOV = NV, NV + 1, NV + 2

# ---------- Greek -> Linear B-style spelling (fixed rules) ----------
G = {'α': 'a', 'ε': 'e', 'η': 'e', 'ι': 'i', 'ο': 'o', 'ω': 'o', 'υ': 'u', 'β': 'p', 'γ': 'k', 'δ': 'd', 'ζ': 'z', 'θ': 't',
     'κ': 'k', 'λ': 'r', 'μ': 'm', 'ν': 'n', 'ξ': 'ks', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'φ': 'p', 'χ': 'k',
     'ψ': 'ps', 'f': 'w', 'j': 'j'}
VOW = set('aeiou')
def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c))
def to_lb(gr):
    ph = ''.join(G.get(c, '') for c in strip_acc(gr))
    out = []; i = 0; n = len(ph)
    while i < n:
        c = ph[i]
        if c in VOW: out.append(c.upper()); i += 1; continue
        j = i
        while j < n and ph[j] not in VOW: j += 1
        if j == n: break                                   # word-final consonants dropped
        cl = ph[i:j]; v = ph[j]
        if len(cl) > 1 and cl[0] in 'snrm' and i > 0: cl = cl[1:]   # syllable-final s/n/r/m dropped
        for k, cc in enumerate(cl):
            out.append((cc + v).upper())
        out[-1] = (cl[-1] + v).upper(); i = j + 1
    return out
def lex_cognate(idx):
    L = []
    for i in idx:
        for g in greek[i]:
            s = to_lb(g)
            if s: L.append(s)
    return L

# ---------- LM ----------
def fit_lm(lex):
    c = np.full((NV + 3, NV + 3), K_SMOOTH)
    for w in lex:
        seq = [BOS] + [VI.get(s, OOV) for s in w] + [EOS]
        for a, b in zip(seq, seq[1:]): c[a, b] += 1
    c[:, BOS] = 0; c[:, OOV] = 0          # never predict BOS/OOV from decoded text
    c[OOV, :] = K_SMOOTH
    return np.log(c / c.sum(1, keepdims=True) + 1e-300)

# ---------- cipher construction ----------
def build(cipher_idx, homophones, group, seed_key=32001):
    rng = random.Random(seed_key); rngh = random.Random(32002); rngg = random.Random(32003)
    freq = collections.Counter(s for i in cipher_idx for s in words[i])
    signs_of = {}
    if homophones:                                         # ~400 sign IDs, allographs proportional to frequency
        tot = sum(freq.values()); target = 400
        for v in VALUES:
            k = max(1, min(11, round(target * freq[v] / tot))) if freq[v] else 1
            signs_of[v] = k
    else:
        signs_of = {v: 1 for v in VALUES}
    ids = [(v, j) for v in VALUES for j in range(signs_of[v])]; rng.shuffle(ids)
    sid = {x: n for n, x in enumerate(ids)}; truth = np.array([VI[v] for v, _ in ids])
    texts = []; idx = list(cipher_idx); rngg.shuffle(idx)
    if group:
        while idx:
            k = rngg.choice([1, 2, 3]); texts.append([s for i in idx[:k] for s in words[i]]); idx = idx[k:]
    else:
        texts = [words[i] for i in idx]
    enc = [[sid[(s, rngh.randrange(signs_of[s]))] for s in t] for t in texts]
    types = collections.Counter(tuple(t) for t in enc)
    return types, truth, len(ids)

class Scorer:
    def __init__(self, types, nsign, lm):
        self.lm = lm; tl = list(types); self.cnt = np.array([types[t] for t in tl], float)
        L = max(map(len, tl)) + 2; self.M = np.full((len(tl), L), -1, int); self.len = np.array([len(t) for t in tl])
        for r, t in enumerate(tl): self.M[r, 1:len(t) + 1] = t
        self.by = [np.array(sorted({r for r, t in enumerate(tl) if s in t}), int) for s in range(nsign)]
        self.tokens = sum(len(t) * types[t] for t in tl); self.tl = tl
    def score_rows(self, mp, rows):
        M = self.M[rows]; V = np.where(M >= 0, mp[np.maximum(M, 0)], -1)
        V[:, 0] = BOS; ln = self.len[rows]; V[np.arange(len(rows)), ln + 1] = EOS
        a, b = V[:, :-1], V[:, 1:]; ok = (a >= 0) & (b >= 0)
        lp = np.where(ok, self.lm[np.maximum(a, 0), np.maximum(b, 0)], 0.0).sum(1)
        return lp
    def total(self, mp):
        return self.score_rows(mp, np.arange(len(self.tl)))

def anneal(sc, nsign, bijective, seed):
    rng = np.random.default_rng(seed)
    mp = rng.permutation(NV)[:nsign] if (bijective and nsign == NV) else rng.integers(0, NV, nsign)
    rs = sc.total(mp); cur = float((rs * sc.cnt).sum()); best = (cur, mp.copy())
    for step in range(STEPS):
        T = T0 + (T1 - T0) * step / STEPS
        if bijective or rng.random() < 0.2:
            i, j = rng.choice(nsign, 2, replace=False); new = mp.copy(); new[i], new[j] = mp[j], mp[i]
            rows = np.union1d(sc.by[i], sc.by[j])
        else:
            i = int(rng.integers(nsign)); new = mp.copy(); new[i] = rng.integers(NV); rows = sc.by[i]
        if len(rows) == 0: mp = new; continue
        nr = sc.score_rows(new, rows); d = float(((nr - rs[rows]) * sc.cnt[rows]).sum())
        if d >= 0 or rng.random() < math.exp(d / (T * 10)):
            mp = new; rs[rows] = nr; cur += d
            if cur > best[0]: best = (cur, mp.copy())
    return best

def accuracy(sc, mp, truth):
    tok = ok = 0; per = collections.Counter(); perok = collections.Counter()
    for t, c in zip(sc.tl, sc.cnt):
        for s in t:
            tok += c; per[s] += c
            if mp[s] == truth[s]: ok += c; perok[s] += c
    types = [s for s in per if per[s] >= 5]
    return ok / tok, sum(perok[s] == per[s] for s in types) / max(1, len(types))

def freq_baseline(sc, truth, lex):
    sf = collections.Counter();
    for t, c in zip(sc.tl, sc.cnt):
        for s in t: sf[s] += c
    lf = collections.Counter(VI[s] for w in lex for s in w if s in VI)
    order = [v for v, _ in lf.most_common()] + [v for v in range(NV) if v not in lf]
    mp = np.zeros(len(truth), int)
    ranked = [s for s, _ in sf.most_common()]
    for k, s in enumerate(ranked): mp[s] = order[min(k, len(order) - 1)]
    return accuracy(sc, mp, truth)[0]

def run(name, lex, cipher_idx, homophones, group, bijective):
    types, truth, nsign = build(cipher_idx, homophones, group)
    sc = Scorer(types, nsign, fit_lm(lex))
    chains = [anneal(sc, nsign, bijective, 32010 + k) for k in range(CHAINS)]
    best = max(chains, key=lambda x: x[0])
    acc, tacc = accuracy(sc, best[1], truth)
    true_obj = float((sc.total(truth) * sc.cnt).sum())
    res = dict(condition=name, sign_ids=nsign, text_types=len(types), tokens=int(sc.tokens), lexicon_forms=len(lex),
               token_accuracy=acc, type_accuracy=tacc, freq_baseline=freq_baseline(sc, truth, lex),
               best_objective=best[0], true_key_objective=true_obj, chain_objectives=[c[0] for c in chains],
               chain_accuracies=[accuracy(sc, c[1], truth)[0] for c in chains])
    print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()}), flush=True)
    return res

def main():
    allidx = list(range(len(words))); half = allidx[:]; random.Random(32004).shuffle(half)
    h1, h2 = sorted(half[:len(half) // 2]), sorted(half[len(half) // 2:])
    orc = [words[i] for i in allidx]; cog = lex_cognate(allidx)
    rs = random.Random(32005); shuf = [rs.sample(w, len(w)) for w in cog]; held = lex_cognate(h2)
    cov = sum(1 for i in allidx if any(to_lb(g) == words[i] for g in greek[i])) / len(words)
    print('cognate lexicon forms', len(cog), '| words whose LB spelling is reproduced exactly by rules:', round(cov, 3), flush=True)
    only = sys.argv[2:] or None
    conds = [('A', orc, allidx, False, False, True), ('B', cog, allidx, False, False, True), ('B0', shuf, allidx, False, False, True),
             ('C', cog, allidx, True, False, False), ('D', cog, allidx, True, True, False),
             ('E', held, h1, False, False, True), ('F', held, h1, True, True, False)]
    out = dict(source=str(SRC), source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(), rule_exact_coverage=cov,
               settings=dict(steps=STEPS, chains=CHAINS, T0=T0, T1=T1, k=K_SMOOTH), results=[])
    for c in conds:
        if only and c[0] not in only: continue
        out['results'].append(run(*c))
    acc = {r['condition']: r['token_accuracy'] for r in out['results']}
    if 'D' in acc and 'F' in acc:
        D, F = acc['D'], acc['F']
        out['verdict'] = ('FEASIBLE-FROM-FAMILY' if F >= .7 else 'FEASIBLE-WITH-LEXICON' if D >= .7 else
                          'INFEASIBLE' if D < .4 and F < .4 else 'MARGINAL')
        print('VERDICT', out['verdict'])
    (P / ('results' + ('_' + ''.join(only) if only else '') + '.json')).write_text(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
