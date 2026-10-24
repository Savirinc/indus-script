"""Round 59: traded-goods vocabulary in Yajnadevam-key readings (Sanskrit, Proto-Dravidian). See PROTOCOL.md (locked first).
Stdlib only. Run from this folder: python3 -I run59.py   (needs ../../ext/lexicons and ../../ext/neurodecipher as for round 47)"""
import sys, json, random, re, statistics, collections
from pathlib import Path
P = Path(__file__).resolve().parent; LAB = P.parent
sys.path.insert(0, str(LAB / 'round47')); sys.path.insert(0, str(LAB / 'round57'))
import run47 as R
import run57 as M          # collapse, merged_skel, name_skel, skels, scramble, T, stats (round 57, unchanged)
SEEDS = range(59201, 59201 + 1000)

def lex(fn): return [l.split('\t')[0] for l in (P / fn).open(encoding='utf-8') if l.strip() and not l.startswith('#')]
def by_len(sk):
    d = collections.defaultdict(list)
    for s in sk: d[len(s)].append(s)
    return d

def decoy_pool(com, pool, seed):
    rng = random.Random(seed); cset = set(com); pl = by_len([s for s in M.skels(pool) if s not in cset]); out = []
    for L, xs in by_len(com).items():
        out += rng.sample(pl[L], min(len(xs), len(pl[L])))
    return out

def shuffle_T(texts, key, bins, proc, gaz, seeds):
    return [M.T([M.merged_skel(proc([k2[s] for s in t])) for t in texts], gaz)[0]
            for k2 in (R.shuffle_key(key, bins, random.Random(sd)) for sd in seeds)]

def main():
    LOG = (P / 'run59.log').open('w', encoding='utf-8')
    def log(*a): print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()
    out = dict(protocol='PROTOCOL.md', n_shuffles=len(SEEDS))
    key = json.load(open(LAB / 'round46-brahmi-coverage' / 'expanded-map.json'))
    TRAIN, _, _ = R.load_corpus(); kept = [t for t in TRAIN if all(s in key for s in t)]
    signs = sorted({s for t in kept for s in t}); ksub = {s: key[s] for s in signs}; bins = R.freq_bins(kept, signs)
    out['corpus'] = dict(texts=len(kept), tokens=sum(len(t) for t in kept), signs=len(signs)); log('corpus', out['corpus'])

    # ---------- positive control: Linear B commodity words ----------
    words, greek = R.lb_data(); n = len(words); rs = random.Random(47301); idx = list(range(n)); rs.shuffle(idx)
    halfB = idx[n // 2:]; density = out['corpus']['tokens'] / len(signs)
    target = round(sum(len(words[i]) for i in halfB) / density)
    lt, truth = R.lb_build(words, halfB, target, True); lbins = R.freq_bins(lt, sorted(truth))
    rows = [int(l.split('\t')[0]) for l in (P / 'lb_commodity_rows.tsv').open(encoding='utf-8') if l.strip() and not l.startswith('#')]
    lbw = [''.join(R.lb_value(s) for s in words[i]) for i in rows]
    glb = M.skels(lbw); ident = lambda labs: ''.join(labs)
    lsk = [M.merged_skel(ident([truth[s] for s in t])) for t in lt]
    Treal, hits = M.T(lsk, glb); st = M.stats(Treal, shuffle_T(lt, truth, lbins, ident, glb, SEEDS))
    scr = [M.T(lsk, M.scramble(glb, 59501 + i))[0] / len(glb) for i in range(20)]
    rate = Treal / len(glb); scr95 = sorted(scr)[18]
    passed = Treal >= 5 and st['pct'] >= 0.99 and st['z'] >= 3 and rate > scr95
    out['positive_control'] = dict(skeletons=len(glb), T=Treal, stats=st, rate=rate, scrambled_95=scr95, matched=dict(hits), passed=passed)
    log('PC Linear B commodities:', 'PASS' if passed else 'FAIL', out['positive_control'])

    # ---------- Indus ----------
    sk = [M.merged_skel(R.read_c([ksub[s] for s in t])) for t in kept]
    out['lexicons'] = {}
    for name, cf, pf in (('Sanskrit', 'lex_skt_commodity.tsv', 'pool_skt_other.tsv'), ('Proto-Dravidian', 'lex_pdr_commodity.tsv', 'pool_pdr_other.tsv')):
        raw = lex(cf); com = M.skels(raw); gloss = collections.defaultdict(list)
        for w, l in zip(raw, [l.rstrip('\n').split('\t')[1] for l in (P / cf).open(encoding='utf-8') if l.strip() and not l.startswith('#')]):
            s = M.name_skel(w)
            if len(gloss[s]) < 3: gloss[s].append(f'{w} ({l[:40]})')
        Treal, hits = M.T(sk, com); shuf = shuffle_T(kept, ksub, bins, R.read_c, com, SEEDS); st = M.stats(Treal, shuf)
        rate = Treal / len(com)
        a = [M.T(sk, M.scramble(com, 59501 + i))[0] / len(com) for i in range(20)]
        pool = lex(pf); b = []
        for i in range(20):
            d = decoy_pool(com, pool, 59601 + i); b.append(M.T(sk, d)[0] / len(d))
        a95, b95 = sorted(a)[18], sorted(b)[18]
        res = dict(skeletons=len(com), T=Treal, stats=st, rate=rate, scrambled_mean=statistics.mean(a), scrambled_95=a95,
                   ordinary_mean=statistics.mean(b), ordinary_95=b95)
        robust = None
        if st['pct'] >= 0.99 and 2.5 <= st['z'] <= 3.5:
            zs = [M.stats(Treal, shuffle_T(kept, ksub, bins, R.read_c, com, range(61001 + j * 1000, 62001 + j * 1000)))['z'] for j in range(10)]
            robust = sum(z >= 3 for z in zs); res['replicate_z'] = zs
        if not passed: v = 'VOID (control failed)'
        elif st['pct'] >= 0.99 and st['z'] >= 3 and rate > a95 and rate > b95 and (robust is None or robust >= 8): v = 'SUPPORT'
        elif st['pct'] >= 0.99 and st['z'] >= 3 and rate > a95 and rate <= b95: v = 'WORDS, NOT GOODS'
        elif st['pct'] >= 0.95 and rate <= a95: v = 'ARTEFACT'
        elif st['pct'] < 0.95: v = 'NULL'
        else: v = 'MIXED'
        res['verdict'] = v
        res['top'] = [dict(skeleton=s, texts=c, words=gloss.get(s, [])) for s, c in hits.most_common(25)]
        out['lexicons'][name] = res
        log(f'{name}: skeletons {len(com)} T {Treal} null {st["null_mean"]} ({st["null_sd"]}) z {st["z"]} pct {st["pct"]:.3f} '
            f'rate {rate:.3f} scrambled95 {a95:.3f} ordinary95 {b95:.3f} -> {v}')
        log('  top:', [(s, c) for s, c in hits.most_common(10)])
    json.dump(out, (P / 'results.json').open('w', encoding='utf-8'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
