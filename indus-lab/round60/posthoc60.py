"""Round 60 POST-HOC, DESCRIPTIVE ONLY (written after the verdict; does not change it).
How unusual is the atlas key's order gain among more wrong keys? 100 further scrambled keys, seeds 47001-47100."""
import json, random, statistics, sys
from pathlib import Path
P = Path(__file__).resolve().parent; sys.path.insert(0, str(P))
import run60 as M
A, R = M.A, M.R
recs = [c for c in A.CAND if A.signs_of(c)]
for c in recs: c['signs'] = A.signs_of(c)
alltexts = [[s for s in c['signs'] if s in A.KEY] for c in recs]
signs = sorted({s for t in alltexts for s in t}); bins = R.freq_bins(alltexts, signs); base = {s: A.KEY[s] for s in signs}
seen, texts = set(), []
for c in recs:
    t = tuple(c['signs'])
    if len(t) >= 3 and all(s in A.KEY for s in t) and t not in seen: seen.add(t); texts.append(list(t))
iperm = M.perms_for(texts, 60101)
atlas = json.load(open(P / 'results.json'))['atlas']['G']
G = []
for sd in range(47001, 47101):
    G.append(M.arm(texts, M.key_score(R.shuffle_key(base, bins, random.Random(sd))), iperm)[0]['G'])
pre = [v['G'] for v in json.load(open(P / 'results.json'))['scrambled'].values()]
allG = pre + G
out = dict(atlas_G=atlas, extra_keys=100, extra_at_or_above=sum(g >= atlas for g in G), all120_at_or_above=sum(g >= atlas for g in allG),
           all120_mean=statistics.mean(allG), all120_sd=statistics.stdev(allG), atlas_z_among_keys=(atlas - statistics.mean(allG)) / statistics.stdev(allG),
           all120_max=max(allG), extra_G=G)
json.dump(out, open(P / 'posthoc60.json', 'w'), indent=1)
print({k: v for k, v in out.items() if k != 'extra_G'})
