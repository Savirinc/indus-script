"""Round 45 analysis (see PROTOCOL.md). Dravidian reference read from round43 split files."""
import json, statistics
from pathlib import Path
P = Path(__file__).resolve().parent


def summary(files):
    rs = [json.loads(f.read_text()) for f in files]
    n = len(rs[0]['null'])
    Tr = statistics.mean(r['real'] for r in rs)
    Tk = [statistics.mean(r['null'][k] for r in rs) for k in range(n)]
    pct = [sum(v < r['real'] for v in r['null']) / len(r['null']) for r in rs]
    return {'T_real': Tr, 'T_null_mean': statistics.mean(Tk), 'pooled_p': (1 + sum(t >= Tr for t in Tk)) / (n + 1),
            'mean_percentile': statistics.mean(pct), 'per_split_beaten': [round(p * n) for p in pct]}


out = {'PDR': summary([P.parent / 'round43' / f'split_indus_{i}.json' for i in range(10)]),
       'FIN': summary([P / f'split_FIN_{i}.json' for i in range(10)]),
       'EUS': summary([P / f'split_EUS_{i}.json' for i in range(10)])}
c = [out['FIN'], out['EUS']]
if any(x['pooled_p'] <= 0.15 for x in c): dec = 'ARTEFACT'
elif all(x['pooled_p'] > 0.30 for x in c) and all(out['PDR']['mean_percentile'] - x['mean_percentile'] >= 0.20 for x in c): dec = 'DRAVIDIAN-SPECIFIC'
else: dec = 'INCONCLUSIVE'
out['decision'] = dec
(P / 'results.json').write_text(json.dumps(out, indent=1))
for k in ('PDR', 'FIN', 'EUS'):
    o = out[k]; print(f"{k}: real {o['T_real']:.3f} null {o['T_null_mean']:.3f} pooled p {o['pooled_p']:.4f} mean pct {o['mean_percentile']:.3f} per split {o['per_split_beaten']}")
print('DECISION', dec)
