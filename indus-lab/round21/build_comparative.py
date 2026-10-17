"""Observed cognate evidence; does not generate or assert ancestral words."""
from pathlib import Path
import csv,json,collections,hashlib
P=Path(__file__).resolve().parent;R=P.parent
src=R/'round14/dravlex/cldf/forms.csv'
rows=list(csv.DictReader(src.open()))
eligible=[r for r in rows if r['Loan'].lower()=='false' and r['Segments'].strip() and r['Cognacy'].strip()]
groups=collections.defaultdict(list)
for r in eligible:
    groups[(r['Parameter_ID'],r['Cognacy'])].append({k:r[k] for k in ['ID','Language_ID','Parameter_ID','Form','Segments','Cognacy','Source']})
ledger=[dict(concept=c,cognacy_label=g,languages=len({r['Language_ID'] for r in rs}),forms=rs,reconstruction=None,status='Observed forms and imported cognacy; no proto-form inferred') for (c,g),rs in sorted(groups.items())]
(P/'comparative_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
# One initial correspondence per concept per ordered language/segment pair.
observations=set()
for (c,g),rs in groups.items():
    for a in rs:
        for b in rs:
            if a['Language_ID']!=b['Language_ID']:
                aa=[s for s in a['Segments'].split() if s!='+'];bb=[s for s in b['Segments'].split() if s!='+']
                if aa and bb:observations.add((c,a['Language_ID'],b['Language_ID'],aa[0],bb[0]))
mapping=collections.defaultdict(set)
for c,a,b,x,y in observations:mapping[(a,b,x,y)].add(c)
correspondences=[dict(source_language=a,target_language=b,source_initial=x,target_initial=y,concepts=sorted(cs),concept_count=len(cs)) for (a,b,x,y),cs in sorted(mapping.items())]
(P/'initial_correspondences.json').write_text(json.dumps(correspondences,ensure_ascii=False,indent=2))
ta_ka=[r for r in correspondences if r['source_language']=='Tamil' and r['target_language']=='Kannada' and r['source_initial']=='p']
checks=[dict(target_initial=r['target_initial'],support_excluding_tooth=[c for c in r['concepts'] if c!='89_tooth']) for r in ta_ka]
out=dict(raw_forms=len(rows),eligible_forms=len(eligible),concepts=len({r['Parameter_ID'] for r in eligible}),languages=len({r['Language_ID'] for r in eligible}),cognate_groups=len(ledger),cross_language_groups=sum(x['languages']>=2 for x in ledger),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),Tamil_p_to_Kannada=checks,limitations=['Cognacy labels and loan flags supplied by dataset, not independently proved.','Initial correspondences are descriptive; no full alignment, sound-law direction, ancestral chronology, or Proto-Dravidian inference.','Tooth selected after inspecting examples: illustrative leave-one-concept-out check, not blinded prospective validation.','No Indus values or Meluhhan words assigned.'])
(P/'summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
