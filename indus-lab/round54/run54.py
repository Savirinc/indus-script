"""Round 54: free-combination test for a syllabic core. See PROTOCOL.md (committed before this file).
Standard library only. Run from this folder: python3 run54.py"""
import sys, json, math, random, collections, time
from pathlib import Path
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round52')); sys.path.insert(0, str(P.parent / 'round30'))
import run52 as R52
import foreign_context as FC

SEED = 54001; B = 50; PERMS = 30; MINF = 10
CORPORA = ['OBL', 'OAL', 'SEAL', 'SUX', 'EGY', 'OBI', 'CHN']
GOLD = {'OBL', 'OAL', 'SEAL'}

def log(*a):
    print(*a, flush=True); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def load(code):
    for d in (P / 'controls', P.parent / 'round52b' / 'controls', P.parent / 'round52' / 'controls'):
        f = d / f'{code}.txt'
        if f.exists():
            units = []; flags = collections.defaultdict(collections.Counter)
            for l in f.open(encoding='utf-8'):
                if not l.strip(): continue
                toks = []
                for t in l.split():
                    if code in GOLD and t[-2] == '/': s, fl = t[:-2], t[-1]; flags[s][fl] += 1
                    else: s = t
                    toks.append(s)
                units.append(toks)
            return units, flags
    raise SystemExit(code)

def neighbours(texts):
    R = collections.defaultdict(set); L = collections.defaultdict(set)
    for t in texts:
        for a, b in zip(t, t[1:]): R[a].add(b); L[b].add(a)
    return R, L

def freedom(texts, rng):
    cnt = collections.Counter(s for t in texts for s in t)
    keep = {s for s, c in cnt.items() if c >= MINF}
    R, L = neighbours(texts)
    obs = {s: len(R[s]) + len(L[s]) for s in keep}
    exp = collections.Counter()
    for _ in range(PERMS):
        sh = [t[:] for t in texts]
        for t in sh: rng.shuffle(t)
        R2, L2 = neighbours(sh)
        for s in keep: exp[s] += len(R2[s]) + len(L2[s])
    F = {s: obs[s] / (exp[s] / PERMS) if exp[s] else 0 for s in keep}
    return F, cnt

def auc(pos, neg):
    if not pos or not neg: return float('nan')
    wins = sum(1 if p > n else 0.5 if p == n else 0 for p in pos for n in neg)
    return wins / (len(pos) * len(neg))

def labels(flags, keep):
    lab = {}
    for s in keep:
        c = flags.get(s); 
        if not c: continue
        tot = sum(c.values())
        if c['p'] / tot >= 0.7: lab[s] = 'PHON'
        elif c['l'] / tot >= 0.7: lab[s] = 'LOGO'
    return lab

