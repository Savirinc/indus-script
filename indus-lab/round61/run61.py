#!/usr/bin/env python
"""Round 61: are the atlas's Indus sign / Brahmi letter pairs closer in shape than random pairings, and than letters any script
could supply? See PROTOCOL.md (with Amendment 1). Run from this folder: ../../ext/venv/bin/python run61.py
(needs Pillow, numpy, scipy, fontTools; fonts via round48/fetch_fonts.sh)."""
import json, hashlib, importlib.util, pathlib, collections
import numpy as np
from scipy.optimize import linear_sum_assignment

HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('r48', ROOT / 'indus-lab' / 'round48' / 'run48.py')
R48 = importlib.util.module_from_spec(spec); spec.loader.exec_module(R48)   # rendering and descriptor B, unchanged
FONTS = R48.FONTS; log = R48.log
NPERM, NDRAW, K = 10000, 200, 22

LETTERS = {'a': '𑀅', 'i': '𑀇', 'u': '𑀉', 'b': '𑀩', 'c': '𑀘', 'd': '𑀤', 'g': '𑀕', 'j': '𑀚', 'k': '𑀓', 'l': '𑀮', 'm': '𑀫',
           'n': '𑀦', 'p': '𑀧', 'r': '𑀭', 's': '𑀲', 't': '𑀢', 'v': '𑀯', 'y': '𑀬'}
PH = [f'U+{cp:04X}' for cp in range(0x10900, 0x10916)]   # alf..tau
GREEK_IDX = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21]   # skips wau, sade, qof
GREEK_CP = [0x0391, 0x0392, 0x0393, 0x0394, 0x0395, 0x0396, 0x0397, 0x0398, 0x0399, 0x039A, 0x039B, 0x039C, 0x039D, 0x039E,
            0x039F, 0x03A0, 0x03A1, 0x03A3, 0x03A4]
CONTROLS = {'PC-A1 Phoenician->Greek': ([PH[i] for i in GREEK_IDX], 'GreekCaps', [f'U+{c:04X}' for c in GREEK_CP], 61011),
            'PC-A2 Phoenician->Aramaic': (PH, 'ImperialAramaic', [f'U+{c:04X}' for c in range(0x10840, 0x10856)], 61012),
            'NC-A1 Phoenician->LinearA': (PH, 'LinearA', [f'U+{c:04X}' for c in range(0x10600, 0x10616)], 61013),
            'NC-A2 Phoenician->OldHungarian': (PH, 'OldHungarian', [f'U+{c:04X}' for c in range(0x10C80, 0x10C96)], 61014)}

def verify_fonts():
    sums = dict(reversed(l.split()) for l in (ROOT / 'indus-lab' / 'round48' / 'SHA256SUMS').read_text().splitlines() if l.strip())
    used = {'indus-font.ttf'} | {fn for fn, _ in R48.SCRIPTS.values()}
    bad = [fn for fn in sorted(used) if hashlib.sha256((FONTS / fn).read_bytes()).hexdigest() != sums.get(fn)]
    if bad: raise SystemExit(f'font hash mismatch: {bad}')
    return sorted(used)

def paired_test(D, labels, seed):
    """D[i, l]: distance of item i to letter l; labels[i]: its paired letter. Permute labels (keeps letter counts)."""
    n, L = D.shape; ar = np.arange(n); s_real = D[ar, labels].mean()
    cnt = np.bincount(labels, minlength=L); real_l = np.bincount(labels, weights=D[ar, labels], minlength=L) / np.maximum(cnt, 1)
    rng = np.random.default_rng(seed); S = np.empty(NPERM); le = np.zeros(L)
    for p in range(NPERM):
        perm = rng.permutation(labels); d = D[ar, perm]; S[p] = d.mean()
        le += (np.bincount(perm, weights=d, minlength=L) / np.maximum(cnt, 1)) <= real_l
    return dict(n=int(n), S_real=float(s_real), perm_mean=float(S.mean()), perm_sd=float(S.std()),
                p=float((S <= s_real).mean()), z=float((s_real - S.mean()) / S.std())), real_l, le / NPERM

def opt_costs(C, rng, k=K):
    """C: groups x letters cost. Optimal one-to-one assignment cost over NDRAW random k-letter subsets."""
    out = np.empty(NDRAW)
    for d in range(NDRAW):
        cols = rng.choice(C.shape[1], k, replace=False); sub = C[:, cols]
        r, c = linear_sum_assignment(sub); out[d] = sub[r, c].sum()
    return out

