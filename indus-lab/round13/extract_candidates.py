"""Extract narrow pottery candidates. Complete inscription != complete vessel."""
from pathlib import Path
import csv, re, json, hashlib
p=Path(__file__).resolve().parent
raw=p.parent/'raw/inscriptions.csv'
rows=list(csv.DictReader(raw.open()))
out=[]
for r in rows:
    if not r['type'].startswith('POT'): continue
    t=re.findall(r'\d+',r['text'])
    if r['complete']=='Y' and re.fullmatch(r'\+\d+(?:-\d+)*\+',r['text']) and len(t)==2 and '700' in t and any(31<=int(x)<=38 for x in t):
        fields=['id','cisi','site','excavation-idno','area-section','text','type','material','horizontal(mm)','vertical(mm)','thickness(mm)']
        item={k:r[k] for k in fields}
        item['capacity_litres']=None
        item['whole_vessel_verified']=False
        item['stroke_count_from_catalogue']=next(int(x)-30 for x in t if x!='700')
        out.append(item)
(p/'pot-candidates.json').write_text(json.dumps(out,indent=2)+'\n')
(p/'extraction-contract.json').write_text(json.dumps({'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'candidates':len(out),'zero_dimension_records':sum(all(x[k]=='0' for k in ['horizontal(mm)','vertical(mm)','thickness(mm)']) for x in out),'zero_interpretation':'missing/unusable, never zero capacity','complete_flag':'inscription completeness, not vessel completeness','excluded_calibration_object':'H-370 has strokes without700','search_is_exploratory':True},indent=2)+'\n')
print(f'{len(out)} candidates; capacity observations unavailable')
