"""Round 57: Bhaty 2024 place-name claim. See PROTOCOL.md (committed first, 0766692). Stdlib only.
Usage: python3 run57.py   (from this folder; needs ../../ext/lexicons and ../../ext/neurodecipher as for round 47)"""
import json, random, re, sys, unicodedata, collections
from pathlib import Path
P = Path(__file__).resolve().parent; LAB = P.parent
sys.path.insert(0, str(LAB / 'round47')); import run47 as R
NSHUF = 1000; SEEDS = range(57201, 57201 + NSHUF)

# ---------- collapse and skeletons (protocol, matching rule) ----------
SUB = {'š': 's', 'ś': 's', 'ṣ': 's', 'z': 's', 'x': 's', 'ŋ': 'g', 'ḫ': 'k', 'h': 'k', 'ṭ': 't', 'θ': 't',
       'f': 'p', 'w': 'v', 'q': 'k', 'y': 'j'}
MERGE = {'g': 'k', 'd': 't', 'b': 'p', 'j': 'c', 'l': 'r'}
def collapse(s):
    s = s.lower()
    s = ''.join(SUB.get(c, c) for c in s)                      # before stripping, so š ḫ ŋ are caught
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    s = ''.join(SUB.get(c, c) for c in s)
    return re.sub(r'[^a-z]', '', s)
def merged_skel(s):
    s = re.sub(r'[aeiou]', '', s)
    s = ''.join(MERGE.get(c, c) for c in s)
    return re.sub(r'(.)\1+', r'\1', s)
def name_skel(n): return merged_skel(collapse(n))

# ---------- gazetteers ----------
def g_epsd():
    out = []
    for l in open(LAB / 'round51' / 'epsd2_lemmas.tsv', encoding='utf-8'):
        f = l.rstrip('\n').split('\t')
        if len(f) >= 3 and f[2] in ('GN', 'SN'): out.append(f[0])
    return out
def g_bhaty(): return [l.split('\t')[0] for l in open(P / 'bhaty_places.tsv', encoding='utf-8') if l.strip() and not l.startswith('#')]
def g_fin(): return [w for l in open(P / 'finnish_places.txt', encoding='utf-8') if not l.startswith('#') for w in l.split()]
def g_lb(): return [l.split('\t')[0].replace('-', '') for l in open(P / 'linearb_places.tsv', encoding='utf-8') if l.strip() and not l.startswith('#')]
def skels(names, k=3): return sorted({s for s in map(name_skel, names) if len(s) >= k})
def skels2(names): return sorted({s for s in map(name_skel, names) if len(s) == 2})
def scramble(sk, seed):
    rng = random.Random(seed); out = []
    for s in sk:
        c = list(s)
        for _ in range(21):
            rng.shuffle(c); t = re.sub(r'(.)\1+', r'\1', ''.join(c))
            if t != s: break
        out.append(t)
    return out          # keep duplicates out of the count only if identical strings
def T(text_skels, gaz):
    g = set(gaz); n = 0; hits = collections.Counter()
    for ts in text_skels:
        found = {ts[i:j] for i in range(len(ts)) for j in range(i + 2, len(ts) + 1) if ts[i:j] in g}
        n += len(found); hits.update(found)
    return n, hits
def stats(real, shuf):
    mu = sum(shuf) / len(shuf); sd = (sum((x - mu) ** 2 for x in shuf) / (len(shuf) - 1)) ** 0.5
    return dict(T=real, null_mean=round(mu, 2), null_sd=round(sd, 2), z=round((real - mu) / sd, 2) if sd else 0.0,
                pct=sum(x < real for x in shuf) / len(shuf), p_upper=(1 + sum(x >= real for x in shuf)) / (len(shuf) + 1))

def run_gaz(texts, key, bins, proc, gazes):
    sk = [merged_skel(proc([key[s] for s in t])) for t in texts]
    real = {g: T(sk, v) for g, v in gazes.items()}
    shuf = {g: [] for g in gazes}; anyhits = {g: collections.Counter() for g in gazes}
    for sd in SEEDS:
        k2 = R.shuffle_key(key, bins, random.Random(sd)); s2 = [merged_skel(proc([k2[s] for s in t])) for t in texts]
        for g, v in gazes.items():
            n, h = T(s2, v); shuf[g].append(n)
            for name in real[g][1]:
                if h[name] >= real[g][1][name]: anyhits[g][name] += 1
    return {g: stats(real[g][0], shuf[g]) for g in gazes}, real, anyhits