def main():
    fonts = verify_fonts(); log('fonts verified', len(fonts))
    pool, dropped = R48.load_scripts(); log('pool', len(pool), 'dropped', len(dropped))
    by = {(g.script, g.label): g for g in pool}
    emap = json.loads((ROOT / 'indus-lab' / 'round46-brahmi-coverage' / 'expanded-map.json').read_text())
    fp = FONTS / 'indus-font.ttf'; cmap = R48.TTFont(str(fp)).getBestCmap()
    pairs, indus, missing = [], [], []
    for code, val in sorted(emap.items()):
        if val not in LETTERS: continue
        cp = 0xE000 + int(code); m = R48.render(fp, cp) if cp in cmap else None
        if m is None or m.sum() == 0: missing.append(code); continue
        indus.append(R48.Glyph('Indus', code, m, R48.render(fp, cp, grid=R48.G2))); pairs.append((code, val))
    letters = sorted(LETTERS); lid = {l: k for k, l in enumerate(letters)}
    bglyph = [by[('Brahmi', f'U+{ord(LETTERS[l]):04X}')] for l in letters]
    (HERE / 'pairs.tsv').write_text('code\tvalue\tbrahmi\tcodepoint\n' + ''.join(
        f'{c}\t{v}\t{LETTERS[v]}\tU+{ord(LETTERS[v]):04X}\n' for c, v in pairs))
    log('pairs', len(pairs), 'missing indus glyphs', len(missing))

    # ---- Part A controls ----
    ctrl = {}
    for name, (src, tscript, tgt, seed) in CONTROLS.items():
        ok = [(s, t) for s, t in zip(src, tgt) if ('Phoenician', s) in by and (tscript, t) in by]
        Dc = R48.dist_matrix([by[('Phoenician', s)] for s, _ in ok], [by[(tscript, t)] for _, t in ok], 'B')
        res, _, _ = paired_test(Dc, np.arange(len(ok)), seed); res['dropped_pairs'] = len(src) - len(ok); ctrl[name] = res
        log(name, res)
    a_pass = all(ctrl[n]['p'] < 0.01 for n in ctrl if n.startswith('PC')) and all(ctrl[n]['p'] >= 0.05 for n in ctrl if n.startswith('NC'))

    # ---- Part A, Indus ----
    Dl = R48.dist_matrix(indus, bglyph, 'B'); labels = np.array([lid[v] for _, v in pairs])
    A, real_l, p_l = paired_test(Dl, labels, 61001)
    per_letter = {l: dict(n=int((labels == lid[l]).sum()), mean_paired=float(real_l[lid[l]]), p=float(p_l[lid[l]])) for l in letters}
    A_verdict = 'VOID' if not a_pass else ('PAIRS SHAPE-CLOSE' if A['p'] < 0.01 else 'WEAK' if A['p'] < 0.05 else 'NOT CLOSER THAN RANDOM')
    log('Part A', A, A_verdict)

    # ---- Part B ----
    D_all = R48.dist_matrix(indus, pool, 'B')
    Gm = np.zeros((len(letters), len(indus)))
    for i, (_, v) in enumerate(pairs): Gm[lid[v], i] = 1
    names = list(R48.SCRIPTS); cols = {n: [j for j, g in enumerate(pool) if g.script == n] for n in names}
    bcols = cols['Brahmi']; atlas = float(sum((Gm[lid[l]] @ D_all[:, pool.index(bglyph[lid[l]])]) for l in letters))
    B = {}
    for k, n in enumerate(names):
        C = Gm @ D_all[:, cols[n]]; oc = opt_costs(C, np.random.default_rng(61101 + k))
        B[n] = dict(letters=len(cols[n]), opt_mean=float(oc.mean()), opt_median=float(np.median(oc)), share_le_atlas=float((oc <= atlas).mean()))
    order = sorted(names, key=lambda n: B[n]['opt_mean'])
    for r, n in enumerate(order): B[n]['rank'] = r + 1
    log('Part B atlas cost', atlas, 'Brahmi rank', B['Brahmi']['rank'])

    # ---- B-control ----
    unrel = sorted(R48.UNRELATED); bctrl = {}
    for tag, (src, tscript, tgt), base in (('Greek', CONTROLS['PC-A1 Phoenician->Greek'][:3], 61201),
                                           ('Aramaic', CONTROLS['PC-A2 Phoenician->Aramaic'][:3], 61301)):
        ok = [(s, t) for s, t in zip(src, tgt) if ('Phoenician', s) in by and (tscript, t) in by]
        q = [by[('Phoenician', s)] for s, _ in ok]
        actual = float(np.trace(R48.dist_matrix(q, [by[(tscript, t)] for _, t in ok], 'B')))
        Dq = R48.dist_matrix(q, pool, 'B'); med = {}
        for k, n in enumerate(unrel): med[n] = float(np.median(opt_costs(Dq[:, cols[n]], np.random.default_rng(base + k))))
        bctrl[tag] = dict(groups=len(ok), actual=actual, unrelated_median_opt=med, passed=all(actual < m for m in med.values()))
        log('B-control', tag, bctrl[tag]['passed'], actual, min(med.values()))
    b_pass = all(v['passed'] for v in bctrl.values())
    if not b_pass: B_verdict = 'METHOD-FAIL'
    elif any(B[n]['share_le_atlas'] >= 0.5 for n in unrel): B_verdict = 'FITTABLE IN ANY SCRIPT'
    elif B['Brahmi']['rank'] == 1 and all(B[n]['share_le_atlas'] < 0.05 for n in unrel): B_verdict = 'BRAHMI STANDS OUT'
    else:
        fail = (['Brahmi not ranked 1st'] if B['Brahmi']['rank'] != 1 else []) + \
               [f'{n} reaches atlas in {B[n]["share_le_atlas"]:.0%} of draws' for n in unrel if B[n]['share_le_atlas'] >= 0.05]
        B_verdict = 'IN BETWEEN: ' + '; '.join(fail)
    res = dict(protocol_sha256=hashlib.sha256((HERE / 'PROTOCOL.md').read_bytes()).hexdigest(), fonts_verified=fonts,
               n_pairs=len(pairs), missing_indus_glyphs=missing, pool_size=len(pool), pool_dropped=dropped,
               controls_A=ctrl, part_A_controls_pass=a_pass, part_A=A, per_letter=per_letter, part_A_verdict=A_verdict,
               atlas_cost=atlas, part_B=B, B_controls=bctrl, part_B_controls_pass=b_pass, part_B_verdict=B_verdict)
    (HERE / 'results.json').write_text(json.dumps(res, indent=1, ensure_ascii=False, default=lambda o: o.item()))
    log('VERDICT A:', A_verdict, '| B:', B_verdict)

if __name__ == '__main__':
    main()
