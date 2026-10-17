"""Round 43 runner. Usage: python3 run43.py <indus|lb> <split_ids e.g. 0,1,2> <nperm> <kuiper> <jambu> <drdb> <ids> <linb_cog>
Setups copied verbatim from round 42 run42.py; model from round 41 anchored.py (unchanged)."""
import sys, json, re, collections
from pathlib import Path
P = Path(__file__).resolve().parent
mode, splits, nperm = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], int(sys.argv[3])
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
_fit = A.fit
def fit_clear(*a):  # deviation: clear the LM memo cache per fit (memory only; results unchanged)
    lm.cache.clear(); return _fit(*a)
A.fit = fit_clear
pseed = 43100 if mode == 'indus' else 43300
for i in splits:
    out_f = P / f'split_{mode}_{i}.json'
    if out_f.exists(): continue
    sd = 41001 if i < 0 else 43001 + i  # i = -1: reproduction check of round 42's split
    tr, te = A.split(texts, sd)
    out = {'mode': mode, 'split': i, 'seed': sd, 'train': len(tr), 'test': len(te)}
    out['real'] = A.heldout(te, fit_clear(tr, anchors, inv, lm, 41050), lm)
    out['null'] = [A.heldout(te, fit_clear(tr, A.permute(anchors, groups, pseed + k), inv, lm, 41050), lm) for k in range(nperm)]
    out_f.write_text(json.dumps(out, indent=1))
    print(mode, i, round(out['real'], 3), 'beats', sum(v < out['real'] for v in out['null']), '/', nperm, flush=True)
