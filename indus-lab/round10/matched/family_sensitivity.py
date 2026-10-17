# Supplemental explicitly exploratory stress test; do not modify frozen round09.
import runpy,json,collections
from pathlib import Path
p=Path(__file__).resolve().parent
# Load functions without running model/report output a second time.
scope={};code=(p/'analyze.py').read_text().split('result=dict(status=')[0]
scope['__file__']=str(p/'analyze.py');exec(compile(code,str(p/'analyze.py'),'exec'),scope)
rows=scope['rows'];cond=scope['conditional'];out={}
for site in ['Harappa','Mohenjo-daro']:
 rs=[r for r in rows if r['site']==site];families=collections.defaultdict(set)
 for i,r in enumerate(rs):
  b=sorted(r['tokens'])
  for j in range(len(b)):families[tuple(b[:j]+b[j+1:])].add(i)
 tested=[]
 for core,ix in families.items():
  if sum(rs[i]['tablet'] and rs[i]['sign400'] for i in ix)<2:continue
  remaining=[r for i,r in enumerate(rs) if i not in ix]
  tested.append(dict(core=list(core),removed_ids=[rs[i]['id'] for i in sorted(ix)],removed_cisi=[rs[i]['cisi'] for i in sorted(ix)],**cond(remaining,False)))
 out[site]=dict(definition='All same-length records that can be reduced to this unordered core by deleting one sign occurrence. Test each nontransitive family containing >=2 sign400 tablets. Wider formula families remain untested.',tested_families=len(tested),results=sorted(tested,key=lambda r:-r['exact_two_sided_p']))
json.dump(out,(p/'family_sensitivity.json').open('w'),indent=2)
print(json.dumps({s:{'families':r['tested_families'],'worst':r['results'][:1]} for s,r in out.items()},indent=2))
