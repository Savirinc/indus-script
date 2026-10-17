"""Prespecified structural null; no numerical or linguistic interpretation."""
import csv,json,re,collections as C,random,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parent
raw=P.parents[1]/'raw'/'inscriptions.csv'
by=C.defaultdict(list)
for r in csv.DictReader(raw.open()):by[r['id'].split('.')[0]].append(r)
ledger=[];data=[]
unknown={'','-','--','none','unknown'}
for stem,rr in by.items():
    reason=None;target=[];other=[]
    for r in rr:
        if r['complete']!='Y' or not re.fullmatch(r'\+\d+(?:-\d+)*\+',r['text']):reason='incomplete_or_complex_face';break
        t=list(map(int,re.findall(r'\d+',r['text'])))
        if any(x in (0,999) for x in t):reason='unknown_or_separator';break
        if len(t)==2 and 700 in t and any(31<=x<=38 for x in t):target.append((r,next(x for x in t if x!=700)))
        else:other.append(r['text'])
    if reason is None and len(target)!=1:reason='multiple_target_faces' if len(target)>1 else 'no_target_face'
    if reason is None and not other:reason='no_other_face'
    strata={(r['site'].strip(),r['material'].strip().lower(),r['type'].strip()) for r in rr}
    if reason is None and len(strata)!=1:reason='inconsistent_stratum'
    if reason is None and any(v.lower() in unknown for v in next(iter(strata))):reason='unknown_stratum'
    if reason is None and any(not r['sides'].isdigit() or int(r['sides'])!=len(rr) for r in rr):reason='unverified_face_count'
    entry={'stem':stem,'ids':[r['id'] for r in rr],'cisi':rr[0]['cisi'],'status':reason or 'included'}
    ledger.append(entry)
    if reason is None:data.append(dict(entry,stratum=list(next(iter(strata))),context=sorted(other),code=target[0][1],target_face=target[0][0]['id'],excavation=rr[0]['excavation-idno']))
strata=C.defaultdict(list)
for i,r in enumerate(data):strata[tuple(r['stratum'])].append(i)
contexts=[(tuple(r['stratum']),tuple(r['context'])) for r in data]
codes=[r['code'] for r in data]
def score(vals):
    cells=C.Counter((contexts[i],x) for i,x in enumerate(vals))
    return sum(n*(n-1)//2 for n in cells.values())
observed=score(codes);den=sum(n*(n-1)//2 for n in C.Counter(contexts).values())
rng=random.Random(12026);null=[]
for _ in range(999):
    v=codes.copy()
    for ids in strata.values():
        vals=[codes[i] for i in ids];rng.shuffle(vals)
        for i,x in zip(ids,vals):v[i]=x
    null.append(score(v))
unique={(contexts[i],x) for i,x in enumerate(codes)}
remaining_contexts=C.Counter(k for k,x in unique)
movable=sum(len({codes[i] for i in ids})>1 and len({contexts[i] for i in ids})>1 for ids in strata.values())
result={'input_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'eligibility_counts':dict(C.Counter(x['status'] for x in ledger)),'included_object_stems':len(data),'strata':len(strata),'strata_with_code_and_context_variation':movable,'contexts':len(set(contexts)),'same_context_pairs':den,'observed_same_context_same_code_pairs':observed,'null_draws':999,'null_min':min(null),'null_max':max(null),'null_mean':sum(null)/len(null),'conditional_reference_p_upper':(1+sum(x>=observed for x in null))/1000 if len(set(null))>1 else None,'reference_status':'Exploratory conditional label-shuffle reference only; physical-object and production-family exchangeability unverified. Not a population inference or semantic test.','copy_aware_sensitivity':{'unique_context_code_configurations':len(unique),'remaining_same_context_pairs':sum(n*(n-1)//2 for n in remaining_contexts.values()),'observed':0,'all_valid_unique_configuration_null_scores':0,'p_value':None,'status':'Blocked by mathematical degeneracy: after one representative per context/code cell, same-context same-code pair count is always zero. Unrestricted permutation would create disallowed duplicate cells and is not a valid copy-collapsed control.'},'semantic_conclusion':'None. Quantity and category labels can both generate these associations.'}
for name,value in [('ledger.json',ledger),('eligible-objects.json',data),('results.json',result),('null-scores.json',null)]:
    (P/name).write_text(json.dumps(value,indent=2))
print(json.dumps(result,indent=2))
