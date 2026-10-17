"""Optional: python index_book.py book.pdf > page_index.json. Requires PyMuPDF."""
import fitz,json,sys,re,hashlib
p=sys.argv[1]; d=fitz.open(p)
terms=['copper','impression','stratigraph','provenance','unicorn']
pages=[]
for i,page in enumerate(d):
    text=page.get_text()
    pages.append({'pdf_page':i+1,'text_chars':len(text),'keywords':{term:len(re.findall(re.escape(term),text,re.I)) for term in terms}})
print(json.dumps({'sha256':hashlib.sha256(open(p,'rb').read()).hexdigest(),'pages':pages},indent=2))
