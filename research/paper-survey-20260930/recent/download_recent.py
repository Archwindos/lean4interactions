import json,urllib.request,hashlib,subprocess,concurrent.futures
from pathlib import Path
b=Path(__file__).parent
rows=json.loads((b/'arxiv-author-recent.json').read_text())
(b/'pdf').mkdir(exist_ok=True);(b/'text').mkdir(exist_ok=True);(b/'metadata').mkdir(exist_ok=True)
def fetch(r):
 vid=r['source_url'].rsplit('/',1)[1];pdf=b/'pdf'/(vid+'.pdf');url='https://arxiv.org/pdf/'+vid
 try:
  if not pdf.exists():
   data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read()
   if not data.startswith(b'%PDF'):raise ValueError('not_pdf')
   pdf.write_bytes(data)
  info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
  subprocess.run(['pdftotext','-layout',str(pdf),str(b/'text'/(vid+'.txt'))],check=True,capture_output=True)
  (b/'metadata'/(vid+'.pdfinfo.txt')).write_text(info)
  return dict(r,pdf_url=url,local_pdf=str(pdf),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),download_status='ok')
 except Exception as e:return dict(r,pdf_url=url,download_status='failed',error=repr(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 out=list(pool.map(fetch,rows))
(b/'downloads.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
for r in out:print(r['source_url'].rsplit('/',1)[1],r['download_status'],r.get('error',''),flush=True)
