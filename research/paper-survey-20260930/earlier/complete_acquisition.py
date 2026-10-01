"""Acquire and page-extract the complete public <=2022 author arXiv index."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, re, subprocess, urllib.request

ROOT = Path(__file__).resolve().parent
INDEX = json.loads((ROOT/'publication-index/arxiv-author-earlier.json').read_text())

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=40) as response:
        # Reading sized blocks avoids HTTPResponse.read() requiring an exact content length.
        chunks=[]
        while True:
            b=response.read(512*1024)
            if not b: break
            chunks.append(b)
        data=b''.join(chunks)
        size=response.headers.get('Content-Length')
        if size and len(data)!=int(size): raise ValueError(f'Truncated body {len(data)}/{size}')
        return data,response.url,dict(response.headers)

def extract(pdf_path,directory):
    info=subprocess.run(['pdfinfo',str(pdf_path)],capture_output=True,text=True,check=True)
    count=int(next(l.split(':')[1] for l in info.stdout.splitlines() if l.startswith('Pages:')))
    pages=[]
    for i in range(1,count+1):
        t=subprocess.run(['pdftotext','-f',str(i),'-l',str(i),'-layout',str(pdf_path),'-'],capture_output=True,text=True,check=True).stdout
        pages.append({'page':i,'text':t.rstrip('\f\n')})
    (directory/'pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
    (directory/'text.txt').write_text('\n\n'.join(f'=== PDF PAGE {x["page"]} ===\n'+x['text'] for x in pages))
    subprocess.run(['pdftotext','-layout',str(pdf_path),str(directory/'layout.txt')],capture_output=True,check=True)
    return count,pages

def fetch(entry):
    fixed=entry['id'].rsplit('/',1)[-1]
    arxiv_id,version=fixed.split('v')
    version='v'+version
    directory=ROOT/'papers'/arxiv_id;directory.mkdir(parents=True,exist_ok=True)
    record={'arxiv_id':arxiv_id,'version':version,'title':entry['title'],'authors':entry['authors'],
            'first_public_date':entry['published'],'updated':entry['updated'],'journal_ref':entry['journal_ref'],
            'source_url':f'https://arxiv.org/abs/{fixed}', 'pdf_url':f'https://arxiv.org/pdf/{fixed}',
            'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attempts':[]}
    try:
        pdf_path=directory/(fixed+'.pdf')
        if not pdf_path.exists():
            for url in [f'https://arxiv.org/pdf/{fixed}',f'https://export.arxiv.org/pdf/{fixed}',
                        f'https://arxiv.org/pdf/{arxiv_id}',f'https://export.arxiv.org/pdf/{arxiv_id}']:
                try:
                    data,resolved,headers=get(url)
                    if not data.startswith(b'%PDF'): raise ValueError('Not a PDF')
                    filename=headers.get('Content-Disposition',headers.get('content-disposition',''))
                    found=re.search(r'(\d{4}\.\d{4,5}v\d+)',filename)
                    if found and found.group(1)!=fixed: raise ValueError('Response version mismatch: '+found.group(1))
                    pdf_path.write_bytes(data)
                    record['download_url']=url;record['response_headers']=headers
                    record['attempts'].append({'url':url,'status':'ok','bytes':len(data)})
                    break
                except Exception as e: record['attempts'].append({'url':url,'status':'error','error':str(e)})
        if not pdf_path.exists(): raise ValueError('All public PDF endpoints failed; see attempts')
        count,pages=extract(pdf_path,directory)
        record.update({'local_pdf':str(pdf_path.relative_to(ROOT.parent.parent.parent)),
                       'sha256':hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
                       'total_pages':count,'first_page':pages[0]['text'][:3500],
                       'status':'downloaded_extracted_requires_manual_review'})
        headings=[]
        for p in pages:
            for line in p['text'].splitlines():
                if re.search(r'\b(?:Theorem|Lemma|Proposition|Corollary|Proof|proof|derivation|Derivation)\b',line):
                    headings.append({'page':p['page'],'text':line.strip()})
        record['automatic_heading_hits']=headings
    except Exception as e:
        record['status']='download_or_extract_error';record['error']=str(e)
    (directory/'acquisition.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
    return record

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records=[]
        for record in pool.map(fetch,INDEX):
            records.append(record)
            print(json.dumps({k:record.get(k) for k in ['arxiv_id','title','version','total_pages','status','error']},ensure_ascii=False),flush=True)
    (ROOT/'acquisition-index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
