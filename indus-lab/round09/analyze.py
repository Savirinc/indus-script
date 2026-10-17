import csv,re,json,hashlib,collections
from pathlib import Path
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score,roc_auc_score,confusion_matrix
P=Path(__file__).resolve().parent; root=P.parent
raw=root/'raw/inscriptions.csv'
rows=list(csv.DictReader(raw.open()))
fix={r['id'] for r in json.load((root/'review08/object_type_corrections.json').open())}
rr=[]
for r in rows:
 typ='TAB' if r['id'] in fix else r['type'].split(':')[0]
 t=re.findall(r'\d+',r['text']); t=[int(x) for x in t]
 if typ not in ['SEAL','TAB'] or r['complete']!='Y' or len(t)<3 or any(x in (0,999) for x in t):continue
 rr.append(dict(id=r['id'],cisi=r['cisi'],site=r['site'],exc=r['excavation-idno'],tokens=t,y=int(typ=='TAB'),text=r['text']))
p=list(range(len(rr)))
def find(i):
 while p[i]!=i:p[i]=p[p[i]];i=p[i]
 return i
def union(a,b):p[find(a)]=find(b)
seen={}
for i,r in enumerate(rr):
 keys=[('stem',r['id'].split('.')[0]),('bag',tuple(sorted(r['tokens'])))]
 for name,val in [('cisi',r['cisi']),('exc',r['exc'])]:
  if val.strip() not in ('','-','?','None','0'):keys.append((name,r['site'] if name=='exc' else '',val.strip()))
 for k in keys:
  if k in seen:union(i,seen[k])
  else:seen[k]=i
comp=collections.defaultdict(list)
for i,r in enumerate(rr):comp[find(i)].append(r)
usable=[]; excluded=collections.Counter(); grouping=[]
for g in comp.values():
 conflict=len({r['y'] for r in g})>1; cross=len({r['site'] for r in g})>1
 reason='conflicting_labels' if conflict else 'multiple_sites' if cross else 'retained'
 excluded[reason]+=1
 s=sorted(g,key=lambda r:r['id'])[0]
 grouping.append(dict(representative=s['id'],members=[r['id'] for r in g],reason=reason))
 if reason=='retained':usable.append(s)
json.dump(grouping,(P/'groups.json').open('w'),indent=2)
counts=collections.Counter((r['site'],r['y']) for r in usable)
out=dict(protocol_sha256=hashlib.sha256((P/'protocol.md').read_bytes()).hexdigest(),raw_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),eligible_rows=len(rr),components=len(comp),group_disposition=dict(excluded),site_class_counts={f'{s}: {"tablet" if y else "seal"}':n for (s,y),n in counts.items()},transfers=[])
for train_site,test_site in [('Harappa','Mohenjo-daro'),('Mohenjo-daro','Harappa')]:
 tr=[r for r in usable if r['site']==train_site];te=[r for r in usable if r['site']==test_site]
 yt=np.array([r['y'] for r in tr]); y=np.array([r['y'] for r in te])
 if any(sum(a==k)<30 for a in [yt,y] for k in [0,1]):
  out['transfers'].append(dict(train=train_site,test=test_site,status='insufficient_groups'));continue
 v=DictVectorizer(sparse=False)
 X=v.fit_transform([{str(t):1 for t in r['tokens']} for r in tr]);Z=v.transform([{str(t):1 for t in r['tokens']} for r in te])
 l=np.log([len(r['tokens']) for r in tr]);ll=np.log([len(r['tokens']) for r in te]);sd=l.std() or 1
 l=((l-l.mean())/sd)[:,None];ll=((ll-np.log([len(r['tokens']) for r in tr]).mean())/sd)[:,None]
 models={}; preds={}
 for name,a,b in [('length_only',l,ll),('signs_and_length',np.column_stack([X,l]),np.column_stack([Z,ll]))]:
  m=LogisticRegression(C=1,class_weight='balanced',max_iter=3000).fit(a,yt);prob=m.predict_proba(b)[:,1];pred=(prob>=.5).astype(int);preds[name]=pred
  models[name]=dict(balanced_accuracy=balanced_accuracy_score(y,pred),auc=roc_auc_score(y,prob),confusion_seal_tablet=confusion_matrix(y,pred).tolist())
  if name=='signs_and_length':
   co=list(zip(v.get_feature_names_out(),m.coef_[0][:-1]));models[name]['exploratory_coefficients']=dict(tablet=sorted(co,key=lambda x:-x[1])[:10],seal=sorted(co,key=lambda x:x[1])[:10])
  for r,pr,pp in zip(te,prob,pred):r[name]=dict(probability_tablet=float(pr),prediction=int(pp))
 rng=np.random.default_rng(20261007);delta=[]
 # Stratified bootstrap preserves both class denominators.
 ix=[np.flatnonzero(y==k) for k in [0,1]]
 for _ in range(2000):
  j=np.concatenate([rng.choice(a,len(a),replace=True) for a in ix])
  delta.append(balanced_accuracy_score(y[j],preds['signs_and_length'][j])-balanced_accuracy_score(y[j],preds['length_only'][j]))
 out['transfers'].append(dict(train=train_site,test=test_site,train_groups=len(tr),test_groups=len(te),models=models,paired_gain_95pct=np.quantile(delta,[.025,.975]).tolist()))
 json.dump(te,(P/f'predictions-{test_site}.json').open('w'),indent=2)
json.dump(out,(P/'results.json').open('w'),indent=2)
print(json.dumps(out,indent=2))
