import sys, json, random
sys.path.insert(0, '/Users/arhampartapjain/indus-script/indus-lab/round57')
import run57 as M
R = M.R
names = ['Kandahar', 'Qandahar', 'Gandhara', 'Jaya', 'Jayah']
for n in names: print(n, '->', M.name_skel(n))
key = json.load(open(M.LAB / 'round46-brahmi-coverage' / 'expanded-map.json'))
KB = dict(key); KB['435'] = 'o'; KB['436'] = 'o'
TRAIN, _, _ = R.load_corpus(); kept = [t for t in TRAIN if all(s in KB for s in t)]
signs = sorted({s for t in kept for s in t}); ks = {s: KB[s] for s in signs}; bins = R.freq_bins(kept, signs)
sk = lambda k: [M.merged_skel(R.read_c([k[s] for s in t])) for t in kept]
real = sk(ks)
uniq = sorted({M.name_skel(n) for n in names})
cnt = {u: sum(u in s for s in real) for u in uniq}
ge = {u: 0 for u in uniq}; tot = {u: 0 for u in uniq}
for sd in M.SEEDS:
    s2 = sk(R.shuffle_key(ks, bins, random.Random(sd)))
    for u in uniq:
        c = sum(u in s for s in s2); tot[u] += c; ge[u] += c >= cnt[u]
print('texts', len(kept))
for u in uniq: print(u, 'real', cnt[u], 'shuffle mean', round(tot[u] / 1000, 1), 'share of wrong keys with as many', ge[u] / 1000)
ex = [(t, R.read_c([ks[s] for s in t])) for t, s in zip(kept, real) if 'kntkr' in s][:5]
print(ex)
