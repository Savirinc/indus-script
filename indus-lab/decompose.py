"""Exploratory disconnected-part decomposition of standardized glyphs, not photographs.
Run: OPENBLAS_NUM_THREADS=2 python decompose.py
Requires numpy, scipy, Pillow, fontTools. No meaning or sign identity inferred.
"""
import collections as C, json,pathlib
import numpy as np
from PIL import Image,ImageFont,ImageDraw
from scipy.ndimage import label,binary_fill_holes
from fontTools.ttLib import TTFont
ROOT=pathlib.Path(__file__).resolve().parent;OUT=ROOT/'components';OUT.mkdir(exist_ok=True)
def write(name,data):(OUT/name).write_text(json.dumps(data,indent=2))
def normalize(a):
    ys,xs=np.where(a);im=Image.fromarray((a[min(ys):max(ys)+1,min(xs):max(xs)+1]*255).astype('uint8'))
    im.thumbnail((28,28));c=Image.new('L',(32,32));c.paste(im,((32-im.width)//2,(32-im.height)//2));return (np.asarray(c)>100).reshape(-1)
def main():
    cat=json.load(open(ROOT/'expanded/catalogue.json'));fontpath=ROOT/'raw/sk_indus_script-webfont.ttf'
    cmap=TTFont(fontpath).getBestCmap();font=ImageFont.truetype(str(fontpath),160)
    parts=[];glyphs=[];masks=[]
    for row in cat:
        cps=[int(h,16) for h in row['font_codepoints'].split()]
        if not cps or any(c not in cmap for c in cps):continue
        txt=''.join(chr(c) for c in cps);box=font.getbbox(txt);im=Image.new('L',(box[2]-box[0]+8,box[3]-box[1]+8));ImageDraw.Draw(im).text((4-box[0],4-box[1]),txt,font=font,fill=255)
        a=np.asarray(im)>100;ys,xs=np.where(a)
        if not len(xs):continue
        a=a[min(ys):max(ys)+1,min(xs):max(xs)+1];labs,n=label(a,np.ones((3,3)))
        local=[]
        # Preserve every nonempty component, including small marks; flag rather than silently remove.
        for j in range(1,n+1):
            b=labs==j;yy,xx=np.where(b);bbox=[int(min(xx)),int(min(yy)),int(max(xx)+1),int(max(yy)+1)];holes,_=label(binary_fill_holes(b)&~b)
            p={'id':row['sign']+':'+str(j),'sign':row['sign'],'part':j,'bbox':bbox,'glyph_size':[a.shape[1],a.shape[0]],'area_pixels':int(b.sum()),'area_fraction':float(b.sum()/a.sum()),'holes':int(holes.max()),'tiny':int(b.sum())<8}
            parts.append(p);local.append(p);masks.append(normalize(b))
        nested=[]
        for outer in local:
            for inner in local:
                if outer is inner:continue
                x,y,z,w=outer['bbox'];i,j,k,l=inner['bbox']
                if x<i and y<j and z>k and w>l:nested.append([outer['id'],inner['id']])
        glyphs.append({'sign':row['sign'],'parts':len(local),'bbox_containment':nested,'tokens':row['tokens']})
        if row['sign']=='809':np.savez(OUT/'809_masks.npz',mask=a,labels=labs)
    matrix=np.array(masks,dtype=np.float32);areas=matrix.sum(axis=1);inter=matrix@matrix.T;ious=inter/(areas[:,None]+areas[None,:]-inter)
    neighbours=[]
    for i,p in enumerate(parts):
        candidates=np.argsort(-ious[i]);seen=set();best=[]
        for j in candidates:
            q=parts[j]
            if q['sign']==p['sign'] or q['sign'] in seen:continue
            seen.add(q['sign']);best.append({'part_id':q['id'],'sign':q['sign'],'iou':round(float(ious[i,j]),4)})
            if len(best)==5:break
        neighbours.append({'part_id':p['id'],'matches':best})
    # Build connected graph of high-similarity part templates. Components are candidate families only.
    parent=list(range(len(parts)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i in range(len(parts)):
        for j in np.flatnonzero(ious[i,i+1:]>=.85)+i+1:
            if parts[i]['holes']==parts[j]['holes']:
                a,b=find(i),find(int(j))
                if a!=b:parent[b]=a
    grouped=C.defaultdict(list)
    for i,p in enumerate(parts):grouped[find(i)].append(p['id'])
    clusters=sorted(grouped.values(),key=lambda x:(-len(x),x[0]))
    # Compare glyph-level component-family similarity with usage-context similarity.
    comp_index={part:ci for ci,cluster in enumerate(clusters) for part in cluster}
    bags=C.defaultdict(C.Counter)
    for p in parts:bags[p['sign']][comp_index[p['id']]]+=1
    ctxt=json.load(open(ROOT/'expanded/context_neighbours.json'));observations=[]
    for sign,near in ctxt.items():
        for q in near:
            other=q['sign']
            if sign not in bags or other not in bags:continue
            a,b=bags[sign],bags[other];keys=set(a)|set(b)
            score=sum(min(a[k],b[k]) for k in keys)/sum(max(a[k],b[k]) for k in keys)
            observations.append({'sign':sign,'context_neighbour':other,'context_cosine':q['similarity'],'component_bag_jaccard':score})
    write('glyph_parts.json',glyphs);write('parts.json',parts);write('part_neighbours.json',neighbours);write('candidate_part_families.json',clusters);write('component_context_comparison.json',observations)
    summary={'rendered_signs':len(glyphs),'connected_parts':len(parts),'single_connected_signs':sum(x['parts']==1 for x in glyphs),'multiple_connected_signs':sum(x['parts']>1 for x in glyphs),'candidate_part_families':len(clusters),'part_similarity_threshold':.85,'family_rule':'Transitive connected components of normalized-mask IoU >= .85 and same hole count; not equivalence classes of ancient sign identity.','sign809':next(x for x in glyphs if x['sign']=='809'),'matched_context_links':len(observations),'context_links_sharing_candidate_parts':sum(x['component_bag_jaccard']>0 for x in observations)}
    write('summary.json',summary);print(json.dumps(summary,indent=2));print(json.dumps([x for x in neighbours if x['part_id'].startswith('809:')],indent=2))
if __name__=='__main__':main()
