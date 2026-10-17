"""Round 38: word-level donor attribution. See PROTOCOL.md. Reuses round 37 data loaders/normalisation.
Usage: python3 attribution.py <kuiper_djvu.txt> <jambu_repo> <dravidian_db_dir> <lexibank_ids_repo>"""
import sys, json, random, collections
from pathlib import Path
import numpy as np
from rapidfuzz.distance import Levenshtein
from rapidfuzz import process
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'round37'))
import fingerprint as F

FAMS = ['PDR', 'MUNDA', 'BUR', 'EUS', 'FIN']


def best_match(words, lex):
    """returns list of (best_similarity, best_word) for each word against lexicon (normalised Levenshtein similarity)."""
    out = []
    for w in words:
        r = process.extractOne(w, lex, scorer=Levenshtein.normalized_similarity)
        out.append((r[1], r[0]))
    return out


def attribution(targets, background, lex, label, seed_bg=38001, seed_boot=38002):
    rng = random.Random(seed_bg)
    bylen = collections.defaultdict(list)
    for w in background: bylen[len(w)].append(w)
    bgsets = []
    for w in targets:
        pool = [x for x in bylen.get(len(w), []) if x != w] or [x for L in (len(w) - 1, len(w) + 1) for x in bylen.get(L, [])]
        bgsets.append(rng.sample(pool, min(5, len(pool))))
    allbg = sorted({x for s in bgsets for x in s})
    d = {}; pairs = {}
    for f in FAMS:
        tm = best_match(targets, lex[f]); bm = dict(zip(allbg, [s for s, _ in best_match(allbg, lex[f])]))
        d[f] = np.array([tm[i][0] - np.mean([bm[x] for x in bgsets[i]]) for i in range(len(targets))])
        pairs[f] = sorted([(round(tm[i][0], 3), targets[i], tm[i][1]) for i in range(len(targets))], reverse=True)[:30]
    A = {f: float(d[f].mean()) for f in FAMS}
    rb = np.random.default_rng(seed_boot); n = len(targets); boots = []
    for _ in range(1000):
        idx = rb.integers(0, n, n); boots.append({f: d[f][idx].mean() for f in FAMS})
    p1 = {f: sum(max(FAMS, key=lambda k: b[k]) == f for b in boots) / 1000 for f in FAMS}
    pc = {f: sum(b[f] > b['EUS'] and b[f] > b['FIN'] for b in boots) / 1000 for f in FAMS}
    ci = {f: [float(np.percentile([b[f] for b in boots], q)) for q in (2.5, 97.5)] for f in FAMS}
    print(f'== {label}: {n} target words')
    for f in sorted(FAMS, key=lambda k: -A[k]):
        print(f'   {f:6s} A={A[f]:+.4f}  CI {ci[f][0]:+.4f}..{ci[f][1]:+.4f}  P(rank1)={p1[f]:.2f}  P(>both controls)={pc[f]:.2f}')
    return dict(label=label, n=n, A=A, ci95=ci, p_rank1=p1, p_beats_controls=pc, top_pairs=pairs)


def main():
    hw = F.cdial_headwords(); kw = F.kuiper_words(); dl = F.dravloans(hw)
    inh = F.inherited(hw, kw + dl)
    norm = lambda ws: sorted({F.norm(w) for w in ws} - {''})
    K, D, B = norm(kw), norm(dl), norm(inh)
    lex = {k: norm(v) for k, v in {'PDR': F.lex_pdr(), 'MUNDA': F.lex_munda(), 'BUR': F.lex_bur(),
                                     'EUS': F.ids_lang({'Basque'}), 'FIN': F.ids_lang({'Finnish'})}.items()}
    print('sizes', {k: len(v) for k, v in lex.items()}, 'kuiper', len(K), 'dravloans', len(D), 'background', len(B))
    out = {'control': attribution(D, B, lex, 'POSITIVE CONTROL: Dravidian loans')}
    c = out['control']; out['control_PASS'] = c['p_rank1']['PDR'] >= 0.9 and c['ci95']['PDR'][0] > 0
    print('CONTROL', 'PASS' if out['control_PASS'] else 'FAIL')
    out['kuiper'] = attribution(K, B, lex, 'KUIPER foreign words')
    k = out['kuiper']
    if not out['control_PASS']:
        dec = 'UNINTERPRETABLE (control failed)'
    else:
        best = [f for f in FAMS if k['p_rank1'][f] >= 0.9 and k['ci95'][f][0] > 0 and k['p_beats_controls'][f] >= 0.95]
        sec = [f for f in FAMS if f not in best and k['ci95'][f][0] > 0 and k['p_beats_controls'][f] >= 0.95]
        dec = (f'BEST-SUPPORTED DONOR: {best[0]}' if best else 'NO FAMILY ATTRIBUTABLE') + (f'; secondary: {sec}' if sec else '')
    out['decision'] = dec; print('DECISION', dec)
    (P / 'results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
