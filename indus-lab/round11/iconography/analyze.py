from pathlib import Path
import csv,json,collections,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
raw={r['id']:r for r in csv.DictReader((ROOT/'raw/inscriptions.csv').open())}
rows=[dict(r,symbol=raw[r['id']]['symbol']) for r in json.load((ROOT/'round10/matched/analysis_rows.json').open()) if r['tablet']]
# Reuse the reviewed exact conditional implementation without invoking earlier experiment.
source=ROOT/'round10/matched/analyze.py'; scope={'__file__':str(source)}
exec(compile(source.read_text().split('result=dict(status=')[0],str(source),'exec'),scope)
def category(s):
 if s=='Gavi':return 'Gavi_label'
 if s=='None':return 'raw_None'
 if s.strip() in ['','-','?']:return 'missing'
 if s in ['Mult','Othr']:return s
 return 'other_specific_label'
def counts(rs,field):
 c=collections.defaultdict(lambda:[0,0])
 for r in rs:c[r[field]][r['sign400']]+=1
 return {k:dict(without400=v[0],with400=v[1],total=sum(v)) for k,v in sorted(c.items())}
for r in rows:r['category']=category(r['symbol'])
out=dict(status='Exploratory, selected sign and imagery label; nominal p values not selection-adjusted.',protocol_sha256=hashlib.sha256((P/'protocol.md').read_bytes()).hexdigest(),category_definition='Gavi label vs other specific labels; raw Mult, Othr, None, missing separated. Label is not actual motif presence or absence.',by_site={})
for site in ['Harappa','Mohenjo-daro']:
 rs=[r for r in rows if r['site']==site]
 entry=dict(raw_label_counts=counts(rs,'symbol'),category_counts=counts(rs,'category'),comparisons={})
 for name,categories in [('specific_labels',['Gavi_label','other_specific_label']),('include_Mult_Othr',['Gavi_label','other_specific_label','Mult','Othr'])]:
  sub=[dict(r,tablet=int(r['symbol']=='Gavi')) for r in rs if r['category'] in categories]
  # Reuse target field name `tablet` internally, replacing it with label Gavi indicator;
  # every physical record in this analysis already has raw object type TAB:B.
  if len({r['tablet'] for r in sub})<2:ans=dict(status='not_estimable_no_both_label_classes',groups=len(sub),Gavi_groups=sum(r['tablet'] for r in sub))
  else:ans=dict(status='estimated',groups=len(sub),table_rows_Gavi_other_cols_400_present_absent=scope['table'](sub),length_conditioned=scope['conditional'](sub))
  if ans['status']=='estimated':
   cc=ans['length_conditioned'];cc['observed_Gavi_with_sign']=cc.pop('observed_tablets_with_sign');cc['null_expected_Gavi_with_sign']=cc.pop('null_expected_tablets_with_sign')
   ss,pp,_=scope['distribution'](scope['terms'](sub),0.);obs=cc['observed_Gavi_with_sign']
   cc['equal_tail_two_sided_p']=min(1.,2.*min(float(pp[ss<=obs].sum()),float(pp[ss>=obs].sum())))
  entry['comparisons'][name]=ans
 out['by_site'][site]=entry
out['M482_audit']=dict(raw={k:raw['2966.1'][k] for k in ['id','cisi','symbol','type','text','sides']},observation='Coordinator reports photographic Gavi on M-482. This agent has not independently inspected that photograph.',interpretation='Mult is not a negative Gavi label: one image category cannot express all motifs on an object. This does not by itself prove a catalogue error.',consequence='Neither Gavi vs other labels nor raw None vs labelled picture constitutes validated motif presence/absence.')
json.dump(rows,(P/'analysis_rows.json').open('w'),indent=2)
json.dump(out,(P/'results.json').open('w'),indent=2)
print(json.dumps(out,indent=2))
