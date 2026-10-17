"""Round 42 runner. Usage: python3 run42.py <indus|lb> <perm_start> <perm_end> <jambu> <drdb> <ids> <kuiper> <linb_cog>
Reuses round 41 model code unchanged; only anchors / permutation counts differ."""
import sys, json, re, collections
from pathlib import Path
P = Path(__file__).resolve().parent
mode, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rest = sys.argv[4:]
sys.argv = [sys.argv[0], 'x', '60000', '0'] + rest
sys.path.insert(0, str(P.parent / 'round41'))
import anchored as A
F = A.F


def indus_setup():
    sys.path.insert(0, str(P.parent / 'round30'))
    import foreign_context as FC
    pdr = {'fish': 'miin', 'man': 'aal', 'arrow': 'ampu', 'jar': 'agal', 'leaf': 'elay', 'bird': 'pitt',
           'one': 'okk', 'two': 'iir', 'three': 'muuntu', 'four': 'naal', 'five': 'caymtu', 'six': 'caatu', 'seven': 'eezh', 'eight': 'enttu'}
    sc = {'220': 'fish', '090': 'man', '520': 'arrow', '740': 'jar', '803': 'leaf', '806': 'leaf', '269': 'bird',
          '001': 'one', '031': 'one', '002': 'two', '032': 'two', '003': 'three', '013': 'three', '033': 'three',
          '004': 'four', '014': 'four', '034': 'four', '005': 'five', '015': 'five', '035': 'five', '016': 'six', '036': 'six',
          '017': 'seven', '018': 'eight'}
    anchors = {s: F.norm(pdr[c]) for s, c in sc.items()}
    pics = ['220', '090', '520', '740', '803', '806', '269']; nums = [s for s in sc if s not in pics]
    lexw = [w for w in (F.norm(re.split(r'\s*[~,/;]\s*', f)[0]) for f in F.lex_pdr()) if w]
    lm = A.LM(lexw); sy = collections.Counter(x for w in lexw for x in A.syllables(w))
    inv = [s for s, _ in sy.most_common(150)]
    return [tuple(t) for t in FC.TRAIN], anchors, [nums, pics], inv, lm


def lb_setup():
    sys.path.insert(0, str(P.parent / 'round32'))
    sys.argv = [sys.argv[0], rest[-1]]
    import benchmark as B
    words = [tuple(w) for w in B.words]
    freq = collections.Counter(s for w in words for s in w); top = [s for s, _ in freq.most_common(24)]
    lex = [''.join(x.lower() for x in w) for w in B.lex_cognate(range(len(B.words)))]
    return sorted(set(words)), {s: s.lower() for s in top}, [top], sorted({v.lower() for v in B.VALUES}), A.LM(lex)


texts, anchors, groups, inv, lm = indus_setup() if mode == 'indus' else lb_setup()
tr, te = A.split(texts, 41001)
seed0 = 42100 if mode == 'indus' else 42300
out = {'mode': mode, 'train': len(tr), 'test': len(te), 'anchors': len(anchors)}
if a == 0: out['real'] = A.heldout(te, A.fit(tr, anchors, inv, lm, 41050), lm); print('real', out['real'], flush=True)
out['null'] = {}
for k in range(a, b):
    v = A.heldout(te, A.fit(tr, A.permute(anchors, groups, seed0 + k), inv, lm, 41050), lm)
    out['null'][k] = v; print('perm', k, round(v, 3), flush=True)
(P / f'part_{mode}_{a}_{b}.json').write_text(json.dumps(out, indent=1))
