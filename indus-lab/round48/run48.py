#!/usr/bin/env python
"""Round 48: shape-resemblance null test. See PROTOCOL.md. Run with ../../ext/venv/bin/python run48.py (needs Pillow, numpy, scipy;
fonts via fetch_fonts.sh)."""
import json, sys, time, collections, importlib.util, pathlib, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import distance_transform_edt as edt
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; FONTS = ROOT / 'ext' / 'fonts'
G = 40; NPERM = 10000; RARE_N, RARE_DRAWS = 22, 200
T0 = time.time()
def log(*a): print(f'[{time.time()-T0:6.1f}s]', *a, flush=True)

SCRIPTS = {  # name: (font, ranges)  — frozen in PROTOCOL.md
 'Brahmi':('NotoSansBrahmi-Regular.ttf',[(0x11005,0x11033)]),
 'Kharoshthi':('NotoSansKharoshthi-Regular.ttf',[(0x10A00,0x10A00),(0x10A10,0x10A13),(0x10A15,0x10A17),(0x10A19,0x10A35)]),
 'Phoenician':('NotoSansPhoenician-Regular.ttf',[(0x10900,0x10915)]),
 'ImperialAramaic':('NotoSansImperialAramaic-Regular.ttf',[(0x10840,0x10855)]),
 'Samaritan':('NotoSansSamaritan-Regular.ttf',[(0x0800,0x0815)]),
 'GreekCaps':('NotoSans[wdth,wght].ttf',[(0x0391,0x03A1),(0x03A3,0x03A9)]),
 'OldItalic':('NotoSansOldItalic-Regular.ttf',[(0x10300,0x1031F)]),
 'Lycian':('NotoSansLycian-Regular.ttf',[(0x10280,0x1029C)]),
 'Carian':('NotoSansCarian-Regular.ttf',[(0x102A0,0x102D0)]),
 'Lydian':('NotoSansLydian-Regular.ttf',[(0x10920,0x10939)]),
 'OldSouthArabian':('NotoSansOldSouthArabian-Regular.ttf',[(0x10A60,0x10A7C)]),
 'OldNorthArabian':('NotoSansOldNorthArabian-Regular.ttf',[(0x10A80,0x10A9C)]),
 'Gothic':('NotoSansGothic-Regular.ttf',[(0x10330,0x1034A)]),
 'Runic':('NotoSansRunic-Regular.ttf',[(0x16A0,0x16EA)]),
 'OldTurkic':('NotoSansOldTurkic-Regular.ttf',[(0x10C00,0x10C48)]),
 'OldHungarian':('NotoSansOldHungarian-Regular.ttf',[(0x10C80,0x10CB2)]),
 'Glagolitic':('NotoSansGlagolitic-Regular.ttf',[(0x2C00,0x2C2E)]),
 'OldPermic':('NotoSansOldPermic-Regular.ttf',[(0x10350,0x10375)]),
 'Elbasan':('NotoSansElbasan-Regular.ttf',[(0x10500,0x10527)]),
 'Osage':('NotoSansOsage-Regular.ttf',[(0x104B0,0x104D3)]),
 'Tifinagh':('NotoSansTifinagh-Regular.ttf',[(0x2D30,0x2D67)]),
 'NKo':('NotoSansNKo-Regular.ttf',[(0x07CA,0x07EA)]),
 'MeroiticCursive':('NotoSansMeroitic-Regular.ttf',[(0x109A0,0x109B7)]),
 'LinearA':('NotoSansLinearA-Regular.ttf',[(0x10600,0x1065F)]),
 'CyproMinoan':('NotoSansCyproMinoan-Regular.ttf',[(0x12F90,0x12FF0)]),
}
PHOEN_DESC = {'ImperialAramaic','Samaritan','GreekCaps','OldItalic','Lycian','Carian','Lydian','Gothic','OldSouthArabian','OldNorthArabian','Kharoshthi'}
GREEK_SET = {'Phoenician','OldItalic','Lycian','Carian','Lydian','Gothic'}
UNRELATED = {'Runic','OldTurkic','OldHungarian','Glagolitic','OldPermic','Elbasan','Osage','Tifinagh','NKo','LinearA','CyproMinoan'}
T7 = {'a':0x11005,'u':0x11009,'o':0x11011,'k':0x11013,'kh':0x11014,'g':0x11015,'gh':0x11016,'jh':0x1101B,'ṭ':0x1101D,'ḍ':0x1101F,
      'ḍh':0x11020,'d':0x11024,'dh':0x11025,'b':0x11029,'m':0x1102B,'y':0x1102C,'r':0x1102D,'l':0x1102E,'ṣ':0x11031,'s':0x11032,'h':0x11033}

