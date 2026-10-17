"""Round 43 analysis: pooled permutation test across 10 fresh splits (see PROTOCOL.md)."""
import json, statistics
from pathlib import Path
P = Path(__file__).resolve().parent


def load(mode):
    return [json.loads((P / f'split_{mode}_{i}.json').read_text()) for i in range(10)]


def pooled(rs):
    n = len(rs[0]['null'])
    Tr = statistics.mean(r['real'] for r in rs)
    Tk = [statistics.mean(r['null'][k] for r in rs) for k in range(n)]
    return Tr, Tk, (1 + sum(t >= Tr for t in Tk)) / (n + 1)


out = {}
for mode in ('lb', 'indus'):
    rs = load(mode); Tr, Tk, p = pooled(rs)
    per = [{'split': r['split'], 'test': r['test'], 'real': r['real'], 'null_median': statistics.median(r['null']),
            'beaten': sum(v < r['real'] for v in r['null']), 'n': len(r['null']),
            'p': (1 + sum(v >= r['real'] for v in r['null'])) / (1 + len(r['null']))} for r in rs]
    out[mode] = {'T_real': Tr, 'T_null_mean': statistics.mean(Tk), 'T_null_max': max(Tk), 'pooled_p': p,
                 'above_median': sum(x['real'] > x['null_median'] for x in per),
                 'splits_p_le_05': sum(x['p'] <= 0.05 for x in per), 'per_split': per}
lb, ind = out['lb'], out['indus']
gate = lb['pooled_p'] <= 1 / 21 + 1e-12
if not gate: dec = 'UNINFORMATIVE (control failed)'
elif ind['pooled_p'] <= 0.05 and ind['above_median'] >= 8: dec = 'REPLICATED'
elif ind['pooled_p'] <= 0.15: dec = 'SUGGESTIVE'
else: dec = 'NOT REPLICATED'
out['decision'] = dec
(P / 'results.json').write_text(json.dumps(out, indent=1))
for m in ('lb', 'indus'):
    o = out[m]
    print(f"{m}: T_real {o['T_real']:.3f} null mean {o['T_null_mean']:.3f} max {o['T_null_max']:.3f} pooled p {o['pooled_p']:.4f} "
          f"above-median {o['above_median']}/10 splits p<=.05 {o['splits_p_le_05']}/10")
    for x in o['per_split']: print(f"   split {x['split']}: test {x['test']} real {x['real']:.3f} median {x['null_median']:.3f} beats {x['beaten']}/{x['n']} p {x['p']:.3f}")
print('DECISION', dec)
