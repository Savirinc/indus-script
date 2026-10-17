"""Extract a bounded CISI2 pilot without inventing or enhancing image evidence.
Requires PyMuPDF and Pillow. Run with --pdf and --corpus; outputs beside script.
"""
from pathlib import Path
import argparse, hashlib, json, csv, io
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parent
SOURCE='https://archive.org/download/corpus-vol-2_202409/CorpusVol2.pdf'
# Manual object rectangles in ORIGINAL embedded JPEG coordinates, x0,y0,x1,y1.
# Half-open bounds, top-left origin. Captions remain in the intact parent image.
BOXES={
 'M-1543-A':[75,120,351,324], 'M-1543-B':[451,119,724,326],
 'M-1544-A':[74,388,371,636], 'M-1544-B':[436,388,729,636],
 'M-1545-A':[39,695,223,844], 'M-1545-B':[277,691,459,844],
 'M-1546-A':[508,697,614,823], 'M-1546-B':[656,697,768,823],
 'M-1547-A':[93,909,355,1046], 'M-1547-B':[436,909,699,1050],
}

def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--pdf',required=True);ap.add_argument('--corpus',required=True);a=ap.parse_args()
 pdf=Path(a.pdf); cb=Path(a.corpus); doc=fitz.open(pdf); page=doc[260]
 ims=page.get_images(full=True)
 assert len(ims)==1, 'Recheck source image layout before using fixed rectangles'
 im=ims[0]; data=doc.extract_image(im[0]); assert (data['width'],data['height'])==(805,1132)
 assert sha(pdf.read_bytes())=='727132579a485ee626e48a64c663148a85fbc0811fb523818fd615231f8a327d','Source changed'
 (ROOT/'images').mkdir(exist_ok=True)
 original=ROOT/'images/cisi2-pdf261-original.jpg';original.write_bytes(data['image'])
 img=Image.open(io.BytesIO(data['image'])).convert('RGB'); faces=[]
 for fid,box in BOXES.items():
  crop=img.crop(box); target=ROOT/'images'/f'{fid}.png';crop.save(target)
  # PNG must preserve the exact decoded source pixels: no resizing/filtering.
  assert Image.open(target).convert('RGB').tobytes()==crop.tobytes()
  obj,face=fid.rsplit('-',1)
  faces.append({'face_id':fid,'object_id':obj,'catalogue_face_label':face,'source_id':'CISI2-1991-scan',
    'pdf_page_1based':261,'printed_page':'226','source_image':'images/cisi2-pdf261-original.jpg',
    'crop_image':str(target.relative_to(ROOT)),'bbox_xyxy_native_pixels':box,
    'pixel_dimensions':list(crop.size),'crop_sha256':sha(target.read_bytes()),
    'orientation':'as published; no rotation or mirroring','reading_direction':None,
    'transcription':None,'transcription_status':'not independently recovered',
    'missing_or_unreadable_is_not_blank':True,'segmentation':None,
    'catalogue_link_method':'manual pairing of printed A/B captions; not physical-object authentication',
    'production_family_id':None,'group_membership_verified':False})
 safe=['id','cisi','site','excavation-idno','material','type','preservation','condition','sides','dir.','text length','signs','horizontal(mm)','vertical(mm)','text']
 objects=sorted({x['object_id'] for x in faces}); claims=[]
 with cb.open(newline='') as f:
  for row in csv.DictReader(f):
   if row['cisi'].strip() in objects:
    claims.append({'object_id':row['cisi'].strip(),'source':'field-cady-derived CSV already used in lab',
      'source_csv_sha256':sha(cb.read_bytes()),'status':'imported assertions; not photo-verified',
      'face_assignment':None,'face_assignment_note':'decimal record suffix is not assumed equivalent to printed A/B',
      'fields':{k:row.get(k) for k in safe}})
 write('faces.json',faces)
 write('objects.json',[{'object_id':o,'face_ids':[f'{o}-A',f'{o}-B'],'catalogue_page':226,'site_as_catalogued':'Mohenjo-daro','object_type_as_catalogued':'incised copper tablet','manufacturing_independence':'unknown','selected_by':'all five objects on one targeted page; not representative sample'} for o in objects])
 write('imported-assertions.json',claims)
 write('source.json',{'source_id':'CISI2-1991-scan','url':SOURCE,'pdf_sha256':sha(pdf.read_bytes()),'pdf_pages':len(doc),'embedded_image_xref':im[0],'embedded_image_sha256':sha(data['image']),'pixel_dimensions':[805,1132],'pdf_page_1based':261,'printed_page':226,'ppi':[round(im[2]/page.rect.width*72,2),round(im[3]/page.rect.height*72,2)],'scope':'One targeted page only','operations':'Exact embedded JPEG extraction; lossless rectangular crops of decoded RGB pixels; no enhancement','rights':'Published catalogue imagery; public access does not establish an open licence. No whole book redistributed.'})
 checks={'source_hash_matches':True,'faces':len(faces),'objects':len(objects),'all_faces_have_unique_ids':len({x['face_id'] for x in faces})==len(faces),'every_object_has_A_and_B':all({x['catalogue_face_label'] for x in faces if x['object_id']==o}=={'A','B'} for o in objects),'lossless_crop_pixel_checks_passed':len(faces),'imported_assertion_rows':len(claims),'photographically_verified_sign_sequences':0,'scope_note':'Integrity checks validate extraction and identifiers, not readability, meanings or archaeological independence.'}
 assert all(checks[k] for k in ['all_faces_have_unique_ids','every_object_has_A_and_B'])
 write('validation.json',checks);print(json.dumps(checks))

if __name__=='__main__':main()
