from cross_city import *
def masks(s):return [s[:i]+('*',)+s[i+1:] for i in range(len(s))]
def deletions(s):return [s[:i]+s[i+1:] for i in range(len(s))]
out=[]
for subset in ['all','SEAL:S']:
    for source in cities:
        target=next(c for c in cities if c!=source);train=sorted(collect(source,subset));alltest=sorted(set(collect(target,subset))-set(train))
        ts=set(train);tm={x for s in train for x in masks(s)};td={x for s in train for x in deletions(s)}
        test=[s for s in alltest if s not in td and not any(x in tm for x in masks(s)) and not any(x in ts for x in deletions(s))]
        actual,pred=evaluate(fit(train),test,True);groups=collections.defaultdict(list)
        for s in train:groups[len(s)].append(s)
        controls=[]
        for seed in range(200):
            rng=random.Random(f'round27positions:{subset}:{source}:{seed}');sh=[]
            for length,seqs in sorted(groups.items()):
                columns=[list(x) for x in zip(*seqs)]
                for col in columns:rng.shuffle(col)
                sh.extend(tuple(x) for x in zip(*columns))
            scores,_=evaluate(fit(sh),test);controls.append(scores)
        summary={}
        for k in actual:
            vals=[r[k]['bigram_bits_per_token'] for r in controls]
            summary[k]=dict(mean=sum(vals)/200,minimum=min(vals),maximum=max(vals),controls_at_least_as_good=sum(v<=actual[k]['bigram_bits_per_token'] for v in vals),controls=200)
        out.append(dict(subset=subset,source=source,target=target,near_duplicates_removed=len(alltest)-len(test),test_types=len(test),actual=actual,position_preserving_controls=summary,predictions=pred))
        print(subset,source,len(test),actual['internal'],summary['internal'],flush=True)
(P/'robustness.json').write_text(json.dumps(out,indent=2))