def main():
    global LOG
    LOG = (P / 'run54.log').open('w', encoding='utf-8'); t0 = time.time()
    indus = [list(t) for t in FC.TRAIN]; lengths = [len(t) for t in indus]; R52.N = sum(lengths)
    data = {c: load(c) for c in CORPORA}
    for c, (u, fl) in data.items(): log(c, 'units', len(u), 'tokens', sum(len(x) for x in u), 'flagged types', len(fl))
    # per-sample freedom tables
    tables = {}
    for ci, c in enumerate(CORPORA):
        units, flags = data[c]; idx = R52.build_index(units, lengths); tables[c] = []
        for b in range(B):
            r = random.Random(SEED + ci * 1000 + b)
            texts = R52.indus_sample(units, idx, lengths, r)
            F, cnt = freedom(texts, r); tables[c].append((F, cnt))
        log(c, 'done', round(time.time() - t0, 1), 's', 'types f>=10 per sample', round(sum(len(F) for F, _ in tables[c]) / B, 1))
    # positive control: AUC on OBL, OAL (gold); SEAL reported
    aucs = {}; pooled = []
    for c in ('OBL', 'OAL', 'SEAL'):
        vals = []
        for F, cnt in tables[c]:
            lab = labels(data[c][1], F.keys())
            pos = [F[s] for s in lab if lab[s] == 'PHON']; neg = [F[s] for s in lab if lab[s] == 'LOGO']
            vals.append(auc(pos, neg))
            if c != 'SEAL': pooled += [(F[s], lab[s]) for s in lab]
        aucs[c] = sum(vals) / B
        log('AUC', c, round(aucs[c], 3), 'PHON/LOGO types in last sample', len(pos), len(neg))
    control = 'PASS' if aucs['OBL'] >= 0.75 and aucs['OAL'] >= 0.75 else 'METHOD-FAIL'
    # theta: balanced accuracy on pooled OBL+OAL types
    best = None
    for th in sorted({round(v, 3) for v, _ in pooled}):
        tp = sum(1 for v, l in pooled if l == 'PHON' and v >= th); P_ = sum(1 for _, l in pooled if l == 'PHON')
        tn = sum(1 for v, l in pooled if l == 'LOGO' and v < th); N_ = sum(1 for _, l in pooled if l == 'LOGO')
        ba = 0.5 * (tp / P_ + tn / N_)
        if best is None or ba > best[1]: best = (th, ba)
    theta = best[0]; log('theta', theta, 'balanced accuracy', round(best[1], 3), 'positive control', control)
    # core share per corpus
    def core_share(F, cnt):
        tot = sum(cnt[s] for s in F); core = sum(cnt[s] for s in F if F[s] >= theta)
        cov = tot / sum(cnt.values())
        return core / tot if tot else 0, cov
    res = {}
    for c in CORPORA:
        cs = [core_share(F, cnt) for F, cnt in tables[c]]
        m = sum(x for x, _ in cs) / B; sd = math.sqrt(sum((x - m) ** 2 for x, _ in cs) / (B - 1)); cov = sum(y for _, y in cs) / B
        medF = sorted(v for F, _ in tables[c] for v in F.values()); medF = medF[len(medF) // 2]
        res[c] = dict(C=m, C_sd=sd, coverage=cov, median_F=medF)
        log(c, 'core share C', round(m, 3), '±', round(sd, 3), 'coverage f>=10', round(cov, 3), 'median F', round(medF, 3))
    C_akk = min(res['OBL']['C'], res['OAL']['C']); sd_akk = max(res['OBL']['C_sd'], res['OAL']['C_sd'])
    C_logo = max(res['CHN']['C'], res['OBI']['C']); sd_logo = max(res['CHN']['C_sd'], res['OBI']['C_sd'])
    neg_ok = C_akk - C_logo >= 0.20
    log('negative control: C_akk', round(C_akk, 3), 'C_logo', round(C_logo, 3), 'gap', round(C_akk - C_logo, 3), 'PASS' if neg_ok else 'FAIL')
    # Indus
    F_i, cnt_i = freedom(indus, random.Random(SEED + 999)); C_i, cov_i = core_share(F_i, cnt_i)
    top = sorted(F_i.items(), key=lambda kv: -kv[1])[:15]; bot = sorted(F_i.items(), key=lambda kv: kv[1])[:15]
    log('Indus C', round(C_i, 3), 'coverage', round(cov_i, 3), 'types f>=10', len(F_i), 'median F', round(sorted(F_i.values())[len(F_i) // 2], 3))
    log('Indus highest F', [(s, round(v, 2), cnt_i[s]) for s, v in top])
    log('Indus lowest F', [(s, round(v, 2), cnt_i[s]) for s, v in bot])
    if control != 'PASS' or not neg_ok: verdict = 'METHOD-FAIL'
    elif C_i >= C_akk - 2 * sd_akk and C_i > C_logo + 2 * sd_logo: verdict = 'CORE-PRESENT'
    elif C_i <= C_logo + 2 * sd_logo and C_i < C_akk - 2 * sd_akk: verdict = 'NO-CORE'
    else: verdict = 'BETWEEN'
    log('VERDICT', verdict)
    json.dump(dict(seed=SEED, B=B, perms=PERMS, minf=MINF, aucs=aucs, theta=theta, balanced_acc=best[1], control=control,
                   negative_control=dict(C_akk=C_akk, C_logo=C_logo, ok=neg_ok), corpora=res,
                   indus=dict(C=C_i, coverage=cov_i, F=F_i, counts={s: cnt_i[s] for s in F_i}), verdict=verdict),
              (P / 'results.json').open('w'), indent=1)
    log('done', round(time.time() - t0, 1), 's')

if __name__ == '__main__': main()
