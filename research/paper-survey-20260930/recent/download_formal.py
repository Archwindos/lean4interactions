import concurrent.futures, hashlib, json, pathlib, re, subprocess, urllib.request
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[2]
ITEMS=[
 ('iclr2024-sparse','https://openreview.net/forum?id=3pWSL8My6B','https://openreview.net/pdf?id=3pWSL8My6B','2305.01939'),
 ('iclr2024-generalizable','https://openreview.net/forum?id=OCqyFVFNeF','https://openreview.net/pdf?id=OCqyFVFNeF','2401.16318'),
 ('icml2023-bayesian','https://proceedings.mlr.press/v202/ren23a.html','https://proceedings.mlr.press/v202/ren23a/ren23a.pdf','2302.13095'),
 ('icml2024-layerwise','https://proceedings.mlr.press/v235/cheng24b.html','https://raw.githubusercontent.com/mlresearch/v235/main/assets/cheng24b/cheng24b.pdf','2409.08712'),
 ('aaai2024-generalization','https://ojs.aaai.org/index.php/AAAI/article/view/29655','https://ojs.aaai.org/index.php/AAAI/article/download/29655/31115','2302.13091'),
 ('acl2024-semantic-heads','https://aclanthology.org/2024.findings-acl.412/','https://aclanthology.org/2024.findings-acl.412.pdf','2402.13055'),
]

def request(url):
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read()

def fetch(item):
 key,source,pdfurl,aid=item
 out={'id':key,'source_url':source,'pdf_url':pdfurl,'arxiv_id':aid}
 try:
  pdf=BASE/'pdf'/f'{key}.pdf'
  if not pdf.exists():
   data=request(pdfurl)
   if not data.startswith(b'%PDF'):raise ValueError('Not PDF')
   pdf.write_bytes(data)
  info=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True,check=True).stdout
  (BASE/'metadata'/f'{key}.pdfinfo.txt').write_text(info)
  n=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
  subprocess.run(['pdftotext','-layout',str(pdf),str(BASE/'text'/f'{key}.txt')],check=True)
  pages=[]
  for p in range(1,n+1):
   text=subprocess.run(['pdftotext','-layout','-f',str(p),'-l',str(p),str(pdf),'-'],capture_output=True,text=True,check=True).stdout
   pages.append({'page':p,'text':text})
  (BASE/'text'/f'{key}.pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n')
  out.update(local_pdf=str(pdf.relative_to(ROOT)),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),total_pages=n,download_status='ok')
  try:
   landing=request(source)
   (BASE/'metadata'/f'{key}.landing.html').write_bytes(landing)
   out['local_landing']=str((BASE/'metadata'/f'{key}.landing.html').relative_to(ROOT))
  except Exception as exc:out['landing_error']=repr(exc)
 except Exception as exc:out.update(download_status='failed',error=repr(exc))
 print(key,out['download_status'],out.get('total_pages'),out.get('error',''),flush=True)
 return out

if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  rows=list(pool.map(fetch,ITEMS))
 (BASE/'formal-downloads.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
