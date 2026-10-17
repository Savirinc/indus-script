"""Exploratory (post-decision) diagnostic: do shuffles that keep same-concept signs equal score higher?"""
import sys, json, statistics, itertools, random
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parent
SC = {'220':'fish','090':'man','520':'arrow','740':'jar','803':'leaf','806':'leaf','269':'bird','001':'one','031':'one','002':'two','032':'two','003':'three','013':'three','033':'three','004':'four','014':'four','034':'four','005':'five','015':'five','035':'five','016':'six','036':'six','017':'seven','018':'eight'}
pics=['220','090','520','740','803','806','269']; nums=[s for s in SC if s not in pics]
def permute(an, groups, seed):  # identical to round41 anchored.permute
    rng = random.Random(seed); out = dict(an)
    for g in groups:
        vals = [an[s] for s in g]; rng.shuffle(vals); out.update(zip(g, vals))
    return out
pairs=[(a,b) for a,b in itertools.combinations(SC,2) if SC[a]==SC[b]]
an={s:c for s,c in SC.items()}
kept=[]
for k in range(60):
    pa=permute(an,[nums,pics],43100+k); kept.append(sum(pa[a]==pa[b] for a,b in pairs))
print('same-concept pairs',len(pairs),'kept by shuffles: mean',np.mean(kept),'max',max(kept))
for name,files in [('PDR',[P.parent/'round43'/f'split_indus_{i}.json' for i in range(10)]),('FIN',[P/f'split_FIN_{i}.json' for i in range(10)]),('EUS',[P/f'split_EUS_{i}.json' for i in range(10)])]:
    rs=[json.loads(f.read_text()) for f in files if f.exists()]
    T=[statistics.mean(r['null'][k] for r in rs) for k in range(60)]
    print(name,len(rs),'splits; corr(kept pairs, shuffle score) =',round(np.corrcoef(kept,T)[0,1],3))
