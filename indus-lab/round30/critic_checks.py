"""Round 30 critic checks: POST HOC, written after seeing P1 results and the foreign texts. Exploratory only."""
import sys,json,random,statistics,collections
from pathlib import Path
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
import foreign_context as F
res=json.loads((P/'results.json').read_text())
# rebuild control pool scores (deterministic)
ctrl=[]
for t in F.TRAIN:
    if 'SEAL:S' in F.core_types[t]['types']:
        c=dict(key='C'+'-'.join(t),text=t);c.update(F.score(t));ctrl.append(c)
out={}
# (1) seal-format confound: in-region round & cylinder seals, scored leave-neighbourhood-out
inreg=[]
for r in F.rows:
    if r['region'] in F.CORE and r['type'] in ('SEAL:C','SEAL:CY'):
        s=F.clean(r)
        if s: d=dict(id=r['id'],site=r['site'],type=r['type'],text=s,key='X'+r['id']);d.update(F.score(s));inreg.append(d)
for m in ('M1','M3'):
    t=F.test_group(inreg,ctrl,m,'r30critic:'+m);t.pop('_null');out['inregion_round_cyl_'+m]=t
    print('in-region round/cyl seals',m,'n',t['n'],'mean pct %.3f p %.4f'%(t['mean_percentile'],t['p_one_sided']))
    for x in t['per_text']:print('   ',x)
# (2) shared structure WITHIN foreign round seals vs pooled-token reshuffle
FC=[tuple(x['text']) for x in res['groups']['F_C']]
def stats(texts):
    init=collections.Counter(t[0] for t in texts);pairs_init=sum(c*(c-1)//2 for c in init.values())
    bg=collections.Counter(b for t in texts for b in set(zip(t,t[1:])));shared_bg=sum(1 for c in bg.values() if c>=2)
    return pairs_init,shared_bg
obs=stats(FC);toks=[x for t in FC for x in t];lens=[len(t) for t in FC];rng=random.Random('r30critic:share');null=[]
for _ in range(20000):
    rng.shuffle(toks);it=iter(toks);null.append(stats([tuple(next(it) for _ in range(L)) for L in lens]))
out['within_FC']=dict(observed_initial_pairs=obs[0],observed_shared_bigrams=obs[1],
  p_initial=(1+sum(n[0]>=obs[0] for n in null))/20001,p_bigram=(1+sum(n[1]>=obs[1] for n in null))/20001,
  null_mean_initial=statistics.fmean(n[0] for n in null),null_mean_bigram=statistics.fmean(n[1] for n in null))
print('within F_C',out['within_FC'])
# (3) how do key recurring foreign signs behave in core seals?
coreS=[t for t in F.TRAIN if 'SEAL:S' in F.core_types[t]['types']]
for sg in ('091','055','031','220','001'):
    n=sum(sg in t for t in coreS);ini=sum(t[0]==sg for t in coreS)
    fn=sum(sg in t for t in FC);fi=sum(t[0]==sg for t in FC)
    out.setdefault('sign_positions',{})[sg]=dict(core_texts_with=n,core_initial=ini,core_total=len(coreS),FC_texts_with=fn,FC_initial=fi,FC_total=len(FC))
    print(sg,out['sign_positions'][sg])
(P/'critic_results.json').write_text(json.dumps(out,indent=2,default=list))
