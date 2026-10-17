"""Round 45 runner. Usage: python3 run45.py <FIN|EUS> <split_ids> <nperm> <kuiper> <jambu> <drdb> <ids> <linb_cog>
Model = round 41 anchored.py unchanged; anchors/LM/inventory from the control language's IDS list."""
import sys, json, re, collections
from pathlib import Path
P = Path(__file__).resolve().parent
lang, splits, nperm = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], int(sys.argv[3])
rest = sys.argv[4:]
sys.argv = [sys.argv[0], 'x', '60000', '0'] + rest
sys.path.insert(0, str(P.parent / 'round41')); sys.path.insert(0, str(P.parent / 'round30'))
import anchored as A
import foreign_context as FC
F = A.F

WORDS = {'FIN': {'fish': 'kala', 'man': 'mies', 'arrow': 'nuoli', 'jar': 'pata', 'leaf': 'lehti', 'bird': 'lintu',
                 'one': 'üksi', 'two': 'kaksi', 'three': 'kolme', 'four': 'nelyæ', 'five': 'wiisi', 'six': 'kuusi',
                 'seven': 'seitsemæn', 'eight': 'kahdeksan'},
         'EUS': {'fish': "a'raɲ", 'man': "'gison", 'arrow': "'fleša", 'jar': "tʰi'piɲa", 'leaf': "'oṣto", 'bird': "'čori",
                 'one': 'bat', 'two': "'biga", 'three': "'hiru", 'four': 'lau', 'five': 'boṣt', 'six': 'ṣei',
                 'seven': "'saspi", 'eight': "'sorc̷i"}}
SC = {'220': 'fish', '090': 'man', '520': 'arrow', '740': 'jar', '803': 'leaf', '806': 'leaf', '269': 'bird',
      '001': 'one', '031': 'one', '002': 'two', '032': 'two', '003': 'three', '013': 'three', '033': 'three',
      '004': 'four', '014': 'four', '034': 'four', '005': 'five', '015': 'five', '035': 'five', '016': 'six', '036': 'six',
      '017': 'seven', '018': 'eight'}
anchors = {s: F.norm(WORDS[lang][c]) for s, c in SC.items()}
pics = ['220', '090', '520', '740', '803', '806', '269']; nums = [s for s in SC if s not in pics]
lexw = [w for w in (F.norm(f) for f in F.ids_lang({'Finnish' if lang == 'FIN' else 'Basque'})) if w]
lm = A.LM(lexw); sy = collections.Counter(x for w in lexw for x in A.syllables(w))
inv = [s for s, _ in sy.most_common(150)]
texts = [tuple(t) for t in FC.TRAIN]
if splits == [-1]:
    print(lang, 'anchors', anchors, 'lexicon', len(lexw), 'inv', len(inv), inv[:20]); sys.exit()
for i in splits:
    out_f = P / f'split_{lang}_{i}.json'
    if out_f.exists(): continue
    tr, te = A.split(texts, 43001 + i)
    def fit(a):
        lm.cache.clear(); return A.fit(tr, a, inv, lm, 41050)
    out = {'lang': lang, 'split': i, 'test': len(te), 'real': A.heldout(te, fit(anchors), lm)}
    out['null'] = [A.heldout(te, fit(A.permute(anchors, [nums, pics], 43100 + k)), lm) for k in range(nperm)]
    out_f.write_text(json.dumps(out, indent=1))
    print(lang, i, round(out['real'], 3), 'beats', sum(v < out['real'] for v in out['null']), '/', nperm, flush=True)
