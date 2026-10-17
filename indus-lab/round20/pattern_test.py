from pathlib import Path
import csv,re,json,random,collections,hashlib
P=Path(__file__).resolve().parent; ROOT=P.parent
def pattern(seq):
    ids={};return tuple(ids.setdefault(s,len(ids)) for s in seq)
def evaluate(lines,words):
    lengths=collections.Counter(map(len,words)); pats=collections.Counter(pattern(w) for w in words)
    supported=[s for s in lines if lengths[len(s)]]
    counts=[pats[pattern(s)] for s in lines]
    hits=[c for c in counts if c]
    return dict(lines=len(lines),length_supported=len(supported),pattern_matches=len(hits),coverage=len(hits)/len(lines),mean_candidates_when_matched=sum(hits)/len(hits) if hits else None,uniquely_matching_lines=sum(c==1 for c in counts),word_types=len(words))
def main():
    a=ROOT/'raw/inscriptions.csv';b=ROOT/'round14/dravlex/cldf/forms.csv'
    records=list(csv.DictReader(a.open()));eligible=[];occ=[]
    for r in records:
        t=r['text'] or ''
        if re.fullmatch(r'\+\d{3}(?:[-/]\d{3})*\+',t) and '000' not in re.findall(r'\d{3}',t):
            eligible.append(r);occ.extend(tuple(s.split('-')) for s in t[1:-1].split('/'))
    lines=sorted(set(occ)); langs=collections.defaultdict(set)
    for r in csv.DictReader(b.open()):
        if r['Loan'].lower()=='false' and r['Segments'].strip() and r['Cognacy'].strip():
            w=tuple(s for s in r['Segments'].split() if s!='+')
            if w:langs[r['Language_ID']].add(w)
    results={l:{'stored':evaluate(lines,w),'reversed':evaluate([s[::-1] for s in lines],w)} for l,w in sorted(langs.items())}
    ta=sorted(langs['Tamil']);null=[]
    for seed in range(20000,20200):
        rng=random.Random(seed);words=[]
        for w in ta:
            q=list(w);rng.shuffle(q);words.append(tuple(q))
        null.append(evaluate(lines,set(words)))
    out=dict(input_hashes={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [a,b]},raw_records=len(records),eligible_records=len(eligible),excluded_records=len(records)-len(eligible),line_occurrences=len(occ),unique_lines=len(lines),unique_lines_no_repeated_sign=sum(len(set(s))==len(s) for s in lines),languages=results,tamil_shuffled=null,interpretation='Necessary local pattern compatibility only; no global key or translations inferred. Related languages and shuffled words are not language identification.')
    (P/'pattern_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ['languages','tamil_shuffled']},indent=2));print('Tamil',results['Tamil']);print('Null matches min/mean/max',min(x['pattern_matches'] for x in null),sum(x['pattern_matches'] for x in null)/len(null),max(x['pattern_matches'] for x in null))
if __name__=='__main__':main()
