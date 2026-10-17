from pathlib import Path
import csv,json,re,hashlib,collections
from fractions import Fraction
P=Path(__file__).resolve().parent;src=P.parent/'raw/inscriptions.csv'
keys=['id','cisi','material','type','symbol','dir.','text','excavation-idno']
rows=[{k:r[k] for k in keys} for r in csv.DictReader(src.open()) if r['material']=='Copper' and r['type'].startswith('TAB')]
by=collections.defaultdict(list)
for r in rows:by[r['cisi']].append(r)
objects=[];excluded=[]
for obj,rs in sorted(by.items()):
    labels={r['symbol'] for r in rs}-{'','None','-','Unknown','Othr'}
    seqs={tuple(r['text'][1:-1].split('-')) for r in rs if r['dir.'] in {'R/L','L/R'} and re.fullmatch(r'\+\d{3}(?:-\d{3})*\+',r['text']) and '000' not in r['text'][1:-1].split('-')}
    if len(labels)!=1 or not seqs:
        excluded.append(dict(object=obj,reason='ambiguous/unspecified motif' if len(labels)!=1 else 'no clean directed text'));continue
    longest=[s for s in seqs if len(s)==max(map(len,seqs))]
    if len(longest)!=1:excluded.append(dict(object=obj,reason='tied longest texts'));continue
    objects.append(dict(object=obj,label=next(iter(labels)),text=longest[0]))
families=collections.defaultdict(list)
for r in objects:families[r['text']].append(r)
def dist(a,b):
    row=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        nxt=[i]
        for j,y in enumerate(b,1):nxt.append(min(row[j]+1,nxt[-1]+1,row[j-1]+(x!=y)))
        row=nxt
    return Fraction(row[-1],max(len(a),len(b)))
def unanimous(labels):
    s=set(labels);return next(iter(s)) if len(s)==1 else None
pred=[]
for r in objects:
    same=[q for q in families[r['text']] if q['object']!=r['object']]
    train=[q for q in objects if q['text']!=r['text']]
    ds={s:dist(r['text'],s) for s in families if s!=r['text']};best=min(ds.values())
    near=[s for s,d in ds.items() if d==best]
    ct=collections.Counter(q['label'] for q in train);m=max(ct.values());baseline=unanimous(k for k,v in ct.items() if v==m)
    pred.append(dict(r,exact_prediction=unanimous(q['label'] for q in same),held_family_prediction=unanimous(q['label'] for s in near for q in families[s]),majority_prediction=baseline,nearest_distance=str(best),nearest_texts=near,label_absent_in_training=r['label'] not in ct))
def score(key):
    return dict(correct=sum(r[key]==r['label'] for r in pred),predicted=sum(r[key] is not None for r in pred),total=len(pred),family_mean_success=sum(sum(q[key]==q['label'] for q in pred if q['text']==s)/len(rs) for s,rs in families.items())/len(families))
out=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),copper_rows=len(rows),catalogue_objects=len(by),eligible_objects=len(objects),excluded_objects=len(excluded),text_families=len(families),label_counts=dict(collections.Counter(r['label'] for r in objects)),conflicting_text_families=sum(len({q['label'] for q in rs})>1 for rs in families.values()),scores={k:score(k) for k in ['exact_prediction','held_family_prediction','majority_prediction']},label_absent_in_training=sum(r['label_absent_in_training'] for r in pred))
for name,data in [('results',out),('predictions',pred),('excluded',excluded),('copper_source_ledger',rows)]:
    (P/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(json.dumps(out,indent=2))
