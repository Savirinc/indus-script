"""Round 41: do Dravidian rebus anchors predict unseen Indus texts better than permuted anchors? See PROTOCOL.md.
Usage: python3 anchored.py <mode: lb|indus> <steps> <nperm> <jambu> <drdb> <ids> <kuiper> <linb_cog>"""
import sys, re, csv, json, math, random, collections, unicodedata
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parent
MODE, STEPS, NPERM = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.argv = [sys.argv[0]] + sys.argv[4:8] + sys.argv[8:]
sys.path.insert(0, str(P.parent / 'round37'))
import fingerprint as F


class LM:
    def __init__(self, words, k=0.1):
        self.k = k; self.c3 = collections.Counter(); self.c2 = collections.Counter(); al = set('$')
        for w in words:
            s = '^^' + w + '$'; al |= set(w)
            for i in range(2, len(s)): self.c3[s[i - 2:i + 1]] += 1; self.c2[s[i - 2:i]] += 1
        self.V = len(al); self.cache = {}
    def lp(self, w):
        if w in self.cache: return self.cache[w]
        s = '^^' + w + '$'; t = 0.0
        for i in range(2, len(s)):
            t += math.log((self.c3[s[i - 2:i + 1]] + self.k) / (self.c2[s[i - 2:i]] + self.k * self.V))
        self.cache[w] = t; return t


def syllables(w):
    return re.findall(r'[^aeiou]*[aeiou]+(?:[^aeiou](?![aeiou]))?', w)


def fit(train, anchors, inv, lm, seed):
    """train: list of tuples of sign ids. anchors: sign->string. inv: list of strings. returns key dict."""
    rng = random.Random(seed)
    signs = sorted({s for t in train for s in t}); free = [s for s in signs if s not in anchors]
    key = dict(anchors);
    for s in free: key[s] = rng.randrange(len(inv))
    val = lambda s: anchors[s] if s in anchors else inv[key[s]]
    by = collections.defaultdict(list)
    for i, t in enumerate(train):
        for s in set(t): by[s].append(i)
    freq = collections.Counter(s for t in train for s in t)
    cur = [lm.lp(''.join(val(s) for s in t)) for t in train]
    F_ = collections.Counter();
    for s in free: F_[key[s]] += freq[s]
    xlx = lambda x: x * math.log(x) if x > 0 else 0.0
    for step in range(STEPS):
        T = 3.0 + (0.05 - 3.0) * step / STEPS
        s = rng.choice(free); old = key[s]; new = rng.randrange(len(inv))
        if new == old: continue
        key[s] = new
        rows = by[s]; nv = [lm.lp(''.join(val(x) for x in train[i])) for i in rows]
        d = sum(nv) - sum(cur[i] for i in rows)
        fo, fn = F_[old], F_[new]
        d += -(xlx(fo - freq[s]) + xlx(fn + freq[s]) - xlx(fo) - xlx(fn))
        if d >= 0 or rng.random() < math.exp(d / T):
            for i, v in zip(rows, nv): cur[i] = v
            F_[old] -= freq[s]; F_[new] += freq[s]
        else:
            key[s] = old
    return {s: val(s) for s in signs}


def heldout(test, key, lm):
    return float(np.mean([lm.lp(''.join(key.get(s, '') for s in t)) for t in test]))


def near(a, b):
    if a == b: return True
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) == 1
    if abs(len(a) - len(b)) == 1:
        s, l = (a, b) if len(a) < len(b) else (b, a)
        return any(l[:i] + l[i + 1:] == s for i in range(len(l)))
    return False


def split(texts, seed):
    rng = random.Random(seed); t = list(texts); rng.shuffle(t); n = int(0.8 * len(t))
    tr, te = t[:n], t[n:]
    trs = set(tr); te = [x for x in te if not any(near(x, y) for y in tr if abs(len(x) - len(y)) <= 1)]
    return tr, te


def permute(anchors, groups, seed):
    rng = random.Random(seed); out = dict(anchors)
    for g in groups:
        vals = [anchors[s] for s in g]; rng.shuffle(vals); out.update(zip(g, vals))
    return out


def run(texts, anchors, groups, inv, lm, label):
    tr, te = split(texts, 41001)
    print(f'== {label}: train {len(tr)} test {len(te)} anchors {len(anchors)} inventory {len(inv)} steps {STEPS}', flush=True)
    real = heldout(te, fit(tr, anchors, inv, lm, 41050), lm)
    print(f'   real anchors held-out LL = {real:.3f}', flush=True)
    null = []
    for k in range(NPERM):
        pa = permute(anchors, groups, 41100 + k)
        null.append(heldout(te, fit(tr, pa, inv, lm, 41050), lm)); print(f'   perm {k}: {null[-1]:.3f}', flush=True)
    p = (1 + sum(v >= real for v in null)) / (1 + NPERM)
    print(f'   p = {p:.4f}', flush=True)
    return dict(label=label, train=len(tr), test=len(te), real=real, null=null, p=p)


def linb():
    sys.path.insert(0, str(P.parent / 'round32'))
    sys.argv = [sys.argv[0], sys.argv[-1]]
    import benchmark as B
    words = [tuple(w) for w in B.words]
    freq = collections.Counter(s for w in words for s in w)
    top = [s for s, _ in freq.most_common(17)]
    anchors = {s: s.lower() for s in top}
    groups = [top]
    lex = [''.join(x.lower() for x in w) for w in B.lex_cognate(range(len(B.words)))]
    lm = LM(lex); inv = sorted({v.lower() for v in B.VALUES})
    texts = sorted(set(words))
    return run(texts, anchors, groups, inv, lm, 'LINEAR B control')


def indus():
    sys.path.insert(0, str(P.parent / 'round30'))
    import foreign_context as FC
    pdr = {'fish': 'miin', 'man': 'aal', 'arrow': 'ampu', 'one': 'okk', 'two': 'iir', 'three': 'muuntu',
           'five': 'caymtu', 'six': 'caatu', 'seven': 'eezh', 'eight': 'enttu'}
    pdr = {k: F.norm(v) for k, v in pdr.items()}
    sign_concept = {'220': 'fish', '090': 'man', '520': 'arrow', '001': 'one', '031': 'one', '002': 'two', '032': 'two',
                    '003': 'three', '013': 'three', '033': 'three', '005': 'five', '015': 'five', '035': 'five',
                    '016': 'six', '036': 'six', '017': 'seven', '018': 'eight'}
    anchors = {s: pdr[c] for s, c in sign_concept.items()}
    nums = [s for s, c in sign_concept.items() if c not in ('fish', 'man', 'arrow')]; pics = ['220', '090', '520']
    lexw = [F.norm(re.split(r'\s*[~,/;]\s*', f)[0]) for f in F.lex_pdr()]; lexw = [w for w in lexw if w]
    lm = LM(lexw)
    sy = collections.Counter(x for w in lexw for x in syllables(w))
    inv = [s for s, _ in sy.most_common(150)]
    texts = [tuple(t) for t in FC.TRAIN]
    return run(texts, anchors, [nums, pics], inv, lm, 'INDUS (Dravidian anchors)')


if __name__ == '__main__':
    r = linb() if MODE == 'lb' else indus()
    (P / f'results_{MODE}_{STEPS}_{NPERM}.json').write_text(json.dumps(r, indent=1))
