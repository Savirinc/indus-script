"""Fixed stdlib phonetic baseline on annotated known-language concepts."""
import csv,json,pathlib,collections as C,random,hashlib,statistics
P=pathlib.Path(__file__).resolve().parent
source=P.parent/'dravlex/cldf/forms.csv'
rows=list(csv.DictReader(source.open()));groups=C.defaultdict(list);excluded=C.Counter()
for r in rows:
    if r['Loan'].strip().lower()!='false':excluded['not_explicit_nonloan']+=1;continue
    if not r['Segments'].strip():excluded['empty_segments']+=1;continue
    if not r['Cognacy'].strip():excluded['empty_cognacy']+=1;continue
    groups[r['Parameter_ID']].append(r)
def lev(a,b):
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]
def auc(pairs):
    # Score-grouped Mann-Whitney AUC, positive score should be larger.
    counts=C.defaultdict(lambda:[0,0])
    for score,pos in pairs:counts[score][bool(pos)]+=1
    negatives=sum(x[0] for x in counts.values());positives=sum(x[1] for x in counts.values())
    if not positives or not negatives:return None
    seen=0;wins=0.
    for score,(n,p) in sorted(counts.items()):wins+=p*(seen+n/2);seen+=n
    return wins/(positives*negatives)
assert auc([(0,False),(1,True)])==1
assert auc([(1,False),(0,True)])==0
assert auc([(1,False),(1,True)])==.5
assert lev(['a','b'],['a','c'])==1
graphs={};actual=[];concepts=[]
for concept,rs in sorted(groups.items()):
    edges=[];label=[r['Cognacy'].strip() for r in rs];segments=[r['Segments'].split() for r in rs]
    for i in range(len(rs)):
        for j in range(i):
            if rs[i]['Language_ID']==rs[j]['Language_ID']:continue
            score=1-lev(segments[i],segments[j])/max(len(segments[i]),len(segments[j]))
            edges.append((i,j,score))
    pairs=[(s,label[i]==label[j]) for i,j,s in edges]
    actual.extend(pairs);graphs[concept]=(edges,label)
    concepts.append({'concept':concept,'forms':len(rs),'pairs':len(pairs),'positive_pairs':sum(p for s,p in pairs),'auc':auc(pairs)})
rng=random.Random(14026);controls=[]
for k in range(100):
    pool=[];macro=[]
    for edges,label in graphs.values():
        ls=label.copy();rng.shuffle(ls)
        pp=[(s,ls[i]==ls[j]) for i,j,s in edges];pool.extend(pp)
        a=auc(pp)
        if a is not None:macro.append(a)
    controls.append({'pooled_auc':auc(pool),'macro_auc':statistics.mean(macro) if macro else None})
def summarize(vals):
    vals=[v for v in vals if v is not None]
    return {'mean':statistics.mean(vals),'min':min(vals),'max':max(vals),'draws':len(vals)} if vals else None
result={'source_relative':'dravlex/cldf/forms.csv','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_forms':len(rows),'included_forms':sum(map(len,groups.values())),'excluded':dict(excluded),'languages':len({r['Language_ID'] for rs in groups.values() for r in rs}),'concepts':len(groups),'cross_language_within_concept_pairs':len(actual),'positive_pairs':sum(p for s,p in actual),'negative_pairs':sum(not p for s,p in actual),'pooled_auc':auc(actual),'macro_auc':statistics.mean(x['auc'] for x in concepts if x['auc'] is not None),'concepts_with_both_classes':sum(x['auc'] is not None for x in concepts),'shuffled_control_pooled':summarize([r['pooled_auc'] for r in controls]),'shuffled_control_macro':summarize([r['macro_auc'] for r in controls]),'p_value':None,'interpretation':'Descriptive known-language phonetic baseline using oracle concept and expert cognacy annotations. Artificial-label controls are not historical nulls. No Indus inference or family identification.'}
for name,value in [('results.json',result),('concept-results.json',concepts),('permutations.json',controls)]:
    (P/name).write_text(json.dumps(value,indent=2))
print(json.dumps(result,indent=2))
