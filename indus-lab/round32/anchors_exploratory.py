"""EXPLORATORY: at Indus-matched density (~239 sign IDs), how many anchored sign values make the rest recoverable?
Anchors = the k most frequent sign IDs given their true values. Accuracy reported on NON-anchored tokens."""
import sys,json,random,collections
ks=[int(x) for x in sys.argv[2:]];sys.argv=sys.argv[:2]
import benchmark as B
t=230
def build(ci,h,g,seed_key=32001):
    freq=collections.Counter(s for i in ci for s in B.words[i]);tot=sum(freq.values())
    rng=random.Random(seed_key);rngh=random.Random(32002)
    so={v:(max(1,min(11,round(t*freq[v]/tot))) if freq[v] else 1) for v in B.VALUES}
    ids=[(v,j) for v in B.VALUES for j in range(so[v])];rng.shuffle(ids);sid={x:n for n,x in enumerate(ids)}
    truth=B.np.array([B.VI[v] for v,_ in ids]);enc=[[sid[(s,rngh.randrange(so[s]))] for s in B.words[i]] for i in ci]
    return collections.Counter(tuple(e) for e in enc),truth,len(ids)
B.build=build
lex=B.lex_cognate(range(len(B.words)));out=[]
types,truth,n=build(list(range(len(B.words))),True,False)
f=collections.Counter(x for tt,c in types.items() for x in tt for _ in range(c))
for k in ks:
    anchored=[s for s,_ in f.most_common(k)];B.ANCHORS={s:int(truth[s]) for s in anchored}
    sc=B.Scorer(types,n,B.fit_lm(lex))
    ch=[B.anneal(sc,n,False,32010+j) for j in range(B.CHAINS)];best=max(ch,key=lambda x:x[0])
    tok=ok=0
    for tt,c in zip(sc.tl,sc.cnt):
        for s in tt:
            if s in B.ANCHORS: continue
            tok+=c;ok+=c*(best[1][s]==truth[s])
    share=sum(f[s] for s in anchored)/sum(f.values())
    r=dict(anchors=k,anchored_token_share=share,nonanchored_token_accuracy=ok/tok,best_obj=best[0],true_obj=B.objective(sc,truth))
    print(json.dumps(r),flush=True);out.append(r)
(B.P/f"anchors_{'_'.join(map(str,ks))}.json").write_text(json.dumps(out,indent=2))
