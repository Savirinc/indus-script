"""Indus evidence lab. Python 3 standard library. No semantic readings assumed."""
import argparse, collections as C, csv, hashlib, itertools, json, pathlib, random, sqlite3

ROOT = pathlib.Path(__file__).resolve().parent
def read_tsv(name):
    with (ROOT/'raw'/name).open() as f:
        return list(csv.DictReader((l for l in f if not l.startswith('#')), delimiter='\t'))
def lines(text):
    out, current = [], []
    for token in text.split():
        if token in ('0','999'):
            if current: out.append(tuple(current))
            current=[]
        else: current.append(token)
    if current: out.append(tuple(current))
    return tuple(out)
def dump(name, data):
    (ROOT/'results'/name).write_text(json.dumps(data,indent=2,ensure_ascii=False))
def main():
    rows=read_tsv('corpus.tsv'); (ROOT/'results').mkdir(exist_ok=True)
    for r in rows: r['lines']=lines(r['signs_reading'])
    db=sqlite3.connect(ROOT/'results'/'evidence.sqlite')
    db.executescript('''
    DROP TABLE IF EXISTS objects; DROP TABLE IF EXISTS lines; DROP TABLE IF EXISTS substitutions;
    CREATE TABLE objects(id TEXT PRIMARY KEY,cisi TEXT,site TEXT,type TEXT,complete TEXT,direction TEXT,motif TEXT,raw_json TEXT);
    CREATE TABLE lines(object_id TEXT,line_no INTEGER,signs TEXT,PRIMARY KEY(object_id,line_no));
    CREATE TABLE substitutions(left_sequence TEXT,right_sequence TEXT,position INTEGER,left_sign TEXT,right_sign TEXT);
    CREATE TABLE IF NOT EXISTS image_views(id TEXT PRIMARY KEY,object_id TEXT,source_id TEXT,page INTEGER,bbox_json TEXT,view_kind TEXT,sha256 TEXT,orientation TEXT,review_status TEXT);
    CREATE TABLE IF NOT EXISTS sign_occurrences(id TEXT PRIMARY KEY,view_id TEXT,bbox_json TEXT,scheme TEXT,sign_id TEXT,alternative_ids TEXT,damage TEXT,review_status TEXT);
    CREATE TABLE IF NOT EXISTS hypotheses(id TEXT PRIMARY KEY,claim TEXT,prediction TEXT,alternative TEXT,test_spec TEXT,status TEXT);
    ''')
    for r in rows:
        db.execute('INSERT INTO objects VALUES (?,?,?,?,?,?,?,?)',tuple(r[k] for k in ['sealid','cisi','site','type','complete','direction','motif'])+(json.dumps({k:v for k,v in r.items() if k!='lines'}),))
        db.executemany('INSERT INTO lines VALUES (?,?,?)',[(r['sealid'],i+1,' '.join(s)) for i,s in enumerate(r['lines'])])
    groups=C.defaultdict(list)
    for r in rows: groups[r['lines']].append(r)
    recurrence=[]
    for seq,rr in groups.items():
        if len(rr)>1:
            recurrence.append(dict(sequence=' / '.join(' '.join(s) for s in seq),records=len(rr),sites=sorted({r['site'] for r in rr}),types=dict(C.Counter(r['type'] for r in rr)),motifs=dict(C.Counter(r['motif'] or '[unrecorded]' for r in rr)),objects=[r['cisi'] or 'ICIT:'+r['sealid'] for r in rr]))
    recurrence.sort(key=lambda r:(-r['records'],r['sequence']))
    by_type=[]
    for typ in sorted({r['type'] for r in rows}):
        rr=[r for r in rows if r['type']==typ]; n=len({r['lines'] for r in rr})
        by_type.append(dict(type=typ,records=len(rr),distinct_sequences=n,excess_copy_fraction=round(1-n/len(rr),4)))
    # Complete records, known source reading direction. No fused-sign expansion.
    clean=[r for r in rows if r['complete']=='Y' and r['direction'] in ('R/L','L/R')]
    unique_lines=sorted({s for r in clean for s in r['lines'] if len(s)>=2})
    tokens=C.Counter(s for line in unique_lines for s in line)
    starts=C.Counter(line[0] for line in unique_lines); ends=C.Counter(line[-1] for line in unique_lines)
    position=[dict(sign=s,tokens=n,start=starts[s],end=ends[s]) for s,n in tokens.most_common(30)]
    # Exploratory replication of known positional observation; NOT preregistered discovery.
    rng=random.Random(20261005); target='740'; observed=ends[target]
    null=[]
    for _ in range(999):
        null.append(sum(rng.choice(line)==target for line in unique_lines))
    test=dict(sign=target,eligible_distinct_lines=len(unique_lines),observed_terminal=observed,expected_terminal=sum(line.count(target)/len(line) for line in unique_lines),null_mean=sum(null)/len(null),null_min=min(null),null_max=max(null),permutations=len(null),p_one_sided=(1+sum(x>=observed for x in null))/(1+len(null)),seed=20261005,interpretation='Positional structure under supplied segmentation and direction; no sound or meaning inferred. Exploratory replication of a known pattern.')
    # Single substitutions in equal-length, complete, one-line sequences.
    single=sorted({r['lines'][0] for r in clean if len(r['lines'])==1 and 3<=len(r['lines'][0])<=12})
    wild=C.defaultdict(list)
    for seq in single:
        for i in range(len(seq)): wild[(i,seq[:i]+('*',)+seq[i+1:])].append(seq)
    edges=[]
    for (i,_),ss in wild.items():
        for a,b in itertools.combinations(ss,2):
            item=(' '.join(a),' '.join(b),i+1,a[i],b[i]); edges.append(item)
    db.executemany('INSERT INTO substitutions VALUES (?,?,?,?,?)',edges)
    db.commit();db.close()
    summary=dict(records=len(rows),sites=len({r['site'] for r in rows}),records_with_cisi=sum(bool(r['cisi']) for r in rows),distinct_object_sequences=len(groups),tokens_without_expanding_compounds=sum(len(s) for r in rows for s in r['lines']),motif_recorded=sum(r['motif'] not in ('','None','-') for r in rows),source_transcription='Bourdeau corpus.tsv, ICIT-derived; not independently read from photographs',exact_sequence_repeat_groups=len(recurrence),cross_site_repeat_groups=sum(len(r['sites'])>1 for r in recurrence),eligible_complete_direction_records=len(clean),single_substitution_edges=len(edges),image_views_reviewed=0)
    dump('summary.json',summary);dump('recurrence.json',recurrence);dump('by_type.json',by_type);dump('position.json',position);dump('position_test.json',test);dump('substitutions.json',[dict(zip(['left','right','position','left_sign','right_sign'],e)) for e in edges])
    dump('input_hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'raw').glob('*.tsv'))})
    print(json.dumps(dict(summary=summary,position_test=test,largest_groups=recurrence[:3],types=[r for r in by_type if r['records']>=100]),indent=2))
if __name__=='__main__': main()
