#!/usr/bin/env python3
"""Check source attribution in Chromium without changing an intermediate snapshot."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse
from check_admitted_preview import ROOT,WORK,EVIDENCE,sync_playwright


def main(base,candidate_ui,report_name):
    if Path(report_name).name!=report_name or not report_name.endswith('.json') or report_name.startswith('root-'):
        raise ValueError('Expected a local non-root JSON report name')
    ui_path=WORK/('ui' if candidate_ui else 'preview')/'reader.js'
    paths=[WORK/'preview/data.public.json',WORK/'preview/data.public.js',WORK/'preview/reader.js',ui_path,Path(__file__).resolve()]
    paths=list(dict.fromkeys(paths))
    def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    before=hashes();data=json.loads(paths[0].read_text());results=data['math']['results'];checks=[];errors=[];external=[]
    def check(name,value,detail=None):checks.append({'name':name,'passed':bool(value),'detail':detail})
    # These are actual declared source classes in the existing snapshot. The
    # expected attribution is independently specified, rather than inferred
    # from the rendered label or the language of the author text.
    specs=[
        ('manual-author-proof','icml2022-transformation','original-proof','complete_manual_formal_proof_transcription','author'),
        ('manual-author-statement','neurips2021-robustness','statement','complete_manual_source_statement_transcription','author'),
        ('author-statement','icml2023-bayesian','statement','formal_author_transcription','author'),
        ('author-proof','icml2023-bayesian','original-proof','formal_author_transcription','author'),
        ('project-statement','neurips2024-dynamics','statement','formal_mathematical_transcription_with_project_chinese_translation','project'),
        ('project-proof','neurips2024-dynamics','original-proof','formal_complete_mathematical_transcription_with_project_chinese_translation','project'),
        ('no-author-proof','icml2023-bayesian','original-proof','no_local_author_proof','none'),
    ]
    cases=[]
    for label,paper,tab,kind,expected in specs:
        field='original_proof' if tab=='original-proof' else 'original_statement'
        row=next((r for r in results if r['paper_id']==paper and r.get(field+'_source_type')==kind and not r.get(field+'_note') and not r.get(field+'_heading')),None)
        check('actual-source-class:'+label,row is not None,{'paper_id':paper,'source_type':kind})
        if row:cases.append({'label':label,'tab':tab,'source_type':kind,'expected':expected,'row':row})
    material_specs=[('definition',lambda r:r.get('proof_target') is False and r.get('kind')=='definition' and r.get('proof_steps')),
                    ('experiment',lambda r:r.get('proof_target') is False and r.get('kind') in {'empirical','experimental_result','experiment'} and r.get('proof_steps')),
                    ('definition-with-Lean-evidence',lambda r:r.get('proof_target') is False and r.get('lean',{}).get('declarations') and r.get('proof_steps'))]
    materials=[]
    for label,predicate in material_specs:
        row=next((r for r in results if predicate(r)),None);check('actual-source-material:'+label,row is not None)
        if row:materials.append({'label':label,'row':row})
    with sync_playwright() as engine:
        browser=engine.chromium.launch(headless=True,args=['--no-sandbox']);context=browser.new_context(viewport={'width':1440,'height':1050})
        origin=urlparse(base);candidate=ui_path.read_text()
        def route(request):
            url=urlparse(request.request.url)
            if url.scheme in ('http','https') and (url.hostname,url.port)!=(origin.hostname,origin.port):external.append(request.request.url);request.abort()
            elif candidate_ui and url.path.endswith('/reader.js'):request.fulfill(status=200,content_type='application/javascript',body=candidate)
            else:request.continue_()
        context.route('**/*',route);page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
        for language in ['zh','en']:
            page.goto(base,wait_until='networkidle');page.evaluate('(lang)=>localStorage.setItem("proof-reader-language",lang)',language)
            for case in cases:
                row=case['row'];label=language+':'+case['label']+':'+row['id']
                page.goto(base+'papers/'+row['paper_id']+'/results/'+row['id']+'/',wait_until='networkidle')
                page.locator('#tab-'+case['tab']).click()
                notes=page.locator('#reader-panel .source-notes').all_inner_texts();headings=page.locator('#reader-panel .original-section h2').all_inner_texts()
                text='\n'.join(notes);heading='\n'.join(headings)
                expected=case['expected']
                if expected=='author':
                    check('author-attribution:'+label,('作者原文' in text and '作者原' in heading) if language=='zh' else ('author’s original wording' in text and 'Author ' in heading),{'notes':notes,'headings':headings})
                    check('author-not-mislabeled-as-translation:'+label,'原证明推导的中文说明' not in text and '数学内容与译文' not in heading and 'project translation or explanation' not in text)
                elif expected=='project':
                    check('project-explanation-disclosed:'+label,('项目译述' in text and '项目译述' in heading) if language=='zh' else ('project translation or explanation' in text and 'project explanation' in heading),{'notes':notes,'headings':headings})
                else:
                    check('no-local-author-proof-disclosed:'+label,'未提供本条独立的作者证明' in text if language=='zh' else 'provides no separate local author proof' in text,{'notes':notes,'headings':headings})
                    check('no-author-proof-not-missing-transcription:'+label,'未转录这一部分的完整原文' not in text and 'full source text is not transcribed' not in text)
                check('source-math:'+label,not page.evaluate('window.READER_MATH_ERRORS||[]'),page.evaluate('window.READER_MATH_ERRORS||[]'))
                check('source-width:'+label,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            for material in materials:
                row=material['row'];label=language+':'+material['label']+':'+row['id']
                page.goto(base+'papers/'+row['paper_id']+'/results/'+row['id']+'/',wait_until='networkidle');page.locator('#tab-rewrite').click()
                tab=page.locator('#tab-rewrite').inner_text();heading=page.locator('#reader-panel .complete-proof-heading').first.inner_text()
                check('source-material-explanation-label:'+label,tab==('Entry explanation' if language=='en' else '条目说明') and heading==('Entry explanation' if language=='en' else '条目说明'),{'tab':tab,'heading':heading,'source_role':row.get('rewrite_role'),'rewrite_status':row.get('rewrite_status'),'machine_evidence_role':row.get('lean',{}).get('evidence_role')})
                check('source-material-not-proof-idea:'+label,not page.locator('#reader-panel .proof-idea h2').filter(has_text='Proof idea' if language=='en' else '证明思路').count())
                check('source-material-math:'+label,not page.evaluate('window.READER_MATH_ERRORS||[]'))
                check('source-material-width:'+label,page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                if material['label']=='definition-with-Lean-evidence':
                    page.locator('#tab-lean').click();check('definition-machine-evidence-still-accessible:'+label,page.locator('.lean-declarations code').count()>0)
        check('no-js-errors',not errors,errors);check('no-external-requests',not external,external);browser.close()
    after=hashes();check('snapshot-unchanged',before==after)
    report={'status':'passed' if all(c['passed'] for c in checks) else 'failed','scope':'Actual author-transcription/project-translation/no-local-author-proof source attribution, plus definition/experiment explanation labels and accessible existing definition Lean evidence in Chinese and English. No mathematical admission, source-page completeness, Lean freshness or whole-library browser acceptance.','candidate_ui_route_override':candidate_ui,'published_preview_modified':False,'served_paper_count':len(data['papers']),'panels_checked':(len(cases)+len(materials))*2,'selected_cases':[{k:v for k,v in c.items() if k!='row'}|{'result_id':c['row']['id']} for c in cases],'source_material_cases':[{'label':c['label'],'result_id':c['row']['id']} for c in materials],'snapshot_hashes':{'before':before,'after':after},'checks':checks,'js_errors':errors,'external_requests':external}
    (EVIDENCE/report_name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'panels_checked':report['panels_checked'],'checks':len(checks),'failures':[c for c in checks if not c['passed']]},ensure_ascii=False))
    return report['status']!='passed'


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8004/');parser.add_argument('--candidate-ui',action='store_true');parser.add_argument('--report-name',default='source-presentation-checks.json')
    args=parser.parse_args();raise SystemExit(main(args.base,args.candidate_ui,args.report_name))
