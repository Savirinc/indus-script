"""Exploratory sign400 test in fixed round09 representative groups; not a new discovery scan."""
from pathlib import Path
import csv,json,hashlib,collections,math
import numpy as np
from scipy.stats import fisher_exact,hypergeom
from scipy.optimize import brentq
from scipy.special import logsumexp
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
raw_path=ROOT/'raw/inscriptions.csv'
raw={r['id']:r for r in csv.DictReader(raw_path.open())}
rows=[]
for site in ['Harappa','Mohenjo-daro']:
 for r in json.load((ROOT/f'round09/predictions-{site}.json').open()):
  typ=raw[r['id']]['type']
  if typ not in ['TAB:B','SEAL:S']:continue
  rows.append(dict(id=r['id'],cisi=r['cisi'],site=site,type=typ,tablet=int(typ=='TAB:B'),sign400=int(400 in r['tokens']),length=len(r['tokens']),tokens=r['tokens']))
def table(rs):
 return [[sum(r['tablet']==y and r['sign400']==x for r in rs) for x in [1,0]] for y in [1,0]]
def strata(rs):
 d=collections.defaultdict(list)
 for r in rs:d[(r['site'],r['length'])].append(r)
 return [(k,table(v)) for k,v in sorted(d.items())]
def terms(rs):
 ts=[]
 for k,t in strata(rs):
  (a,b),(c,d)=t;n=a+b+c+d;m=a+b;ex=a+c
  lo=max(0,m+ex-n);hi=min(m,ex)
  support=np.arange(lo,hi+1)
  ts.append((k,t,support,hypergeom.logpmf(support,n,ex,m)))
 return ts

def distribution(ts,eta):
 pmf=np.array([1.]);off=0;expect=0.
 for _,_,ss,lp in ts:
  lp=lp+eta*ss;pp=np.exp(lp-logsumexp(lp));pmf=np.convolve(pmf,pp);off+=int(ss[0]);expect+=float(np.dot(ss,pp))
 return np.arange(off,off+len(pmf)),pmf,expect

def conditional(rs,ci=True):
 ts=terms(rs);obs=sum(t[0][0] for _,t,_,_ in ts)
 ss,pp,ex=distribution(ts,0.)
 pval=float(pp[np.abs(ss-ex)>=abs(obs-ex)-1e-10].sum())
 num=sum(t[0][0]*t[1][1]/np.sum(t) for _,t,_,_ in ts)
 den=sum(t[0][1]*t[1][0]/np.sum(t) for _,t,_,_ in ts)
 informative=[(k,t) for k,t,s,_ in ts if len(s)>1]
 ans=dict(exact_two_sided_p=min(1.,pval),observed_tablets_with_sign=obs,null_expected_tablets_with_sign=ex,mantel_haenszel_odds_ratio=num/den if den else None,informative_strata=len(informative),informative_groups=sum(sum(map(sum,t)) for _,t in informative))
 if ci:
  if obs==ss[0]:est=0.
  elif obs==ss[-1]:est=None
  else:est=math.exp(brentq(lambda z:distribution(ts,z)[2]-obs,-40.,40.))
  def tail(z,upper):
   s,p,_=distribution(ts,z);return float(p[s>=obs].sum() if upper else p[s<=obs].sum())
  low=0. if obs==ss[0] else math.exp(brentq(lambda z:tail(z,True)-.025,-40.,40.))
  high=None if obs==ss[-1] else math.exp(brentq(lambda z:tail(z,False)-.025,-40.,40.))
  ans.update(conditional_common_odds_ratio=est,conditional_exact_95pct_ci=[low,high])
 return ans

def summarize(rs,sensitivity=True):
 t=table(rs);fo,fp=fisher_exact(t)
 a,b=t[0];c,d=t[1]
 out=dict(groups=len(rs),table_rows_tablet_seal_cols_sign_present_absent=t,sign_rate_tablet=a/(a+b),sign_rate_seal=c/(c+d),unadjusted_odds_ratio=float(fo),fisher_two_sided_p=float(fp),length_conditioned=conditional(rs),strata=[dict(site=k[0],length=k[1],table=t) for k,t in strata(rs)])
 if sensitivity:
  loo=[]
  for i,r in enumerate(rs):
   x=conditional(rs[:i]+rs[i+1:],False);loo.append(dict(removed_id=r['id'],removed_cisi=r['cisi'],p=x['exact_two_sided_p'],mh_odds_ratio=x['mantel_haenszel_odds_ratio']))
  out['leave_one_representative_group_out']=dict(number=len(loo),maximum_p=max(loo,key=lambda a:a['p']),minimum_mh_odds_ratio=min(loo,key=lambda a:a['mh_odds_ratio']),all_p_below_05=all(r['p']<.05 for r in loo))
  out['leave_one_site_length_stratum_out']=[dict(removed_site=k[0],removed_length=k[1],**conditional([r for r in rs if (r['site'],r['length'])!=k],False)) for k,t in strata(rs) if sum(t[0]) and sum(t[1])]
 return out
result=dict(status='Exploratory follow-up: sign400 selected using previous round; p values are not selection-adjusted discovery evidence.',raw_sha256=hashlib.sha256(raw_path.read_bytes()).hexdigest(),contrast='Raw subtype TAB:B vs SEAL:S; corrected SEAL:R tablets are outside this contrast.',scope='Round09 retained deterministic representative rows, with original complete>=3-sign eligibility and duplicate exclusions. Not physical object census.',method='Exact conditional randomization given tablet count and sign400 count within each site and exact length; convolve hypergeometric distributions; two-sided tails by absolute departure of total tablet/sign overlap from null expectation. Common odds-ratio MLE/CI assumes common conditional effect; MH estimate descriptive. Leave-one representative equals leave-one exact multiset pattern here, not leave-one broader formula family.',by_site={s:summarize([r for r in rows if r['site']==s]) for s in ['Harappa','Mohenjo-daro']},pooled_site_length=summarize(rows))
json.dump(rows,(P/'analysis_rows.json').open('w'),indent=2)
json.dump(result,(P/'results.json').open('w'),indent=2)
for s,r in result['by_site'].items(): print(s,json.dumps({k:v for k,v in r.items() if k not in ['strata','leave_one_site_length_stratum_out']}))
print('POOLED',result['pooled_site_length']['length_conditioned'])
