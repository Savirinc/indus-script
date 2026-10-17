from pathlib import Path
import sys,json,collections,random,statistics,hashlib
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'round27'))
from cross_city import collect,fit,evaluate
splits=json.loads((P.parent/'round27/robustness.json').read_text())
results=[]
for spec in splits:
    source,subset=spec['source'],spec['subset'];original=sorted(collect(source,subset));test=[tuple(x['text']) for x in spec['predictions']]
    obs,_=evaluate(fit(original),test)
    by=collections.defaultdict(list)
    for i,s in enumerate(original):by[len(s)].append(i)
    eligible=[n for n,ids in by.items() if n>=2 and len(ids)>=2]
    totalcells=sum(map(len,original));rowbags=[collections.Counter(s) for s in original]
    cols={(n,j):collections.Counter(original[i][j] for i in ids) for n,ids in by.items() for j in range(n)}
    samples=[]
    for chain in range(10):
        rng=random.Random(f'round28:{subset}:{source}:{chain}');state=[list(s) for s in original];accepted=0
        for step in range(40000):
            n=rng.choice(eligible);i,k=rng.sample(by[n],2);j,l=rng.sample(range(n),2)
            a,b=state[i][j],state[i][l]
            if a!=b and state[k][j]==b and state[k][l]==a:
                state[i][j],state[i][l]=b,a;state[k][j],state[k][l]=a,b;accepted+=1
            if step+1>20000 and (step+1-20000)%2000==0:
                assert all(collections.Counter(s)==rowbags[i] for i,s in enumerate(state))
                assert all(collections.Counter(state[i][j] for i in ids)==cols[n,j] for n,ids in by.items() for j in range(n))
                scores,_=evaluate(fit([tuple(s) for s in state]),test)
                assert abs(scores['first']['bigram_bits_per_token']-obs['first']['bigram_bits_per_token'])<1e-10
                assert abs(scores['end']['bigram_bits_per_token']-obs['end']['bigram_bits_per_token'])<1e-10
                samples.append(dict(chain=chain,proposals=step+1,accepted=accepted,changed_cells=sum(a!=b for s,t in zip(state,original) for a,b in zip(s,t)),changed_rows=sum(tuple(s)!=t for s,t in zip(state,original)),internal_loss=scores['internal']['bigram_bits_per_token']))
    losses=[s['internal_loss'] for s in samples];o=obs['internal']['bigram_bits_per_token']
    item=dict(source=source,target=spec['target'],subset=subset,train_types=len(original),test_types=len(test),source_cells=totalcells,observed_loss=o,control_loss_mean=statistics.mean(losses),control_loss_min=min(losses),control_loss_max=max(losses),controls_at_least_as_good=sum(v<=o for v in losses),controls=len(losses),mean_changed_cell_fraction=statistics.mean(s['changed_cells']/totalcells for s in samples),mean_changed_row_fraction=statistics.mean(s['changed_rows']/len(original) for s in samples),accepted_moves_final_each_chain=[s['accepted'] for s in samples if s['proposals']==40000],samples=samples)
    results.append(item);print(json.dumps({k:v for k,v in item.items() if k!='samples'}),flush=True)
(P/'results.json').write_text(json.dumps(results,indent=2))
