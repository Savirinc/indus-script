"""Round 35: can Gulf round seals be read as attested Gulf-period names better than as fake names? See PROTOCOL.md."""
import json, random, sys, collections, hashlib
from pathlib import Path
P = Path(__file__).resolve().parent

NAMES = ["na-na-za", "sa-ma-ar", "a-li-a-hi", "ma-ni-um", "na-du-be-li", "we-du-um", "a-tu", "ri-mu-um", "ia-ag-li-il",
         "su-mu-le-il", "u-la-pa-ni-pa", "sa-mu-a", "ri-ip-qa-tum", "sa-ri-tam-bi", "pa-qa-da", "a-ba-si-di-a", "ha-din-il",
         "ia-ta-ra-tim", "te-em-en-za-ag", "mi-il-ki-il", "in-za-ak-ga-mil", "i-din-nin-in-za-ak", "in-za-ki", "ku-un-in-za-ki",
         "ia-mi-u", "in-za-ak", "pa-ni-pa"]
NAMES = [tuple(n.split('-')) for n in NAMES]
# reading order as stored after R/L reversal (round30 groups) + Dilmun seal from Bourdeau gulf.md
SEALS = {"2153.1": "091-840-413-831", "3863.1": "160-090-055-060-190", "3897.1": "528-220-924-340-093",
         "3898.1": "415-803-001-328-004-002", "5227.1": "091-031-455-220", "5228.1": "091-032-001-033",
         "5229.1": "055-220-091-001-093-031", "5232.1": "055-099-121-055-831-031-071", "Dilmun(B)": "415-803-001-717-354"}
SEALS = {k: tuple(v.split('-')) for k, v in SEALS.items()}
STROKES = {"001", "002", "003", "004", "031", "032", "033"}


def candidates(seal, pool):
    """All (assignments) by which seal reads as a name: contiguous run, either direction, covering >=60% of signs."""
    out = []
    for seq in {seal, seal[::-1]}:
        n = len(seq)
        for name in set(pool):
            k = len(name)
            if k < 2 or k > n or k < 0.6 * n: continue
            for i in range(n - k + 1):
                run = seq[i:i + k]; a = {}
                ok = True
                for s, y in zip(run, name):
                    if a.get(s, y) != y: ok = False; break
                    a[s] = y
                if ok: out.append(a)
    # dedupe
    uniq = {tuple(sorted(a.items())) for a in out}
    return [dict(u) for u in uniq]


def best(seals, pool):
    """Exact max number of seals readable with one consistent key (backtracking, seals ordered by fewest candidates)."""
    cands = [candidates(s, pool) for s in seals]
    order = sorted(range(len(seals)), key=lambda i: len(cands[i]))
    cands = [cands[i] for i in order]
    bestv = [0]; n = len(cands)
    def rec(i, key, got):
        if got + (n - i) <= bestv[0]: return
        if i == n: bestv[0] = max(bestv[0], got); return
        for a in cands[i]:
            if all(key.get(s, y) == y for s, y in a.items()):
                added = [s for s in a if s not in key]
                for s in added: key[s] = a[s]
                rec(i + 1, key, got + 1)
                for s in added: del key[s]
                if bestv[0] == n: return
        rec(i + 1, key, got)
    rec(0, {}, 0)
    return bestv[0]


def fake_pool(rng):
    syl = [y for n in NAMES for y in n]
    return [tuple(rng.choice(syl) for _ in n) for n in NAMES]


def test(seals, nfake=200, seed=35001):
    sr = best(seals, NAMES)
    fakes = [best(seals, fake_pool(random.Random(seed + i))) for i in range(nfake)]
    p = (1 + sum(f >= sr for f in fakes)) / (1 + nfake)
    return dict(S_real=sr, n_seals=len(seals), fake_mean=sum(fakes) / nfake, fake_max=max(fakes),
                fake_dist=dict(collections.Counter(fakes)), p=p)


def synthetic(rng, lens, nsign):
    syls = sorted({y for n in NAMES for y in n}); ids = [f"S{i:03d}" for i in range(nsign)]
    key = {y: rng.choice(ids) for y in syls}
    out = []
    for L in lens:
        nm = rng.choice([n for n in NAMES if len(n) <= L and len(n) >= 0.6 * L] or NAMES)
        seq = [key[y] for y in nm]
        while len(seq) < L:
            f = rng.choice(ids); seq = [f] + seq if rng.random() < .5 else seq + [f]
        out.append(tuple(seq))
    return out


def main():
    res = {}
    sets = {"primary": list(SEALS.values()),
            "drop_5228": [v for k, v in SEALS.items() if k != "5228.1"],
            "drop_strokes": [tuple(x for x in v if x not in STROKES) for v in SEALS.values() if len([x for x in v if x not in STROKES]) >= 2]}
    for name, seals in sets.items():
        res[name] = test(seals); print(name, json.dumps(res[name]), flush=True)
    # power
    lens = [len(v) for v in SEALS.values()]; nsign = len({x for v in SEALS.values() for x in v})
    rng = random.Random(35500); hits = 0; detail = []
    for r in range(100):
        syn = synthetic(rng, lens, nsign); t = test(syn, nfake=100, seed=36000 + r * 1000)
        hits += t["p"] < 0.05; detail.append((t["S_real"], round(t["fake_mean"], 2), t["p"]))
    res["power"] = dict(share_p_lt_0_05=hits / 100, examples=detail[:15]); print("power", hits / 100, detail[:10], flush=True)
    pw = res["power"]["share_p_lt_0_05"]; p = res["primary"]["p"]
    res["decision"] = ("NON-INFORMATIVE (power<0.5)" if pw < .5 else "SUPPORT" if p < .05 else "NO SUPPORT" if p > .2 else "INCONCLUSIVE")
    print("DECISION", res["decision"])
    (P / "results.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
