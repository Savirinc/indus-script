"""Explore one-added-component candidates against exact inscription contexts.
Consumes prior decomposition and full-snapshot outputs; no semantic labels inferred.
"""
import collections as C,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent;OUT=ROOT/'additive';OUT.mkdir(exist_ok=True)
def read(p):return json.load(open(ROOT/p))
families=read('components/candidate_part_families.json');parts=read('components/parts.json')
mapping={p:i for i,f in enumerate(families) for p in f};bags=C.defaultdict(C.Counter)
for p in parts:bags[p['sign']][mapping[p['id']]]+=1
swaps={frozenset((x['sign_a'],x['sign_b'])):x for x in read('expanded/substitutions.json')}
lookup=C.defaultdict(list)
for r in read('expanded/records.json'):
    if r['complete']!='Y' or r['dir.'].strip().upper()!='R/L':continue
    for p,s in zip(r['text'].split('/'),r['segments_visual']):
        if p.startswith('+') and p.endswith('+') and None not in s:
            lookup[' '.join(reversed(s))].append({k:r[k] for k in ['id','cisi','site','type','symbol']})
candidates=[]
for a,aa in bags.items():
    for b,bb in bags.items():
        if sum(bb.values())!=sum(aa.values())+1 or aa-bb:continue
        hit=swaps.get(frozenset((a,b)),{})
        row={'base':a,'extended':b,'base_parts':sum(aa.values()),'matching_contexts':hit.get('contexts',0),'examples':[]}
        for ex in hit.get('examples',[]):
            e=dict(ex);e['left_records']=lookup[e['left']];e['right_records']=lookup[e['right']]
            matched=[(x,y) for x in e['left_records'] for y in e['right_records'] if (x['site'],x['type'])==(y['site'],y['type'])]
            e['same_site_type_record_pairs']=len(matched)
            valid=[(x,y) for x,y in matched if x['symbol'] not in ('','None','-') and y['symbol'] not in ('','None','-')]
            e['pairs_with_two_recorded_motifs']=len(valid)
            e['pairs_same_broad_motif']=sum(x['symbol'].split(':')[0]==y['symbol'].split(':')[0] for x,y in valid)
            row['examples'].append(e)
        candidates.append(row)
candidates.sort(key=lambda x:(-x['matching_contexts'],int(x['base']),int(x['extended'])))
summary={'one_extra_component_candidates':len(candidates),'pairs_with_matching_contexts':sum(x['matching_contexts']>0 for x in candidates),'matching_contexts_total':sum(x['matching_contexts'] for x in candidates),'method':'Component-family multiset containment plus exactly one part, intersected with prior one-sign substitutions. Geometry and component roles are not guaranteed by this filter.','result_status':'Exploratory candidate retrieval; no significance test, decipherment, or claim of novelty.'}
(OUT/'candidates.json').write_text(json.dumps(candidates,indent=2));(OUT/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
