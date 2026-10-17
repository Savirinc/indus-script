"""Meaning-blind cross-language lexical retrieval; stdlib only."""
import csv,json,pathlib,collections as C,hashlib,random,statistics,time
P=pathlib.Path(__file__).resolve().parent
source=P.parents[1]/'round14/dravlex/cldf/forms.csv'
allrows=list(csv.DictReader(source.open()))
rs=[r for r in allrows if r['Loan'].strip().lower()=='false' and r['Segments'].strip() and r['Cognacy'].strip()]
by=C.defaultdict(list)
for i,r in enumerate(rs):by[r['Language_ID']].append(i)
seg=[tuple(r['Segments'].split()) for r in rs]
def lev(a,b):
    if a==b:return 0
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        cur=[i]
        for j,y in enumerate(b,1):cur.append(min(cur[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=cur
    return prev[-1]
# Compare exact rational normalized distances using cross multiplication.
best={};ties={};pairs=0;cache={}
for i in range(len(rs)):
    for j in range(i):
        li,lj=rs[i]['Language_ID'],rs[j]['Language_ID']
        if li==lj:continue
        key=tuple(sorted((seg[i],seg[j])))
        if key not in cache:cache[key]=lev(*key)
        d=cache[key];n=max(len(seg[i]),len(seg[j]));pairs+=1
        for q,t,l in [(i,j,lj),(j,i,li)]:
            k=(q,l);old=best.get(k)
            if old is None or d*old[1]<old[0]*n:best[k]=(d,n);ties[k]=[t]
            elif d*old[1]==old[0]*n:ties[k].append(t)
labels=[(r['Parameter_ID'],r['Cognacy'].strip()) for r in rs]
conceptcounts={l:C.Counter(labels[i][0] for i in ids) for l,ids in by.items()}
cogcounts={l:C.Counter(labels[i] for i in ids) for l,ids in by.items()}
out=[]
for (q,l),tt in sorted(ties.items()):
    concept,cog=labels[q];N=len(by[l]);same=conceptcounts[l][concept];cognate=cogcounts[l][labels[q]]
    out.append({'query_id':rs[q]['ID'],'query_index':q,'source_language':rs[q]['Language_ID'],'target_language':l,'candidate_count':N,'top_ties':len(tt),'top_candidate_indices':tt,'same_concept':sum(labels[t][0]==concept for t in tt)/len(tt),'same_concept_cognacy':sum(labels[t]==labels[q] for t in tt)/len(tt),'uniform_same_concept':same/N,'uniform_same_concept_cognacy':cognate/N,'cognate_available':cognate>0,'concept_available':same>0})
metrics=['same_concept','same_concept_cognacy','uniform_same_concept','uniform_same_concept_cognacy']
def summarize(rows):
    groups=C.defaultdict(list)
    for r in rows:groups[(r['source_language'],r['target_language'])].append(r)
    return {'queries':len(rows),'ordered_language_pairs':len(groups),'micro':{k:statistics.mean(r[k] for r in rows) for k in metrics},'language_pair_macro':{k:statistics.mean(statistics.mean(r[k] for r in rr) for rr in groups.values()) for k in metrics}}
directions=[]
for a in sorted(by):
    for b in sorted(by):
        if a==b:continue
        rr=[r for r in out if r['source_language']==a and r['target_language']==b]
        directions.append({'source':a,'target':b,**summarize(rr),'cognate_available_queries':sum(r['cognate_available'] for r in rr)})
controls=[]
for seed in range(15026,15046):
    rng=random.Random(seed);shuffled=labels.copy()
    for ids in by.values():
        ls=[labels[i] for i in ids];rng.shuffle(ls)
        for i,v in zip(ids,ls):shuffled[i]=v
    sums=[0.,0.]
    for r in out:
        q=r['query_index'];tt=r['top_candidate_indices'];sums[0]+=sum(shuffled[t][0]==labels[q][0] for t in tt)/len(tt);sums[1]+=sum(shuffled[t]==labels[q] for t in tt)/len(tt)
    controls.append({'seed':seed,'same_concept':sums[0]/len(out),'same_concept_cognacy':sums[1]/len(out)})
result={'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'eligible_forms':len(rs),'languages':len(by),'unordered_cross_language_form_pairs_scored':pairs,'all_queries':summarize(out),'cognate_available_queries':summarize([r for r in out if r['cognate_available']]),'ties':{'queries_with_ties':sum(r['top_ties']>1 for r in out),'mean_top_tie_size':statistics.mean(r['top_ties'] for r in out),'maximum_top_tie_size':max(r['top_ties'] for r in out)},'shuffled_target_labels':{k:{'mean':statistics.mean(r[k] for r in controls),'min':min(r[k] for r in controls),'max':max(r[k] for r in controls)} for k in ['same_concept','same_concept_cognacy']},'p_value':None,'interpretation':'Meaning labels excluded from scoring; phonetic values and segmentation known. All languages are related. Artificial-label controls, not historical inference. No Indus or family-identification conclusion.'}
assert len(out)==len(rs)*(len(by)-1)
assert all(0<=r[k]<=1 for r in out for k in metrics)
for name,value in [('results.json',result),('queries.json',out),('language-pairs.json',directions),('shuffled-controls.json',controls),('form-index.json',[{'index':i,'id':r['ID']} for i,r in enumerate(rs)])]:
    (P/name).write_text(json.dumps(value,indent=2))
print(json.dumps(result,indent=2))
