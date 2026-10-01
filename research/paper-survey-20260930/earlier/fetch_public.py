"""Public-paper evidence acquisition; writes only inside this survey directory."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, html, json, re, subprocess, urllib.request
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
IDS = [
    '2111.06206','2207.11694','2205.15130','2205.15146','2205.01940',
    '2111.06236','2010.14978','2010.05045','2009.11729','2010.04055',
    '2106.10938','2105.10719','2108.06895','2006.15920','2007.04298',
    '2112.00980','2210.09020','2111.03536','2111.03505','1911.09017',
    '1901.02184','1911.09040','2006.13016','2003.08365','1901.09546',
    '1906.04109','2208.08741','1908.01581','2003.03622',
]

def get(url):
    request = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (public research survey)'})
    with urllib.request.urlopen(request, timeout=50) as response:
        return response.read(), response.url

def fetch_arxiv(arxiv_id):
    directory = ROOT/'papers'/arxiv_id
    directory.mkdir(parents=True, exist_ok=True)
    record = {'arxiv_id':arxiv_id, 'source_url':f'https://arxiv.org/abs/{arxiv_id}',
              'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        body, resolved = get(record['source_url'])
        (directory/'abs.html').write_bytes(body)
        page = body.decode('utf-8', errors='replace')
        def meta(name):
            found = re.findall(r'<meta\s+name="'+re.escape(name)+r'"\s+content="([^"]*)"', page)
            return [html.unescape(x) for x in found]
        record['title'] = meta('citation_title')[0]
        record['authors'] = meta('citation_author')
        record['first_public_date'] = (meta('citation_date') or [None])[0]
        record['journal_ref'] = meta('citation_journal_title')
        versions = re.findall(re.escape(arxiv_id)+r'v(\d+)', page)
        record['version'] = 'v'+str(max(map(int,versions))) if versions else 'v1'
        if arxiv_id=='2111.06206': record['version']='v6'
        record['pdf_url'] = f'https://arxiv.org/pdf/{arxiv_id}{record["version"]}'
        pdf_path = directory/(arxiv_id+record['version']+'.pdf')
        if not pdf_path.exists():
            pdf, pdf_resolved = get(record['pdf_url'])
            if not pdf.startswith(b'%PDF'): raise ValueError('Response is not a PDF')
            pdf_path.write_bytes(pdf)
        record['sha256'] = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
        record['local_pdf'] = str(pdf_path.relative_to(ROOT.parent.parent.parent))
        reader = PdfReader(pdf_path)
        record['total_pages'] = len(reader.pages)
        pages = [{'page':i+1,'text':p.extract_text() or ''} for i,p in enumerate(reader.pages)]
        (directory/'pages.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2))
        (directory/'text.txt').write_text('\n\n'.join(f'=== PDF PAGE {p["page"]} ===\n'+p['text'] for p in pages))
        # Layout text is a second extraction useful for checking two-column proofs.
        subprocess.run(['pdftotext','-layout',str(pdf_path),str(directory/'layout.txt')], check=True)
        record['first_page'] = pages[0]['text'][:2400]
        headings = []
        for p in pages:
            for m in re.finditer(r'\b(?:Theorem|Lemma|Proposition|Corollary|Proof)\b[^\n]{0,130}', p['text']):
                headings.append({'page':p['page'],'text':m.group(0)})
        record['automatic_heading_hits'] = headings
        record['status'] = 'downloaded_extracted_requires_manual_review'
    except Exception as error:
        record['status']='download_or_extract_error'
        record['error']=str(error)
    (directory/'acquisition.json').write_text(json.dumps(record, ensure_ascii=False, indent=2))
    return record

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results=[]
        for r in executor.map(fetch_arxiv,IDS):
            results.append(r)
            print(json.dumps({k:r.get(k) for k in ['arxiv_id','title','version','total_pages','status','error']},ensure_ascii=False),flush=True)
    (ROOT/'acquisition-index.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
