import csv,json,re,hashlib,collections
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'raw/inscriptions.csv'; rows=list(csv.DictReader(p.open()))
out=Path(__file__).parent
counts={k:dict(collections.Counter(r[k] for r in rows)) for k in ['time','period','phase']}
h=[r for r in rows if r['site']=='Harappa']
# Interpret only explicit HARP-style labels provisionally. Old numeric schemes
# and 5A/5B remain unassigned until the provenance of their scheme is verified.
mapdates={'1':(-3700,-2800),'2':(-2800,-2600),'3A':(-2600,-2450),'3B':(-2450,-2200),'3C':(-2200,-1900),'3B/C':(-2450,-1900),'3':(-2600,-1900),'4':(-1900,-1800)}
export=[]
for r in h:
 m=re.fullmatch(r'Period (1|2|3A|3B|3C|3B/C|3|4)(?:-\d+)?',r['time'])
 candidate_key=m[1] if m else None
 harp_prefix=bool(re.match(r'^H(?:\d{2}|20\d{2})-', r['excavation-idno']))
 key=candidate_key if harp_prefix else None
 d=mapdates.get(key)
 export.append({k:r[k] for k in ['id','cisi','site','excavation-idno','time','period','phase','type','material','symbol','text']} | {'label_only_candidate_bin':candidate_key or 'UNASSIGNED','harp_id_prefix':harp_prefix,'provisional_bin':key or 'UNASSIGNED','earliest_year':d[0] if d else '', 'latest_year':d[1] if d else '', 'dating_status':'harp_prefix_candidate_not_object_verified' if d else ('legacy_scheme_unverified' if candidate_key and not harp_prefix else 'scheme_or_date_unverified')})
with (out/'harappa_chronology_candidates.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(export[0]));w.writeheader();w.writerows(export)
summary={'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_records':len(rows),'harappa_records':len(h),'global_raw_label_counts':counts,'harappa_raw_time_counts':dict(collections.Counter(r['time'] for r in h)),'provisional_bins':dict(collections.Counter(r['provisional_bin'] for r in export)),'note':'Counts are source rows, not independently verified objects. Crosswalk is provisional; no significance test or sign chronology inferred. Translation columns excluded.'}
(out/'chronology_audit.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:summary[k] for k in ['source_records','harappa_records','provisional_bins']},indent=2))
