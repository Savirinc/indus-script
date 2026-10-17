"""Reproduce coverage only; proposed readings are not translations."""
import csv,json,re,hashlib,collections
from pathlib import Path
P=Path(__file__).resolve().parent

def js(name):
 s=(P/name).read_text(); return json.loads(s[s.index('{'):].rstrip(';\n '))
j=js('texts.js'); data=[dict(zip(j['columns'],r)) for r in j['rows']]
xl={r['sign']:r for r in csv.DictReader(open(P/'xlits.csv'))}
# Table 7 PUA glyphs transcribed from Nov 13 2024 PDF p23 (printed 23).
# This older font is NOT the repo's E000+sign-ID font.
entries=[('a','E06C'),('i','E261'),('u','E53B'),('e','E3B3'),('o','E402'),('k','E4C7'),('kh','E275'),('g','E3EA'),('gh','E3EA'),('ṅ','E56B'),('c','E210'),('ch','E210'),('j','E322'),('jh','E365'),('ñ','E427'),('ṭ','E34F'),('ṭh','E6D3'),('ḍ','E346'),('ḍh','E353'),('ṇ','E538'),('t','E443'),('th','E6C3'),('d','E346'),('dh','E37D'),('n','E538'),('p','E566'),('ph','E566'),('b','E503'),('bh','E577'),('m','E10A'),('y','E59C'),('r','E1FF'),('l','E405'),('v','E559'),('ś','E304'),('ṣ','E190'),('s','E19B'),('h','E190')]
old=list(csv.DictReader(open(P/'glyphs.tsv'),delimiter='\t'))
cross=[];strict={}
for sound,cp in entries:
 ids=[r['glyph'].zfill(3) for r in old if r['codepoints']==cp]
 status='unique font crosswalk' if len(ids)==1 else ('multiple catalogue candidates' if ids else 'unresolved')
 cross.append(dict(sound=sound,pdf_codepoint=cp,candidate_ids=ids,status=status))
 if len(ids)==1: strict.setdefault(ids[0],[]).append(sound)
(P/'table7-crosswalk.json').write_text(json.dumps(cross,ensure_ascii=False,indent=2))
valid={k:v['xlit'] for k,v in xl.items() if v['xlit'].strip() and k not in ('000','999')}
out=[];tokens=collections.Counter(); fully=0;cleann=cleanf=0
for r in data:
 lines=[re.findall(r'\d{3}',s) for s in r['text_code'].split('/')]
 flat=sum(lines,[]);tokens.update(flat)
 missing=sorted(set(flat)-valid.keys());ok=bool(flat) and not missing
 direction=str(r['direction']).strip().upper()
 oriented=direction in ('R/L','L/R') and len(lines)==1
 ids=flat[::-1] if direction=='R/L' and len(lines)==1 else flat
 clean=str(r['complete']).strip().upper() in ('Y','YES') and oriented and not any(x in ('000','999') for x in flat) and not any(x in r['text_code'] for x in '[]')
 fully+=ok;cleann+=clean;cleanf+=clean and ok
 out.append(dict(id=r['id'],cisi=r['cisi'].strip(' <'),site=r['site'],text_code=r['text_code'],direction=direction,order='reading order' if oriented else 'stored order; direction or line order unresolved',candidate_tokens=[valid.get(x,'?'+x) for x in ids],all_tokens_assigned=ok,missing_ids=missing,strict_singleline_complete=clean,table7_unique_crosswalk_all=bool(flat) and all(x in strict for x in flat)))
summary=dict(records=len(data),mapping_rows=len(xl),usable_mapping_ids=len(valid),distinct_observed_codes=len(tokens),tokens=sum(tokens.values()),assigned_tokens=sum(n for k,n in tokens.items() if k in valid),all_tokens_assigned_records=fully,strict_singleline_complete_records=cleann,strict_singleline_complete_all_assigned=cleanf,table7_entries=len(entries),table7_distinct_drawings=len(set(cp for _,cp in entries)),table7_unique_crosswalk_entries=sum(r['status']=='unique font crosswalk' for r in cross),table7_unique_crosswalk_ids=len(strict),table7_unresolved_entries=sum(r['status']=='unresolved' for r in cross),table7_ambiguous_entries=sum(r['status']=='multiple catalogue candidates' for r in cross),table7_uniquely_crosswalked_token_count=sum(tokens[k] for k in strict),table7_unique_crosswalk_complete_records=sum(r['table7_unique_crosswalk_all'] for r in out),unassigned_codes=[dict(id=k,count=n,mapping_present=k in xl) for k,n in tokens.most_common() if k not in valid],m304=[r for r in out if r['cisi']=='M-304'])
(P/'results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));(P/'candidate-readings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(P/'manifest.json').write_text(json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in P.iterdir() if f.is_file() and f.name not in ('manifest.json','REPORT.md')},indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
