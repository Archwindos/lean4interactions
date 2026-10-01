#!/usr/bin/env python3
"""Intermediate browser checks for explicit admitted papers and reading paths."""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from evidence_paths import EVIDENCE

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'reader'
TOOLS=ROOT/'research/reader-redesign-20260930/browser-tools'
sys.path.insert(0,str(TOOLS/'python'))
os.environ['PLAYWRIGHT_BROWSERS_PATH']=str(TOOLS/'browsers')
from playwright.sync_api import sync_playwright

PAPERS={'neurips2021-robustness','neurips2024-dynamics'}
TARGETS={'robustness-entropy-interaction','robustness-dropout-expansion','robustness-classical-uniqueness',
         'dyn-regression','dyn-taylor','dyn-noise-split','dyn-uniqueness'}

def main(base,papers=None,targets=None,report_name='eight-paper-browser-checks.json',prefix='eight'):
    papers=set(papers or PAPERS);targets=set(targets or TARGETS)
    if Path(report_name).name!=report_name or not report_name.endswith('.json') or report_name.startswith('root-'):
        raise ValueError('Expected a local non-root JSON report name')
    if not prefix.replace('-','').isalnum():raise ValueError('Expected a simple screenshot prefix')
    paths=[WORK/'preview/data.public.json',WORK/'preview/data.public.js',WORK/'preview/reader.js',
           WORK/'preview/reader.css',EVIDENCE/'build-manifest.json',Path(__file__).resolve(),
           ROOT/'corpus/public/reader/input-manifest.json']
    def hashes():
        return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    before=hashes()
    data=json.loads(paths[0].read_text())
    manifest=json.loads((EVIDENCE/'build-manifest.json').read_text())
    configured=json.loads(paths[-1].read_text())
    configured_ids={row['paper_id'] for row in configured['papers']}
    if not papers<=configured_ids:raise ValueError('Selected papers are not admitted inputs')
    selected=[row for row in data['math']['results'] if row['id'] in targets]
    if {row['id'] for row in selected}!=targets:raise ValueError('Selected result is absent from the built snapshot')
    checks=[];errors=[];external=[];screens=[]
    def check(name,value,detail=None):
        checks.append({'name':name,'passed':bool(value),'detail':detail})
    def cjk(selector):
        return page.locator(selector).evaluate_all("xs=>xs.map(x=>{const y=x.cloneNode(true);y.querySelectorAll('.katex,code,pre,.raw-source').forEach(z=>z.remove());return y.textContent}).filter(x=>/[\u3400-\u9fff]/.test(x))")
    def inspect(label):
        check('math:'+label,not page.evaluate('window.READER_MATH_ERRORS||[]'))
        check('viewport:'+label,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    def screenshot(name):
        path=EVIDENCE/name;page.screenshot(path=str(path))
        screens.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'url':page.url})
    for path in paths[:4]:
        response=urlopen(base+path.relative_to(WORK/'preview').as_posix())
        check('served:'+path.name,hashlib.sha256(response.read()).hexdigest()==before[str(path.relative_to(ROOT))])
        response.close()
    with sync_playwright() as engine:
        browser=engine.chromium.launch(headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1440,'height':1050})
        page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
        origin=urlparse(base)
        def route(request):
            url=urlparse(request.request.url)
            if url.scheme in ('http','https') and (url.hostname,url.port)!=(origin.hostname,origin.port):
                external.append(request.request.url);request.abort()
            else:request.continue_()
        context.route('**/*',route)
        page.goto(base,wait_until='networkidle')
        check('explicit-paper-manifest',{row['id'] for row in data['papers']}==configured_ids)
        assets={item['path']:item['sha256'] for item in manifest['public_file_allowlist']}
        images=[]
        for paper in data['papers']:
            if paper['id'] not in papers:continue
            page.goto(base+'papers/'+paper['id']+'/',wait_until='networkidle')
            expected=[row for row in data['math']['results'] if row['paper_id']==paper['id']]
            check('directory:'+paper['id'],page.locator('.result-list a[data-result]').count()==len(expected))
            inspect('directory:'+paper['id'])
            for source in paper['sources']:
                response=page.request.get(base+source['public_path'].lstrip('/'))
                check('formal-pdf:'+source['id'],response.ok and hashlib.sha256(response.body()).hexdigest()==source['sha256'])
                response.dispose()
                check('source-page-coverage:'+source['id'],set(source['page_images'])=={str(i) for i in range(1,source['total_pages']+1)})
                for number,path in source['page_images'].items():
                    response=page.request.get(base+path.lstrip('/'))
                    check('source-bytes:'+source['id']+':'+number,response.ok and hashlib.sha256(response.body()).hexdigest()==assets[path.lstrip('/')])
                    response.dispose();images.append({'source_id':source['id'],'page':number,'url':base+path.lstrip('/')})
        decoded=page.evaluate('''async rows=>{const output=[];for(const row of rows){const image=new Image();image.src=row.url;try{await image.decode();output.push({...row,width:image.naturalWidth,height:image.naturalHeight,decoded:true});}catch(e){output.push({...row,decoded:false});}}return output;}''',images)
        for row in decoded:check('source-decode:'+row['source_id']+':'+row['page'],row['decoded'] and row['width']>0 and row['height']>0)
        shared=[row for row in data['math']['shared_proofs'] if row.get('paper_id') in papers]
        samples=[next(row for row in selected if row['paper_id']==paper_id)
                 for paper_id in sorted(papers) if any(row['paper_id']==paper_id for row in selected)]
        for language in ('zh','en'):
            page.locator('#language-select').select_option(language)
            page.wait_for_function('window.READER_LANGUAGE === '+json.dumps(language))
            for result in selected+shared:
                path=('proofs/'+result['id']+'/') if result in shared else 'papers/'+result['paper_id']+'/results/'+result['id']+'/'
                page.goto(base+path,wait_until='networkidle')
                check('title:'+language+':'+result['id'],page.locator('h1').inner_text()==(result['title'] if language=='zh' else result['translations']['en']['title']))
                if page.locator('#tab-rewrite').count():
                    page.locator('#tab-rewrite').click();inspect(language+':'+result['id'])
                    if language=='en':check('english-proof:'+result['id'],not cjk('.condition,.definition-item,.proof-idea,.proof-step,.shared-intro,.caveat-body'))
                    button=page.locator('.proof-step .step-to-lean').first
                    if button.count():
                        step=button.locator('..').get_attribute('data-step-id');button.click()
                        check('lean-jump:'+language+':'+result['id'],page.locator('#tab-lean').get_attribute('aria-selected')=='true')
                        target=page.locator('.lean-map[data-step-id="'+step+'"]').first
                        target.locator('.return-step').click()
                        check('step-return:'+language+':'+result['id'],page.locator('#tab-rewrite').get_attribute('aria-selected')=='true' and page.evaluate('window.READER_LANGUAGE')==language)
                for tab in ('statement','original-proof','lean'):
                    if not page.locator('#tab-'+tab).count():continue
                    page.locator('#tab-'+tab).click();inspect(language+':'+result['id']+':'+tab)
                    if language=='en' and tab=='lean':check('english-lean:'+result['id'],not cjk('.lean-intro,.lean-map'))
                    if language=='en' and tab in ('statement','original-proof'):
                        page.locator('#reader-panel details').evaluate_all('xs=>xs.forEach(x=>x.open=true)')
                        check('english-source-labels:'+result['id']+':'+tab,not cjk('.source-links,.source-notes,details>summary'),cjk('.source-links,.source-notes,details>summary'))
                    if tab=='original-proof' and result.get('issues'):
                        check('visible-source-issues:'+language+':'+result['id'],all(
                            page.locator('#reader-panel .error-message a[href="'+issue['public_path']+'"]').count()>0
                            for issue in result['issues'] if issue.get('public_path')))
                if language=='en' and result in samples:
                    page.locator('#tab-rewrite').click();screenshot(prefix+'-'+result['id']+'-en.png')
        for paper_id in sorted(papers):
            page.goto(base+'symbols/?paper='+paper_id,wait_until='networkidle')
            page.locator('.symbol-card').evaluate_all('xs=>xs.forEach(x=>x.open=true)')
            check('expanded-symbols-English:'+paper_id,not cjk('.symbol-card'),cjk('.symbol-card'))
            inspect('symbols:'+paper_id)
        page.set_viewport_size({'width':390,'height':844})
        for result in samples:
            page.goto(base+'papers/'+result['paper_id']+'/results/'+result['id']+'/',wait_until='networkidle')
            page.locator('#tab-rewrite').click();inspect('mobile:'+result['id'])
        check('no-browser-errors',not errors,errors);check('no-external-requests',not external,external)
        browser.close()
    after=hashes();check('snapshot-stable-during-browser-check',before==after)
    for item in manifest['inputs']:
        path=ROOT/item['path'];check('current-build-input:'+item['path'],path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'])
    report={'status':'passed' if all(row['passed'] for row in checks) else 'failed','scope':'intermediate_admitted_source_and_selected_browser_checks_not_twelve_paper_acceptance',
            'snapshot_hashes':{'before':before,'after':after},'paper_count':len(data['papers']),'papers':sorted(papers),'selected_result_ids':sorted(targets),
            'shared_proof_ids':[row['id'] for row in shared],
            'source_pages_decoded':len(decoded),'checks':checks,'screenshots':screens,'js_errors':errors,'external_requests':external}
    (EVIDENCE/report_name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'checks':len(checks),'source_pages_decoded':len(decoded),
                      'failures':[{'name':row['name'],'detail':str(row['detail'])[:300]} for row in checks if not row['passed']][:12]},ensure_ascii=False))
    return report['status']!='passed'

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8004/')
    parser.add_argument('--paper',action='append');parser.add_argument('--result',action='append')
    parser.add_argument('--report-name',default='eight-paper-browser-checks.json');parser.add_argument('--screenshot-prefix',default='eight')
    args=parser.parse_args()
    raise SystemExit(main(args.base,args.paper,args.result,args.report_name,args.screenshot_prefix))
