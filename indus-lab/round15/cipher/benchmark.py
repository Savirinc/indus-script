from pathlib import Path
import csv,json,hashlib,time,collections
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
CONFIG=dict(seed_split=15101,seed_key=15102,seed_solver=15103,train_fraction=.8,restarts=6,proposals=15000,temperature_start=2.,temperature_end=.02,smoothing=.1,weights=[.1,.3,.6],random_baselines=100)
def words(rows,language):
 return [(r['Parameter_ID'],tuple(s for s in r['Segments'].split() if s!='+')) for r in rows if r['Language_ID']==language and r['Loan'].strip().lower()=='false' and r['Segments'].strip() and r['Cognacy'].strip()]
def make_model(reference,K):
 # Fixed non-substituted boundary symbol B; conditional trigram probability.
 B=K;C=K+1;alpha=CONFIG['smoothing'];uni=np.zeros(C);bi=np.zeros((C,C));tri=np.zeros((C,C,C))
 for w in reference:
  seq=[B,B]+list(w)+[B]
  for i in range(2,len(seq)):
   a,b,c=seq[i-2:i+1];uni[c]+=1;bi[b,c]+=1;tri[a,b,c]+=1
 pu=(uni+alpha)/(uni.sum()+alpha*C)
 pb=(bi+alpha)/(bi.sum(axis=1,keepdims=True)+alpha*C)
 pt=(tri+alpha)/(tri.sum(axis=2,keepdims=True)+alpha*C)
 logp=np.log(.1*pu[None,None,:]+.3*pb[None,:,:]+.6*pt)
 return logp,uni[:K]
def solve(cipher_training,reference,K,seed):
 # API has no key, target forms, concepts, alignments, or test inputs.
 rng=np.random.default_rng(seed);logp,reference_frequency=make_model(reference,K)
 grams=collections.Counter();cf=np.zeros(K)
 for w in cipher_training:
  for c in w:cf[c]+=1
  s=[K,K]+list(w)+[K]
  for j in range(2,len(s)):grams[tuple(s[j-2:j+1])]+=1
 g=np.array(list(grams),dtype=int);cnt=np.array(list(grams.values()))
 def score(m):return float(np.dot(logp[m[g[:,0]],m[g[:,1]],m[g[:,2]]],cnt))
 def random_map():return np.r_[rng.permutation(K),K]
 freq=np.arange(K+1);freq[np.argsort(-cf,kind='stable')]=np.argsort(-reference_frequency,kind='stable')
 baselines=[random_map() for _ in range(CONFIG['random_baselines'])]
 bscore=[score(m) for m in baselines];rb=baselines[int(np.argmax(bscore))]
 best=freq.copy();bestscore=score(best);traces=[];start=time.monotonic()
 for run in range(CONFIG['restarts']):
  m=freq.copy() if run==0 else random_map();cur=score(m);initial=cur;accepted=0;localbest=cur
  if cur>bestscore:bestscore=cur;best=m.copy()
  for step in range(CONFIG['proposals']):
   a,b=rng.choice(K,2,replace=False);m[a],m[b]=m[b],m[a];new=score(m)
   temp=CONFIG['temperature_start']*(CONFIG['temperature_end']/CONFIG['temperature_start'])**(step/(CONFIG['proposals']-1))
   if new>=cur or rng.random()<np.exp(min(0.,(new-cur)/temp)):
    cur=new;accepted+=1;localbest=max(localbest,new)
    if new>bestscore:bestscore=new;best=m.copy()
   else:m[a],m[b]=m[b],m[a]
  traces.append(dict(chain=run,initial_score=initial,final_score=cur,best_score=localbest,accepted=accepted))
 return dict(recovered=best,frequency=freq,random_best_score=rb,random_maps=baselines,trace=traces,training_score=bestscore,frequency_score=score(freq),random_best_training_score=max(bscore),runtime_seconds=time.monotonic()-start)
def evaluate(mapping,key_inverse,cipher_train,cipher_test,plain_test):
 seen=set(c for w in cipher_train for c in w);testtypes=set(c for w in cipher_test for c in w)
 decoded=[tuple(int(mapping[c]) for c in w) for w in cipher_test]
 total=sum(map(len,plain_test));correct=sum(a==b for w,v in zip(decoded,plain_test) for a,b in zip(w,v))
 seenpairs=[(mapping[c],p) for cw,pw in zip(cipher_test,plain_test) for c,p in zip(cw,pw) if c in seen]
 return dict(training_seen_key_types=len(seen),training_seen_key_correct=sum(mapping[c]==key_inverse[c] for c in seen),training_seen_key_accuracy=sum(mapping[c]==key_inverse[c] for c in seen)/len(seen),heldout_key_types=len(testtypes),heldout_key_correct=sum(mapping[c]==key_inverse[c] for c in testtypes),heldout_words=len(plain_test),heldout_exact_words=sum(a==b for a,b in zip(decoded,plain_test)),heldout_exact_word_accuracy=sum(a==b for a,b in zip(decoded,plain_test))/len(plain_test),heldout_tokens=total,heldout_correct_tokens=int(correct),heldout_token_accuracy=correct/total,heldout_tokens_with_training_seen_type=len(seenpairs),heldout_seen_type_token_accuracy=float(np.mean([a==b for a,b in seenpairs])))
