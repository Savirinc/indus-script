import sys,pickle,statistics
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'lab'/'round30'))
import foreign_context as F
ctrl=[c for c in pickle.loads((H/'ctrl.pkl').read_bytes()) if 'SEAL:S' in c['types']]
FC=pickle.load(open(H/'fc.pkl','rb'))['FC']
for x in ctrl+FC: x['G']=x['M1']-x['M2']   # positive = bigram worse than unigram (transitions unattested)
print('FC G (M1-M2):',[round(f['G'],2) for f in FC])
print('ctrl G median %.2f, share>0 %.3f'%(statistics.median(c['G'] for c in ctrl),sum(c['G']>0 for c in ctrl)/len(ctrl)))
r=F.test_group(FC,ctrl,'G','g',nnull=5000);print('transition-excess G test',round(r['mean_percentile'],3),r['p_one_sided'],[round(x['percentile'],2) for x in r['per_text']])
