import csv,re,json,collections
from pathlib import Path
P=Path(__file__).parent;R=P.parent
rows=[];pairs=[];contexts=collections.defaultdict(list)
for r in csv.DictReader(open(R/'raw/inscriptions.csv')):
 if r['complete']!='Y' or not re.fullmatch(r'\+\d+(?:-\d+)+\+',r['text']):continue
 t=[int(a) for a in re.findall(r'\d+',r['text'])]
 if any(a in (0,999) for a in t) or 700 not in t:continue
 a={k:r[k] for k in ['id','cisi','site','type','material','symbol','text','dir.']};a['tokens']=t;rows.append(a)
 for j in range(len(t)-1):
  if (t[j]==700 and t[j+1] in range(1,8)) or (t[j+1]==700 and t[j] in range(1,8)):
   n=j+1 if t[j]==700 else j;c=t.copy();v=c[n];c[n]='STROKES';a2=a|{'stroke_code':v,'pair_visual':t[j:j+2],'context':c};pairs.append(a2);contexts[tuple(c)].append(a2)
unique={tuple(a['tokens']) for a in rows};withpair={tuple(a['tokens']) for a in pairs}
families=[]
for c,rr in contexts.items():
 vs=sorted({a['stroke_code'] for a in rr})
 if len(vs)>=2:families.append({'context':c,'stroke_variants':vs,'records':rr})
result={'scope':'Simple complete text rows; adjacency in stored visual order; exploratory known hypothesis','records_with700':len(rows),'unique_texts_with700':len(unique),'records_with_adjacent_strokes':len({a['id'] for a in pairs}),'unique_texts_with_adjacent_strokes':len(withpair),'unique_2token_pairs':[list(t) for t in sorted(withpair) if len(t)==2],'variable_stroke_families':families,'all_700_rows':rows,'all_pair_rows':pairs}
json.dump(result,open(P/'quantity-results.json','w'),indent=2)
print({k:v for k,v in result.items() if k not in ['variable_stroke_families','all_700_rows','all_pair_rows']})
for f in families:print('FAMILY',f['context'],f['stroke_variants'],[(a['cisi'],a['text']) for a in f['records']][:25])
