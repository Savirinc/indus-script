from pathlib import Path
import csv,json,re,collections,math,random,hashlib
P=Path(__file__).resolve().parent;src=P.parent/'raw/inscriptions.csv'
rows=list(csv.DictReader(src.open()));cities=['Harappa','Mohenjo-daro']
def collect(city,subset):
    out=collections.defaultdict(set)
    for r in rows:
        if r['site']!=city or (subset=='SEAL:S' and r['type']!='SEAL:S'):continue
        if r['dir.'] not in ['R/L','L/R'] or not re.fullmatch(r'\+\d{3}(?:-\d{3})+\+',r['text']):continue
        s=tuple(r['text'][1:-1].split('-'))
        if '000' in s:continue
        if r['dir.']=='R/L':s=s[::-1]
        out[s].add(r['cisi'])
    return out
def fit(train):
    counts=collections.Counter(x for s in train for x in s);counts['EOS']=len(train)
    vocab=set(counts)|{'UNK'};den=sum(counts.values())+.5*len(vocab)
    u={x:(counts[x]+.5)/den for x in vocab};big=collections.defaultdict(collections.Counter)
    for s in train:
        for a,b in zip(('BOS',)+s,s+('EOS',)):big[a][b]+=1
    return u,big,{a:sum(ct.values()) for a,ct in big.items()}
def evaluate(model,test,details=False):
    u,big,tot=model;v=set(u);acc={k:[0.,0.,0] for k in ['all','first','internal','end']};rec=[]
    for raw in test:
        s=tuple(x if x in v else 'UNK' for x in raw);bu=bb=0.
        for i,(a,b) in enumerate(zip(('BOS',)+s,s+('EOS',))):
            pu=u[b];pb=(big.get(a,{}).get(b,0)+5*pu)/(tot.get(a,0)+5)
            lu,lb=-math.log2(pu),-math.log2(pb);bu+=lu;bb+=lb
            kind='first' if i==0 else 'end' if i==len(s) else 'internal'
            for k in ['all',kind]:acc[k][0]+=lu;acc[k][1]+=lb;acc[k][2]+=1
        if details:rec.append(dict(text=raw,unigram_bits=bu,bigram_bits=bb,tokens=len(s)+1))
    out={k:dict(unigram_bits_per_token=a/n,bigram_bits_per_token=b/n,gain_bits_per_token=(a-b)/n,tokens=n) for k,(a,b,n) in acc.items()}
    return out,rec
def main():
    results=[];ledger=[];allpred=[]
    for subset in ['all','SEAL:S']:
        for source in cities:
            target=next(c for c in cities if c!=source);trainmap=collect(source,subset);testmap=collect(target,subset)
            train=sorted(trainmap);test=sorted(set(testmap)-set(trainmap));model=fit(train)
            actual,preds=evaluate(model,test,True);rev,_=evaluate(fit([s[::-1] for s in train]),test)
            shuffled=[]
            for seed in range(200):
                rng=random.Random(f'round27:{subset}:{source}:{seed}');seqs=[]
                for s in train:
                    t=list(s);rng.shuffle(t);seqs.append(tuple(t))
                sc,_=evaluate(fit(seqs),test);shuffled.append({k:d['bigram_bits_per_token'] for k,d in sc.items()})
            summary={}
            for k in actual:
                vals=[s[k] for s in shuffled];summary[k]=dict(mean=sum(vals)/len(vals),minimum=min(vals),maximum=max(vals),controls_at_least_as_good=sum(x<=actual[k]['bigram_bits_per_token'] for x in vals),controls=len(vals))
            vocab=set(model[0]);signs=[x for s in test for x in s]
            results.append(dict(subset=subset,source=source,target=target,train_types=len(train),target_types_before_exclusion=len(testmap),shared_types_excluded=len(set(testmap)&set(trainmap)),test_types=len(test),test_sign_tokens=len(signs),unknown_test_sign_tokens=sum(x not in vocab for x in signs),actual=actual,reversed_source=rev,shuffle=summary))
            ledger.append(dict(subset=subset,source=source,target=target,train=[dict(text=s,objects=sorted(trainmap[s])) for s in train],test=[dict(text=s,objects=sorted(testmap[s])) for s in test]))
            allpred.append(dict(subset=subset,source=source,target=target,predictions=preds))
            print(subset,source,'->',target,len(train),len(test),actual['internal'],flush=True)
    out=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),conditions=results)
    for name,data in [('results',out),('split_ledger',ledger),('predictions',allpred)]:
        (P/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
