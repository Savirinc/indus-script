"""Merge independent legibility assessments and create a portable review document."""
from pathlib import Path
import json, re, base64, html
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def norm(s):
 m=re.fullmatch(r'M[- ]?(\d+)[- ]?([AB])',s)
 if not m:raise ValueError(s)
 return f'M-{m[1]}-{m[2]}'
def write(n,v):(ROOT/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
faces=read('faces.json'); objects=read('objects.json'); imported=read('imported-assertions.json')
reviews={}
for name in ['a','b']:
 entries=read(f'reviewer-{name}.json'); reviews[name]={norm(r['face_id']):r for r in entries}
 assert len(reviews[name])==10 and set(reviews[name])=={f['face_id'] for f in faces}
joined={r['object_id'] for r in imported}; coverage=[];queue=[]
for o in objects:
 coverage.append({'object_id':o['object_id'],'csv_match':'exact catalogue ID' if o['object_id'] in joined else 'no exact match; independent relaxed alias search also found none','is_new_inscription':None})
for f in faces:
 fid=f['face_id']; rs=[reviews[n][fid] for n in ['a','b']]
 f['reviews']=[{'reviewer':n,**{k:v for k,v in reviews[n][fid].items() if k!='face_id'}} for n in ['a','b']]
 f['full_sequence_readability_agreement']=len({r['full_sequence_readable'] for r in rs})==1
 f['needs_better_image']=not all(r['full_sequence_readable'] for r in rs)
 f['consensus_status']='abstain: full sequence not readable' if all(not r['full_sequence_readable'] for r in rs) else 'requires reconciliation'
 # Never turn an imported sequence into a visual transcription.
 assert f['transcription'] is None
 queue.append({'face_id':fid,'priority':'first' if f['object_id']=='M-1547' else 'next','reason':'Resolve existing imported sequence and proposed paired-reverse constraint' if f['object_id']=='M-1547' else 'Resolve an unmatched catalogue object and its visible markings','requested_evidence':'higher-resolution original photo or independent early plate; retain catalogue caption and accession ID','no_model_filling':True})
write('reviewed-faces.json',faces);write('coverage.json',coverage);write('acquisition-queue.json',queue)
summary={'objects':len(objects),'faces':len(faces),'independent_visual_reviewers':2,'faces_with_two_abstentions':sum(all(not r['full_sequence_readable'] for r in f['reviews']) for f in faces),'exact_csv_matched_objects':len(joined),'unmatched_catalogue_objects':len(objects)-len(joined),'newly_deciphered_signs':0,'representative_sample':False,'independent_archaeological_validation':False}
write('pilot-summary.json',summary)
def data(path):
 p=ROOT/path;mime='image/jpeg' if p.suffix=='.jpg' else 'image/png'
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
def e(v):return html.escape(' '.join(map(str,v)) if isinstance(v,list) else str(v))
parts=['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CISI 2 — verified extraction pilot</title><style>
body{font:17px/1.55 system-ui,sans-serif;max-width:1120px;margin:auto;padding:32px;background:#f3f1eb;color:#182626}h1{font-size:38px;line-height:1.15}h2{margin:0}p{max-width:85ch}.note{border-left:4px solid #9a602c;padding:12px 18px;background:#fff8ec}.cards{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:white;padding:20px;border:1px solid #d3dad5;border-radius:10px}.photo{width:100%;height:260px;object-fit:contain;background:#eee;image-rendering:auto}.meta{font:13px/1.5 monospace;color:#40534c}.status{color:#8b4419;font-weight:650}summary{cursor:pointer}section{margin:36px 0}a{color:#176753}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #ccc} @media(max-width:700px){.cards{grid-template-columns:1fr}h1{font-size:29px}}</style>
<p>CISI VOLUME 2 · PILOT 01 · 10 OCTOBER 2026</p><h1>Five objects. Ten faces.<br>Uncertainty preserved.</h1>
<p>Native scan extraction and independent visual review of M-1543–M-1547, printed page 226 / PDF page 261. This is a targeted difficult page, not a representative test of the whole volume.</p>
<p class="note"><strong>Result:</strong> 10 exact-pixel crops and 10 face records checked. Both reviewers abstained from complete transcription on every face. One object matches the existing CSV; four remain unmatched. No new reading or meaning is claimed.</p>
<p>Display enlargement adds no source detail. Source page: 805 × 1132 pixels, approximately 100 ppi. Images are unenhanced; crops preserve the decoded source pixels. Descriptions concern photograph visibility, not proof that a surface originally lacked marks.</p>''']
for o in objects:
 oid=o['object_id']; parts.append(f'<section><h2>{e(oid)}</h2><p>{"Exact CSV catalogue-ID match; imported readings remain unverified." if oid in joined else "No matching catalogue ID found in our current CSV, including a relaxed alias check. Not established as a new inscription."}</p><div class="cards">')
 for f in [r for r in faces if r['object_id']==oid]:
  parts.append(f'<article class="card"><h3>{e(f["face_id"])}</h3><img class="photo" alt="Unenhanced source crop {e(f["face_id"])}" src="{data(f["crop_image"])}"><p class="meta">Native crop {f["pixel_dimensions"][0]} × {f["pixel_dimensions"][1]} px · as published</p><p class="status">Complete transcription: unresolved</p>')
  for r in f['reviews']:
   parts.append(f'<details><summary>Reviewer {r["reviewer"].upper()}</summary><p>{e(r["visible_features"])}</p><p>{e(r["rationale"])}</p></details>')
  parts.append(f'<p class="meta">Parent coordinates: {f["bbox_xyxy_native_pixels"]}</p></article>')
 parts.append('</div>')
 if oid in joined:
  parts.append('<details><summary>Separate imported assertions — not image-derived ground truth</summary><p>Record suffixes are not assumed to identify printed A/B faces.</p><ul>')
  for r in imported:
   if r['object_id']==oid:parts.append(f'<li>Record {e(r["fields"]["id"])}: <code>{e(r["fields"]["text"])}</code>; direction label {e(r["fields"]["dir."])}</li>')
  parts.append('</ul></details>')
 parts.append('</section>')
parts.append(f'<section><h2>Intact parent page</h2><p>Use the printed captions to check face assignments. Five objects are not ten independent observations.</p><img style="width:100%;max-width:805px" alt="Intact CISI2 printed page226" src="{data("images/cisi2-pdf261-original.jpg")}"></section>')
parts.append('<section><h2>Next evidence request</h2><p>Prioritise clearer M-1547 A/B photographs and catalogue membership evidence. Then investigate M-1543–M-1546 identifiers. Do not fill unreadable regions from imported strings or proposed meanings.</p><p>Source: Shah and Parpola (eds.), <em>Corpus of Indus Seals and Inscriptions 2: Collections in Pakistan</em>, 1991. <a href="https://archive.org/download/corpus-vol-2_202409/CorpusVol2.pdf">Source scan</a>. Catalogue imagery retains its source rights; no open licence is asserted.</p><p>The companion bundle contains the reproducible extraction code, checksums, exact rectangles, separate imported assertions and review records. No model was trained and no generative restoration was performed.</p></section></html>')
(ROOT/'review.html').write_text(''.join(parts));print(json.dumps(summary))
