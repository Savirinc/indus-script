from pathlib import Path
import csv,json,re,collections
P=Path(__file__).parent
by=collections.defaultdict(list)
for r in csv.DictReader(open(P.parent/'raw/inscriptions.csv')):by[r['id'].split('.')[0]].append(r)
fam=collections.defaultdict(list)
for stem,rr in by.items():
 q=[];other=[]
 if any(r['complete']!='Y' or not re.fullmatch(r'\+\d+(?:-\d+)*\+',r['text']) or any(int(x) in (0,999) for x in re.findall(r'\d+',r['text'])) for r in rr):continue
 for r in rr:
  if r['complete']!='Y' or not re.fullmatch(r'\+\d+(?:-\d+)*\+',r['text']):continue
  t=[int(x) for x in re.findall(r'\d+',r['text'])]
  if any(x in (0,999) for x in t):continue
  if len(t)==2 and 700 in t and any(x in range(31,39) for x in t):q.append((r,next(x for x in t if x!=700)))
  else:other.append(r['text'])
 if not q or not other:continue
 for r,n in q:
  fam[(r['site'],tuple(sorted(set(other))))].append({'stem':stem,'id':r['id'],'cisi':r['cisi'],'type':r['type'],'stroke_code':n,'quantity_text':r['text'],'other_texts':sorted(set(other)),'excavation-idno':r['excavation-idno']})
out=[]
for (site,other),rs in fam.items():
 variants=sorted({r['stroke_code'] for r in rs})
 if len(variants)>1:out.append({'site':site,'other_texts':other,'stroke_variants':variants,'records':rs})
out.sort(key=lambda a:-len(a['records']))
json.dump(out,open(P/'crossface-strict-results.json','w'),indent=2)
for a in out:print(a['site'],a['other_texts'],a['stroke_variants'],'records',len(a['records']),[(r['cisi'],r['stroke_code']) for r in a['records']][:15])
