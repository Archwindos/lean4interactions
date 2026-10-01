"""Acquire venue-hosted accepted papers; arXiv is never a fallback here."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json
from complete_acquisition import get,extract
ROOT=Path(__file__).resolve().parent
HTML={
 'transferability-iclr2021':'https://openreview.net/forum?id=X76iqnUbBjz',
 'dropout-iclr2021':'https://openreview.net/forum?id=Jacdvfjicf7',
 'complex-privacy-iclr2020':'https://openreview.net/forum?id=SHDG97ukaIH',
 'bottleneck-iclr2022':'https://openreview.net/forum?id=iRCUlgmdfHJ',
 'discarding-icml2022':'https://proceedings.mlr.press/v162/ma22b.html',
 'graph-iccv2015':'https://openaccess.thecvf.com/content_iccv_2015/html/Zhang_Mining_And-Or_Graphs_ICCV_2015_paper.html',
 'quaternion-eccv2020':'https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/3539_ECCV_2020_paper.php',
}
PDF={
 'bn-aaai2024':['https://ojs.aaai.org/index.php/AAAI/article/download/29978/31715'],
 'advtrain-aaai2024':['https://ojs.aaai.org/index.php/AAAI/article/download/29032/29956'],
 'robustness-neurips2021-main':['https://papers.nips.cc/paper/2021/file/1f4fe6a4411edc2ff625888b4093e917-Paper.pdf'],
 'robustness-neurips2021-supp':['https://papers.nips.cc/paper/2021/file/1f4fe6a4411edc2ff625888b4093e917-Supplemental.pdf'],
 'discarding-icml2022':['https://proceedings.mlr.press/v162/ma22b/ma22b.pdf'],
 'graph-iccv2015-main':['https://openaccess.thecvf.com/content_iccv_2015/papers/Zhang_Mining_And-Or_Graphs_ICCV_2015_paper.pdf'],
}
for key,oid in [('transferability-iclr2021','X76iqnUbBjz'),('dropout-iclr2021','Jacdvfjicf7'),('complex-privacy-iclr2020','SHDG97ukaIH'),('masked-iclr2023','YV8tP7bW6Kt'),('bottleneck-iclr2022','iRCUlgmdfHJ')]:
 PDF[key]=[f'https://openreview.net/pdf?id={oid}',f'https://api.openreview.net/pdf?id={oid}',f'https://api2.openreview.net/pdf?id={oid}']
def fetch(job):
 key,urls,kind=job;r={'key':key,'kind':kind,'requested_url':urls[0],'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attempts':[]}
 for url in urls:
  try:
   data,resolved,headers=get(url)
   if kind=='pdf' and not data.startswith(b'%PDF'):raise ValueError('Not a PDF')
   if kind=='pdf':
    d=ROOT/'venue-papers'/key;d.mkdir(parents=True,exist_ok=True);p=d/(key+'.pdf');p.write_bytes(data)
    count,pages=extract(p,d);r['total_pages']=count;r['first_page']=pages[0]['text'][:3500]
   else:p=ROOT/'publication-index'/(key+'.html');p.write_bytes(data)
   r.update(status='ok',url=url,resolved_url=resolved,local_file=str(p.relative_to(ROOT.parent.parent.parent)),sha256=hashlib.sha256(data).hexdigest(),response_headers=headers)
   r['attempts'].append({'url':url,'status':'ok'})
   break
  except Exception as e:r['attempts'].append({'url':url,'status':'error','error':str(e)})
 else:r.update(status='error',error=r['attempts'][-1]['error'])
 return r
if __name__=='__main__':
 jobs=[(k,[u],'html') for k,u in HTML.items()]+[(k,u,'pdf') for k,u in PDF.items()]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  results=[]
  for r in pool.map(fetch,jobs):
   results.append(r);print(json.dumps({k:r.get(k) for k in ['key','status','total_pages','error']},ensure_ascii=False),flush=True)
 (ROOT/'formal-source-index.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
