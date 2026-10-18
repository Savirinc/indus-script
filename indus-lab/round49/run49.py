#!/usr/bin/env python3
"""Round 49: tournament of published Indus sign keys under the round-47 instrument. See PROTOCOL.md.
Usage: python3 run49.py   (from this folder; needs ../../ext/lexicons, ../../ext/neurodecipher, ../../ext/cyphersolver_keys)"""
import sys, re, json, csv, math, random, collections, unicodedata, importlib.util, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent; LAB = HERE.parent; ROOT = LAB.parent
sys.argv = ['x']
spec = importlib.util.spec_from_file_location('r47', LAB / 'round47' / 'run47.py'); r47 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r47)
LM, bits_per_char, summarize, lb_data, lb_build = r47.LM, r47.bits_per_char, r47.summarize, r47.lb_data, r47.lb_build
BIN, NSHUF, NDRAW, STEPS, CHAINS, MIN_SIGNS = 10, 1000, 5, 60000, 3, 25
T0 = time.time()
def log(*a): print(f'[{time.time()-T0:7.1f}s]', *a, flush=True)

# ---------------- common alphabet ----------------
def common(s):
    s = unicodedata.normalize('NFD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('A', 'a').replace('E', 'ai').replace('O', 'au').lower()
    s = re.sub(r'([kgcjtdpb])h', r'\1', s)
    s = s.replace('h', 's').replace('w', 'v').replace('z', 's').replace('f', 'p').replace('x', 'k').replace('q', 'k')
    return re.sub(r'[^aiueokgcjtdnpbmyrlvs]', '', s)

# ---------------- lexicons ----------------
def load_lexicons():
    L47 = r47.load_lexicons()
    L = {'Sanskrit': {common(w) for w in L47['Sanskrit']}, 'Finnish': {common(w) for w in L47['Finnish']}, 'Basque': {common(w) for w in L47['Basque']},
         'PDr': {common(w) for w in L47['PDr']}}
    tam = set()
    for r in csv.DictReader(open(LAB / 'external' / 'dravidian_db_v1.1' / 'forms.csv', encoding='utf-8')):
        if r['Language_ID'] == 'Tamil':
            w = re.sub(r'\([^)]*\)', '', r['Form']); w = re.split(r'[,;/~ ]', w.strip())[0]
            if w: tam.add(common(w))
    L['Tamil'] = tam
    return {k: sorted(w for w in v if len(w) >= 2) for k, v in L.items()}

# ---------------- keys ----------------
def load_tsv_key(fn):
    key = {}
    for l in open(ROOT / 'ext' / 'cyphersolver_keys' / fn, encoding='utf-8'):
        if not l.strip() or l.startswith('#'): continue
        p = l.rstrip('\n').split('\t')
        if len(p) >= 2 and p[1].strip(): key[p[0].strip().zfill(3)] = p[1].strip()
    return key
KEYS = {  # name: (loader, home language, verdict-bearing?)
 'Fairservis1992': (lambda: load_tsv_key('fairservis1992.tsv'), 'Tamil', True),
 'Fairservis1992_wide': (lambda: load_tsv_key('fairservis1992_wide.tsv'), 'Tamil', False),
 'Parpola1994': (lambda: load_tsv_key('parpola1994.tsv'), 'Tamil', True),
 'Kak1988': (lambda: load_tsv_key('kak1988.tsv'), 'Sanskrit', True),
 'Mahadevan2014': (lambda: load_tsv_key('mahadevan2014.tsv'), 'Tamil', True),
 'Yajnadevam2024_ref': (lambda: json.load(open(LAB / 'round46-brahmi-coverage' / 'expanded-map.json')), 'Sanskrit', False),
}

# ---------------- reading procedure: maximal covered runs of >= 2 signs ----------------
def runs_of(texts, key):
    out = []
    for t in texts:
        run = []
        for s in t:
            if s in key: run.append(s)
            else:
                if len(run) >= 2: out.append(tuple(run))
                run = []
        if len(run) >= 2: out.append(tuple(run))
    return out
def read(labels): return ''.join(labels)

def freq_bins(texts, signs):
    f = collections.Counter(s for t in texts for s in t); order = sorted(signs, key=lambda s: (-f[s], s))
    return [order[i:i+BIN] for i in range(0, len(order), BIN)]
def shuffle_key(key, bins, rng):
    new = dict(key)
    for b in bins:
        labs = [key[s] for s in b]; rng.shuffle(labs)
        for s, l in zip(b, labs): new[s] = l
    return new
def score(runs, key, lms):
    rd = [read([key[s] for s in t]) for t in runs]; rd = [x for x in rd if x]
    return {L: sum(bits_per_char(lm, rd) for lm in ms) / len(ms) for L, ms in lms.items()}
def null_test(runs, key, bins, lms, seed0):
    real = score(runs, key, lms); shuf = {L: [] for L in lms}
    for i in range(NSHUF):
        sc = score(runs, shuffle_key(key, bins, random.Random(seed0 + i)), lms)
        for L in lms: shuf[L].append(sc[L])
    return summarize(real, shuf)

def fit_key(runs, key, lm, seed, steps=STEPS):
    rng = random.Random(seed); signs = sorted(key); labs = [key[s] for s in signs]; rng.shuffle(labs)
    k = dict(zip(signs, labs)); by = collections.defaultdict(set)
    for i, t in enumerate(runs):
        for s in set(t): by[s].add(i)
    cur = [lm.lp(read([k[s] for s in t])) for t in runs]; total = sum(cur)
    for step in range(steps):
        T = 3.0 + (0.05 - 3.0) * step / steps; a, b = rng.sample(signs, 2)
        if k[a] == k[b]: continue
        k[a], k[b] = k[b], k[a]; rows = by[a] | by[b]
        nv = {i: lm.lp(read([k[s] for s in runs[i]])) for i in rows}; d = sum(nv.values()) - sum(cur[i] for i in rows)
        if d >= 0 or rng.random() < math.exp(d / T):
            for i, v in nv.items(): cur[i] = v
            total += d
        else: k[a], k[b] = k[b], k[a]
    return k, total

def collapse_key(key, signs): return {s: common(key[s]) for s in signs}

def main():
    out = dict(protocol='PROTOCOL.md', bin=BIN, n_shuffles=NSHUF, n_draws=NDRAW, steps=STEPS, chains=CHAINS, min_signs=MIN_SIGNS)
    log('lexicons'); LX = load_lexicons(); out['lexicon_sizes'] = {k: len(v) for k, v in LX.items()}; log(out['lexicon_sizes'])
    TEST_LANGS = ['Sanskrit', 'Tamil', 'Finnish', 'Basque']
    size = min(len(LX[L]) for L in TEST_LANGS); out['matched_lexicon_size'] = size
    def draws(lex, sz, base=49101): return [LM(random.Random(base + d).sample(lex, sz)) if sz < len(lex) else LM(lex) for d in range(NDRAW)]
    lms = {L: draws(LX[L], size) for L in TEST_LANGS}; lms['PDr'] = [LM(LX['PDr'])]
    TRAIN, types, m304 = r47.load_corpus(); tokfreq = collections.Counter(s for t in TRAIN for s in t); NTOK = sum(tokfreq.values())
    out['corpus'] = dict(text_types=len(TRAIN), tokens=NTOK, sign_types=len(tokfreq)); density = NTOK / len(tokfreq)
    # ---- keys and coverage ----
    keys = {}
    for name, (loader, home, bearing) in KEYS.items():
        raw = loader(); signs = sorted(s for s in raw if s in tokfreq and common(raw[s]))
        cov = sum(tokfreq[s] for s in signs) / NTOK; rr = runs_of(TRAIN, set(signs))
        keys[name] = dict(key=collapse_key(raw, signs), raw={s: raw[s] for s in signs}, home=home, bearing=bearing, signs=len(signs), coverage=cov, runs=len(rr), run_tokens=sum(len(t) for t in rr), run_list=rr)
        log(f'{name}: {len(signs)} signs, coverage {cov:.3f}, {len(rr)} runs, {sum(len(t) for t in rr)} run tokens')
    out['keys'] = {n: {k: v for k, v in d.items() if k not in ('run_list', 'key', 'raw')} for n, d in keys.items()}
    # ---- positive controls at each tested coverage level ----
    words, greek = lb_data(); n = len(words); rs = random.Random(47301); idx = list(range(n)); rs.shuffle(idx); halfA, halfB = idx[:n // 2], idx[n // 2:]
    pc2_target = round(sum(len(words[i]) for i in halfB) / density)
    grk = sorted({common(r47.col_grk(g)) for i in halfA for g in greek[i] if len(common(r47.col_grk(g))) >= 2})
    pc_size = min(len(grk), size); out['pc_lexicon_size'] = pc_size
    pc_lms = {'Greek': draws(grk, pc_size)}; pc_lms.update({L: draws(LX[L], pc_size) for L in TEST_LANGS})
    lb_texts, truth = lb_build(words, halfB, pc2_target, True); truth = {s: common(v) for s, v in truth.items()}
    lb_freq = collections.Counter(s for t in lb_texts for s in t); lb_tot = sum(lb_freq.values())
    out['pc_geometry'] = dict(texts=len(lb_texts), sign_ids=len(truth), tokens=lb_tot)
    levels = sorted({round(keys[n]['coverage'], 2) for n in keys if keys[n]['signs'] >= MIN_SIGNS and keys[n]['coverage'] < 0.97})
    out['positive_controls'] = {}
    for li, lev in enumerate(levels):
        subs = []
        for c in range(3):
            rng = random.Random(49301 + 10 * li + c); ids = sorted(truth); rng.shuffle(ids); keep_ids = set(ids)
            for s in ids:
                if sum(lb_freq[x] for x in keep_ids) / lb_tot <= lev + 0.03: break
                keep_ids.discard(s)
            cov = sum(lb_freq[x] for x in keep_ids) / lb_tot; sub = {s: truth[s] for s in keep_ids}; rr = runs_of(lb_texts, keep_ids)
            summ = null_test(rr, sub, freq_bins(lb_texts, sorted(sub)), pc_lms, 49201 + 1000 * (10 * li + c))
            zg = summ['Greek']['z']; ok = summ['Greek']['percentile'] >= 0.99 and zg >= 3 and all(zg - summ[L]['z'] >= 2 for L in TEST_LANGS)
            subs.append(dict(coverage=cov, sign_ids=len(sub), runs=len(rr), run_tokens=sum(len(t) for t in rr), scores=summ, passed=ok))
            log(f'PC level {lev}: subset {c} cov {cov:.3f} ids {len(sub)} runs {len(rr)} Greek z {zg:.2f} pct {summ["Greek"]["percentile"]:.3f} others ' + ', '.join(f'{L} {summ[L]["z"]:.2f}' for L in TEST_LANGS) + (' PASS' if ok else ' fail'))
        out['positive_controls'][str(lev)] = dict(subsets=subs, passed=sum(s['passed'] for s in subs) >= 2)
        log(f'PC level {lev}: {"PASS" if out["positive_controls"][str(lev)]["passed"] else "FAIL"}')
    # ---- keys ----
    out['results'] = {}; out['fitted'] = {}; verdicts = {}
    for name, d in keys.items():
        key, rr, home = d['key'], d['run_list'], d['home']
        if d['signs'] < MIN_SIGNS:
            verdicts[name] = 'NOT TESTABLE (signs)'; out['results'][name] = dict(readings=[(('-'.join(t)), read([key[s] for s in t])) for t in rr[:30]]); log(name, verdicts[name]); continue
        bins = freq_bins(TRAIN, sorted(key)); summ = null_test(rr, key, bins, lms, 49201 + 7919 * (list(keys).index(name) + 1)); out['results'][name] = dict(scores=summ)
        log(name, {L: (round(v['z'], 2), v['percentile']) for L, v in summ.items()})
        lev = str(round(d['coverage'], 2)); pc_ok = out['positive_controls'].get(lev, {}).get('passed', d['coverage'] >= 0.97)
        fits = {}
        for L in ('Finnish', 'Basque', 'Tamil', 'Sanskrit'):
            best = None
            for c in range(CHAINS):
                sd = 49401 + 100 * list(keys).index(name) + 3 * ['Finnish', 'Basque', 'Tamil', 'Sanskrit'].index(L) + c
                k, obj = fit_key(rr, key, lms[L][0], sd)
                if best is None or obj > best[1]: best = (k, obj, sd)
            fits[L] = dict(seed=best[2], objective=best[1], scores=null_test(rr, best[0], bins, lms, 49201 + 104729 + list(keys).index(name)))
            log(f'  fitted {L}: ' + ', '.join(f'{M} {v["z"]:.2f}' for M, v in fits[L]['scores'].items()))
        out['fitted'][name] = fits
        zh, ph = summ[home]['z'], summ[home]['percentile']; others = [L for L in TEST_LANGS if L != home]; imp = ['Finnish', 'Basque']
        if not pc_ok: v = 'NOT TESTABLE (positive control fails at this coverage)'
        elif ph < 0.95: v = 'NULL'
        elif any(summ[L]['percentile'] >= 0.95 for L in imp) or zh - max(summ[L]['z'] for L in imp) < 2: v = 'ARTEFACT'
        elif ph >= 0.99 and zh >= 3 and all(zh - summ[L]['z'] >= 2 for L in others): v = 'SUPPORT'
        else: v = 'MIXED'
        verdicts[name] = v if d['bearing'] else f'{v} (reference, not verdict-bearing)'; log(name, 'VERDICT', verdicts[name])
    out['verdicts'] = verdicts
    # ---- diagnostics: readings of the 15 most frequent texts ----
    cnt = collections.Counter({t: len(ids) for t, ids in types.items()}); top = [t for t, _ in cnt.most_common(15)]
    out['diagnostic_readings'] = {name: [{'text': '-'.join(t), 'n': cnt[t], 'reading': '|'.join(read([d['key'][s] for s in r]) for r in runs_of([t], set(d['key'])))} for t in top] for name, d in keys.items()}
    json.dump(out, open(HERE / 'results.json', 'w'), indent=1)
    log('VERDICTS', verdicts)

if __name__ == '__main__': main()