def main():
 start=time.monotonic();src=ROOT/'round14/dravlex/cldf/forms.csv';rows=list(csv.DictReader(src.open()));ta=words(rows,'Tamil');ma=words(rows,'Malayalam')
 alphabet=sorted({s for _,w in ta+ma for s in w});ix={s:i for i,s in enumerate(alphabet)};K=len(alphabet)
 concepts=sorted({c for c,w in ta});rng=np.random.default_rng(CONFIG['seed_split']);rng.shuffle(concepts);trainc=set(concepts[:int(len(concepts)*CONFIG['train_fraction'])])
 train=sorted({tuple(ix[s] for s in w) for c,w in ta if c in trainc and w});test0={tuple(ix[s] for s in w) for c,w in ta if c not in trainc and w};test=sorted(test0-set(train))
 key=np.random.default_rng(CONFIG['seed_key']).permutation(K);inverse=np.argsort(key)
 enc=lambda ws:[tuple(int(key[s]) for s in w) for w in ws]
 ct=enc(train);ce=enc(test)
 # Independent seeded shuffle eliminates preprocessing concept/order hints.
 rng.shuffle(ct); references={l:sorted({tuple(ix[s] for s in w) for _,w in ls if w}) for l,ls in [('Malayalam',ma),('Tamil_positive_control',ta)]}
 # All fits finish before any hidden-answer scoring.
 fits={l:solve(ct,ref,K,CONFIG['seed_solver']+i) for i,(l,ref) in enumerate(references.items())}
 out=dict(protocol_sha256=hashlib.sha256((P/'protocol.md').read_bytes()).hexdigest(),raw_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),config=CONFIG,eligibility='Loan false, nonempty Segments and Cognacy; + delimiter removed; atomic remaining CLDF segments. Cognacy/Parameter_ID not solver inputs.',data=dict(eligible_Tamil_forms=len(ta),eligible_Malayalam_forms=len(ma),Tamil_concepts=len(concepts),train_concepts=len(trainc),test_concepts=len(concepts)-len(trainc),train_distinct_words=len(train),heldout_distinct_words=len(test),heldout_identical_to_training_removed=len(test0-set(test)),oracle_alphabet_size=K,reference_unique_words={l:len(r) for l,r in references.items()}),conditions={})
 for l,f in fits.items():
  ev={name:evaluate(f[name],inverse,ct,ce,test) for name in ['recovered','frequency','random_best_score']}
  randev=[evaluate(m,inverse,ct,ce,test) for m in f['random_maps']]
  out['conditions'][l]=dict(evaluations=ev,unselected_random_map_token_accuracy_mean=float(np.mean([e['heldout_token_accuracy'] for e in randev])),unselected_random_map_word_accuracy_mean=float(np.mean([e['heldout_exact_word_accuracy'] for e in randev])),trace=f['trace'],training_score=f['training_score'],frequency_score=f['frequency_score'],random_best_training_score=f['random_best_training_score'],runtime_seconds=f['runtime_seconds'],recovered_mapping={f'C{i:03}':alphabet[int(f['recovered'][i])] for i in range(K)})
 out['total_runtime_seconds']=time.monotonic()-start
 json.dump(out,(P/'results.json').open('w'),indent=2,default=lambda x:x.item())
 json.dump(dict(cipher_training=[[f'C{c:03}' for c in w] for w in ct],unaligned_references={l:[[alphabet[s] for s in w] for w in r] for l,r in references.items()},candidate_inventory=alphabet),(P/'solver_inputs.json').open('w'),indent=2)
 json.dump(dict(note='Evaluation harness only; not passed to solver.',key={f'C{i:03}':alphabet[int(inverse[i])] for i in range(K)},heldout_cipher=[[f'C{c:03}' for c in w] for w in ce],heldout_plaintext=[[alphabet[s] for s in w] for w in test]),(P/'evaluation_answers.json').open('w'),indent=2)
 print(json.dumps({l:v['evaluations'] for l,v in out['conditions'].items()},indent=2,default=lambda x:x.item()));print('RUNTIME',out['total_runtime_seconds'])
if __name__=='__main__':main()
