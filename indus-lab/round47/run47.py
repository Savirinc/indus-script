"""Round 47: is Yajnadevam's key Sanskrit-specific? See PROTOCOL.md (committed first). Stdlib only, Python 3.9+.
Usage: python3 run47.py            (run from this folder; needs ../../ext/lexicons via fetch_lexicons.sh and ../../ext/neurodecipher)"""
import csv, json, math, random, re, sys, time, unicodedata, collections
from pathlib import Path
P = Path(__file__).resolve().parent; LAB = P.parent; ROOT = LAB.parent
LEX = ROOT / 'ext' / 'lexicons'; COG = ROOT / 'ext' / 'neurodecipher' / 'data' / 'linear_b-greek.cog'
csv.field_size_limit(10 ** 9)
T0 = time.time()
def log(*a): print(f'[{time.time()-T0:7.1f}s]', *a, flush=True)
BIN, NSHUF, NDRAW, STEPS, CHAINS = 20, 1000, 5, 60000, 3
K = 0.1; LN2 = math.log(2)

# ---------------- alphabet collapse (PROTOCOL §Alphabet) ----------------
def keep(s): return re.sub(r'[^a-zA]', '', s)
SLP = dict(a='a', A='A', i='i', I='i', u='u', U='u', f='ri', F='ri', x='li', X='li', e='e', E='ai', o='o', O='au',
           k='k', K='k', g='g', G='g', N='n', c='c', C='c', j='j', J='j', Y='n', w='t', W='t', q='d', Q='d', R='n',
           t='t', T='t', d='d', D='d', n='n', p='p', P='p', b='b', B='b', m='m', y='y', r='r', l='l', L='l', v='v',
           S='s', z='s', s='s', h='s', M='n', H='s')
def col_san(w): return keep(''.join(SLP.get(c, '') for c in w))
def strip_acc(s): return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
FIN = {'ä': 'a', 'ö': 'o', 'y': 'u', 'å': 'o', 'h': 's', 'f': 'p', 'c': 'k', 'q': 'k', 'w': 'v', 'x': 'ks', 'z': 's', 'š': 's', 'ž': 'j'}
def col_fin(w): return keep(''.join(FIN.get(c, c) for c in w.lower()))
def col_eus(w):
    w = w.lower(); w = re.sub(r't[xsz]', 'c', w); w = w.replace('ll', 'l').replace('rr', 'r')
    w = ''.join({'x': 's', 'z': 's', 'ñ': 'n', 'h': 's', 'f': 'p', 'w': 'v', 'ç': 's'}.get(c, c) for c in w)
    return keep(strip_acc(w))
GRK = {'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 's', 'η': 'e', 'θ': 't', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n',
       'ξ': 'ks', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'u', 'φ': 'p', 'χ': 'k', 'ψ': 'ps', 'ω': 'o', 'f': 'v', 'j': 'j'}
def col_grk(w): return keep(''.join(GRK.get(c, '') for c in strip_acc(w.lower())))
# round37 fingerprint.norm, copied (that module needs numpy and argv)
MAP37 = {'ǯ': 'j', 'ǰ': 'j', 'č': 'c', 'ć': 'c', 'ž': 's', 'ś': 's', 'ṣ': 's', 'ʃ': 's', 'ɕ': 's', 'š': 's', 'ʂ': 's', 'ŋ': 'n', 'ñ': 'n', 'ṅ': 'n', 'ɲ': 'n', 'ṇ': 'n', 'ɳ': 'n',
         'ɖ': 'd', 'ḍ': 'd', 'ʈ': 't', 'ṭ': 't', 'ɭ': 'l', 'ḷ': 'l', 'ɽ': 'r', 'ɾ': 'r', 'ṛ': 'r', 'ʀ': 'r', 'ə': 'a', 'ɐ': 'a',
         'æ': 'a', 'ä': 'a', 'ɛ': 'e', 'ɔ': 'o', 'ö': 'o', 'ø': 'o', 'ɪ': 'i', 'ɨ': 'i', 'ʊ': 'u', 'ü': 'u', 'ɟ': 'j', 'ʤ': 'j',
         'ʧ': 'c', 'ɣ': 'g', 'ɡ': 'g', 'β': 'b', 'ɸ': 'p', 'ð': 'd', 'θ': 't', 'χ': 'k', 'x': 'k', 'q': 'k', 'w': 'v', 'z': 's',
         'ʒ': 's', 'ʐ': 's', 'ɦ': 'h', 'ʰ': '', 'ʔ': '', 'ˀ': '', "'": '', 'ʼ': '', 'ː': '', ':': '', 'ḥ': 'h', 'ṁ': 'n', 'ṃ': 'n', 'y': 'y', 'f': 'p'}
