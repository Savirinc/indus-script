import sys, json, random, re, unicodedata, collections
sys.path.insert(0, '/Users/arhampartapjain/indus-script/indus-lab/round47'); import run47 as R
def nm(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('dzh', 'j').replace('zh', 'j'); s = re.sub(r'[^a-z]', '', s)
    s = re.sub(r'([kgcjtdpb])h', r'\1', s)
    return re.sub(r'h$', '', s)
G = set()
for l in open(sys.argv[1], encoding='utf-8'):
    f = l.split('\t')
    for n in [f[1], f[2]] + f[3].split(','):
        if n: G.add(nm(n))
print('Afghan place-name forms:', len(G), '| jaya in gazetteer:', 'jaya' in G)
key = json.load(open('/Users/arhampartapjain/indus-script/indus-lab/round46-brahmi-coverage/expanded-map.json'))
TRAIN, _, _ = R.load_corpus(); kept = [t for t in TRAIN if all(s in key for s in t)]
signs = sorted({s for t in kept for s in t}); ks = {s: key[s] for s in signs}; bins = R.freq_bins(kept, signs)
rd = lambda k, t: nm(R.read_v([k[s] for s in t]))
# every 2-sign text type: share whose reading is an Afghan place name
two = [t for t in kept if len(t) == 2]
real = sum(rd(ks, t) in G for t in two) / len(two)
sh = []
for sd in range(57201, 57401):
    k2 = R.shuffle_key(ks, bins, random.Random(sd)); sh.append(sum(rd(k2, t) in G for t in two) / len(two))
print(f'2-sign texts: {len(two)}; share reading as an Afghan place name: atlas key {real:.1%}; 200 wrong keys mean {sum(sh)/len(sh):.1%} (min {min(sh):.1%}, max {max(sh):.1%})')
# the jaya pair under wrong keys
pair = ('003', '156'); hits = []
for sd in range(57201, 58201):
    k2 = R.shuffle_key(ks, bins, random.Random(sd)); r = rd(k2, pair); hits.append((r, r in G))
print('pair 003-156 under atlas key:', rd(ks, pair), '| wrong keys whose reading is also an Afghan place:', sum(h for _, h in hits), 'of 1000')
print('examples:', [r for r, h in hits if h][:15])
