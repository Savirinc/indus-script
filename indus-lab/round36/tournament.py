"""Round 36 rebus tournament. See PROTOCOL.md. Usage: python3 tournament.py <rebus_data dir> [chinese|indus]"""
import sys, csv, json, random, re, math, collections
from pathlib import Path
P = Path(__file__).resolve().parent
D = Path(sys.argv[1]); MODE = sys.argv[2] if len(sys.argv) > 2 else 'chinese'
LANGS = ['pdr', 'san', 'pmu', 'pkher', 'sat', 'unr', 'srb', 'khr', 'bsk', 'elx', 'sux', 'eus', 'fin', 'jpn', 'och']
CONTROLS = {'eus', 'fin', 'jpn'}
NUMS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
NPERM = 2000


def norm(s):
    return re.sub(r'[^a-z]', '', (s or '').lower())


def lang_words(code):
    w = {}
    for r in csv.DictReader(open(D / f'lang_{code}.tsv', encoding='utf-8'), delimiter='\t'):
        c, f = r['concept'].strip(), norm(r['form_ipa_or_simplified'])
        if c and f and c not in w: w[c] = f
    return w


def lev(a, b):
    p = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        q = [i]
        for j, y in enumerate(b, 1): q.append(min(p[j] + 1, q[j - 1] + 1, p[j - 1] + (x != y)))
        p = q
    return p[-1]


def sim(a, b):
    return 1 - lev(a, b) / max(len(a), len(b), 1)


def contexts(texts, signs):
    ctx = {s: collections.Counter() for s in signs}
    for t in texts:
        seq = ['<B>'] + list(t) + ['<E>']
        for i in range(1, len(seq) - 1):
            if seq[i] in ctx:
                ctx[seq[i]]['L' + seq[i - 1]] += 1; ctx[seq[i]]['R' + seq[i + 1]] += 1
    return ctx


def cos(a, b):
    num = sum(v * b.get(k, 0) for k, v in a.items())
    den = math.sqrt(sum(v * v for v in a.values()) * sum(v * v for v in b.values()))
    return num / den if den else 0.0


def rank(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(x, y):
    if len(x) < 3: return float('nan')
    rx, ry = rank(x), rank(y); mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def score(tags, words, ctx, seed):
    """tags: sign->concept. words: concept->form. Returns observed rho, percentile, n signs, n pairs."""
    S = [s for s in tags if tags[s] in words and sum(ctx[s].values()) > 0]
    if len(S) < 6: return dict(n_signs=len(S), rho=None, pct=None)
    pairs = [(a, b) for i, a in enumerate(S) for b in S[i + 1:]
             if tags[a] != tags[b] and not (tags[a] in NUMS and tags[b] in NUMS)]
    Dv = [cos(ctx[a], ctx[b]) for a, b in pairs]
    def rho_for(wmap):
        return spearman([sim(wmap[tags[a]], wmap[tags[b]]) for a, b in pairs], Dv)
    obs = rho_for(words)
    concepts = sorted({tags[s] for s in S}); num_c = [c for c in concepts if c in NUMS]; obj_c = [c for c in concepts if c not in NUMS]
    rng = random.Random(seed); null = []
    for _ in range(NPERM):
        perm = dict(words)
        for grp in (num_c, obj_c):
            vals = [words[c] for c in grp]; rng.shuffle(vals); perm.update(zip(grp, vals))
        null.append(rho_for(perm))
    pct = sum(v < obs for v in null) / NPERM
    return dict(n_signs=len(S), n_pairs=len(pairs), rho=obs, pct=pct)


def tournament(texts, tags, truth_words, label):
    ctx = contexts(texts, list(tags))
    res = {}
    langs = {c: lang_words(c) for c in LANGS}
    if truth_words: langs['TRUE'] = truth_words
    for code, w in langs.items():
        res[code] = score(tags, w, ctx, 36000)
    ranked = sorted([(v['pct'], k) for k, v in res.items() if v['pct'] is not None], reverse=True)
    print(f'== {label}: {len(texts)} texts, {sum(map(len, texts))} tokens, {len(tags)} tagged signs')
    for p, k in ranked: print(f'   {k:6s} pct={p:.3f} rho={res[k]["rho"]:+.3f} signs={res[k]["n_signs"]} pairs={res[k]["n_pairs"]}')
    return dict(label=label, texts=len(texts), tokens=sum(map(len, texts)), results=res, ranking=[k for _, k in ranked])


def chinese():
    lines = [l.strip() for l in open(D / 'chinese_corpus_trad.txt', encoding='utf-8') if l.strip()]
    freq = collections.Counter(ch for l in lines for ch in l)
    pic = list(csv.DictReader(open(D / 'chinese_pictographs.tsv', encoding='utf-8'), delimiter='\t'))
    out = {}
    def mk(rows):
        tags, truth = {}, {}
        for r in rows:
            mc = norm((r['mc_baxter_phonoml'] or '').split(';')[0])
            if r['char'] and mc and freq[r['char']] >= 5 and r['char'] not in tags:
                tags[r['char']] = r['concept']; truth.setdefault(r['concept'], mc)
        return tags, truth
    tags, truth = mk(pic)
    out['C-full'] = tournament(lines, tags, truth, 'C-full')
    keep = {'jar/pot', 'fish', 'man', 'arrow', 'bird', 'leaf', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight'}
    tags2, truth2 = mk([r for r in pic if r['concept'] in keep])
    rng = random.Random(36100); pool = lines[:]; rng.shuffle(pool); sub = []; n = 0
    while n < 8726: sub.append(pool.pop()); n += len(sub[-1])
    out['C-indus'] = tournament(sub, tags2, truth2, 'C-indus')
    out['C-indus-fullcorpus'] = tournament(lines, tags2, truth2, 'C-indus tags, full corpus (exploratory)')
    for k in ('C-full', 'C-indus'):
        r = out[k]; t = r['results']['TRUE']
        out[k]['PASS'] = bool(t['pct'] is not None and t['pct'] >= 0.95 and r['ranking'] and r['ranking'][0] == 'TRUE')
        print(k, 'PASS' if out[k]['PASS'] else 'FAIL')
    (P / 'chinese_control_results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False))


def indus():
    sys.path.insert(0, str(P.parent / 'round30'))
    import foreign_context as F
    tags = {}
    for l in open(P / 'indus_pictograph_tags.tsv'):
        if l.startswith('#') or not l.strip(): continue
        s, c, _ = l.rstrip('\n').split('\t'); tags[s] = c
    out = tournament([list(t) for t in F.TRAIN], tags, None, 'Indus')
    (P / 'indus_results.json').write_text(json.dumps(out, indent=2))


if __name__ == '__main__':
    chinese() if MODE == 'chinese' else indus()
