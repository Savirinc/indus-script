import sys, json, random, statistics, collections, pickle, itertools
from pathlib import Path
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H / 'lab' / 'round30'))
import foreign_context as F
ctrl_all = pickle.loads((H / 'ctrl.pkl').read_bytes())
ctrl_S = [c for c in ctrl_all if 'SEAL:S' in c['types']]
FC = pickle.load(open(H / 'fc.pkl', 'rb'))['FC']
def T(items, ctrl, m='M1', n=5000, tag=''):
    r = F.test_group(items, ctrl, m, 'crit' + tag, nnull=n)
    return round(r['mean_percentile'], 3), r['p_one_sided'], r['n']

# per-control leave-self-out percentile within its length pool
def selfpct(c, m='M1'):
    pool, _ = F.pool_for(len(c['text']), [x for x in ctrl_S if x[m] is not None])
    return F.pct(c[m], pool, m, self_id=c['key'])
for c in ctrl_S: c['sp'] = selfpct(c)
byid = {}
for r in F.rows: byid[r['id']] = r
def attr(c, k): return collections.Counter(byid[i][k] for i in c['ids'])

def subgroup(name, pred):
    g = [c for c in ctrl_S if pred(c)]
    if len(g) < 5: print(name, 'n', len(g)); return
    sp = [c['sp'] for c in g]
    rr = random.Random(name); draws = [statistics.fmean(rr.sample(sp, 8)) for _ in range(5000)] if len(sp) >= 8 else []
    print('%-30s n=%4d mean selfpct %.3f  P(mean of 8 >= 0.916)=%s' % (name, len(g), statistics.fmean(sp), (sum(d >= .916 for d in draws) / len(draws)) if draws else '-'))

# preservation / condition confound
print('conditions core SEAL:S rows', collections.Counter(byid[i]['condition'] for c in ctrl_S for i in c['ids']).most_common(8))
for cond in ('Good', 'Fair', 'Poor'):
    subgroup('all rows condition=' + cond, lambda c, cond=cond: set(attr(c, 'condition')) == {cond})
subgroup('complete=Y only', lambda c: set(attr(c, 'complete')) == {'Y'})
subgroup('any row L/R', lambda c: 'L/R' in attr(c, 'dir.'))
# sites
for s in ['Mohenjo-daro', 'Harappa', 'Dholavira', 'Lothal', 'Chanhu-daro', 'Kalibangan', 'Banawali']:
    subgroup('site=' + s, lambda c, s=s: set(attr(c, 'site')) == {s})
subgroup('peripheral (not H/MD)', lambda c: not (set(attr(c, 'site')) & {'Mohenjo-daro', 'Harappa'}))
subgroup('single-site small (<20 seals)', lambda c: all(byid[i]['site'] not in ('Mohenjo-daro','Harappa','Dholavira','Lothal','Chanhu-daro','Kalibangan') for i in c['ids']))
# novelty-matched: controls whose nearest other core type is >=k edits
def lev(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j-1] + 1, p + (x != y))
    return d[-1]
for c in ctrl_S:
    c['nn'] = min(lev(c['text'], t) for t in F.TRAIN if t != c['text'])
print('FC nearest-core distances', [min(lev(f['text'], t) for t in F.TRAIN) for f in FC])
for k in (2, 3):
    subgroup('controls nn>=%d' % k, lambda c, k=k: c['nn'] >= k)
    print('  FC vs pool nn>=%d' % k, T(FC, [c for c in ctrl_S if c['nn'] >= k], tag='nn%d' % k))
# relative-distance matched: nn/len >= 0.5
subgroup('controls nn/len>=0.5', lambda c: c['nn'] / len(c['text']) >= .5)
print('  FC vs pool nn/len>=0.5', T(FC, [c for c in ctrl_S if c['nn'] / len(c['text']) >= .5], tag='rel'))
# poor-condition pool
poor = [c for c in ctrl_S if 'Poor' in attr(c, 'condition')]
print('FC vs poor-condition pool', len(poor), T(FC, poor, tag='poor'))

# direction: reverse the two L/R foreign seals; and reverse all FC
def rescore(f, t):
    g = dict(f); g['text'] = t; g.update(F.score(t)); return g
FC_dir = [rescore(f, f['text'][::-1]) if f['dir'] == 'L/R' else f for f in FC]
print('L/R ones reversed', T(FC_dir, ctrl_S), [(f['id'], round(f['M1'], 2)) for f in FC_dir if f['dir'] == 'L/R'])
FC_rev = [rescore(f, f['text'][::-1]) for f in FC]
print('all FC reversed', T(FC_rev, ctrl_S))
FC_best = [min(a, b, key=lambda x: x['M1']) for a, b in zip(FC, FC_rev)]
# fair version: give controls best-of-two-directions too
ctrl_best = []
for c in ctrl_S:
    r = F.score(c['text'][::-1]); d = dict(c)
    if r['M1'] < c['M1']: d.update(M1=r['M1'])
    ctrl_best.append(d)
print('best-of-direction (both sides)', T(FC_best, ctrl_best, tag='best'))
# other non-core groups: unknown-provenance SEAL:S complete clean texts
unkS = []
for r in F.rows:
    if r['site'] == 'Unknown' and r['type'] == 'SEAL:S':
        s = F.clean(r)
        if s: d = dict(id=r['id'], site='Unknown', text=s, key='X' + r['id']); d.update(F.score(s)); unkS.append(d)
print('Unknown-provenance SEAL:S', T(unkS, ctrl_S, tag='unkS'))
# M3 for FC with UNK signs: check UNK handling in M3
print('FC M3 per text', [(f['id'], round(f['M3'], 2), f['unk']) for f in FC])
