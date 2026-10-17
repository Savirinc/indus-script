"""Sensitivity audit: line-local versus record-level edge markers.
Preserves earlier results. Alternative policy requires complete R/L record,
intact outer '+' edges, and no placeholders in the individual line.
This does not establish line ordering or adjudicate source transcription.
"""
import json,pathlib,collections as C
ROOT=pathlib.Path(__file__).resolve().parent;OUT=ROOT/'review';OUT.mkdir(exist_ok=True)
rows=json.load(open(ROOT/'expanded/records.json'));old=set();new=set();ledger=[]
for r in rows:
    eligible=r['complete']=='Y' and r['dir.'].strip().upper()=='R/L'
    record_intact=r['text'].startswith('+') and r['text'].endswith('+')
    a=[];b=[]
    for i,(p,s) in enumerate(zip(r['text'].split('/'),r['segments_visual'])):
        legible=None not in s and len(s)>=2
        before=eligible and legible and p.startswith('+') and p.endswith('+')
        after=eligible and legible and record_intact
        if before:old.add(tuple(reversed(s)));a.append(i+1)
        if after:new.add(tuple(reversed(s)));b.append(i+1)
    ledger.append({'id':r['id'],'cisi':r['cisi'],'multiline':'/' in r['text'],'complete_RL':eligible,'outer_edges_intact':record_intact,'old_lines':a,'alternative_lines':b})
def contexts(lines,left='220',right='231'):
    result=[]
    for s in sorted(lines):
        if not 3<=len(s)<=12:continue
        for i,g in enumerate(s):
            if g==left:
                t=s[:i]+(right,)+s[i+1:]
                if t in lines:result.append({'left':' '.join(s),'right':' '.join(t),'position':i+1})
    return result
summary={'old_distinct_lines':len(old),'alternative_distinct_lines':len(new),'additional_distinct_lines':len(new-old),'removed_distinct_lines':len(old-new),'multiline_records':sum(x['multiline'] for x in ledger),'complete_RL_multiline_records':sum(x['multiline'] and x['complete_RL'] for x in ledger),'old_contributing_multiline_records':sum(x['multiline'] and bool(x['old_lines']) for x in ledger),'alternative_contributing_multiline_records':sum(x['multiline'] and bool(x['alternative_lines']) for x in ledger),'old_220_231_contexts':contexts(old),'alternative_220_231_contexts':contexts(new),'status':'Sensitivity run only; historical reports retained. Alternative parsing convention must be verified against source documentation and photographs before replacing canonical results.'}
(OUT/'multiline_ledger.json').write_text(json.dumps(ledger,indent=2));(OUT/'multiline_sensitivity.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
