"""One requested sampling sensitivity; fixed sign400, no discovery scan."""
from pathlib import Path
import json,csv,re,collections
p=Path(__file__).resolve().parent
scope={'__file__':str(p/'analyze.py')}
code=(p/'analyze.py').read_text().split('result=dict(status=')[0]
exec(compile(code,str(p/'analyze.py'),'exec'),scope)
raw=list(csv.DictReader((p.parents[1]/'raw/inscriptions.csv').open()))
groups=collections.defaultdict(list);eligible=collections.Counter()
for r in raw:
 if r['site'] not in ['Harappa','Mohenjo-daro'] or r['type'] not in ['TAB:B','SEAL:S'] or r['complete']!='Y':continue
 t=[int(x) for x in re.findall(r'\d+',r['text'])]
 if len(t)<3 or any(x in (0,999) for x in t):continue
 eligible[r['site']]+=1
 groups[(r['site'],tuple(sorted(t)))].append(dict(id=r['id'],cisi=r['cisi'],site=r['site'],type=r['type'],tablet=int(r['type']=='TAB:B'),sign400=int(400 in t),length=len(t),tokens=t,material=r['material']))
rows=[];conflicts=collections.Counter()
for (site,bag),g in groups.items():
 if len({r['tablet'] for r in g})>1:conflicts[site]+=1;continue
 rows.append(sorted(g,key=lambda r:r['id'])[0])
out=dict(status='Exploratory alternative sampling sensitivity, not independent replication.',definition='Raw complete Y >=3-sign records, no000/999, raw TAB:B/SEAL:S only. Group exact unordered multiset within site; exclude conflicting target labels within such groups; deterministic lexicographic ID representative. Shared patterns across cities retained. Physical-object/excavation links and near-duplicate formulas are not consolidated, so rows need not be independent objects.',eligible_rows=dict(eligible),conflicting_multiset_groups=dict(conflicts),by_site={s:scope['summarize']([r for r in rows if r['site']==s],False) for s in ['Harappa','Mohenjo-daro']},material_tables={s:{typ:dict(collections.Counter(r['material'] for r in rows if r['site']==s and r['type']==typ)) for typ in ['TAB:B','SEAL:S']} for s in ['Harappa','Mohenjo-daro']})
json.dump(rows,(p/'alternative_sampling_rows.json').open('w'),indent=2)
json.dump(out,(p/'alternative_sampling_results.json').open('w'),indent=2)
print(json.dumps({s:{'table':x['table_rows_tablet_seal_cols_sign_present_absent'],'conditional':x['length_conditioned']} for s,x in out['by_site'].items()},indent=2))
print('materials',out['material_tables'])