def norm37(s):
    s = (s or '').lower(); out = []
    for ch in s:
        if ch in MAP37: out.append(MAP37[ch]); continue
        d = unicodedata.normalize('NFD', ch); out.append(MAP37.get(d[0], d[0]))
    s = ''.join(out); s = re.sub(r'[^a-z]', '', s); s = re.sub(r'([kgcjtdpb])h', r'\1', s); return s
def col_pdr(w):
    w = re.sub(r'\([^)]*\)', '', w); w = re.split(r'[,;/~]', w)[0]      # first alternative, optional segments dropped
    return keep(norm37(w).replace('h', 's'))
def skeleton(s): return re.sub(r'[aAeiou]', '', s)

# ---------------- lexicons ----------------
def load_lexicons():
    L = {}
    san = set()
    for line in open(LEX / 'mw.txt', encoding='utf-8'):
        m = re.search(r'<k1>([^<]+)<', line)
        if m: san.add(col_san(m.group(1)))
    L['Sanskrit'] = san
    L['Finnish'] = {col_fin(l.strip().lstrip('﻿')) for l in open(LEX / 'kaikkisanat.txt', encoding='utf-8') if l.strip()}
    eus = set()
    for l in list(open(LEX / 'eu.dic', encoding='utf-8'))[1:]:
        w = l.split('/')[0].strip()
        if w and not w.startswith('-'): eus.add(col_eus(w))
    L['Basque'] = eus
    pdr = set()
    for r in csv.DictReader(open(LAB / 'external' / 'dravidian_db_v1.1' / 'pdr_04.csv', encoding='utf-8')):
        if r['source_classification'] == 'Proto-Dravidian': pdr.add(col_pdr(r['reconstruction']))
    L['PDr'] = pdr
    L = {k: sorted(w for w in v if len(w) >= 2) for k, v in L.items()}
    return L

# ---------------- language model (round41 LM, stdlib) ----------------
class LM:
    def __init__(self, words, k=K):
        c3 = collections.Counter(); c2 = collections.Counter(); al = set('$')
        for w in words:
            s = '^^' + w + '$'; al |= set(w)
            for i in range(2, len(s)): c3[s[i-2:i+1]] += 1; c2[s[i-2:i]] += 1
        V = len(al); self.V = V
        self.lp3 = {t: math.log((n + k) / (c2[t[:2]] + k * V)) for t, n in c3.items()}
        self.lp2 = {ctx: math.log(k / (n + k * V)) for ctx, n in c2.items()}
        self.unk = math.log(1.0 / V)
    def lp(self, w):
        s = '^^' + w + '$'; t = 0.0; lp3 = self.lp3; lp2 = self.lp2; unk = self.unk
        for i in range(2, len(s)):
            tri = s[i-2:i+1]; v = lp3.get(tri)
            if v is None: v = lp2.get(tri[:2], unk)
            t += v
        return t
def bits_per_char(lm, readings):
    tot = sum(lm.lp(r) for r in readings); n = sum(len(r) + 1 for r in readings)   # +1 for the end symbol
    return -tot / LN2 / n

# ---------------- reading procedures ----------------
END = re.compile(r'([iu]|an|as)$'); VOW = re.compile(r'^[aiu]$')
def read_v(labels):                     # lipi index.vue xlitize(), reading order
    s = labels[0]
    for nxt in labels[1:]:
        if not END.search(s) and not VOW.match(nxt): s += 'a'
        s += nxt
    if not END.search(s): s += 'a'
    return s
def read_c(labels): return ''.join(skeleton(l.replace('an', 'n').replace('as', 's')) for l in labels)

# ---------------- corpus (round30 FC.TRAIN logic) ----------------
CORE = {'Inter-Riverine', 'Lower Indus', 'Gujarat/Kutch', 'Eastern Headwaters', 'Upper Indus'}
def load_corpus():
    rows = list(csv.DictReader((LAB / 'raw' / 'inscriptions.csv').open(encoding='utf-8')))
    types = collections.defaultdict(set); m304 = None
    for r in rows:
        if r['region'] not in CORE: continue
        if r['dir.'] not in ('R/L', 'L/R') or not re.fullmatch(r'\+\d{3}(?:-\d{3})+\+', r['text']): continue
        s = tuple(r['text'][1:-1].split('-'))
        if '000' in s: continue
        s = s[::-1] if r['dir.'] == 'R/L' else s
        types[s].add(r['id'])
        if r.get('cisi', '').strip(' <') == 'M-304': m304 = s
    return sorted(types), types, m304

