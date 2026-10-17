"""Index embedded raster resolution; no claim to read all book contents."""
import fitz, json, argparse, hashlib
from pathlib import Path
from collections import Counter
p=argparse.ArgumentParser();p.add_argument('--pdf',required=True);a=p.parse_args()
doc=fitz.open(a.pdf);rows=[]
for i,page in enumerate(doc):
 images=page.get_images(full=True)
 if not images:
  rows.append({'pdf_page_1based':i+1,'image_count':0});continue
 im=max(images,key=lambda z:z[2]*z[3])
 rows.append({'pdf_page_1based':i+1,'image_count':len(images),'largest_image_xref':im[0],'largest_image_pixels':[im[2],im[3]],'ppi_if_image_fills_page':[round(im[2]/page.rect.width*72,2),round(im[3]/page.rect.height*72,2)],'printed_page':None,'objects_not_indexed':True})
out={'pdf_sha256':hashlib.sha256(Path(a.pdf).read_bytes()).hexdigest(),'pages':rows,'scope':'Raster metadata inventory, not object recognition, OCR, or a reading of the volume'}
Path(__file__).with_name('page-image-index.json').write_text(json.dumps(out,indent=2)+'\n')
print({'pages':len(rows),'horizontal_ppi_rounded':dict(Counter(round(r['ppi_if_image_fills_page'][0]) for r in rows if r['image_count']))})