def main():
    out = dict(protocol='PROTOCOL.md (0766692)', n_shuffles=NSHUF)
    key = json.load(open(LAB / 'round46-brahmi-coverage' / 'expanded-map.json'))
    KB = dict(key); KB['435'] = 'o'; KB['436'] = 'o'
    TRAIN, types, _ = R.load_corpus(); kept = [t for t in TRAIN if all(s in KB for s in t)]
    signs = sorted({s for t in kept for s in t}); ksub = {s: KB[s] for s in signs}; bins = R.freq_bins(kept, signs)
    out['corpus'] = dict(types=len(kept), tokens=sum(len(t) for t in kept), signs=len(signs))
    R.log('corpus', out['corpus'])

    # ---- gazetteers ----
    ba_names = g_epsd() + g_bhaty()
    G = dict(BA=skels(ba_names), FIN=skels(g_fin()))
    G['SCR'] = scramble(G['BA'], 57501)
    out['gazetteers'] = {k: len(v) for k, v in G.items()}
    out['gazetteers']['BA_names_raw'] = len(ba_names); out['gazetteers']['SCR_identical_to_BA'] = sum(a == b for a, b in zip(G['BA'], G['SCR']))
    G2 = dict(BA2=skels2(ba_names))
    R.log('gazetteers', out['gazetteers'])

    # ---- positive control: Linear B PC2 geometry ----
    words, greek = R.lb_data(); n = len(words); rs = random.Random(47301); idx = list(range(n)); rs.shuffle(idx)
    halfB = idx[n // 2:]; density = out['corpus']['tokens'] / len(signs)
    target = round(sum(len(words[i]) for i in halfB) / density)
    lt, truth = R.lb_build(words, halfB, target, True); lbins = R.freq_bins(lt, sorted(truth))
    glb = skels(g_lb()); GLB = dict(LB=glb, LBSCR=scramble(glb, 57502))
    pc, pcreal, _ = run_gaz(lt, truth, lbins, lambda labs: ''.join(labs), GLB)
    passed = (pcreal['LB'][0] >= 10 and pc['LB']['pct'] >= 0.99 and pc['LB']['z'] >= 3 and pc['LBSCR']['pct'] < 0.95)
    out['positive_control'] = dict(texts=len(lt), sign_ids=len(truth), gazetteer=len(glb), scores=pc,
                                   matched=dict(pcreal['LB'][1].most_common(15)), passed=passed)
    R.log('PC', 'PASS' if passed else 'FAIL', pc)

    # ---- Indus ----
    res, real, anyh = run_gaz(kept, ksub, bins, R.read_c, {**G, **G2})
    out['indus'] = res
    per = {g: res[g]['T'] / max(1, len(G[g])) for g in ('BA', 'SCR', 'FIN')}; out['per_name_rate'] = per
    out['top_BA_matches'] = dict(real['BA'][1].most_common(25))
    bh = {name_skel(n): n for n in g_bhaty() if len(name_skel(n)) >= 2}
    allbh = {**{s: real['BA'][1].get(s, 0) for s in bh if len(s) >= 3}, **{s: real['BA2'][1].get(s, 0) for s in bh if len(s) == 2}}
    out['bhaty_names'] = {bh[s]: dict(skeleton=s, texts_matched=c,
                                      share_shuffles_as_many=(anyh['BA'][s] if len(s) >= 3 else anyh['BA2'][s]) / NSHUF if c else None)
                          for s, c in allbh.items()}
    # Moka cluster
    clus = sum(any(tuple(t[i:i + 3]) in (('255', '435', '690'), ('255', '436', '690')) for i in range(len(t) - 2)) for t in kept)
    mk_real = sum('mk' in merged_skel(R.read_c([ksub[s] for s in t])) for t in kept)
    mk_shuf = []
    for sd in SEEDS:
        k2 = R.shuffle_key(ksub, bins, random.Random(sd)); mk_shuf.append(sum('mk' in merged_skel(R.read_c([k2[s] for s in t])) for t in kept))
    out['moka'] = dict(cluster_texts=clus, texts_with_mk=mk_real, mk_null=stats(mk_real, mk_shuf))
    R.log('indus', res); R.log('moka', out['moka'])

    if not passed: v = 'METHOD-FAIL'
    else:
        b, s, f = res['BA'], res['SCR'], res['FIN']
        if b['pct'] >= 0.99 and b['z'] >= 3 and s['pct'] < 0.95 and f['pct'] < 0.95 and per['BA'] > per['SCR']: v = 'SUPPORT'
        elif b['pct'] >= 0.95 and (s['pct'] >= 0.95 or f['pct'] >= 0.95 or per['BA'] <= per['SCR']): v = 'ARTEFACT'
        elif b['pct'] < 0.95: v = 'NULL'
        else: v = 'MIXED'
    out['verdict'] = v; R.log('VERDICT', v)
    json.dump(out, open(P / 'results.json', 'w'), indent=1, ensure_ascii=False)

    # ---- secondary: round 47 LM test on K_B ----
    R.log('secondary LM test'); LX = R.load_lexicons(); size = min(len(v) for v in LX.values())
    lms = {L: [R.LM(random.Random(47101 + d).sample(v, size)) if size < len(v) else R.LM(v) for d in range(R.NDRAW)] for L, v in LX.items()}
    VOWB = re.compile(r'^[aiuo]$')
    def read_vb(labels):
        s = labels[0]
        for nxt in labels[1:]:
            if not R.END.search(s) and not VOWB.match(nxt): s += 'a'
            s += nxt
        if not R.END.search(s): s += 'a'
        return s
    rl, sh = R.null_scores(kept, ksub, bins, lms, read_vb, SEEDS)
    out['lm_test'] = R.summarize(rl, sh)
    R.log('LM', {L: (round(x['z'], 2), x['percentile']) for L, x in out['lm_test'].items()})
    json.dump(out, open(P / 'results.json', 'w'), indent=1, ensure_ascii=False)
if __name__ == '__main__': main()
