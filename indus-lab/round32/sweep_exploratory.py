"""EXPLORATORY (post hoc): where does recovery collapse as the sign inventory grows? Cognate lexicon, word boundaries."""
import sys,json,random,collections
from pathlib import Path
sys.argv=[sys.argv[0],sys.argv[1]]+sys.argv[2:]
import benchmark as B
targets=[int(x) for x in sys.argv[2:]]
out=[]
for t in targets:
    orig=B.build
    def build(ci,h,g,seed_key=32001,t=t):
        freq=collections.Counter(s for i in ci for s in B.words[i]);tot=sum(freq.values())
        rng=random.Random(seed_key);rngh=random.Random(32002)
        so={v:(max(1,min(11,round(t*freq[v]/tot))) if (freq[v] and t>70) else 1) for v in B.VALUES}
        ids=[(v,j) for v in B.VALUES for j in range(so[v])];rng.shuffle(ids);sid={x:n for n,x in enumerate(ids)}
        truth=B.np.array([B.VI[v] for v,_ in ids])
        enc=[[sid[(s,rngh.randrange(so[s]))] for s in B.words[i]] for i in ci]
        return collections.Counter(tuple(e) for e in enc),truth,len(ids)
    B.build=build
    r=B.run(f'sweep_{t}_many2one',B.lex_cognate(range(len(B.words))),list(range(len(B.words))),True,False,False)
    B.build=orig;out.append(r)
Path(B.P/f"sweep_{'_'.join(map(str,targets))}.json").write_text(json.dumps(out,indent=2))
