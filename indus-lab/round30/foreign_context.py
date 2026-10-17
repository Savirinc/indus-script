"""Round 30: foreign-context inscription test. See PROTOCOL.md (fixed before scoring).
Standard library only. Run from the folder containing indus-lab."""
from pathlib import Path
import sys, csv, re, json, math, random, collections, statistics, hashlib
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round27')); sys.path.insert(0, str(P.parent / 'round29'))
from cross_city import fit, evaluate, src
import conditional_order as C29

rows = list(csv.DictReader(src.open()))
CORE = {'Inter-Riverine', 'Lower Indus', 'Gujarat/Kutch', 'Eastern Headwaters', 'Upper Indus'}
F_SITES_IRAN = {'Susa', 'Luristan', 'Tepe Yahya'}
F_SITES_CA = {'Altyn Depe', 'Gonur Depe'}


def clean(r):
    if r['dir.'] not in ('R/L', 'L/R') or not re.fullmatch(r'\+\d{3}(?:-\d{3})+\+', r['text']): return None
    s = tuple(r['text'][1:-1].split('-'))
    if '000' in s: return None
    return s[::-1] if r['dir.'] == 'R/L' else s


def group(r):
    if r['region'] in CORE: return 'core'
    if r['region'] in ('Mesopotamia', 'Persian Gulf') or r['site'] in F_SITES_IRAN or r['site'] in F_SITES_CA: return 'F'
    if r['site'] == 'Unknown' and r['type'] == 'SEAL:C': return 'U_C'
    return None


core_types = collections.defaultdict(lambda: {'ids': set(), 'types': set()})
foreign = []; unknown_c = []
for r in rows:
    g = group(r); s = clean(r)
    if g is None or s is None: continue
    if g == 'core':
        core_types[s]['ids'].add(r['id']); core_types[s]['types'].add(r['type'])
    else:
        rec = dict(id=r['id'], site=r['site'], region=r['region'], type=r['type'], dir=r['dir.'], text=s)
        (foreign if g == 'F' else unknown_c).append(rec)
TRAIN = sorted(core_types)

# one-edit neighbourhood index
mask_idx = collections.defaultdict(set); del_idx = collections.defaultdict(set)
for t in TRAIN:
    for i in range(len(t)):
        mask_idx[t[:i] + ('*',) + t[i + 1:]].add(t); del_idx[t[:i] + t[i + 1:]].add(t)
TRAIN_SET = set(TRAIN)


def neighbourhood(s):
    out = {s} & TRAIN_SET
    for i in range(len(s)):
        out |= mask_idx.get(s[:i] + ('*',) + s[i + 1:], set())   # substitution
        d = s[:i] + s[i + 1:]
        if d in TRAIN_SET: out.add(d)                               # s minus one sign
    out |= del_idx.get(s, set())                                    # s plus one sign
    return out


def score(s, extra_exclude=()):
    excl = neighbourhood(s)
    for e in extra_exclude: excl |= neighbourhood(e)
    model = fit([t for t in TRAIN if t not in excl])
    res, _ = evaluate(model, [s])
    m1 = res['all']['bigram_bits_per_token']; m2 = res['all']['unigram_bits_per_token']
    v = set(model[0]); sm = tuple(x if x in v else 'UNK' for x in s)
    m3 = None
    if len(sm) <= 9 and C29.n_perms(sm) >= 2:
        big = C29.make_big(model); Z, sc, _ = C29.make_dp(sm, None, big, 0, 1)
        m3 = (Z - sc(sm)) - math.log2(C29.n_perms(sm))
    unk = sum(x not in v for x in s) / len(s)
    return dict(M1=m1, M2=m2, M3=m3, unk=unk)


def pool_for(L, controls):
    for w in (0, 1, 2, 3, 5, 99):
        p = [c for c in controls if abs(len(c['text']) - L) <= w]
        if len(p) >= 30: return p, w
    return controls, 99


def pct(v, pool, metric, self_id=None):
    vals = [c[metric] for c in pool if c[metric] is not None and c['key'] != self_id]
    if not vals: return None
    return (sum(x < v for x in vals) + 0.5 * sum(x == v for x in vals)) / len(vals)


def test_group(items, controls, metric, seed, nnull=20000):
    items = [it for it in items if it[metric] is not None]
    if not items: return None
    pools = []; pcts = []
    for it in items:
        pool, w = pool_for(len(it['text']), [c for c in controls if c[metric] is not None])
        pools.append(pool); pcts.append(pct(it[metric], pool, metric))
    obs = statistics.fmean(pcts)
    # precompute percentiles of each control within each distinct pool
    cache = {}
    def cpct(i, c):
        k = (i, c['key'])
        if k not in cache: cache[k] = pct(c[metric], pools[i], metric, self_id=c['key'])
        return cache[k]
    rng = random.Random(seed); null = []
    for _ in range(nnull):
        null.append(statistics.fmean(cpct(i, rng.choice(pools[i])) for i in range(len(items))))
    p = (1 + sum(x >= obs for x in null)) / (1 + nnull)
    return dict(n=len(items), mean_percentile=obs, p_one_sided=p, null_mean=statistics.fmean(null),
                null_q99=sorted(null)[int(.99 * nnull)], per_text=[dict(id=it['id'], site=it['site'], len=len(it['text']), value=it[metric], percentile=q) for it, q in zip(items, pcts)], _null=null)


