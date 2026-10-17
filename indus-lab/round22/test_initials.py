"""Five-fold, concept-held-out initial prediction. Standard library only."""
from pathlib import Path
import json, hashlib, collections, random, statistics
P=Path(__file__).resolve().parent
src=P.parent/'round21/comparative_ledger.json'
ledger=json.loads(src.read_text())
langs=sorted({r['Language_ID'] for g in ledger for r in g['forms']} - {'Tamil'})
def initial(r):
    return next(s for s in r['Segments'].split() if s!='+')
def fold(c):return int(hashlib.sha256(c.encode()).hexdigest(),16)%5
def mode(xs,prefer=None):
    ct=collections.Counter(xs);best=max(ct.values());ties=sorted(x for x,n in ct.items() if n==best)
    return prefer if prefer in ties else ties[0]
def fitpredict(train,test):
    table=collections.defaultdict(list)
    for c,x,y in train:table[x].append(y)
    return [mode(table[x],x) if x in table else x for c,x,y in test]
results=[];predictions=[];pooled_shuffle=[0]*100
for lang in langs:
    raw=collections.defaultdict(lambda:[set(),set()])
    for g in ledger:
        a=[r for r in g['forms'] if r['Language_ID']=='Tamil']
        b=[r for r in g['forms'] if r['Language_ID']==lang]
        if a and b:
            raw[g['concept']][0].update(map(initial,a));raw[g['concept']][1].update(map(initial,b))
    data=[(c,next(iter(a)),next(iter(b))) for c,(a,b) in sorted(raw.items()) if len(a)==len(b)==1]
    hits=copy=major=unseen=0;sh=[0]*100
    for f in range(5):
        train=[r for r in data if fold(r[0])!=f];test=[r for r in data if fold(r[0])==f]
        if not test:continue
        assert train and not ({r[0] for r in train}&{r[0] for r in test})
        pred=fitpredict(train,test);base=mode([y for c,x,y in train])
        known={x for c,x,y in train}
        for (c,x,y),p in zip(test,pred):
            hits+=p==y;copy+=x==y;major+=base==y;unseen+=x not in known
            predictions.append(dict(target_language=lang,concept=c,fold=f,source=x,actual=y,predicted=p,copy=x,majority=base,unseen_source=x not in known))
        for s in range(100):
            ys=[y for c,x,y in train];random.Random(f'{lang}:{f}:{s}:round22').shuffle(ys)
            shuffled=[(c,x,y) for (c,x,_),y in zip(train,ys)]
            sh[s]+=sum(p==r[2] for p,r in zip(fitpredict(shuffled,test),test))
    for s in range(100):pooled_shuffle[s]+=sh[s]
    n=len(data)
    results.append(dict(language=lang,n=n,ambiguous_excluded=len(raw)-n,correct=hits,copy_correct=copy,majority_correct=major,unseen_source=unseen,accuracy=hits/n,copy_accuracy=copy/n,shuffle_correct_mean=statistics.mean(sh),shuffle_correct_range=[min(sh),max(sh)]))
n=sum(r['n'] for r in results)
out=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),folds=5,shuffle_replicates=100,records=n,languages=results,pooled={k:sum(r[k] for r in results) for k in ['correct','copy_correct','majority_correct','unseen_source']},shuffle_correct_mean=statistics.mean(pooled_shuffle),shuffle_correct_range=[min(pooled_shuffle),max(pooled_shuffle)])
(P/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(P/'predictions.json').write_text(json.dumps(predictions,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
