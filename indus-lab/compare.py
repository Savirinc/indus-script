"""Separate-source descriptive checks and catalogue references for substitution examples."""
import collections as C,csv,json,pathlib
from expand import tokens
ROOT=pathlib.Path(__file__).resolve().parent;OUT=ROOT/'expanded'
profiles=[]
for fn,col in [('corpus.tsv','signs_reading'),('corpus_m77_added.tsv','signs_reading'),('cisi_mayig.tsv','signs')]:
    with (ROOT/'raw'/fn).open() as f: rows=list(csv.DictReader((s for s in f if not s.startswith('#')),delimiter='\t'))
    counts=C.Counter();ends=C.Counter();seqs=set()
    for r in rows:
        chunks=[[]]
        for g in r[col].split():
            if g in ('0','999','P000'):chunks.append([])
            else:chunks[-1].append(g)
        for s in chunks:
            counts.update(s)
            if len(s)>1:seqs.add(tuple(s))
    for s in seqs:ends[s[-1]]+=1
    profiles.append({'file':fn,'rows':len(rows),'observed_nonplaceholder_ids':len(counts),'tokens':sum(counts.values()),'distinct_segments_min2':len(seqs),'top_counts':counts.most_common(12),'top_terminal':ends.most_common(12),'note':'Different numbering schemes and mapped additions remain separate; unknown gaps split segments. Counts are descriptive, not independent validation.'})
(OUT/'separate_source_profiles.json').write_text(json.dumps(profiles,indent=2))
rows=json.load(open(OUT/'records.json'));look=C.defaultdict(list)
for r in rows:
    if r['dir.'].strip().upper()=='R/L' and r['complete']=='Y':
        for p in r['text'].split('/'):
            s=tokens(p)
            if p.startswith('+') and p.endswith('+') and None not in s:
                look[' '.join(reversed(s))].append({k:r[k] for k in ['id','cisi','site','type','symbol']})
ex=json.load(open(OUT/'substitutions.json'))[:20]
for e in ex:
    for x in e['examples']:x['left_records']=look[x['left']];x['right_records']=look[x['right']]
(OUT/'priority_examples.json').write_text(json.dumps(ex,indent=2))
print([(p['file'],p['rows'],p['observed_nonplaceholder_ids']) for p in profiles])
