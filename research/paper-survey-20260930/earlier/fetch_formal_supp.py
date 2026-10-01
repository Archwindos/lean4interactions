from pathlib import Path
import concurrent.futures,json
from fetch_formal import fetch
ROOT=Path(__file__).resolve().parent
TARGETS=[
 ('bn-aaai2024-supp',['https://ojs.aaai.org/index.php/AAAI/article/download/29978/31716'],'pdf'),
 ('advtrain-aaai2024-supp',['https://ojs.aaai.org/index.php/AAAI/article/download/29032/29957'],'pdf'),
 ('quaternion-eccv2020-main',['https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123650528.pdf'],'pdf'),
]
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  rows=[]
  for r in pool.map(fetch,TARGETS):rows.append(r);print(json.dumps({k:r.get(k) for k in ['key','status','total_pages','error']},ensure_ascii=False),flush=True)
 (ROOT/'formal-supp-source-index.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
