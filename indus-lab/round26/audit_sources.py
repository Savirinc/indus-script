"""Compare supplied elephant records across digital representations; never execute SQL."""
from pathlib import Path
import csv,json,re,hashlib
P=Path(__file__).resolve().parent
data=json.loads((P/'input_records.json').read_text())
sql=(P/'sql_sign_rows.txt').read_text()
triples=[tuple(map(int,t)) for t in re.findall(r'\((\d+),(\d+),(\d+)\)',sql)]
out=[]
for r in data:
    sid=int(r['id'].split('.')[0]);entries=sorted((pos,sign) for obj,sign,pos in triples if obj==sid)
    signs=[x for p,x in entries];csvsigns=[int(s) for s in r['stored_text'].strip('+').split('-')]
    out.append(dict(object=r['cisi'],stored_text=r['stored_text'],fresh_lipi_text=r['fresh_lipi_text'],sql_signs=signs,sql_matches=signs==csvsigns,fresh_lipi_matches=r['fresh_lipi_text']==r['stored_text'],phonetic_constraint_usable=False,reason='Presence/absence of isolated mark not independently established; related digital sources do not constitute independent readings'))
(P/'comparison.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'objects':len(out),'fresh_lipi_matches':sum(r['fresh_lipi_matches'] for r in out),'sql_matches':sum(r['sql_matches'] for r in out)},indent=2))
