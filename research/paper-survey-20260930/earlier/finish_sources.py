from pathlib import Path
import concurrent.futures,json,hashlib,datetime
from complete_acquisition import get,extract
ROOT=Path(__file__).resolve().parent

PAGES={
 'sjtu_jhc':'https://jhc.sjtu.edu.cn/people/members/quanshi-zhang.html',
 'withdrawn-roadmap':'https://arxiv.org/abs/2203.14101',
 'duplicate-robustness':'https://arxiv.org/abs/2111.03536',
 'workshop-icml2021':'https://arxiv.org/abs/2107.08821',
 'workshop-aaai2019':'https://arxiv.org/abs/1901.08813',
 'multivariate-aaai':'https://ojs.aaai.org/index.php/AAAI/article/view/17299',
 'trees-aaai':'https://ojs.aaai.org/index.php/AAAI/article/view/17685',
 'decoder-icml2023':'https://proceedings.mlr.press/v202/tang23i.html',
 'transformation-icml2022':'https://proceedings.mlr.press/v162/ren22b.html',
 'sparse-cvpr2023':'https://openaccess.thecvf.com/content/CVPR2023/html/Ren_Defining_and_Quantifying_the_Emergence_of_Sparse_Concepts_in_DNNs_CVPR_2023_paper.html',
 'masked-iclr2023':'https://openreview.net/forum?id=YV8tP7bW6Kt',
 'bn-aaai2024':'https://ojs.aaai.org/index.php/AAAI/article/view/29978',
 'advtrain-aaai2024':'https://ojs.aaai.org/index.php/AAAI/article/view/29032',
 'robustness-neurips2021':'https://papers.nips.cc/paper/2021/hash/1f4fe6a4411edc2ff625888b4093e917-Abstract.html',
 'shapley-official-code':'https://github.com/yichen928/Multivariate_Shapley_Interactions',
}
PDFS={
 'multivariate-aaai2021':'https://ojs.aaai.org/index.php/AAAI/article/download/17299/17106',
 'trees-aaai2021':'https://ojs.aaai.org/index.php/AAAI/article/download/17685/17492',
 'decoder-icml2023':'https://proceedings.mlr.press/v202/tang23i/tang23i.pdf',
 'transformation-icml2022':'https://proceedings.mlr.press/v162/ren22b/ren22b.pdf',
 'masked-iclr2023':'https://openreview.net/pdf?id=YV8tP7bW6Kt',
 'sparse-cvpr2023-main':'https://openaccess.thecvf.com/content/CVPR2023/papers/Ren_Defining_and_Quantifying_the_Emergence_of_Sparse_Concepts_in_DNNs_CVPR_2023_paper.pdf',
 'sparse-cvpr2023-supp':'https://openaccess.thecvf.com/content/CVPR2023/supplemental/Ren_Defining_and_Quantifying_CVPR_2023_supplemental.pdf',
}
def fetch(x):
    key,url,kind=x;result={'key':key,'url':url,'kind':kind,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        data,resolved,headers=get(url);result['resolved_url']=resolved
        if kind=='html':p=ROOT/'publication-index'/(key+'.html');p.write_bytes(data)
        else:
            if not data.startswith(b'%PDF'):raise ValueError('Not a PDF')
            d=ROOT/'venue-papers'/key;d.mkdir(parents=True,exist_ok=True);p=d/(key+'.pdf');p.write_bytes(data)
            count,pages=extract(p,d);result['total_pages']=count;result['first_page']=pages[0]['text'][:3500]
        result['local_file']=str(p.relative_to(ROOT.parent.parent.parent));result['sha256']=hashlib.sha256(data).hexdigest();result['status']='ok'
    except Exception as e:result['status']='error';result['error']=str(e)
    return result
if __name__=='__main__':
    jobs=[(k,u,'html') for k,u in PAGES.items()]+[(k,u,'pdf') for k,u in PDFS.items()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=[]
        for r in pool.map(fetch,jobs):results.append(r);print(json.dumps({k:r.get(k) for k in ['key','status','total_pages','error']},ensure_ascii=False),flush=True)
    (ROOT/'venue-source-index.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