# ---------------- shuffles ----------------
def freq_bins(texts, signs):
    f = collections.Counter(s for t in texts for s in t)
    order = sorted(signs, key=lambda s: (-f[s], s))
    return [order[i:i+BIN] for i in range(0, len(order), BIN)]
def shuffle_key(key, bins, rng, strata=True):
    new = dict(key)
    if strata:
        for b in bins:
            labs = [key[s] for s in b]; rng.shuffle(labs)
            for s, l in zip(b, labs): new[s] = l
    else:
        signs = [s for b in bins for s in b]; labs = [key[s] for s in signs]; rng.shuffle(labs)
        for s, l in zip(signs, labs): new[s] = l
    return new
def readings(texts, key, proc): return [proc([key[s] for s in t]) for t in texts]

def null_scores(texts, key, bins, lms, proc, seeds, strata=True):
    """lms: {name: [LM per draw]}. returns real S per language and list of shuffle S per language."""
    real = {L: sum(bits_per_char(lm, readings(texts, key, proc)) for lm in ms) / len(ms) for L, ms in lms.items()}
    shuf = {L: [] for L in lms}
    for i, sd in enumerate(seeds):
        k2 = shuffle_key(key, bins, random.Random(sd), strata); rd = readings(texts, k2, proc)
        for L, ms in lms.items(): shuf[L].append(sum(bits_per_char(lm, rd) for lm in ms) / len(ms))
        if (i + 1) % 200 == 0: log(f'   shuffle {i+1}/{len(seeds)}')
    return real, shuf
