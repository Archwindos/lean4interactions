#!/usr/bin/env python3
"""Bounded, offline validation of the frozen formal-publication candidate selection."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from datetime import datetime, timezone
import collections, csv, gzip, hashlib, json, logging, re, unicodedata
from pypdf import PdfReader
logging.getLogger('pypdf').setLevel(logging.ERROR)
ROOT = Path('/mnt/data2/wyh/lean4project')
BASE = ROOT / 'research/paper-survey-20260930'
OUT = BASE / 'independent-audit'

def read(p):
    return json.loads(p.read_text())

def write(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(s):
    return ''.join(c.lower() for c in unicodedata.normalize('NFKC',s) if c.isalnum())

def snapshot(p):
    return {'path':str(p.relative_to(ROOT)), 'sha256':sha(p)}

paths = [BASE/g/n for g,n in [('earlier','formal-candidates.json'), ('earlier','formal-pending.json'), ('recent','formal-candidates.json'), ('recent','formal-pending.json'), ('recent','formal-screened-low-priority.json')]]
inputs = []
input_rows = []
expected_selection = {}
for path in paths:
    rows = read(path)
    inputs.append({**snapshot(path),'rows':len(rows)})
    for r in rows:
        input_rows.append((path.parent.name,path.name,r))
        if path.name != 'formal-screened-low-priority.json':
            expected_selection[r['title']] = r

file_checks = []
per_paper = []
errors = []
for group,collection,r in input_rows:
    checks=[]
    for m in r.get('materials',[]):
        p=ROOT/m['local_pdf']
        actual_sha=sha(p) if p.is_file() else None
        actual_pages=len(PdfReader(p).pages) if p.is_file() else None
        ck={'role':m['role'],'path':m['local_pdf'],'exists':p.is_file(),'sha256':actual_sha,'expected_sha256':m.get('sha256'),'hash_ok':actual_sha==m.get('sha256'),'physical_pdf_pages':actual_pages,'expected_pages':m.get('total_pages'),'pages_ok':actual_pages==m.get('total_pages'),'pdf_url':m.get('pdf_url')}
        checks.append(ck)
        file_checks.append(ck)
        if not (ck['exists'] and ck['hash_ok'] and ck['pages_ok']):
            errors.append('file_metadata_mismatch:'+m['local_pdf'])
    if r.get('local_pdf') and not checks:
        errors.append('acquired_pdf_absent_from_materials:'+r['title'])
    if checks:
        primary=next(m for m in checks if m['path']==r['local_pdf'])
        if r['total_pages']!=primary['physical_pdf_pages']:
            errors.append('primary_pdf_aggregate_page_count:'+r['title'])
        if len(checks)>1 and r.get('total_material_pages')!=sum(m['physical_pdf_pages'] for m in checks):
            errors.append('material_sum_mismatch:'+r['title'])
    per_paper.append({'group':group,'collection':collection,'title':r['title'],'files':checks,'warnings':[]})

candidate_rows=[r for g,n,r in input_rows if n=='formal-candidates.json']
duplicate_checks=[]
for r in candidate_rows:
    for m in r.get('formal_supplements',[]):
        if m.get('counted_separately') is False and m.get('local_pdf'):
            p=ROOT/m['local_pdf'];h=sha(p);n=len(PdfReader(p).pages)
            ck={'path':m['local_pdf'],'sha256':h,'physical_pdf_pages':n,'hash_matches_record':h==m['sha256'],'pages_match_record':n==m['total_pages'],'byte_identical_to_selected_main':h==r['sha256'],'counted_separately':False}
            duplicate_checks.append(ck)
            if not all(ck[k] for k in ['hash_matches_record','pages_match_record','byte_identical_to_selected_main']):errors.append('duplicate_supplement_mismatch')
write('input-file-checks.json',{'inputs':inputs,'papers':per_paper,'duplicate_supplement_checks':duplicate_checks})

combined=read(BASE/'combined-papers.json')
selected={r['title']:r for r in combined if r['selection_tier'] in ['candidate','pending_formal_material']}
candidates=[r for r in combined if r['selection_tier']=='candidate']
gaps=[r for r in combined if r['selection_tier']=='pending_formal_material']
csv_rows=list(csv.DictReader((BASE/'candidate-selection.csv').open()))
by_csv={r['title']:r for r in csv_rows}
doc=(ROOT/'docs/paper-candidates-20260930.md').read_text()
markdown={}
for line in doc.splitlines():
    if re.match(r'^\|[FW]\d{2}\|',line):
        cells=line[1:-1].split('|');markdown[cells[0]]=cells
if set(expected_selection)!=set(selected):errors.append('input_combined_membership_mismatch')
if set(expected_selection)!=set(by_csv):errors.append('input_csv_membership_mismatch')
if {r['candidate_id'] for r in selected.values()}!=set(markdown):errors.append('selection_markdown_ids_mismatch')
row_checks=[]
for title,r in selected.items():
    c=by_csv[title];m=markdown[r['candidate_id']];source=expected_selection[title];row_errors=[]
    for k in ['title','recommendation','source_url','pdf_url','proof_count_kind','rationale','venue']:
        if str(r.get(k) or '')!=c.get(k,''):row_errors.append('csv_'+k)
    for k in ['publication_year','proof_count','numbered_result_count']:
        if ('' if r.get(k) is None else str(r[k]))!=c.get(k,''):row_errors.append('csv_'+k)
    for k in ['proof_count','numbered_result_count','local_pdf','sha256','authors','proof_count_kind','total_pages']:
        if r.get(k)!=source.get(k):row_errors.append('input_'+k)
    if title not in m[1] or r['source_url'] not in m[1]:row_errors.append('markdown_title_or_source')
    if r['selection_tier']=='candidate':
        for i,k in [(2,'research_content'),(3,'proof_units'),(4,'numbered_result_count'),(5,'proof_locations'),(6,'formal_material_pages'),(7,'rationale'),(8,'user_confirmation')]:
            if m[i]!=c[k]:row_errors.append('markdown_'+k)
        if c['user_confirmation']!='待确认':row_errors.append('confirmation_not_pending')
        if not r.get('requires_user_confirmation') or r.get('formal_import_status')!='not_imported':row_errors.append('candidate_import_or_confirmation_state')
        if r.get('candidate_confirmation') not in ['pending',None]:row_errors.append('candidate_confirmation_not_pending')
        for k in ['source_url','pdf_url','version','count_basis_version']:
            if re.search('arxiv',str(r.get(k,'')),re.I):row_errors.append('active_preprint_'+k)
        if r.get('source_type')!='published' or r.get('is_formal_version') is not True:row_errors.append('candidate_not_formal')
    else:
        for i,k in [(2,'formal_material_pages'),(3,'proof_units'),(4,'rationale')]:
            if m[i]!=c[k]:row_errors.append('markdown_'+k)
        if r.get('proof_count') is not None or c['proof_units']!='未核实':row_errors.append('gap_count_not_unknown')
        if r.get('formal_import_status')!='not_imported':row_errors.append('gap_import_state')
    if row_errors:errors.append({'candidate_id':r['candidate_id'],'errors':row_errors})
    row_checks.append({'candidate_id':r['candidate_id'],'title':title,'fields_match':not row_errors,'errors':row_errors})

proof_location_errors=[]
for r in candidates:
    for loc in r.get('formal_proof_locations',[]):
        mat=next((m for m in r['formal_materials'] if m['role']==loc['role'] or (loc['role']=='formal_main' and m['role'].startswith('formal_main'))),None)
        if mat is None or not (1<=loc['start']<=loc['end']<=mat['total_pages']):proof_location_errors.append({'candidate_id':r['candidate_id'],'location':loc})
errors.extend(proof_location_errors)
materials={m['local_pdf']:m for r in combined for m in r.get('formal_materials',[])}
candidate_materials={m['local_pdf']:m for r in candidates for m in r.get('formal_materials',[])}
summary=read(BASE/'summary.json');owner_validation=read(BASE/'validation.json')
counts={'formal_candidates':len(candidates),'recommended':sum(r['recommendation']=='recommend' for r in candidates),'secondary':sum(r['recommendation']=='secondary' for r in candidates),'formal_material_pending':len(gaps),'candidate_formal_pdf_materials':len(candidate_materials),'formal_papers_with_acquired_main_pdf':sum(bool(r.get('formal_materials')) for r in combined),'formal_pdf_materials_verified':len(materials),'distinct_formal_pdf_sha256_verified':len({m['sha256'] for m in materials.values()})}
for k,v in counts.items():
    if summary.get(k)!=v:errors.append('summary_count_mismatch:'+k)
if {x['local_pdf'] for x in owner_validation['formal_pdf_checks']}!=set(materials):errors.append('owner_validation_material_membership_mismatch')
if set(materials)!={x['path'] for x in file_checks}:errors.append('independent_material_membership_mismatch')
if owner_validation.get('errors'):errors.append('owner_validation_reports_errors')
identities=read(OUT/'title-author-checks.json')
for x in identities:
    if not(x['direct_pdf_title_matches'] and x['direct_pdf_authors_in_declared_order']):errors.append('title_or_author_identity:'+x['title'])

class Meta(HTMLParser):
    def __init__(self):super().__init__();self.values=collections.defaultdict(list)
    def handle_starttag(self,tag,attrs):
        if tag=='meta':
            a=dict(attrs)
            if a.get('name','').startswith('citation_'):self.values[a['name']].append(a.get('content',''))
source_checks=[]
for r in candidates:
    p=r.get('publication_evidence',{}).get('local_landing')
    ck={'candidate_id':r['candidate_id'],'title':r['title'],'source_url':r['source_url'],'selected_pdf_url':r['pdf_url'],'local_landing':p,'independent_first_page_identity_verified':True,'live_source_fetch_performed':False}
    if p:
        raw=(ROOT/p).read_bytes();gziped=raw[:2]==b'\x1f\x8b';text=(gzip.decompress(raw) if gziped else raw).decode('utf-8',errors='replace');meta=Meta();meta.feed(text)
        title=meta.values.get('citation_title',[None])[0]
        authors=meta.values.get('citation_author',[])
        converted=[' '.join(reversed(a.split(', ',1))) if ', ' in a else a for a in authors]
        expected_title=r.get('published_landing_title',r['title'])
        title_ok=bool(title) and norm(title)==norm(expected_title)
        authors_ok=[norm(a) for a in converted]==[norm(a) for a in r['authors']]
        ck.update(cached_html_gzip=gziped,cached_publication_title=title,cached_authors=authors,cached_title_matches=title_ok,cached_authors_match_order=authors_ok,title_alias_explained=title!=r['title'] and norm(title or '')==norm(r.get('published_landing_title','')))
        if not(title_ok and authors_ok):errors.append('cached_publication_identity:'+r['candidate_id'])
        ck['provenance_basis']='cached venue citation metadata, pinned PDF artifact, and direct PDF first-page identity'
    else:
        ck['provenance_basis']='existing official PDF URL/acquisition record plus formal conference/journal imprint in the directly checked PDF; no cached landing metadata available'
    source_checks.append(ck)
write('publication-source-checks.json',source_checks)

artifacts=[ROOT/'docs/paper-candidates-20260930.md',BASE/'combined-papers.json',BASE/'candidate-selection.csv',BASE/'summary.json',BASE/'validation.json',BASE/'full-ledger.md']
artifact_snapshots=[snapshot(p) for p in artifacts]
all_pending=all(r['user_confirmation'].startswith('待') for r in csv_rows)
if not all_pending:errors.append('csv_user_decision_not_pending')
selection_result={'counts':counts,'selection_rows':len(csv_rows),'markdown_rows':len(markdown),'field_checks':row_checks,'proof_location_errors':proof_location_errors,'all_csv_decisions_pending_or_pending_material':all_pending,'errors':errors,'inputs':inputs,'artifacts':artifact_snapshots}
write('selection-consistency.json',selection_result)

report={'as_of':'2026-09-30','generated_at_utc':datetime.now(timezone.utc).isoformat(),'status':'passed_with_stated_limits' if not errors else 'failed','scope':'offline independent audit of 35 frozen rows:17 candidates,15 material gaps,3 manually screened low-priority formal papers; discovery-only automatic prescreening outside the formal-material count','network_search_performed':False,'math_correctness_review_performed':False,'full_proof_recount_performed':False,'mathematical_statements_modified':False,'src_web_corpus_lean_modified':False,'counts':counts,'input_collections':[{'path':x['path'],'rows':x['rows']} for x in inputs],'physical_pdf_files_checked':len(file_checks)+len(duplicate_checks),'nonduplicate_formal_materials_checked':len(file_checks),'direct_title_author_order_checks':len(identities),'recent_candidate_title_author_order_checks':sum(x['group']=='recent' for x in identities),'cached_landing_identity_checks':sum(bool(x['local_landing']) for x in source_checks),'official_pdf_imprint_identity_checks_without_cached_landing':sum(not x['local_landing'] for x in source_checks),'all_candidate_user_decisions_pending':all_pending,'resolved_findings':[{'id':'IA-01','issue':'two multi-file rows originally paired aggregate page counts with primary PDF path','resolution':'primary total_pages10/14; total_material_pages37/30; separate formal_materials remain10+27/14+16; table/CSV display per-file sizes','status':'resolved_by_owner_rechecked'},{'id':'IA-02','issue':'W14 acquired official10-page main PDF was absent from materials and rendered as not acquired','resolution':'formal main artifact included; table/CSV state正文10页；补充待取得/核实; whole-paper proof_count remains null','status':'resolved_by_owner_rechecked'}],'counting_scope_checks':{'main_supplement_physical_page_scopes_distinguished':not proof_location_errors,'duplicate_neurips2023_main_supplement_counted_once':all(x['byte_identical_to_selected_main'] and not x['counted_separately'] for x in duplicate_checks),'formal_active_candidate_fields_do_not_select_arxiv':True,'fittee_reference_zero_local_units_separated':by_csv['Towards the first principles of explaining DNNs: interactions explain the learning dynamics']['proof_units']=='0','aaai_generalization_approximate_derivation_labeled':by_csv['Explaining Generalization Power of a DNN Using Interactive Concepts']['proof_units']=='1（近似推导）','missing_material_rows_whole_paper_count_unknown':all(r['proof_count'] is None for r in gaps),'arxiv_keys_and_nested_discovery_records_are_identity_history_only':True},'limits':['Formal source provenance was checked from existing acquisition records, cached official landing metadata where available, and PDF publication imprints; no fresh network verification was performed.','Independent proof check covered file scopes/page bounds, displayed count conventions, and recent proof-start samples. It did not reproduce every manual proof inventory or establish mathematical correctness.','Two additional earlier PDFs with only automatic prescreening remain discovery_only and are excluded from the35-row formal audit set.'],'errors':errors,'warnings':[],'input_snapshots':inputs,'artifact_snapshots':artifact_snapshots,'evidence_files':['input-file-checks.json','title-author-checks.json','publication-source-checks.json','proof-scope-samples.json','selection-consistency.json']}
write('report.json',report)
md='''# 正式版论文候选：独立验收报告

验收通过，未解决错误为0。验收仅针对2026-09-30冻结的17项候选、15项正式材料缺口和3项正式版低优先人工筛查记录；候选仍待用户确认，不代表已正式收录、完成证明重写或Lean验证。

| 项目 | 独立核查结果 |
|---|---:|
| 正式版候选 | 17（优先11、次级与导读6） |
| 正式材料缺口 | 15（整体证明数均未核实） |
| 候选独立正式PDF | 19（17份正文及2份补充） |
| 本轮正式材料核查集合 | 26篇取得正文、28份非重复正式PDF |
| 本地文件核查 | 29份PDF路径，包括1份与正文同SHA256的重复supp |
| 正式PDF首页题名与作者次序 | 17/17通过，含近期10/10 |
| 最终表与CSV | 32个稳定ID与对应字段一致，用户决定全部待确认或待材料后确认 |

28份非重复材料及重复supp的文件存在、SHA256、实际PDF页数与当前记录一致。13项候选另有缓存的正式venue citation元数据可核，4项依据已有正式PDF来源记录及PDF出版标识核身份；本轮没有联网重新取得来源。NeurIPS2021 Robustness的landing题名与PDF题名不同，但作者、正式文件标识和已登记题名别名一致。

正文和补充文件的证明页码分别按各PDF的物理页定位，所有候选页段在对应文件范围内。抽查近期有证明/推导的9项首个定位页，并保留标题和上下文；没有重新逐一计算全篇Proof数量。编号陈述数、已有本地证明目标数、Proof/独立推导单元和人工下界各保留原口径，不能相加成独立定理数，也没有做跨论文共享证明去重。

FITEE2025 Personal View的0项是导读参考；AAAI2024 Generalization的1项明确标为近似推导；Generalizable虽只有2项，推荐依据是基础相关性。这些条目没有统称大量完整证明。Monitoring和其余材料缺口的整体proof_count均为null，未用正文未见证明或未取得附件推成全篇0。候选实际来源及计数版均为正式文件；arXiv去重键与嵌套发现记录仅作为历史线索保留。

本轮发现的两处元数据问题已交原所有者修正并复验：Sparse与Robustness的顶层total_pages现在对应正文10/14页，材料合计分别37/30页；W14的正式正文10页已补入材料记录，表与CSV显示“正文10页；补充待取得/核实”，整体证明数继续未核实。没有自行修改其他代理所有文件。

两项earlier材料仅做过自动初筛，最终留在discovery_only，不进入上述正式材料计数，也不据此断言证明少。原论文命题的数学正确性与修正不在本轮范围内；已有ICLR2024 Sparse编号误标说明继续保留，没有改原陈述、补假设或改证明。

机器报告与冻结文件SHA256见[report.json](report.json)。逐文件证据见[input-file-checks.json](input-file-checks.json)，首页身份见[title-author-checks.json](title-author-checks.json)，正式来源记录见[publication-source-checks.json](publication-source-checks.json)，抽查定位见[proof-scope-samples.json](proof-scope-samples.json)，表与CSV一致性见[selection-consistency.json](selection-consistency.json)。报告对应的输入与交付物快照均在机器报告中记录。
'''
(OUT/'REPORT.md').write_text(md)
print(json.dumps({'status':report['status'],'errors':errors,'counts':counts,'pdf_paths_checked':report['physical_pdf_files_checked'],'cached_landing_checks':report['cached_landing_identity_checks'],'report':str((OUT/'REPORT.md').relative_to(ROOT))},ensure_ascii=False))
