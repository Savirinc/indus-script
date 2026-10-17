import json,random,sys
import name_match as M
lens=[len(v) for v in M.SEALS.values()];nsign=len({x for v in M.SEALS.values() for x in v})
rng=random.Random(35500);hits=0;rows=[]
for r in range(int(sys.argv[1])):
    syn=M.synthetic(rng,lens,nsign);t=M.test(syn,nfake=int(sys.argv[2]),seed=36000+r*1000)
    hits+=t['p']<0.05;rows.append(dict(S_real=t['S_real'],fake_mean=t['fake_mean'],p=t['p']));print(r,rows[-1],flush=True)
json.dump(dict(replicates=len(rows),nfake=int(sys.argv[2]),power=hits/len(rows),rows=rows),open('power_results.json','w'),indent=1)
print('POWER',hits/len(rows))