def summarize(real, shuf):
    out = {}
    for L in real:
        xs = shuf[L]; mu = sum(xs) / len(xs); sd = (sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5
        out[L] = dict(S=real[L], null_mean=mu, null_sd=sd, z=(mu - real[L]) / sd if sd else 0.0,
                      percentile=sum(x >= real[L] for x in xs) / len(xs), n_shuffles=len(xs))
    return out

# ---------------- fitted control (annealing over permutations of the key's own labels) ----------------
def fit_key(texts, key, lm, seed, steps=STEPS):
    rng = random.Random(seed); signs = sorted(key); labs = [key[s] for s in signs]; rng.shuffle(labs)
    k = dict(zip(signs, labs)); by = collections.defaultdict(list)
    for i, t in enumerate(texts):
        for s in set(t): by[s].append(i)
    cur = [lm.lp(read_v([k[s] for s in t])) for t in texts]; total = sum(cur)
    for step in range(steps):
        T = 3.0 + (0.05 - 3.0) * step / steps
        a, b = rng.sample(signs, 2)
        if k[a] == k[b]: continue
        k[a], k[b] = k[b], k[a]
        rows = set(by[a]) | set(by[b]); nv = {i: lm.lp(read_v([k[s] for s in texts[i]])) for i in rows}
        d = sum(nv.values()) - sum(cur[i] for i in rows)
        if d >= 0 or rng.random() < math.exp(d / T):
            for i, v in nv.items(): cur[i] = v
            total += d
        else: k[a], k[b] = k[b], k[a]
    return k, total

# ---------------- Linear B controls (round32 geometry) ----------------
def lb_data():
    rows = [l.rstrip('\n').split('\t') for l in COG.open(encoding='utf-8')][1:]
    words = [[unicodedata.name(c).split()[-1] for c in lb] for lb, _ in rows]
    greek = [g.split('|') if g != '_' else [] for _, g in rows]
    return words, greek
def lb_value(syl): return keep(re.sub(r'\d', '', syl.lower()).replace('w', 'v'))
def lb_build(words, idx, target, group):
    rng = random.Random(32001); rngh = random.Random(32002); rngg = random.Random(32003)
    VALUES = sorted({s for w in words for s in w}); freq = collections.Counter(s for i in idx for s in words[i])
    signs_of = {v: 1 for v in VALUES}
    if target:
        tot = sum(freq.values())
        for v in VALUES: signs_of[v] = max(1, min(11, round(target * freq[v] / tot))) if freq[v] else 1
    ids = [(v, j) for v in VALUES for j in range(signs_of[v])]; rng.shuffle(ids)
    sid = {x: f'L{n:03d}' for n, x in enumerate(ids)}; truth = {sid[x]: lb_value(x[0]) for x in ids}
    texts = []; order = list(idx); rngg.shuffle(order)
    if group:
        while order:
            k = rngg.choice([1, 2, 3]); texts.append([s for i in order[:k] for s in words[i]]); order = order[k:]
    else: texts = [words[i] for i in order]
    enc = sorted({tuple(sid[(s, rngh.randrange(signs_of[s]))] for s in t) for t in texts})
    return enc, truth

def main():
    out = dict(protocol='PROTOCOL.md', bin=BIN, n_shuffles=NSHUF, n_draws=NDRAW, steps=STEPS, chains=CHAINS)
    log('loading lexicons'); LX = load_lexicons()
    out['lexicon_sizes'] = {k: len(v) for k, v in LX.items()}; log('lexicon types', out['lexicon_sizes'])
    key = json.load(open(LAB / 'round46-brahmi-coverage' / 'expanded-map.json'))
    TRAIN, types, m304 = load_corpus(); kept = [t for t in TRAIN if all(s in key for s in t)]
    out['corpus'] = dict(train_types=len(TRAIN), kept=len(kept), dropped_unlabelled=len(TRAIN) - len(kept), tokens=sum(len(t) for t in kept))
    signs = sorted({s for t in kept for s in t}); ksub = {s: key[s] for s in signs}; bins = freq_bins(kept, signs)
    out['corpus']['sign_types'] = len(signs); density = out['corpus']['tokens'] / len(signs); out['corpus']['tokens_per_sign'] = density; log('corpus', out['corpus'])
    # ---- positive controls ----
    words, greek = lb_data(); n = len(words); rs = random.Random(47301); idx = list(range(n)); rs.shuffle(idx)
    halfA, halfB = idx[:n // 2], idx[n // 2:]
    pc2_target = round(sum(len(words[i]) for i in halfB) / density); out['pc2_target_ids'] = pc2_target
    grk = sorted({col_grk(g) for i in halfA for g in greek[i] if len(col_grk(g)) >= 2})
    pc_size = min(len(grk), *(len(v) for v in LX.values())); out['pc_lexicon_size'] = pc_size; log('PC lexicon size', pc_size, 'greek types', len(grk))
    def draws(lex, size): return [LM(random.Random(47101 + d).sample(lex, size)) if size < len(lex) else LM(lex) for d in range(NDRAW)]
    pc_lms = {'Greek': draws(grk, pc_size)}; pc_lms.update({L: draws(v, pc_size) for L, v in LX.items()})
    out['positive_controls'] = {}
    for name, tgt, grp in (('PC1', 0, False), ('PC2', pc2_target, True), ('PC2b', 400, True)):
        texts, truth = lb_build(words, halfB, tgt, grp); psigns = sorted(truth); pbins = freq_bins(texts, psigns)
        log(f'{name}: {len(texts)} texts, {len(psigns)} sign ids, {sum(len(t) for t in texts)} tokens')
        real, shuf = null_scores(texts, truth, pbins, pc_lms, lambda labs: ''.join(labs), range(47201, 47201 + NSHUF))
        summ = summarize(real, shuf); zg = summ['Greek']['z']
        passed = summ['Greek']['percentile'] >= 0.99 and all(zg - summ[L]['z'] >= 2 for L in summ if L != 'Greek')
        out['positive_controls'][name] = dict(texts=len(texts), sign_ids=len(psigns), tokens=sum(len(t) for t in texts), scores=summ, passed=passed)
        log(name, 'PASS' if passed else 'FAIL', {L: round(v['z'], 2) for L, v in summ.items()})
    if not out['positive_controls']['PC1']['passed']:
        out['verdict'] = 'METHOD-FAIL'; json.dump(out, open(P / 'results.json', 'w'), indent=1); log('METHOD-FAIL; stopping'); return
    # ---- Indus ----
    size = min(len(v) for v in LX.values()); out['matched_lexicon_size'] = size
    lms_m = {L: draws(v, size) for L, v in LX.items()}; lms_f = {L: [LM(v)] for L, v in LX.items()}
    out['indus'] = {}
    for tag, proc, lms, strata in (('primary_PV_matched_strata', read_v, lms_m, True), ('PC_matched_strata', read_c, lms_m, True),
                                   ('PV_full_strata', read_v, lms_f, True), ('PV_matched_unrestricted', read_v, lms_m, False)):
        log('indus analysis', tag); real, shuf = null_scores(kept, ksub, bins, lms, proc, range(47201, 47201 + NSHUF), strata)
        out['indus'][tag] = summarize(real, shuf); log(tag, {L: (round(v['z'], 2), v['percentile']) for L, v in out['indus'][tag].items()})
    # ---- matched-budget fitted controls ----
    out['fitted'] = {}
    for L in ('Finnish', 'Basque', 'PDr', 'Sanskrit'):
        best = None
        for c in range(CHAINS):
            sd = 47401 + 3 * ['Finnish', 'Basque', 'PDr', 'Sanskrit'].index(L) + c
            k, obj = fit_key(kept, ksub, lms_m[L][0], sd); log(f'fit {L} chain {c} objective {obj:.1f}')
            if best is None or obj > best[1]: best = (k, obj, sd)
        real, shuf = null_scores(kept, best[0], bins, lms_m, read_v, range(47201, 47201 + NSHUF))
        out['fitted'][L] = dict(seed=best[2], objective=best[1], scores=summarize(real, shuf), key=best[0])
        log('fitted', L, {M: round(v['z'], 2) for M, v in out['fitted'][L]['scores'].items()})
    # ---- verdict ----
    pr = out['indus']['primary_PV_matched_strata']; zs = pr['Sanskrit']['z']; ps = pr['Sanskrit']['percentile']
    ctrl = ['Finnish', 'Basque', 'PDr']; pc2 = out['positive_controls']['PC2']['passed']
    if ps < 0.95: v = 'NULL'
    elif any(pr[L]['z'] >= zs - 2 for L in ctrl) or any(out['fitted'][L]['scores'][L]['z'] >= zs - 2 for L in ('Finnish', 'Basque')): v = 'ARTEFACT'
    elif pc2 and ps >= 0.99 and all(zs - pr[L]['z'] >= 2 for L in ctrl) and all(zs - out['fitted'][L]['scores'][L]['z'] >= 2 for L in ('Finnish', 'Basque')): v = 'SUPPORT'
    else: v = 'MIXED'
    out['verdict'] = v
    # ---- diagnostics ----
    def trace(t):
        labs = [ksub[s] for s in t]; rv = read_v(labs)
        return dict(signs=list(t), labels=labs, reading_PV=rv, reading_PC=read_c(labs), ids=sorted(types[t])[:5],
                    bits_per_char={L: round(bits_per_char(lms_f[L][0], [rv]), 3) for L in LX})
    diag = dict(M304=trace(m304) if m304 and m304 in types and all(s in key for s in m304) else 'M-304 not in kept corpus',
                every_190th=[trace(kept[i]) for i in range(0, len(kept), 190)])
    t7 = json.load(open(LAB / 'round46-brahmi-coverage' / 'table7-crosswalk.json'))
    anch = {i for r in t7 if r['status'] == 'unique font crosswalk' for i in r['candidate_ids']}
    sub = [t for t in kept if sum(s in anch for s in t) / len(t) >= 0.5]
    if len(sub) >= 20:
        real, shuf = null_scores(sub, ksub, bins, {'Sanskrit': lms_m['Sanskrit']}, read_v, range(47201, 47201 + NSHUF))
        diag['table7_subset'] = dict(texts=len(sub), anchored_ids=sorted(anch), scores=summarize(real, shuf))
    else: diag['table7_subset'] = dict(texts=len(sub), note='fewer than 20 texts; not scored')
    diag['sanskrit_refit_vs_author'] = dict(author_z=zs, refit_z=out['fitted']['Sanskrit']['scores']['Sanskrit']['z'])
    out['diagnostics'] = diag
    json.dump(out, open(P / 'results.json', 'w'), indent=1, ensure_ascii=False)
    with open(P / 'per_text.tsv', 'w') as f:
        f.write('text\treading_PV\treading_PC\t' + '\t'.join(f'bits_{L}' for L in LX) + '\n')
        for t in kept:
            labs = [ksub[s] for s in t]; rv = read_v(labs)
            f.write('-'.join(t) + '\t' + rv + '\t' + read_c(labs) + '\t' + '\t'.join(f'{bits_per_char(lms_f[L][0], [rv]):.3f}' for L in LX) + '\n')
    log('VERDICT', v)
if __name__ == '__main__': main()
