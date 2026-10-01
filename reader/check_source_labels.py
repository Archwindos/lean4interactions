#!/usr/bin/env python3
"""Recheck affected source-panel labels after a translation-only UI correction."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse
from check_admitted_preview import ROOT,WORK,EVIDENCE,sync_playwright


def main(base,baseline_name,report_name):
    for name in (baseline_name,report_name):
        if Path(name).name!=name or not name.endswith('.json') or name.startswith('root-'):
            raise ValueError('Expected a local non-root JSON report name')
    baseline_path=EVIDENCE/baseline_name
    prior=json.loads(baseline_path.read_text())
    failures=[row for row in prior['checks'] if not row['passed']]
    if not failures or any(not row['name'].startswith('english-source-labels:') for row in failures):
        raise ValueError('The prerequisite browser run has failures beyond source labels')
    paths=[WORK/'preview/data.public.json',WORK/'preview/data.public.js',WORK/'preview/reader.js',
           WORK/'preview/reader.css',EVIDENCE/'build-manifest.json',Path(__file__).resolve(),baseline_path]
    def fingerprints():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    before=fingerprints();old=prior['snapshot_hashes']['after'];checks=[];errors=[];external=[]
    def check(name,value,detail=None):checks.append({'name':name,'passed':bool(value),'detail':detail})
    for path in paths[:4]:
        if path.name!='reader.js':check('unchanged-before-label-fix:'+path.name,before[str(path.relative_to(ROOT))]==old[str(path.relative_to(ROOT))])
    data=json.loads(paths[0].read_text());results={r['id']:r for r in data['math']['results']}
    manifest=json.loads(paths[4].read_text())
    with sync_playwright() as engine:
        browser=engine.chromium.launch(headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1440,'height':1050})
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        origin=urlparse(base)
        def route(request):
            url=urlparse(request.request.url)
            if url.scheme in ('http','https') and (url.hostname,url.port)!=(origin.hostname,origin.port):
                external.append(request.request.url);request.abort()
            else:request.continue_()
        context.route('**/*',route)
        page.goto(base,wait_until='networkidle');page.locator('#language-select').select_option('en')
        page.wait_for_function('window.READER_LANGUAGE === "en"')
        for ident in prior['selected_result_ids']:
            row=results[ident]
            page.goto(base+'papers/'+row['paper_id']+'/results/'+ident+'/',wait_until='networkidle')
            for tab in ('statement','original-proof'):
                page.locator('#tab-'+tab).click()
                page.locator('#reader-panel details').evaluate_all('xs=>xs.forEach(x=>x.open=true)')
                labels=page.locator('#reader-panel .source-links,#reader-panel .source-notes,#reader-panel details>summary,#reader-panel figcaption').evaluate_all("xs=>xs.map(x=>{const y=x.cloneNode(true);y.querySelectorAll('.katex,code,pre,.raw-source').forEach(z=>z.remove());return y.textContent}).filter(x=>/[\\u3400-\\u9fff]/.test(x))")
                alternatives=page.locator('#reader-panel img[alt]').evaluate_all("xs=>xs.map(x=>x.alt).filter(x=>/[\\u3400-\\u9fff]/.test(x))")
                check('english-source-labels:'+ident+':'+tab,not labels,labels)
                check('english-source-image-alt:'+ident+':'+tab,not alternatives,alternatives)
                check('source-math:'+ident+':'+tab,not page.evaluate('window.READER_MATH_ERRORS||[]'))
                check('source-viewport:'+ident+':'+tab,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        check('no-browser-errors',not errors,errors);check('no-external-requests',not external,external)
        browser.close()
    for row in manifest['inputs']:
        path=ROOT/row['path'];check('current-build-input:'+row['path'],path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'])
    after=fingerprints();check('snapshot-stable-during-source-label-check',before==after)
    report={'status':'passed' if all(r['passed'] for r in checks) else 'failed',
            'scope':'Affected English source labels/alt text/math/width for twenty panels; full source-image decoding and unchanged proof/Lean/symbol paths remain in the prerequisite run.',
            'baseline_report':{'path':str(baseline_path.relative_to(ROOT)),'sha256':before[str(baseline_path.relative_to(ROOT))],
                'passing_checks':sum(r['passed'] for r in prior['checks']),'known_label_failures':len(failures)},
            'snapshot_hashes':{'before':before,'after':after},'selected_result_ids':prior['selected_result_ids'],
            'source_panels_checked':len(prior['selected_result_ids'])*2,'checks':checks,'js_errors':errors,'external_requests':external}
    (EVIDENCE/report_name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'checks':len(checks),'source_panels_checked':report['source_panels_checked'],
                      'failures':[r for r in checks if not r['passed']]},ensure_ascii=False))
    return report['status']!='passed'


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8004/')
    parser.add_argument('--baseline',default='ten-paper-browser-before-source-label-fix.json')
    parser.add_argument('--report-name',default='ten-paper-source-label-checks.json')
    args=parser.parse_args();raise SystemExit(main(args.base,args.baseline,args.report_name))
