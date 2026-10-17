import csv,json,re
from pathlib import Path
p=Path(__file__).resolve().parent
rows=list(csv.DictReader(open(p/'xlits.csv')));m={r['sign']:r['xlit'] for r in rows}
# Mirror the single ordered canonical pass in index.vue mkregex; no recursive invention.
for r in rows:
 if not m[r['sign']]:m[r['sign']]=''.join(m.get(k,'') for k in reversed(r['canonical'].split('-')))
valid={k:v for k,v in m.items() if v.strip() and k not in ('000','999')}
data=json.load(open(p/'candidate-readings.json'))
for r in data:
 ids=re.findall(r'\d{3}',r['text_code'])
 if r['order']=='reading order' and r['direction']=='R/L':ids.reverse()
 r['canonical_expanded_tokens']=[valid.get(k,'?'+k) for k in ids]
 r['canonical_all_assigned']=bool(ids) and all(k in valid for k in ids)
s=dict(usable_ids=len(valid),records_all_assigned=sum(r['canonical_all_assigned'] for r in data),strict_complete_all_assigned=sum(r['canonical_all_assigned'] for r in data if r['strict_singleline_complete']),unresolved_ids=[k for k in m if k not in valid],m304=[r for r in data if r['cisi']=='M-304'])
(p/'canonical-results.json').write_text(json.dumps(s,ensure_ascii=False,indent=2));(p/'candidate-readings.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));(p/'expanded-map.json').write_text(json.dumps(valid,ensure_ascii=False,indent=2));print(json.dumps(s,ensure_ascii=False,indent=2))
