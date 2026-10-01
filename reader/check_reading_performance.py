#!/usr/bin/env python3
"""Measure real local reading, search and scrolling; no mathematical acceptance is inferred."""
import argparse
import hashlib
import json
import statistics
import time
from datetime import datetime,timezone
from pathlib import Path
from check_preview import ROOT,WORK,EVIDENCE,sync_playwright

def main(base,report_name='reading-performance.json'):
 if Path(report_name).name!=report_name or not report_name.endswith('.json') or report_name.startswith('root-'):raise ValueError('Expected a local non-root JSON report name')
 data=json.loads((WORK/'preview/data.public.json').read_text())
 paths=[WORK/'preview/data.public.json',WORK/'preview/data.public.js',WORK/'preview/reader.js',WORK/'preview/reader.css',Path(__file__).resolve(),WORK/'check_preview.py',WORK/'evidence_paths.py',EVIDENCE/'build-manifest.json']
 manifest=json.loads((EVIDENCE/'build-manifest.json').read_text())
 before={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 measurements=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox']);ctx=browser.new_context(viewport={'width':1440,'height':1050},reduced_motion='reduce');page=ctx.new_page()
  long=max(data['math']['results'],key=lambda r:sum(len(str(s.get('body_md','')))+len(str(s.get('formula_tex',''))) for s in r.get('proof_steps',[])))
  largest=max(data['papers'],key=lambda paper:sum(r['paper_id']==paper['id'] for r in data['math']['results']))
  tasks=[('home',''),('largest-paper-directory','papers/'+largest['id']+'/'),('long-proof','papers/'+long['paper_id']+'/results/'+long['id']+'/'),('all-symbols','symbols/')]
  for name,path in tasks:
   samples=[]
   for run in range(5):
    started=time.perf_counter();page.goto(base+path,wait_until='load');page.wait_for_selector('h1');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    samples.append({'run':run,'local_navigation_ms':round((time.perf_counter()-started)*1000,2),**page.evaluate('''()=>{
     const n=performance.getEntriesByType('navigation')[0];return {dom_content_loaded_ms:n.domContentLoadedEventEnd,load_ms:n.loadEventEnd,dom_nodes:document.getElementsByTagName('*').length,katex_nodes:document.querySelectorAll('.katex').length,page_height:document.documentElement.scrollHeight,heap_bytes:performance.memory&&performance.memory.usedJSHeapSize};
    }''')})
   values=[s['local_navigation_ms'] for s in samples]
   measurements.append({'task':name,'path':path,'samples':samples,'median_navigation_ms':statistics.median(values),'maximum_navigation_ms':max(values)})
  page.goto(base,wait_until='load');search=page.locator('.paper-search input');search_times=[]
  for query in ['Theorem','Shapley','interaction','__no_matching_result__','']:
   elapsed=search.evaluate("(x,q)=>{const start=performance.now();x.value=q;x.dispatchEvent(new Event('input',{bubbles:true}));return performance.now()-start}",query)
   search_times.append({'query':query,'synchronous_event_ms':elapsed,'result_count':page.locator('[data-search-result]').count()})
  page.goto(base+'papers/'+long['paper_id']+'/results/'+long['id']+'/',wait_until='load')
  scroll=page.evaluate('''async()=>{
   const frames=[],max=document.documentElement.scrollHeight-innerHeight;let before=performance.now();
   for(let i=0;i<30;i++){scrollTo(0,max*i/29);await new Promise(requestAnimationFrame);const now=performance.now();frames.push(now-before);before=now;}
   return {frames_ms:frames,maximum_frame_ms:Math.max(...frames),reached_end:scrollY>=max-2,horizontal_overflow:document.documentElement.scrollWidth>innerWidth};
  }''')
  ctx.close();browser.close()
 after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 current_inputs=[{'path':item['path'],'sha256':item['sha256'],'current':(ROOT/item['path']).is_file() and hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']} for item in manifest['inputs']]
 report={'status':'measured' if before==after and all(item['current'] for item in current_inputs) else 'stale','scope':'actual_local_chromium_performance_not_remote_network_or_human_usability','recorded_at':datetime.now(timezone.utc).isoformat(),
  'build_inputs':current_inputs,
  'snapshot_hashes':{'before':before,'after':after},'paper_count':len(data['papers']),'result_count':len(data['math']['results']),
  'payload_bytes':{p.name:p.stat().st_size for p in paths[:2]},'measurements':measurements,'search':search_times,'long_proof_scroll':scroll,
  'interpretation':'Five same-browser local navigations mix cold and cached reads; maximum and median are reported. These measurements do not predict a remote host or slower device.'}
 (EVIDENCE/report_name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'navigation_medians_ms':{r['task']:r['median_navigation_ms'] for r in measurements},'max_search_event_ms':max(r['synchronous_event_ms'] for r in search_times),'scroll':{k:v for k,v in scroll.items() if k!='frames_ms'}}))
 return report['status']!='measured'

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8004/');parser.add_argument('--report-name',default='reading-performance.json')
 args=parser.parse_args();raise SystemExit(main(args.base,args.report_name))
