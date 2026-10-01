"""Snapshot author-list blocks and public non-arXiv papers linked by the author."""
from html.parser import HTMLParser
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, re
from complete_acquisition import get, extract

ROOT=Path(__file__).resolve().parent
class Node:
    def __init__(self,tag='',attrs=None): self.tag=tag;self.attrs=dict(attrs or []);self.children=[]
    def text(self): return ' '.join(c if isinstance(c,str) else c.text() for c in self.children)
    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c,Node):yield from c.walk()
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.root=Node();self.stack=[self.root]
    def handle_starttag(self,tag,attrs):
        n=Node(tag,attrs);self.stack[-1].children.append(n)
        if tag not in ['br','img','hr','meta','link','input','source','wbr']:self.stack.append(n)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:self.stack=self.stack[:i];break
    def handle_data(self,data):self.stack[-1].children.append(data)

def normalize(s):return re.sub(r'\s+',' ',s).strip()
parser=Parser();parser.feed((ROOT/'publication-index/qszhang.html').read_text(errors='replace'))
blocks=[]
for n in parser.root.walk():
    if 'dslc-module-DSLC_Text_Simple' in n.attrs.get('class',''):
        links=[{'url':c.attrs.get('href'),'text':normalize(c.text())} for c in n.walk() if c.tag=='a']
        if any(l['text'] in ['PDF','arXiv'] for l in links):
            ps=[normalize(c.text()) for c in n.walk() if c.tag=='p']
            blocks.append({'title':ps[0] if ps else normalize(n.text()),'lines':ps,'text':normalize(n.text()),'links':links})
(ROOT/'publication-index/publication-blocks.json').write_text(json.dumps(blocks,ensure_ascii=False,indent=2))
targets=[]
for b in blocks:
    for l in b['links']:
        url=l['url']
        if url and '.pdf' in url.lower() and 'arxiv.org' not in url and l['text'] in ['PDF','Supplementary']:
            targets.append({'title_from_index':b['title'],'index_text':b['text'],'source_url':'http://qszhang.com/index.php/publications/','pdf_url':url})
targets += [
 {'title_from_index':'Exploring Image Regions Not Well Encoded by an INN','source_url':'https://proceedings.mlr.press/v151/ling22a.html','pdf_url':'https://proceedings.mlr.press/v151/ling22a/ling22a.pdf'},
 {'title_from_index':'Interpretable Generative Adversarial Networks','source_url':'https://ojs.aaai.org/index.php/AAAI/article/view/20015','pdf_url':'https://ojs.aaai.org/index.php/AAAI/article/download/20015/19774'},
 {'title_from_index':'Towards a Deep and Unified Understanding of Deep Neural Models in NLP','source_url':'https://proceedings.mlr.press/v97/guan19a.html','pdf_url':'https://proceedings.mlr.press/v97/guan19a/guan19a.pdf'},
 {'title_from_index':'Towards a Deep and Unified Understanding of Deep Neural Models in NLP (supplement)','source_url':'https://proceedings.mlr.press/v97/guan19a.html','pdf_url':'https://proceedings.mlr.press/v97/guan19a/guan19a-supp.pdf'},
]
(ROOT/'official-targets.json').write_text(json.dumps(targets,ensure_ascii=False,indent=2))

def fetch(t):
    key=t['pdf_url'].rsplit('/',1)[-1].replace('.pdf','')
    if 'article/download' in t['pdf_url']:key='interpretable-gan-aaai2022'
    d=ROOT/'official-papers'/key;d.mkdir(parents=True,exist_ok=True)
    r=dict(t);r['retrieved_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        p=d/(key+'.pdf')
        if not p.exists():
            data,resolved,headers=get(t['pdf_url'])
            if not data.startswith(b'%PDF'):raise ValueError('Not a PDF')
            p.write_bytes(data);r['resolved_pdf_url']=resolved;r['response_headers']=headers
        count,pages=extract(p,d)
        r.update({'total_pages':count,'local_pdf':str(p.relative_to(ROOT.parent.parent.parent)),
                  'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'first_page':pages[0]['text'][:3500],
                  'status':'downloaded_extracted_requires_manual_review'})
    except Exception as e:r['status']='download_or_extract_error';r['error']=str(e)
    (d/'acquisition.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));return r

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=[]
        for r in pool.map(fetch,targets):
            results.append(r);print(json.dumps({k:r.get(k) for k in ['title_from_index','pdf_url','total_pages','status','error']},ensure_ascii=False),flush=True)
    (ROOT/'official-acquisition-index.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
