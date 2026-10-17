from pathlib import Path
import json,hashlib,collections
P=Path(__file__).resolve().parent
src=P.parent/'round21/comparative_ledger.json'
ledger=json.loads(src.read_text())
def tokens(r):return tuple(s for s in r['Segments'].split() if s!='+')
def fold(c):return int(hashlib.sha256(c.encode()).hexdigest(),16)%5
def align(a,b):
    d=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)+1):d[i][0]=i
    for j in range(len(b)+1):d[0][j]=j
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):d[i][j]=min(d[i-1][j-1]+(a[i-1]!=b[j-1]),d[i-1][j]+1,d[i][j-1]+1)
    i,j=len(a),len(b);ops=[]
    while i or j:
        if i and j and d[i][j]==d[i-1][j-1]+(a[i-1]!=b[j-1]):ops.append((i-1,b[j-1]));i-=1;j-=1
        elif i and d[i][j]==d[i-1][j]+1:ops.append((i-1,None));i-=1
        else:ops.append((None,b[j-1]));j-=1
    return d[-1][-1],list(reversed(ops))
def emissions(a,b):
    _,ops=align(a,b);out=[[] for _ in a];last=0
    for i,y in ops:
        if i is not None:last=i
        if y is not None:out[last].append(y)
    return [tuple(x) for x in out]
def context(a,i):return (a[i-1] if i else '^',a[i],a[i+1] if i+1<len(a) else '$')
def choice(counter,copy):
    best=max(counter.values());ties=sorted(x for x,n in counter.items() if n==best)
    return copy if copy in ties else ties[0]
def train(rows):
    plain=collections.defaultdict(collections.Counter);ctx=collections.defaultdict(collections.Counter)
    for r in rows:
        a,b=r['source'],r['target']
        for i,y in enumerate(emissions(a,b)):
            plain[a[i]][y]+=1;ctx[context(a,i)][y]+=1
    return plain,ctx
def predict(a,model,contextual):
    plain,ctx=model;out=[]
    for i,x in enumerate(a):
        c=ctx.get(context(a,i),{}) if contextual else {}
        if sum(c.values())<3:
            c=plain.get(x,{})
            if sum(c.values())<2:c={}
        out.extend(choice(c,(x,)) if c else (x,))
    return tuple(out)
data=[]
for g in ledger:
    by=collections.defaultdict(set)
    for r in g['forms']:by[r['Language_ID']].add(tokens(r))
    if 'Tamil' not in by:continue
    for lang in sorted(set(by)-{'Tamil'}):
        data.append(dict(concept=g['concept'],cognacy=g['cognacy_label'],language=lang,source=sorted(by['Tamil'])[0],target=sorted(by[lang])[0],source_alternatives=sorted(by['Tamil']),target_alternatives=sorted(by[lang])))
preds=[];summaries=[]
for lang in sorted({r['language'] for r in data}):
    rows=[r for r in data if r['language']==lang]
    scores={m:dict(exact=0,edits=0) for m in ['copy','segment','context']}
    for f in range(5):
        tr=[r for r in rows if fold(r['concept'])!=f];te=[r for r in rows if fold(r['concept'])==f]
        assert not ({r['concept'] for r in tr}&{r['concept'] for r in te})
        model=train(tr)
        for r in te:
            a,b=r['source'],r['target'];ps={'copy':a,'segment':predict(a,model,False),'context':predict(a,model,True)}
            rec=dict(r,fold=f,predictions=ps)
            for m,p in ps.items():scores[m]['exact']+=p==b;scores[m]['edits']+=align(p,b)[0]
            preds.append(rec)
    summaries.append(dict(language=lang,records=len(rows),target_segments=sum(len(r['target']) for r in rows),scores=scores))
pooled=dict(records=len(preds),concepts=len({r['concept'] for r in preds}),target_segments=sum(r['target_segments'] for r in summaries),scores={m:{k:sum(r['scores'][m][k] for r in summaries) for k in ['exact','edits']} for m in ['copy','segment','context']})
out=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),pooled=pooled,languages=summaries)
(P/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(P/'predictions.json').write_text(json.dumps(preds,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
