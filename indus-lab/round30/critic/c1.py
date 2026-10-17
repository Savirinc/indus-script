import sys, json, random, statistics, collections, pickle, itertools
from pathlib import Path
LAB = Path(__file__).resolve().parent / 'lab'
sys.path.insert(0, str(LAB / 'round30'))
import foreign_context as F

cache = Path(__file__).resolve().parent / 'ctrl.pkl'
if cache.exists():
    ctrl_all = pickle.loads(cache.read_bytes())
else:
    ctrl_all = []
    for t in F.TRAIN:
        c = dict(key='C' + '-'.join(t), text=t, types=sorted(F.core_types[t]['types']), ids=sorted(F.core_types[t]['ids']))
        c.update(F.score(t)); ctrl_all.append(c)
    cache.write_bytes(pickle.dumps(ctrl_all))
ctrl_S = [c for c in ctrl_all if 'SEAL:S' in c['types']]
FC = [f for f in F.foreign if f['type'] == 'SEAL:C']
for f in FC: f.update(F.score(f['text'])); f['key'] = 'X' + f['id']

def T(items, ctrl, m='M1', n=5000, tag=''):
    r = F.test_group(items, ctrl, m, 'crit' + tag, nnull=n)
    return round(r['mean_percentile'], 3), r['p_one_sided'], r['n']

print('baseline', T(FC, ctrl_S))

# 1. neighbourhood brute force check
def ed1(a, b):
    if a == b: return True
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) == 1
    if abs(len(a) - len(b)) != 1: return False
    s, l = (a, b) if len(a) < len(b) else (b, a)
    return any(l[:i] + l[i+1:] == s for i in range(len(l)))
rng = random.Random(1)
bad = 0
for s in [f['text'] for f in FC] + [c['text'] for c in rng.sample(ctrl_S, 60)]:
    bf = {t for t in F.TRAIN if ed1(s, t)}
    if bf != F.neighbourhood(s): bad += 1; print('MISMATCH', s)
print('neighbourhood mismatches', bad)
print('FC neighbourhood sizes', [len(F.neighbourhood(f['text'])) for f in FC])
print('ctrl_S neighbourhood size dist', collections.Counter(min(len(F.neighbourhood(c['text'])), 5) for c in ctrl_S))

# 2a. length pools
print('FC lengths', [len(f['text']) for f in FC])
for L in range(2, 10): print(' ctrl_S len', L, sum(len(c['text']) == L for c in ctrl_S))
# exact-length pool only
def T_exact(items, ctrl, m='M1', n=5000):
    obs = []; pools = []
    for it in items:
        pool = [c for c in ctrl if len(c['text']) == len(it['text'])]
        pools.append(pool); obs.append(F.pct(it[m], pool, m))
    o = statistics.fmean(obs); rr = random.Random(2); null = []
    pc = {}
    for _ in range(n):
        v = []
        for i, p in enumerate(pools):
            c = rr.choice(p); k = (i, c['key'])
            if k not in pc: pc[k] = F.pct(c[m], p, m, self_id=c['key'])
            v.append(pc[k])
        null.append(statistics.fmean(v))
    return round(o, 3), (1 + sum(x >= o for x in null)) / (1 + n)
print('exact-length pools', T_exact(FC, ctrl_S))
# raw value check: percentile of M1 against ALL ctrl_S regardless of length
print('per text pct vs all lengths', [round(F.pct(f['M1'], ctrl_S, 'M1'), 3) for f in FC])
# M1 vs length in controls
for L in range(2, 10):
    v = [c['M1'] for c in ctrl_S if len(c['text']) == L]
    if v: print(' len', L, 'median M1 %.2f q90 %.2f' % (statistics.median(v), sorted(v)[int(.9 * len(v))]))

# 2b. alternative pools
for name, pool in [('all_types', ctrl_all), ('any_SEAL', [c for c in ctrl_all if any(t.startswith('SEAL') for t in c['types'])]),
                   ('SEAL_R', [c for c in ctrl_all if 'SEAL:R' in c['types']]),
                   ('non_seal', [c for c in ctrl_all if not any(t.startswith('SEAL') for t in c['types'])]),
                   ('SEAL_S_only_unique', [c for c in ctrl_S if len(F.neighbourhood(c['text'])) == 1])]:
    print('pool', name, len(pool), T(FC, pool, tag=name))

# 2c. leave-one-out
for i, f in enumerate(FC):
    print('LOO drop', f['id'], f['site'], T(FC[:i] + FC[i+1:], ctrl_S, tag='loo%d' % i))
# drop both Ur, drop Bahrain/Gulf, etc.
gulf = [f for f in FC if f['region'] == 'Persian Gulf']; nong = [f for f in FC if f['region'] != 'Persian Gulf']
print('Gulf only', T(gulf, ctrl_S), 'non-Gulf', T(nong, ctrl_S))
# drop the 3 texts with any UNK
print('no-UNK texts only', T([f for f in FC if f['unk'] == 0], ctrl_S))

# 2d. sign 091
def rescore(f, fn):
    g = dict(f); g['text'] = fn(f['text']); g.update(F.score(g['text'])); return g
FC_del = [rescore(f, lambda t: tuple(x for x in t if x != '091')) for f in FC]
FC_unk = [rescore(f, lambda t: tuple('UNKX' if x == '091' else x for x in t)) for f in FC]
print('091 deleted', T([f for f in FC_del if len(f['text']) >= 2], ctrl_S), [f['text'] for f in FC_del])
print('091 -> UNK', T(FC_unk, ctrl_S))
print('texts without 091 only', T([f for f in FC if '091' not in f['text']], ctrl_S))
# drop all UNK-producing signs from foreign texts
v = set(F.fit(F.TRAIN)[0])
FC_nounk = [rescore(f, lambda t: tuple(x for x in t if x in v)) for f in FC]
print('UNK signs deleted', T(FC_nounk, ctrl_S))

# 2e near duplicates
def lev(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j-1] + 1, p + (x != y))
    return d[-1]
for a, b in itertools.combinations(FC, 2):
    e = lev(a['text'], b['text'])
    if e <= len(a['text']) - 2 or e <= len(b['text']) - 2: print('FC pair', a['id'], b['id'], 'edit', e)
for f in FC:
    best = min(F.TRAIN, key=lambda t: lev(f['text'], t))
    print('nearest core', f['id'], '-'.join(f['text']), '->', '-'.join(best), lev(f['text'], best), 'ids', sorted(F.core_types[best]['ids'])[:3])
# also reversed direction nearest
for f in FC:
    r = f['text'][::-1]; best = min(F.TRAIN, key=lambda t: lev(r, t))
    print('nearest core (reversed)', f['id'], lev(r, best), '-'.join(best))
pickle.dump(dict(FC=FC), open(Path(__file__).resolve().parent / 'fc.pkl', 'wb'))
