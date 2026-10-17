"""Full-snapshot sign census and exploratory pattern scan. Requires numpy, scipy, Pillow, fontTools."""
import csv, collections as C, json, pathlib, re, hashlib, math
import numpy as np
from scipy.spatial.distance import cdist
from scipy.ndimage import distance_transform_edt
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'expanded';OUT.mkdir(exist_ok=True)
def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False))
def bh(ps):
    idx=np.argsort(ps); out=np.ones(len(ps)); acc=1.
    for rank in range(len(ps),0,-1):
        i=idx[rank-1];acc=min(acc,ps[i]*len(ps)/rank);out[i]=acc
    return out
def tokens(t): return [str(int(x)) if int(x) not in (0,999) else None for x in re.findall(r'\d+',t)]
def main():
    source=list(csv.DictReader(open(ROOT/'raw/inscriptions.csv')))
    # Semantic suggestions are deliberately not ingested into the analysis.
    rows=[{k:v for k,v in r.items() if k not in ('sanskrit','translation','notes','class')} for r in source]
    counts=C.Counter();records=C.defaultdict(set);sites=C.defaultdict(C.Counter);types=C.defaultdict(C.Counter)
    known=[];gaps=0
    for r in rows:
        r['segments_visual']=[tokens(p) for p in r['text'].split('/')]
        all_tokens=[g for line in r['segments_visual'] for g in line]
        gaps+=all_tokens.count(None)
        counts.update(g for g in all_tokens if g is not None)
        for g in set(all_tokens)-{None}:
            records[g].add(r['id']);sites[g][r['site']]+=1;types[g][r['type']]+=1
        # Only declared right-to-left, entire intact lines, no unreadable sign.
        if r['dir.'].strip().upper()=='R/L' and r['complete']=='Y':
            for part,seq in zip(r['text'].split('/'),r['segments_visual']):
                if part.startswith('+') and part.endswith('+') and None not in seq and len(seq)>=2:
                    known.append((tuple(reversed(seq)),r))
    lines=sorted({s for s,r in known})
    positional=[];starts=C.Counter(s[0] for s in lines);ends=C.Counter(s[-1] for s in lines)
    # Exact Poisson-binomial null for terminal / initial membership under uniform line shuffling.
    for sign in sorted(counts,key=int):
        probs=[s.count(sign)/len(s) for s in lines if sign in s]
        pmf=np.array([1.])
        for p in probs:pmf=np.convolve(pmf,[1-p,p])
        for label,cc in [('initial',starts),('terminal',ends)]:
            n=cc[sign]; positional.append(dict(sign=sign,position=label,observed=n,expected=sum(probs),p_upper=float(pmf[n:].sum()),eligible_lines_with_sign=len(probs)))
    qs=bh([x['p_upper'] for x in positional])
    for x,q in zip(positional,qs):x['q_bh']=float(q)
    # Descriptive bigrams and contexts count each exact eligible line once.
    pairs=C.Counter();before=C.defaultdict(C.Counter);after=C.defaultdict(C.Counter)
    for s in lines:
        for a,b in zip(s,s[1:]):pairs[a,b]+=1;after[a][b]+=1;before[b][a]+=1
    pair_rows=[dict(left=a,right=b,distinct_line_occurrences=n) for (a,b),n in pairs.most_common()]
    catalogue=[]
    glyphs={r['glyph']:r['codepoints'] for r in csv.DictReader(open(ROOT/'raw/glyphs.tsv'),delimiter='\t')}
    for g in sorted(set(counts)|set(glyphs)-{'0','999'},key=int):
        catalogue.append(dict(sign=g,tokens=counts[g],records=len(records[g]),sites=dict(sites[g]),types=dict(types[g]),initial=starts[g],terminal=ends[g],before=dict(before[g]),after=dict(after[g]),font_codepoints=glyphs.get(g,'')))
    # Single substitutions preserve exact surrounding positions.
    families=C.defaultdict(list)
    for seq in lines:
        if 3<=len(seq)<=12:
            for i in range(len(seq)):families[(i,seq[:i]+('*',)+seq[i+1:])].append(seq)
    exchange=C.Counter();examples=C.defaultdict(list)
    for (i,context),seqs in families.items():
        for k,a in enumerate(seqs):
            for b in seqs[k+1:]:
                key=tuple(sorted((a[i],b[i]),key=int));exchange[key]+=1
                if len(examples[key])<5:examples[key].append({'position':i+1,'left':' '.join(a),'right':' '.join(b)})
    swaps=[dict(sign_a=a,sign_b=b,contexts=n,examples=examples[a,b]) for (a,b),n in exchange.most_common()]
    # Context similarity (cosine), with initial/final boundary markers; frequency >= 10 eligible lines.
    dims=sorted(set(counts),key=int);di={s:i for i,s in enumerate(dims)}
    eligible=[g for g in dims if sum(g in s for s in lines)>=10]
    matrix=np.zeros((len(eligible),2*len(dims)+2))
    for i,g in enumerate(eligible):
        for h,n in before[g].items():matrix[i,di[h]]=n
        for h,n in after[g].items():matrix[i,len(dims)+di[h]]=n
        matrix[i,-2:]=[starts[g],ends[g]]
    dist=cdist(np.sqrt(matrix),np.sqrt(matrix),'cosine');np.fill_diagonal(dist,np.inf)
    neighbours={g:[dict(sign=eligible[j],similarity=float(1-dist[i,j])) for j in np.argsort(dist[i])[:3]] for i,g in enumerate(eligible)}
    # Render every mapped font entry; normalized masks are derived templates, never artifact photos.
    fontpath=ROOT/'raw/sk_indus_script-webfont.ttf';cmap=TTFont(fontpath).getBestCmap();font=ImageFont.truetype(str(fontpath),100)
    masks=[];mapped=[];missing=[]
    for row in catalogue:
        g=row['sign']; cps=[int(c,16) for c in row['font_codepoints'].split()]
        if not cps or any(c not in cmap for c in cps):missing.append(g);continue
        txt=''.join(chr(c) for c in cps);box=font.getbbox(txt);im=Image.new('L',(max(1,box[2]-box[0]+8),max(1,box[3]-box[1]+8)))
        ImageDraw.Draw(im).text((4-box[0],4-box[1]),txt,font=font,fill=255)
        bb=im.getbbox()
        if not bb:missing.append(g);continue
        im=im.crop(bb);im.thumbnail((56,56));canvas=Image.new('L',(64,64));canvas.paste(im,((64-im.width)//2,(64-im.height)//2));a=np.asarray(canvas)>80
        masks.append(a.reshape(-1).astype(np.float32));mapped.append(g)
    m=np.array(masks);inter=m@m.T;areas=m.sum(axis=1);similar=inter/(areas[:,None]+areas[None,:]-inter);np.fill_diagonal(similar,-1)
    dt=np.array([distance_transform_edt(~a.reshape(64,64).astype(bool)).reshape(-1) for a in m],dtype=np.float32)
    directed=m@dt.T/areas[:,None];chamfer=(directed+directed.T)/2;np.fill_diagonal(chamfer,np.inf)
    shape={g:[dict(sign=mapped[j],mean_stroke_distance_pixels=float(chamfer[i,j]),iou=float(similar[i,j])) for j in np.argsort(chamfer[i])[:3]] for i,g in enumerate(mapped)}
    save('catalogue.json',catalogue);save('positional_tests.json',positional);save('bigrams.json',pair_rows);save('substitutions.json',swaps);save('context_neighbours.json',neighbours);save('shape_neighbours.json',shape)
    save('records.json',rows)
    summary=dict(source_rows=len(rows),source_id_stems=len({r['id'].split('.')[0] for r in rows}),sites=len({r['site'] for r in rows}),observed_sign_ids=len(counts),catalogue_entries=len(catalogue),font_templates_rendered=len(mapped),unrendered_ids=missing,legible_tokens=sum(counts.values()),unreadable_tokens=gaps,signs_with_one_token=sum(n==1 for n in counts.values()),eligible_distinct_lines=len(lines),position_tests=len(positional),position_tests_q_below_005=sum(x['q_bh']<.05 for x in positional),observed_bigrams=len(pairs),substitution_sign_pairs=len(swaps),substitution_context_edges=sum(exchange.values()),context_profile_signs=len(eligible),input_sha256=hashlib.sha256((ROOT/'raw/inscriptions.csv').read_bytes()).hexdigest())
    summary['unreadable_tokens']=sum(len(re.findall(r'(?<!\d)000(?!\d)',r['text'])) for r in rows)
    summary['separator_999_tokens']=sum(len(re.findall(r'(?<!\d)999(?!\d)',r['text'])) for r in rows)
    save('summary.json',summary)
    print(json.dumps(summary,indent=2));print('Top swaps',[(x['sign_a'],x['sign_b'],x['contexts']) for x in swaps[:8]])
    print('Top position effects',[(x['sign'],x['position'],x['observed'],round(x['expected'],1),x['q_bh']) for x in sorted(positional,key=lambda x:x['q_bh'])[:8]])
if __name__=='__main__':main()
