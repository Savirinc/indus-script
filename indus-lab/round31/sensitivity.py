"""Round 31: transcription-sensitivity of round 30 P1, after checking readings against Gadd 1932,
Mahadevan 1977 and Laursen 2010 (text). Scenarios defined from the verification ledger (VERIFICATION.md)
before running. Same model, controls, metric and null as round 30. Texts given in STORED order + direction."""
import sys,json,statistics
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'round30'))
import foreign_context as F
base={r['id']:r for r in json.loads((P.parent/'round30/results.json').read_text())['groups']['F_C']}
def item(i,stored=None,d=None):
    r=dict(base[i]);t=tuple(r['text'])
    if stored is not None:
        s=tuple(stored.split('-'));t=s[::-1] if (d or 'R/L')=='R/L' else s
    r['text']=t;r['key']='X'+i;r.update(F.score(t));return r
ctrl=[]
for t in F.TRAIN:
    if 'SEAL:S' in F.core_types[t]['types']:
        c=dict(key='C'+'-'.join(t),text=t);c.update(F.score(t));ctrl.append(c)
ALL=['2153.1','3863.1','3897.1','3898.1','5227.1','5228.1','5229.1','5232.1']
S={
 'S0_as_round30':[item(i) for i in ALL],
 'S1_drop_5228_pseudo':[item(i) for i in ALL if i!='5228.1'],
 'S2a_3898_Mahadevan_004':[item(i) if i!='3898.1' else item(i,'004-328-001-803-415') for i in ALL],
 'S2b_3898_Gadd_4signs':[item(i) if i!='3898.1' else item(i,'328-001-803-415') for i in ALL],
 'S3_drop_conflicted(5228,3863,5232)':[item(i) for i in ALL if i not in ('5228.1','3863.1','5232.1')],
 'S4_only_independently_supported(3897,3898mah,5227,5229)':[item('3897.1'),item('3898.1','004-328-001-803-415'),item('5227.1'),item('5229.1')],
}
out={}
for k,v in S.items():
    for m in ('M1','M3'):
        r=F.test_group(v,ctrl,m,'r31:'+k+m);r.pop('_null')
        out[k+':'+m]=r;print(f"{k:58s} {m} n={r['n']} mean_pct={r['mean_percentile']:.3f} p={r['p_one_sided']:.4f}",flush=True)
(P/'sensitivity_results.json').write_text(json.dumps(out,indent=2,default=list))
