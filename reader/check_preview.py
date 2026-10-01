#!/usr/bin/env python3
"""Real browser coverage of the complete, independently served formal-paper reader."""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1];WORK=Path(__file__).resolve().parent
TOOLS=ROOT/'research/reader-redesign-20260930/browser-tools'
sys.path.insert(0,str(TOOLS/'python'));os.environ['PLAYWRIGHT_BROWSERS_PATH']=str(TOOLS/'browsers')
from playwright.sync_api import sync_playwright

def main(base):
 started=datetime.now(timezone.utc).isoformat()
 bound_paths=[WORK/'preview/data.public.json',WORK/'preview/data.public.js',WORK/'evidence/build-manifest.json',WORK/'preview/reader.js',WORK/'preview/reader.css',Path(__file__).resolve()]
 def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in bound_paths}
 before=hashes()
 data=json.loads((WORK/'preview/data.public.json').read_text());manifest=json.loads((WORK/'evidence/build-manifest.json').read_text())
 checks=[];errors=[];external=[];screenshots=[]
 def check(name,value,detail=None):checks.append({'name':name,'passed':bool(value),'detail':detail})
 for path in bound_paths:
  if path.is_relative_to(WORK/'preview'):
   relative=path.relative_to(WORK/'preview').as_posix()
   served=hashlib.sha256(urlopen(base+relative).read()).hexdigest()
   check('served-snapshot:'+relative,served==before[str(path.relative_to(ROOT))],served)
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,args=['--no-sandbox']);ctx=b.new_context(viewport={'width':1440,'height':1050});page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  allowed=urlparse(base)
  def route(r):
   u=urlparse(r.request.url)
   if u.scheme in ('http','https') and (u.hostname,u.port)!=(allowed.hostname,allowed.port):external.append(r.request.url);r.abort()
   else:r.continue_()
  ctx.route('**/*',route)
  def inspect(label):
   check('math:'+label,not page.evaluate('window.READER_MATH_ERRORS||[]'),page.evaluate('window.READER_MATH_ERRORS||[]'))
   check('layout:'+label,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  def screenshot(name):
   path=WORK/'evidence'/name;page.screenshot(path=str(path));screenshots.append({'path':str(path.relative_to(WORK)),'url':page.url,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'viewport':page.viewport_size})
  page.goto(base,wait_until='networkidle');page.evaluate("localStorage.setItem('proof-reader-language','zh')");page.reload(wait_until='networkidle');inspect('home');screenshot('01-full-directory-home.png')
  page.locator('.paper-search input').fill('Shapley');check('search-shapley-cross-paper',len(set(page.locator('[data-search-result]').evaluate_all('xs=>xs.map(x=>x.href.split("/")[4])')))>=3)
  screenshot('02-cross-paper-search.png')
  for paper in data['papers']:
   page.goto(base+f"papers/{paper['id']}/",wait_until='networkidle');expected=[r for r in data['math']['results'] if r['paper_id']==paper['id']]
   check('all-directory-entries:'+paper['id'],page.locator('.result-list a[data-result]').count()==len(expected),{'expected':len(expected)})
   check('nonproof-group-folded:'+paper['id'],not page.locator('.source-entry-list').get_attribute('open'))
   inspect('directory:'+paper['id'])
   screenshot('03-directory-'+paper['id']+'.png')
  page.goto(base+'papers/iclr2024-sparse/',wait_until='networkidle');page.locator('.paper-search input').fill('Theorem 6')
  found=page.locator('[data-search-result]').evaluate_all('xs=>xs.map(x=>x.dataset.searchResult)');check('ambiguous-theorem-number-retained',set(found)=={'iclr2024-sparse-theorem3','iclr2024-sparse-theorem6'},found)
  for r in data['math']['results']:
   if data['math']['results'].index(r)%30==0:print('Chinese pages checked: '+str(data['math']['results'].index(r)),flush=True)
   path=f"papers/{r['paper_id']}/results/{r['id']}/";page.goto(base+path,wait_until='load');page.wait_for_selector('h1');inspect(r['id']);check('direct-entry:'+r['id'],page.locator('h1').inner_text()==r['title'])
   for tab in ('statement','original-proof','rewrite','lean'):
    if not page.locator('#tab-'+tab).count():continue
    page.locator('#tab-'+tab).click();inspect(r['id']+':'+tab)
    if tab in ('statement','original-proof'):check('source-linked:'+r['id']+':'+tab,page.locator('#reader-panel a[href*="#page="]').count()>0 or (tab=='original-proof' and not r.get('proof_target')) or r.get('original_proof_source_type')=='no_local_original_proof')
   if r.get('lean',{}).get('evidence_role')=='counterexample' and page.locator('#tab-lean').count():
    page.locator('#tab-lean').click();check('counterexample-not-theorem:'+r['id'],'被检验的原陈述' in page.locator('#reader-panel').inner_text() and '原命题未证明' in r.get('lean',{}).get('label','') or r['statement_assessment']!='refuted')
   if r['id']=='cvpr2023-baseline-faithfulness':check('compound-not-whole-counterexample',r['lean'].get('evidence_role')=='partial_component' and r['statement_assessment']=='partially_refuted')
   if r.get('lean',{}).get('step_map') and page.locator('#tab-rewrite').count():
    page.locator('#tab-rewrite').click();button=page.locator('.proof-step .step-to-lean').first
    if button.count():
     step_id=button.locator('..').get_attribute('data-step-id');button.click();check('step-lean-jump:'+r['id'],page.locator('#tab-lean').get_attribute('aria-selected')=='true' and page.locator('.lean-map[data-step-id="'+step_id+'"]').count()>0)
     target=page.locator('.lean-map[data-step-id="'+step_id+'"]').first
     if target.count():
      check('step-lean-declaration:'+r['id'],target.locator('.lean-declarations code').count()>0)
      maps=[m for m in r['lean']['step_map'] if str(m.get('step_id'))==step_id]
      check('step-lean-current-type-source:'+r['id'],bool(maps) and all(m.get('evidence_status')=='current' and m.get('signature') and m.get('source_path') and isinstance(m.get('line'),int) and m.get('evidence',{}).get('freshness')=='current' and m.get('public_report_path') and m.get('public_source_path') for m in maps))
      target.locator('.return-step').click();check('step-return:'+r['id'],page.locator('#tab-rewrite').get_attribute('aria-selected')=='true' and page.locator('.proof-step[data-step-id="'+step_id+'"]').count()>0)
   if r['id'] in ('cvpr2023-dummy','iclr2024-generalizable-andor','iclr2024-sparse-theorem2'):
    if page.locator('#tab-rewrite').count():page.locator('#tab-rewrite').click()
    screenshot('04-proof-'+r['id']+'.png')
  for proof in data['math']['shared_proofs']:
   page.goto(base+'proofs/'+proof['id']+'/',wait_until='networkidle');check('public-proof-page:'+proof['id'],page.locator('h1').inner_text()==proof['title']);inspect('shared:'+proof['id'])
   if page.locator('#tab-lean').count():page.locator('#tab-lean').click();inspect('shared-lean:'+proof['id'])
  # Every result and shared proof is visited in English, including long text,
  # conditions, reference-resolved shared steps and actual Lean display fields.
  english_pages=0
  page.locator('#language-select').select_option('en');page.wait_for_function("window.READER_LANGUAGE==='en'")
  def core_cjk(selectors):
   return page.locator(selectors).evaluate_all("xs=>xs.map(x=>{const y=x.cloneNode(true);y.querySelectorAll('.katex,code,pre,#language-select').forEach(z=>z.remove());return y.textContent}).filter(x=>/[\u3400-\u9fff]/.test(x))")
  for r in data['math']['results']+data['math']['shared_proofs']:
   shared=r in data['math']['shared_proofs']
   path=('proofs/'+r['id']+'/') if shared else f"papers/{r['paper_id']}/results/{r['id']}/"
   page.goto(base+path,wait_until='load');page.wait_for_selector('h1');english_pages+=1
   if english_pages%30==0:print('English pages checked: '+str(english_pages),flush=True)
   expected=r.get('translations',{}).get('en',{}).get('title')
   check('english-title:'+r['id'],bool(expected) and page.locator('h1').inner_text()==expected)
   cjk_ui=core_cjk('.masthead,.sidebar,.tabs,button');check('english-interface:'+r['id'],not cjk_ui,cjk_ui)
   check('language-persists:'+r['id'],page.evaluate("window.READER_LANGUAGE==='en' && localStorage.getItem('proof-reader-language')==='en'"))
   if page.locator('#tab-rewrite').count():
    page.locator('#tab-rewrite').click();inspect('english-rewrite:'+r['id'])
    cjk=core_cjk('.proof-step,.condition,.definition-item,.proof-idea');check('english-proof-body:'+r['id'],not cjk,cjk)
    check('english-real-proof-steps:'+r['id'],page.locator('.proof-step').count()>0 or not r.get('proof_steps'))
   if page.locator('#tab-lean').count():
    page.locator('#tab-lean').click();inspect('english-lean:'+r['id']);cjk=core_cjk('.lean-intro,.lean-map');check('english-lean-display:'+r['id'],not cjk,cjk)
   for tab in ('statement','original-proof'):
    if page.locator('#tab-'+tab).count():page.locator('#tab-'+tab).click();inspect('english-source:'+r['id']+':'+tab)
   if page.locator('#tab-rewrite').count():page.locator('#tab-rewrite').click();check('return-from-original-keeps-language:'+r['id'],page.evaluate("window.READER_LANGUAGE==='en'"))
  check('all-english-proof-pages',english_pages==len(data['math']['results'])+len(data['math']['shared_proofs']),english_pages)
  for path,label in [('', 'home'),('about/', 'about'),('symbols/', 'symbols')]+[(f"papers/{p['id']}/",p['id']) for p in data['papers']]:
   page.goto(base+path,wait_until='networkidle');inspect('english-directory:'+label)
   leftovers=core_cjk('.masthead,.sidebar,.tabs,button');check('english-directory-interface:'+label,not leftovers,leftovers)
  for review in data.get('review_records',[]):
   page.goto(base+'reviews/'+review['id']+'/',wait_until='load');page.wait_for_selector('h1');inspect('english-review:'+review['id'])
   expected=review.get('translations',{}).get('en',{}).get('title')
   check('english-review-title:'+review['id'],bool(expected) and page.locator('h1').inner_text()==expected)
   leftovers=core_cjk('.masthead,.eyebrow,.breadcrumb,button');check('english-review-interface:'+review['id'],not leftovers,leftovers)
  page.goto(base+'papers/iclr2024-sparse/results/iclr2024-sparse-derivative-cutoff/',wait_until='networkidle')
  page.locator('#tab-rewrite').click();en_body=page.locator('#reader-panel').inner_text();en_formulas=page.locator('#reader-panel .math-block .katex').evaluate_all('xs=>xs.map(x=>x.textContent)')
  check('long-english-proof-has-text',len(en_body)>1500)
  page.locator('#language-select').select_option('zh');page.wait_for_function("window.READER_LANGUAGE==='zh'")
  page.locator('#tab-rewrite').click();zh_body=page.locator('#reader-panel').inner_text();zh_formulas=page.locator('#reader-panel .math-block .katex').evaluate_all('xs=>xs.map(x=>x.textContent)')
  check('long-proof-language-switch-changes-body',en_body!=zh_body and bool(re.search('[\u3400-\u9fff]',zh_body)))
  check('display-formulas-preserved-across-language',en_formulas==zh_formulas,{'en':len(en_formulas),'zh':len(zh_formulas)})
  page.goto(base+'papers/iclr2024-sparse/results/iclr2024-sparse-theorem2/',wait_until='networkidle');page.locator('#tab-rewrite').click()
  check('public-symbol-definitions-folded',page.locator('.proof-symbol-definitions').count()>0 and all(x is None for x in page.locator('.proof-symbol-definitions').evaluate_all('xs=>xs.map(x=>x.getAttribute("open"))')))
  check('T2-three-original-assumptions-visible',all(page.locator('.condition').filter(has_text=label).count()>0 for label in ('Assumption 1','Assumption 2','Assumption 3')))
  page.goto(base+'symbols/',wait_until='networkidle');check('symbols-compact-default',page.locator('.symbol-card[open]').count()==0);inspect('symbols');screenshot('05-symbol-table.png')
  page.locator('.symbol-controls select').select_option('iclr2024-sparse');page.locator('.symbol-controls input').fill('中心化');check('symbol-filter-search',page.locator('.symbol-card').count()>0)
  page.goto(base+'symbols/?paper=iclr2024-generalizable#sym-output-baseline',wait_until='networkidle');check('symbol-deeplink-open',page.locator('#sym-output-baseline').get_attribute('open') is not None);inspect('symbol-deeplink')
  for rec in data.get('review_records',[]):
   page.goto(base+'reviews/'+rec['id']+'/',wait_until='load');page.wait_for_selector('h1');inspect('review:'+rec['id'])
  page.set_viewport_size({'width':390,'height':844})
  for path,label in [('', 'home'),('symbols/','symbols'),('papers/iclr2024-sparse/','directory'),('papers/iclr2024-generalizable/results/iclr2024-generalizable-andor/','andor')]:
   page.goto(base+path,wait_until='networkidle');inspect('mobile:'+label);screenshot('06-mobile-'+label+'.png')
  check('no-js-errors',not errors,errors);check('no-external-requests',not external,external);b.close()
 after=hashes();check('bound-inputs-unchanged-during-browser-run',before==after,{'before':before,'after':after})
 for entry in manifest['inputs']:
  path=ROOT/entry['path'];check('build-input-current:'+entry['path'],path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'])
 report={'status':'passed' if all(c['passed'] for c in checks) else 'failed','scope':'browser_software_and_navigation_only','started_at':started,'finished_at':datetime.now(timezone.utc).isoformat(),'snapshot_hashes':{'before':before,'after':after},'build_generated_at':manifest['generated_at'],'checks':checks,'screenshots':screenshots,'js_errors':errors,'external_requests':external,'browser':'Chromium actual local installation'}
 (WORK/'evidence/browser-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'checks':len(checks),'failure_count':sum(not c['passed'] for c in checks),'failures':[{'name':c['name'],'detail':str(c.get('detail',''))[:300]} for c in checks if not c['passed']][:30],'screenshots':len(screenshots)},ensure_ascii=False))
 return 0 if report['status']=='passed' else 1
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--base',default='http://127.0.0.1:8001/');raise SystemExit(main(a.parse_args().base))
