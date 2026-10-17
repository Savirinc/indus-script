"""Rebuild auditable object/face model. Never merge archaeological objects automatically."""
from pathlib import Path
import csv,json,re,hashlib,collections,sqlite3
P=Path(__file__).resolve().parent; R=P.parent
raw=R/'raw/inscriptions.csv';sha=hashlib.sha256(raw.read_bytes()).hexdigest()
rows=list(csv.DictReader(raw.open()));by=collections.defaultdict(list)
for i,r in enumerate(rows,2):by[r['id'].split('.')[0]].append((i,r))
quarantine={'sanskrit','translation','notes','class','cult'}
objects=[];faceids=set();assert len({r['id'] for r in rows})==len(rows)
for stem,rr in by.items():
 fields=['site','cisi','excavation-idno','type','material','sides'];meta={k:sorted({r[k] for _,r in rr}) for k in fields}
 conflicts={k:v for k,v in meta.items() if len(v)>1}
 faces=[]
 for line,r in rr:
  assert r['id'] not in faceids;faceids.add(r['id'])
  tokens=[{'code':int(m.group()),'raw_code':m.group(),'span':[m.start(),m.end()],'status':'unknown' if int(m.group())==0 else 'boundary_code' if int(m.group())==999 else 'catalogue_transcription'} for m in re.finditer(r'\d+',r['text'])]
  faces.append({'face_row_id':r['id'],'photographic_face':None,'source_line':line,'text_raw':r['text'],'direction_raw':r['dir.'],'complete_raw':r['complete'],'sign_occurrences':tokens,'metadata_raw':{k:v for k,v in r.items() if k not in quarantine},'verification':'unverified_source_transcription'})
 objects.append({'object_group_id':stem,'status':'source_ID_stem_not_verified_physical_identity','metadata_values':meta,'metadata_conflicts':conflicts,'recorded_faces':faces,'all_faces_known':False})
# Candidate alias evidence: matching site/excavation strings plus matching whole recorded text multiset.
index=collections.defaultdict(list)
for o in objects:
 m=o['metadata_values']
 if any(len(m[k])!=1 for k in ['site','excavation-idno']):continue
 exc=m['excavation-idno'][0].strip()
 if exc in ['','-','?','0','None']:continue
 index[(m['site'][0],exc)].append(o)
links=[]
for (site,exc),oo in index.items():
 if len(oo)<2:continue
 sigs={o['object_group_id']:tuple(sorted(f['text_raw'] for f in o['recorded_faces'])) for o in oo}
 links.append({'relation':'possible_alias_or_shared_excavation_identifier','site':site,'excavation_raw':exc,'object_groups':[o['object_group_id'] for o in oo],'cisi':[o['metadata_values']['cisi'] for o in oo],'all_recorded_text_multisets_equal':len(set(sigs.values()))==1,'resolution':'unresolved_do_not_merge'})
contract={'source_file':'raw/inscriptions.csv','source_sha256':sha,'raw_rows':len(rows),'object_groups':len(objects),'physical_object_count':None,'proposed_translation_columns_quarantined':sorted(quarantine),'raw_metadata_is_observation_not_validated_label':True,'photo_face_letters_are_not_row_suffixes':True,'all_recorded_faces_preserved':True,'unseen_holdout_exists':False,'possible_alias_groups':len(links),'alias_groups_with_equal_text_multisets':sum(a['all_recorded_text_multisets_equal'] for a in links),'metadata_conflict_groups':sum(bool(o['metadata_conflicts']) for o in objects)}
(P/'objects.json').write_text(json.dumps({'contract':contract,'objects':objects},indent=2));(P/'alias-candidates.json').write_text(json.dumps(links,indent=2));(P/'contract.json').write_text(json.dumps(contract,indent=2))
db=sqlite3.connect(P/'evidence.sqlite');db.executescript('DROP TABLE IF EXISTS objects; DROP TABLE IF EXISTS faces; DROP TABLE IF EXISTS alias_candidates; CREATE TABLE objects(object_group_id TEXT PRIMARY KEY,metadata_json TEXT,status TEXT); CREATE TABLE faces(face_row_id TEXT PRIMARY KEY,object_group_id TEXT REFERENCES objects(object_group_id),source_line INTEGER,text_raw TEXT,record_json TEXT); CREATE TABLE alias_candidates(candidate_id INTEGER PRIMARY KEY,evidence_json TEXT);')
for o in objects:
 db.execute('INSERT INTO objects VALUES(?,?,?)',(o['object_group_id'],json.dumps(o['metadata_values']),o['status']))
 for f in o['recorded_faces']:db.execute('INSERT INTO faces VALUES(?,?,?,?,?)',(f['face_row_id'],o['object_group_id'],f['source_line'],f['text_raw'],json.dumps(f)))
for i,a in enumerate(links):db.execute('INSERT INTO alias_candidates VALUES(?,?)',(i,json.dumps(a)))
db.commit();assert db.execute('SELECT COUNT(*) FROM faces').fetchone()[0]==len(rows);db.close()
assert sorted(f['face_row_id'] for o in objects for f in o['recorded_faces'])==sorted(r['id'] for r in rows)
print(json.dumps(contract,indent=2))