def main():
    out = dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(), train_types=len(TRAIN))
    print('train types', len(TRAIN), 'foreign', len(foreign), 'unknown SEAL:C', len(unknown_c), flush=True)
    for f in foreign + unknown_c: f.update(score(f['text'])); f['key'] = 'X' + f['id']
    ctrl_all = []
    for t in TRAIN:
        c = dict(key='C' + '-'.join(t), id=sorted(core_types[t]['ids'])[0], site='core', text=t, types=sorted(core_types[t]['types']))
        c.update(score(t)); ctrl_all.append(c)
    ctrl_S = [c for c in ctrl_all if 'SEAL:S' in c['types']]
    out['control_pools'] = dict(SEAL_S=len(ctrl_S), all=len(ctrl_all))
    FC = [f for f in foreign if f['type'] == 'SEAL:C']
    FS = [f for f in foreign if f['type'] in ('SEAL:S', 'TAG:L')]
    out['groups'] = {k: [dict(id=f['id'], site=f['site'], type=f['type'], text=f['text']) for f in v] for k, v in [('F', foreign), ('F_C', FC), ('F_S', FS), ('U_C', unknown_c)]}
    tests = {}
    for name, items, ctrl in [('P1_FC_M1', FC, ctrl_S), ('P2_FS_M1', FS, ctrl_S), ('P3_FC_M2', FC, ctrl_S), ('P3_FC_M3', FC, ctrl_S),
                              ('F_all_M1', foreign, ctrl_S), ('sens_FC_M1_allpool', FC, ctrl_all), ('expl_UC_M1', unknown_c, ctrl_S), ('expl_UC_M3', unknown_c, ctrl_S),
                              ('P2_FS_M3', FS, ctrl_S)]:
        metric = name.split('_')[2] if not name.startswith(('sens', 'expl')) else name.split('_')[2]
        r = test_group(items, ctrl, metric, f'round30:{name}')
        tests[name] = r
        if r: print(name, 'n', r['n'], 'mean pct %.3f' % r['mean_percentile'], 'p %.4f' % r['p_one_sided'], flush=True)
    # P1 decision
    p1 = tests['P1_FC_M1']
    out['P1_decision'] = 'SUPPORT' if p1['p_one_sided'] < 0.01 and p1['mean_percentile'] >= 0.70 else 'CONTRADICT' if p1['p_one_sided'] > 0.20 else 'INCONCLUSIVE'
    p2 = tests['P2_FS_M1']; out['P2_FS_anomalous_p<0.01'] = p2['p_one_sided'] < 0.01
    # power checks for P1
    null = p1['_null']; thr_null = sorted(null)
    lens = [len(f['text']) for f in FC]; rng = random.Random('round30:power')
    m = fit(TRAIN); u = m[0]; signs = [x for x in u if x not in ('EOS', 'UNK')]; w = [u[x] for x in signs]
    pools = [pool_for(L, ctrl_S)[0] for L in lens]
    power = {}
    for kind in ('pseudo_writing', 'order_shuffle'):
        hits = 0
        for sim in range(200):
            pc = []
            for L, pool in zip(lens, pools):
                base = rng.choice([c for c in pool if len(c['text']) == L] or pool)['text']
                if kind == 'pseudo_writing': new = tuple(rng.choices(signs, weights=w, k=len(base)))
                else:
                    t = list(base); rng.shuffle(t); new = tuple(t)
                sc = score(new, extra_exclude=(base,)); pc.append(pct(sc['M1'], pool, 'M1'))
            mp = statistics.fmean(pc); pv = (1 + sum(x >= mp for x in null)) / (1 + len(null))
            hits += (pv < 0.01 and mp >= 0.70)
        power[kind] = hits / 200; print('power', kind, power[kind], flush=True)
    out['power_P1'] = power
    for k, r in tests.items():
        if r: r.pop('_null')
    out['tests'] = tests
    out['foreign_scores'] = [{k: (v if k != 'text' else '-'.join(v)) for k, v in f.items()} for f in foreign + unknown_c]
    (P / 'results.json').write_text(json.dumps(out, indent=2))
    print('P1:', out['P1_decision'], '| P2 FS anomalous:', out['P2_FS_anomalous_p<0.01'])


if __name__ == '__main__':
    main()
