"""Round 29 EXPLORATORY follow-up (post hoc, designed after seeing primary results).
Coarse position model POS3: slot class in {initial, medial, final}; length-independent. Same k=5 interpolation."""
import sys,json,math,random,collections,statistics
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'round27'));sys.path.insert(0,str(P))
from cross_city import collect,fit
import conditional_order as C
def cls(L,i):return 'I' if i==0 else 'F' if i==L-1 else 'M'
def fit_pos3(train,u):
    c=collections.defaultdict(collections.Counter)
    for s in train:
        for i,x in enumerate(s):c[cls(len(s),i)][x]+=1
    tot={k:sum(v.values()) for k,v in c.items()}
    return lambda x,L,i:math.log2((c[cls(L,i)][x]+5*u[x])/(tot[cls(L,i)]+5))
out=[]
for spec in C.splits:
    tr=sorted(collect(spec['source'],spec['subset']));m=fit(tr);v=set(m[0]);pos3=fit_pos3(tr,m[0]);big=C.make_big(m)
    T=[tuple(x if x in v else 'UNK' for x in s['text']) for s in spec['predictions']]
    T=[t for t in T if len(t)<=C.MAXLEN and len(set(t))>1]
    rows=[]
    for t in T:
        r={'U':math.log2(C.n_perms(t))}
        for name,up,ub in [('POS3',1,0),('BIG',0,1),('POS3BIG',1,1)]:
            Z,sc,_=C.make_dp(t,pos3,big,up,ub);r[name]=Z-sc(t)
        rows.append(r)
    tag=f"{spec['subset']}:{spec['source']}"
    def cmp(a,b):
        d=[r[a]-r[b] for r in rows];lo,hi=C.boot_ci(d,'r29x:'+tag+a+b);return round(statistics.fmean(d),3),[round(lo,3),round(hi,3)]
    res=dict(cond=tag,n=len(rows),mean={k:round(statistics.fmean(r[k] for r in rows),3) for k in rows[0]},
             U_minus_BIG=cmp('U','BIG'),U_minus_POS3=cmp('U','POS3'),POS3_minus_POS3BIG=cmp('POS3','POS3BIG'),
             frac_true_order_top=None)
    out.append(res);print(json.dumps(res))
(P/'exploratory_results.json').write_text(json.dumps(out,indent=2))