# ---------------- rendering ----------------
def render(font_path, cp, em=200):
    f = ImageFont.truetype(str(font_path), em)
    im = Image.new('L', (em*3, em*3), 0); ImageDraw.Draw(im).text((em, em), chr(cp), font=f, fill=255)
    bb = im.getbbox()
    if bb is None or bb[2]-bb[0] < 4 or bb[3]-bb[1] < 4: return None
    im = im.crop(bb); w, h = im.size; s = max(w, h)
    sq = Image.new('L', (s, s), 0); sq.paste(im, ((s-w)//2, (s-h)//2))
    a = np.asarray(sq.resize((G, G), Image.LANCZOS), dtype=np.float32) / 255.0
    return a >= 0.5

def zhang_suen(img):
    img = img.copy().astype(np.uint8)
    def nb(i):
        p = np.pad(i, 1)
        P2 = p[:-2,1:-1]; P3 = p[:-2,2:]; P4 = p[1:-1,2:]; P5 = p[2:,2:]; P6 = p[2:,1:-1]; P7 = p[2:,:-2]; P8 = p[1:-1,:-2]; P9 = p[:-2,:-2]
        return [P2,P3,P4,P5,P6,P7,P8,P9]
    while True:
        changed = False
        for step in (0, 1):
            P2,P3,P4,P5,P6,P7,P8,P9 = nb(img)
            B = P2+P3+P4+P5+P6+P7+P8+P9
            seq = [P2,P3,P4,P5,P6,P7,P8,P9,P2]
            A = sum(((seq[k]==0)&(seq[k+1]==1)).astype(np.uint8) for k in range(8))
            if step == 0: c = (P2*P4*P6 == 0) & (P4*P6*P8 == 0)
            else:         c = (P2*P4*P8 == 0) & (P2*P6*P8 == 0)
            m = (img==1)&(B>=2)&(B<=6)&(A==1)&c
            if m.any(): img[m] = 0; changed = True
        if not changed: break
    return img.astype(bool)

def dihedral(a):
    out = []
    for k in range(4):
        r = np.rot90(a, k); out.append(r); out.append(r[:, ::-1])
    return out

class Glyph:
    __slots__ = ('script','label','skel','edt','npx')
    def __init__(self, script, label, mask):
        self.script, self.label = script, label
        self.skel = zhang_suen(mask); self.npx = int(self.skel.sum())
        self.edt = edt(~self.skel)

def load_scripts():
    glyphs, dropped = [], []
    for name, (fn, ranges) in SCRIPTS.items():
        tt = TTFont(str(FONTS / fn)); cm = tt.getBestCmap(); gs = tt.getGlyphSet()
        for lo, hi in ranges:
            for cp in range(lo, hi+1):
                if cp not in cm: continue
                p = BoundsPen(gs); gs[cm[cp]].draw(p)
                if not p.bounds: continue
                m = render(FONTS / fn, cp)
                if m is None or m.sum() == 0: dropped.append((name, f'U+{cp:04X}')); continue
                glyphs.append(Glyph(name, f'U+{cp:04X}', m))
    return glyphs, dropped

def load_indus():
    sys.argv = ['x']
    spec = importlib.util.spec_from_file_location('r47', ROOT / 'indus-lab' / 'round47' / 'run47.py'); r47 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r47)
    types, typemap, m304 = r47.load_corpus()
    freq = collections.Counter(s for t, ids in typemap.items() for s in t for _ in ids)
    codes = sorted(freq, key=lambda c: (-freq[c], c))
    fp = FONTS / 'indus-font.ttf'; tt = TTFont(str(fp)); cm = tt.getBestCmap()
    glyphs, missing = [], []
    for c in codes:
        cp = 0xE000 + int(c)
        m = render(fp, cp) if cp in cm else None
        if m is None or m.sum() == 0: missing.append(c); continue
        glyphs.append(Glyph('Indus', c, m))
    return glyphs, missing, freq

# ---------------- distances ----------------
def dist_matrix(queries, pool, transforms=True):
    """D[i,j] = chamfer distance between query i and pool letter j, min over dihedral transforms of the query."""
    P_edt = np.stack([g.edt.ravel() for g in pool])            # N x G*G
    P_sk = np.stack([g.skel.ravel() for g in pool]).astype(np.float64)
    P_n = P_sk.sum(1)
    D = np.full((len(queries), len(pool)), np.inf)
    for i, q in enumerate(queries):
        for a in (dihedral(q.skel) if transforms else [q.skel]):
            idx = np.flatnonzero(a.ravel())
            if len(idx) == 0: continue
            t1 = P_edt[:, idx].mean(1)
            qe = edt(~a).ravel().astype(np.float64)
            t2 = (P_sk @ qe) / P_n
            d = (t1 + t2) / 2 / G
            np.minimum(D[i], d, out=D[i])
    return D

def enrichment(D, pool, rng_seed, nperm=NPERM):
    names = sorted(set(g.script for g in pool)); idx = {n: k for k, n in enumerate(names)}
    labels = np.array([idx[g.script] for g in pool]); n_s = np.bincount(labels, minlength=len(names))
    nn = D.argmin(1); Nq, N = D.shape
    expected = Nq * n_s / N
    obs = np.bincount(labels[nn], minlength=len(names))
    E = obs / expected
    rng = np.random.default_rng(rng_seed)
    npx = np.array([g.npx for g in pool]); dec = np.searchsorted(np.quantile(npx, np.linspace(0, 1, 11)[1:-1]), npx, side='right')
    out = {}
    for strat in (True, False):
        counts = np.empty((nperm, len(names)))
        for p in range(nperm):
            lab = labels.copy()
            if strat:
                for b in range(10):
                    w = np.flatnonzero(dec == b); lab[w] = rng.permutation(labels[w])
            else: lab = rng.permutation(labels)
            counts[p] = np.bincount(lab[nn], minlength=len(names))
        Ep = counts / expected
        pv = (Ep >= E[None, :]).mean(0); z = (E - Ep.mean(0)) / Ep.std(0)
        out['stratified' if strat else 'unstratified'] = {names[k]: {'n': int(n_s[k]), 'observed': int(obs[k]), 'expected': float(expected[k]), 'E': float(E[k]), 'p': float(pv[k]), 'z': float(z[k])} for k in range(len(names))}
    rank = {n: r+1 for r, n in enumerate(sorted(names, key=lambda n: -E[idx[n]]))}
    for key in out:
        for n in names: out[key][n]['rank_by_E'] = rank[n]
    return out, nn

def rarefied(D, pool, seed):
    names = sorted(set(g.script for g in pool)); rng = np.random.default_rng(seed); res = {}
    for n in names:
        cols = np.flatnonzero(np.array([g.script == n for g in pool]))
        vals = [D[:, rng.choice(cols, RARE_N, replace=False)].min(1).mean() for _ in range(RARE_DRAWS)] if len(cols) >= RARE_N else [D[:, cols].min(1).mean()]
        res[n] = {'mean_nearest_distance': float(np.mean(vals)), 'sd': float(np.std(vals)), 'n': int(len(cols))}
    order = sorted(names, key=lambda n: res[n]['mean_nearest_distance'])
    for r, n in enumerate(order): res[n]['rank'] = r+1
    return res

def control(name, allg, seed, want_sets):
    q = [g for g in allg if g.script == name]; pool = [g for g in allg if g.script != name]
    D = dist_matrix(q, pool); enr, _ = enrichment(D, pool, seed)
    S = enr['stratified']; top = min(S, key=lambda n: S[n]['rank_by_E'])
    return {'query': name, 'n_query': len(q), 'top_by_E': top, 'stratified': S, 'unstratified': enr['unstratified']}

def montage(indus, pool, D, nn, path, k=60):
    """Top-k Indus signs: sign | nearest pool letter | nearest Brahmi letter."""
    bi = [j for j, g in enumerate(pool) if g.script == 'Brahmi']
    cell = 44; cols = 6; rows = (k + cols - 1) // cols
    im = Image.new('L', (cols * cell * 3 + cols * 10, rows * (cell + 14)), 255); dr = ImageDraw.Draw(im)
    for i in range(min(k, len(indus))):
        r, c = divmod(i, cols); x0 = c * (cell * 3 + 10); y0 = r * (cell + 14)
        jb = bi[int(np.argmin(D[i, bi]))]
        for t, g in enumerate((indus[i], pool[int(nn[i])], pool[jb])):
            a = (~g.skel).astype(np.uint8) * 255
            im.paste(Image.fromarray(a).resize((cell, cell), Image.NEAREST), (x0 + t * cell, y0))
        dr.text((x0, y0 + cell), f'{indus[i].label} {pool[int(nn[i])].script[:8]} {D[i,int(nn[i])]:.3f}|B {D[i,jb]:.3f}', fill=0)
    im.save(path)

def main():
    log('loading comparison scripts'); pool, dropped = load_scripts(); log(f'{len(pool)} letters, dropped {len(dropped)}')
    log('loading Indus glyphs'); indus, missing, freq = load_indus(); log(f'{len(indus)} Indus signs with glyphs, {len(missing)} missing: {missing}')
    results = {'protocol': 'PROTOCOL.md', 'grid': G, 'nperm': NPERM, 'pool_size': len(pool), 'dropped_letters': dropped, 'indus_missing_glyphs': missing,
               'pool_counts': dict(collections.Counter(g.script for g in pool))}
    log('positive / negative controls')
    results['controls'] = {}
    for nm, seed in (('Phoenician', 48101), ('GreekCaps', 48102), ('OldHungarian', 48103), ('LinearA', 48104)):
        results['controls'][nm] = control(nm, pool, seed, None); S = results['controls'][nm]['stratified']
        log(f'  {nm}: top={results["controls"][nm]["top_by_E"]}  ' + ', '.join(f'{k}:E={v["E"]:.2f},p={v["p"]:.3f}' for k, v in sorted(S.items(), key=lambda kv: kv[1]['rank_by_E'])[:5]))
    pc1 = results['controls']['Phoenician']['stratified']; pc2 = results['controls']['GreekCaps']['stratified']
    pass1 = pc1['ImperialAramaic']['p'] < 0.05 and pc1['Samaritan']['p'] < 0.05 and results['controls']['Phoenician']['top_by_E'] in PHOEN_DESC
    pass2 = sum(pc2[s]['p'] < 0.05 for s in GREEK_SET) >= 2 and results['controls']['GreekCaps']['top_by_E'] in GREEK_SET
    results['PC1_pass'] = bool(pass1); results['PC2_pass'] = bool(pass2); log(f'PC1 pass={pass1} PC2 pass={pass2}')

    log('Indus distances'); D = dist_matrix(indus, pool); D_id = dist_matrix(indus, pool, transforms=False)
    results['indus'] = {}
    for qname, sel, seed in (('Q1_all', list(range(len(indus))), 48001), ('Q2_top100', list(range(min(100, len(indus)))), 48002)):
        enr, nn = enrichment(D[sel], pool, seed); results['indus'][qname] = enr
        B = enr['stratified']['Brahmi']; log(f'  {qname}: Brahmi E={B["E"]:.2f} obs={B["observed"]} exp={B["expected"]:.1f} p_strat={B["p"]:.4f} p_unstrat={enr["unstratified"]["Brahmi"]["p"]:.4f} rank={B["rank_by_E"]}')
        log('   top5 by E: ' + ', '.join(f'{k}({v["E"]:.2f},p={v["p"]:.3f})' for k, v in sorted(enr['stratified'].items(), key=lambda kv: kv[1]['rank_by_E'])[:5]))
    enr_id, _ = enrichment(D_id, pool, 48005); results['indus']['Q1_identity_only'] = enr_id
    log(f'  identity-only Brahmi: E={enr_id["stratified"]["Brahmi"]["E"]:.2f} p={enr_id["stratified"]["Brahmi"]["p"]:.4f}')
    results['rarefied_Q1'] = rarefied(D, pool, 48006)
    log('  rarefied rank: ' + ', '.join(f'{n}:{v["mean_nearest_distance"]:.4f}' for n, v in sorted(results['rarefied_Q1'].items(), key=lambda kv: kv[1]['rank'])[:6]) + f' | Brahmi rank {results["rarefied_Q1"]["Brahmi"]["rank"]}')
    # Table 7 diagnostic
    t7 = json.load(open(ROOT / 'indus-lab' / 'round46-brahmi-coverage' / 'table7-crosswalk.json'))
    lab = {g.label: i for i, g in enumerate(indus)}; plab = {(g.script, g.label): j for j, g in enumerate(pool)}
    rows = []
    for e in t7:
        if len(e['candidate_ids']) != 1 or e['sound'] not in T7: continue
        c = e['candidate_ids'][0]; j = plab.get(('Brahmi', f'U+{T7[e["sound"]]:04X}'))
        if c not in lab or j is None: continue
        i = lab[c]; d_auth = float(D[i, j]); jn = int(D[i].argmin())
        rows.append({'sign': c, 'sound': e['sound'], 'brahmi': pool[j].label, 'd_author_pair': d_auth, 'd_global_nearest': float(D[i, jn]),
                     'nearest_script': pool[jn].script, 'nearest_letter': pool[jn].label, 'author_pair_is_nearest': bool(jn == j),
                     'rank_of_author_letter': int((D[i] < d_auth).sum()) + 1})
    sel3 = [lab[r['sign']] for r in rows]
    enr3, _ = enrichment(D[sorted(set(sel3))], pool, 48003) if sel3 else ({}, None)
    results['table7'] = {'pairs': rows, 'n_pairs': len(rows), 'author_pair_is_nearest': sum(r['author_pair_is_nearest'] for r in rows),
                         'median_rank_of_author_letter': float(np.median([r['rank_of_author_letter'] for r in rows])) if rows else None, 'Q3_enrichment': enr3}
    log(f'  Table 7: {results["table7"]["author_pair_is_nearest"]}/{len(rows)} author pairs are the global nearest; median rank of his letter {results["table7"]["median_rank_of_author_letter"]}')
    # verdict
    Q1 = results['indus']['Q1_all']['stratified']; Q2 = results['indus']['Q2_top100']['stratified']; B1 = Q1['Brahmi']
    nc = [results['controls'][n]['stratified']['Brahmi'] for n in ('OldHungarian', 'LinearA')]
    unrelated_above = [n for n in UNRELATED if Q1[n]['rank_by_E'] < B1['rank_by_E']]
    if not (pass1 and pass2): v = 'METHOD-FAIL'
    elif B1['p'] >= 0.05: v = 'NULL'
    elif any(x['p'] < 0.05 for x in nc) or unrelated_above: v = 'ARTEFACT'
    elif B1['p'] < 0.01 and B1['rank_by_E'] == 1 and Q2['Brahmi']['p'] < 0.05 and all(B1['E'] > x['E'] for x in nc): v = 'SUPPORT'
    else: v = 'MIXED'
    results['verdict'] = v; results['verdict_inputs'] = {'Q1_Brahmi': B1, 'Q2_Brahmi': Q2['Brahmi'], 'NC_Brahmi': nc, 'unrelated_scripts_ranked_above_Brahmi': unrelated_above}
    log('VERDICT', v)
    json.dump(results, open(HERE / 'results.json', 'w'), indent=1)
    with open(HERE / 'nearest.tsv', 'w') as f:
        f.write('sign\tfreq\tnearest_script\tnearest_letter\td\tnearest_brahmi\td_brahmi\n')
        bi = [j for j, g in enumerate(pool) if g.script == 'Brahmi']
        for i, g in enumerate(indus):
            j = int(D[i].argmin()); jb = bi[int(np.argmin(D[i, bi]))]
            f.write(f'{g.label}\t{freq[g.label]}\t{pool[j].script}\t{pool[j].label}\t{D[i,j]:.4f}\t{pool[jb].label}\t{D[i,jb]:.4f}\n')
    montage(indus, pool, D, D.argmin(1), HERE / 'montage_top60.png')
    log('done')

if __name__ == '__main__': main()
