#!/usr/bin/env python3
"""Record concrete browser task paths before proposing a later UI redesign."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
from check_preview import ROOT,WORK,EVIDENCE,sync_playwright

def main(base):
 data=json.loads((WORK/'preview/data.public.json').read_text())
 records=[];screens=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1440,'height':1050})
  page.goto(base);page.evaluate("localStorage.setItem('proof-reader-language','zh')");page.reload()
  def capture(name,actions):
   screen=EVIDENCE/('workflow-'+name+'.png');page.screenshot(path=str(screen));screens.append({'path':screen.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(screen.read_bytes()).hexdigest()})
   records.append({'task':name,'url':page.url,'actions':[dict(a) for a in actions],'click_or_select_actions':sum(a['kind'] in {'click','select'} for a in actions),
    'visible_header':page.locator('.result-meta').all_text_contents(),'heading_order':page.locator('#reader-panel h2').all_text_contents(),
    'controls':page.locator('.reader-main button').all_text_contents(),
    'proof_step_count':page.locator('.proof-step').count(),'step_lean_button_count':page.locator('.proof-step .step-to-lean').count(),
    'document_height':page.evaluate('document.documentElement.scrollHeight'),'viewport_height':1050,
    'source_issue_visible_in_current_panel':page.locator('#reader-panel .error-message').count()>0})
  # Task 1: find a long proof, read its conditions, inspect one actual Lean step,
  # and return to that same step. Each transition is executed in the browser.
  page.locator('a[href="/papers/iclr2024-sparse/"]').first.click();page.locator('.result-list a[data-result="iclr2024-sparse-derivative-cutoff"]').click()
  actions=[{'kind':'click','target':'Sparse paper from home'},{'kind':'click','target':'Derivative-cutoff result from directory'}]
  last=page.locator('.proof-step').last;last.scroll_into_view_if_needed();actions.append({'kind':'scroll','target':'last proof step'})
  capture('long-proof',actions)
  button=last.locator('.step-to-lean');
  if button.count():
   button.click();actions.append({'kind':'click','target':'Lean comparison for last step'})
   page.locator('.lean-map .return-step').last.click();actions.append({'kind':'click','target':'return to the proof step'});capture('long-proof-return',actions)
  # Task 2: distinguish a false statement from a repaired author proof, and find
  # the exact source error and its complete record.
  page.goto(base);page.locator('a[href="/papers/cvpr2023-sparse-concepts/"]').first.click();page.locator('.result-list a[data-result="cvpr2023-dummy"]').click()
  actions=[{'kind':'click','target':'CVPR paper from home'},{'kind':'click','target':'Dummy result from directory'}];capture('false-statement',actions)
  page.locator('#tab-original-proof').click();actions.append({'kind':'click','target':'author proof tab'});capture('false-statement-source',actions)
  issue=page.locator('.error-message a[href*="/reviews/"]').first
  if issue.count():
   href=issue.get_attribute('href');page.goto(base+href.lstrip('/'));actions.append({'kind':'click','target':'complete source-issue record'});capture('false-statement-issue',actions)
  # Task 3: inspect paper adaptation, shared premises and reusable proof evidence.
  page.goto(base+'papers/cvpr2023-sparse-concepts/results/cvpr2023-reconstruction/')
  actions=[{'kind':'navigation','target':'reconstruction result'}];capture('shared-proof',actions)
  shared=page.locator('.proof-step[data-proof-prefix="shared"]').first
  if shared.count():shared.scroll_into_view_if_needed();actions.append({'kind':'scroll','target':'shared proof after paper adaptation'})
  records[-1]['shared_proof_page_link_count']=page.locator('#reader-panel a[href^="/proofs/"]').count()
  records[-1]['source_proof_issue_access_requires_another_tab']=page.locator('#reader-panel .error-message').count()==0 and bool(next(r for r in data['math']['results'] if r['id']=='cvpr2023-reconstruction').get('related_issue_ids'))
  page.goto(base+'papers/cvpr2023-sparse-concepts/results/cvpr2023-linearity/');capture('repaired-proof-issue',[{'kind':'navigation','target':'result with repaired source proof'}])
  page.locator('#tab-original-proof').click();capture('repaired-proof-issue-source',[{'kind':'navigation','target':'result with repaired source proof'},{'kind':'click','target':'original proof to find the recorded error'}])
  # Task 4: identify a local source symbol, its canonical domain and baseline,
  # and return to the result. The current full-page navigation is observable.
  page.goto(base+'papers/iclr2024-generalizable/results/iclr2024-generalizable-andor/')
  symbol=page.locator('.related-symbols a[href*="#sym-output-baseline"]').first
  symbol.click();actions=[{'kind':'click','target':'output-baseline symbol from a proof'}];capture('symbol-mapping',actions)
  records[-1]['open_symbol_count']=page.locator('.symbol-card[open]').count()
  records[-1]['mapping_count_for_selected_symbol']=page.locator('#sym-output-baseline .symbol-mapping').count()
  records[-1]['current_result_return_link_count']=page.locator('#sym-output-baseline a[href*="/results/iclr2024-generalizable-andor/"]').count()
  browser.close()
 report={'status':'recorded','scope':'agent_browser_task_walkthrough_not_a_human_usability_study','recorded_at':datetime.now(timezone.utc).isoformat(),
  'snapshot_sha256':hashlib.sha256((WORK/'preview/data.public.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'tasks':records,'screenshots':screens}
 (EVIDENCE/'ui-workflow-evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'recorded','task_snapshots':len(records),'screenshots':len(screens)}))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8004/');main(parser.parse_args().base)
