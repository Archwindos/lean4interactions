#!/usr/bin/env python3
"""Formal-publication-only candidate inventory, with preprints retained as discovery."""
import collections, copy, hashlib, json, pathlib, re
ROOT=pathlib.Path('/mnt/data2/wyh/lean4project')
BASE=ROOT/'research/paper-survey-20260930/recent'
REL=BASE.relative_to(ROOT).as_posix()
def read(n):return json.loads((BASE/n).read_text())
def write(n,o):(BASE/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def spanpages(spans):return sorted({p for a,z in spans for p in range(a,z+1)})
def unit(section,pages,targets=None,kind='proof'):
 return {'section':section,'pdf_pages':pages,'numbered_targets':targets or [],'unit_type':kind,'units':1}

DISC=read('screened-discovery-papers.json')
BYID={p['arxiv_id']:p for p in DISC if p.get('arxiv_id')}
DOWNLOADS={e['id']:e for name in ['venue-downloads.json','extra-downloads.json','formal-downloads.json'] for e in read(name)}
for key,url in {
 'icml2025-coalition':'https://proceedings.mlr.press/v267/zheng25d.html',
 'icml2023-harsanyinet':'https://proceedings.mlr.press/v202/chen23s.html',
 'icml2023-symbolic-concepts':'https://proceedings.mlr.press/v202/li23at.html',
}.items():DOWNLOADS[key]['source_url']=url
FORMAL=[
 ('iclr2024-sparse','2305.01939','Where We Have Arrived in Proving the Emergence of Sparse Interaction Primitives in DNNs','ICLR',2024,11,10,10,[[15,27]],'recommend',[
  unit('B.1 Theorem 1',[15],['Theorem 1']),unit('B.2 Lemma 1',[15,16],['Lemma 1']),unit('B.2 Assumption 1-β implies 1-α',[16]),
  unit('B.3 Lemma 2',[16,17],['Lemma 2']),unit('B.3 Lemma 3',[17,18],['Lemma 3']),unit('B.3 Theorem 2',[18,19,20],['Theorem 2']),
  unit('B.4 Main Theorem 3, appendix mislabels it Theorem 6',[20],['Theorem 3']),unit('B.5 Lemma 4',[21],['Lemma 4']),
  unit('B.5 Theorem 4',[21,22,23],['Theorem 4']),unit('B.6 Theorem 5',[23,24,25],['Theorem 5']),unit('B.7 Theorem 6',[25,26,27],['Theorem 6'])],
  '证明密集：10个独立编号结果均有本地证明，加1个假设蕴含证明；含组合矩阵、稀疏上界及三种Shapley指标关系。'),
 ('icml2025-coalition','2309.13411',None,'ICML',2025,10,7,7,[[12,21]],'recommend',[
  unit('C Theorem 3.2 (appendix label Theorem 2)',[12,13,14],['Theorem 3.2']),unit('D Theorem 3.3 (appendix label Theorem 3)',[14,15],['Theorem 3.3']),
  unit('E Theorem 3.4 and Corollary 3.5',[15,16],['Theorem 3.4','Corollary 3.5']),unit('F Theorem 3.6 and Corollary 3.7',[16,17],['Theorem 3.6','Corollary 3.7']),
  unit('G.1 Anonymity',[17,18]),unit('G.2 Symmetry-α',[18,19]),unit('G.3 Symmetry-β',[19,20]),unit('G.4 Additivity',[20]),unit('G.5 Dummy',[21]),unit('G.6 Corollary 3.8 / Efficiency',[21],['Corollary 3.8'])],
  '证明密集：7个编号定理/推论、10个证明小节；coalition与单变量归因关系及AND/OR分配公理可逐项对齐。'),
 ('neurips2024-dynamics','2407.19198',None,'NeurIPS',2024,8,9,7,[[16,24]],'recommend',[
  unit('F.1 Theorem 2 universal matching',[16,17,18],['Theorem 2']),unit('F.2 Lemma 3',[18,19],['Lemma 3']),unit('F.2 Equations (6) and (7)',[19,20]),
  unit('F.3 Lemma 1',[20,21],['Lemma 1']),unit('F.4 Theorem 3',[21,22],['Theorem 3']),unit('F.5 Lemma 2',[22,23],['Lemma 2']),
  unit('F.6 Theorem 4',[23],['Theorem 4']),unit('F.7 Theorem 5',[24],['Theorem 5'])],
  '证明密集：7个本地有专门证明的编号目标及一个方程证明，涵盖噪声、Taylor触发函数、回归最优解和两阶段动态。'),
 ('icml2023-bayesian','2302.13095',None,'ICML',2023,6,7,6,[[15,22]],'recommend',[
  unit('G.1 Lemma 2.1',[15,16],['Lemma 2.1']),unit('G.2 Theorem 2.2',[16,17],['Theorem 2.2']),unit('G.3 Theorem 2.3',[17,18],['Theorem 2.3']),
  unit('G.4 Theorem 2.4',[18,19,20],['Theorem 2.4']),unit('G.5 Theorem 2.5',[20,21,22],['Theorem 2.5']),unit('G.6 Theorem 2.6',[22],['Theorem 2.6'])],
  '证明密集：6个编号目标有对应证明，连接BNN不确定性、概念复杂度、扰动矩及回归权重；Prop G.1声明未算额外证明。'),
 ('icml2023-harsanyinet','2304.01811',None,'ICML',2023,5,5,4,[[12,14],[16,16]],'recommend',[
  unit('B Theorem 2',[12],['Theorem 2']),unit('B Theorem 3',[13],['Theorem 3']),unit('B Theorem 4',[13,14],['Theorem 4']),
  unit('C Lemma 1',[14],['Lemma 1']),unit('E Harsanyi-CNN Setting 2',[16])],
  '证明较集中且Harsanyi基础重要：精确Shapley网络构造有4个本地编号证明及1个CNN扩展证明，适合连接核心有限集合理论。'),
 ('neurips2023-difficulty-main',None,'Towards the Difficulty for a Deep Neural Network to Learn Concepts of Different Complexities','NeurIPS',2023,4,5,3,[[17,21]],'recommend',[
  unit('G.1 Theorem 2',[17,18],['Theorem 2']),unit('G.2 Theorem 3',[18,19],['Theorem 3']),unit('G.3 Theorem 4',[20],['Theorem 4']),
  unit('G.4 Concepts and multi-order interactions',[20,21],kind='complete_derivation')],
  '3个本地编号证明及1个完整组合关系推导，解释复杂概念的学习难度；G.5回归草图另记、不充当完整证明。'),
 ('iclr2024-generalizable','2401.16318','Defining and Extracting Generalizable Interaction Primitives from DNNs','ICLR',2024,2,4,1,[[12,15]],'recommend',[
  unit('C Theorem 2: AND, OR, combined under one Proof block',[12,13,14],['Theorem 2']),unit('D Variance of AND/OR interactions',[15])],
  '证明数量不多，但Harsanyi/AND-OR基础重要：精确重构和方差共2个证明单元；引用的Theorem 1/3及Prop 1不额外算本地证明。'),
 ('icml2024-layerwise','2409.08712',None,'ICML',2024,2,2,2,[[15,16]],'secondary',[
  unit('F Theorem 3.3',[15],['Theorem 3.3']),unit('G Lemma 3.4',[16],['Lemma 3.4'])],
  '逐层知识/交互研究有2个清晰目标与证明，是基础matching到中间层应用的次级候选。'),
 ('aaai2024-generalization','2302.13091',None,'AAAI',2024,1,3,0,[[5,6]],'secondary',[
  unit('Main pp5–6 Taylor/moment and approximate variance-growth analysis',[5,6],kind='approximate_derivation')],
  '公开正式正文有3个编号陈述及1个近似推导；没有专门完整证明附录，应与证明密集成果区分。'),
 ('fitee2025-first-principles',None,'Towards the first principles of explaining DNNs: interactions explain the learning dynamics','FITEE',2025,0,0,0,[],'secondary',[],
  '正式Personal View提供交互理论体系与学习动态导读；本地新证明为0，作为基础参考单列。'),
 ('aaai2025-monitoring',None,'Monitoring Primitive Interactions During the Training of DNNs','AAAI',2025,0,1,0,[],'uncertain',[],
  '正式9页正文有Theorem 2.1，证明指定在未取得的Appendix E；整体证明密度须取得正式补充材料后再判断。'),
 ('icml2023-symbolic-concepts','2302.13080',None,'ICML',2023,0,0,0,[],'low_priority',[],
  '完整正式18页PDF已核：稀疏性、迁移性、判别与语义的实证验证，无本地编号理论证明。'),
 ('acl2024-semantic-heads','2402.13055',None,'Findings of ACL',2024,0,0,0,[],'low_priority',[],
  '完整正式17页PDF及实验附录已核，semantic induction heads研究以实证为主，未见专门数学证明。'),
 ('acl2026-nonliteral',None,'Challenging the Explanation Based on Preceding Tokens: Discovering Transferable Non-Literal Biasing','ACL (short papers)',2026,0,0,0,[],'low_priority',[],
  '完整正式9页PDF已核，非字面token偏置及迁移以实验验证为主，无本地数学证明块。'),
]

def author_evidence(key):
 a=read(f'text/{key}.pages.json');ls=[]
 for p in a[:3]:
  for line in p['text'].splitlines():
   if re.search(r'Quanshi|QUANSHI|Jiao|SJTU|sjtu|zqs1022',line):
    if line.strip() not in ls:ls.append(line.strip())
 assert any('Quanshi' in l or 'QUANSHI' in l for l in ls),key
 assert any(re.search(r'Jiao|sjtu|SJTU',l) for l in ls),key
 return {'identity_status':'verified_formal_pdf','verification':'Formal public PDF author name, SJTU affiliation/email and group coauthors inspected',
  'pdf_pages_checked':[p['page'] for p in a[:3]],'pdf_identity_lines':ls[:20],
  'local_text':f'{REL}/text/{key}.pages.json','identity_sources':['https://jhc.sjtu.edu.cn/people/members/quanshi-zhang.html','http://qszhang.com/index.php/publications/']}

rows=[];inventory=[]
for key,aid,title,venue,year,nproof,nresult,nproved,spans,rec,units,reason in FORMAL:
 d=DOWNLOADS[key];assert d['download_status']=='ok',d
 old=BYID[aid] if aid else next(p for p in DISC if pathlib.Path(p['local_pdf']).stem==key)
 p=copy.deepcopy(old)
 p['discovery_screening_record']={k:old.get(k) for k in ['title','year','arxiv_id','source_url','version','local_pdf','sha256','recommendation','proof_count','numbered_result_count','proof_pages_or_span','research_content']}
 p.update(title=title or old['title'],year=year,publication_year=year,venue=venue,source_type='published',is_formal_version=True,
  formal_publication_verified=True,eligible_for_formal_candidate=rec in ['recommend','secondary'],formal_candidate_status='awaiting_user_confirmation' if rec in ['recommend','secondary'] else 'supplement_pending' if rec=='uncertain' else 'screened_low_proof_priority',
  source_url=d.get('source_url') or old['source_url'],pdf_url=d['pdf_url'],local_pdf=d['local_pdf'],sha256=d['sha256'],
  version=f'{venue} {year} official proceedings/journal PDF',total_pages=len(read(f'text/{key}.pages.json')),
  count_basis_version=f'{venue} {year} official PDF: {key}',
  proof_count=nproof,numbered_result_count=nresult,proved_numbered_result_count=nproved,proof_pages_or_span=spans,proof_page_count=len(spanpages(spans)),
  proof_count_kind='exact_manual_formal_pdf_proof_or_derivation_units',recommendation=rec,rationale=reason,
  authors_evidence=author_evidence(key),manual_evidence_file=f'{REL}/formal-proof-inventory.json',
  proof_evidence=units if units else [{'section':'Full acquired formal PDF inspected; no local proof block verified','pdf_pages':[]}],
  count_method='Manual inspection of this separately downloaded formal PDF, its numbering, proof/derivation block boundaries and physical PDF pages. Not copied from preprint counts.',
  proof_count_scope='selected formal PDF and formally linked supplement only; inaccessible supplements explicitly excluded',
  draft=False,review_complete=True,scope='formal_publication_only',candidate_confirmation='pending',formal_import_status='not_imported',source_versions=[])
 if not aid:
  p['arxiv_id']=None
 p['publication']={'venue':venue,'year':year,'source_url':p['source_url'],'verified':True}
 p['publication_evidence']={'source_url':p['source_url'],'pdf_url':d['pdf_url'],'title_author_venue_match':'verified landing/header plus separately acquired official PDF','local_landing':d.get('local_landing')}
 p['formal_pdf']={'local_pdf':d['local_pdf'],'sha256':d['sha256'],'pdf_url':d['pdf_url'],'total_pages':p['total_pages'],'status':'acquired_and_inspected'}
 p['formal_supplements']=[]
 p['materials']=[{'role':'formal_main_with_included_appendix','label':'正式PDF（含已随正文提供的附录）','local_pdf':d['local_pdf'],'pdf_url':d['pdf_url'],'sha256':d['sha256'],'total_pages':p['total_pages']}]
 p['supplement_status']='appendix inspected in formal PDF' if nproof else 'full acquired formal PDF inspected; no separate supplement relied on'
 p['first_public_year_basis']='formal publication year in candidate table; arXiv first-year retained only in discovery record'
 p.pop('pre_constraint_recommendation',None)
 p.pop('mathematical_issue_refs',None)
 if key=='iclr2024-sparse':
  p['version_notes']='Formal title differs from arXiv title. Main Theorem 3 is mislabeled Theorem 6 in B.4; distinct content counted once. B.7 Theorem 6 proof continues onto physical PDF p27.'
 if key=='iclr2024-generalizable':
  p['version_notes']='Official proceedings PDF has 23 pages; proof pages12–15 differ from acquired arXiv version. Counts independently rechecked on this formal PDF.'
 if key=='icml2025-coalition':
  p['version_notes']='First arXiv release2023; formal ICML2025 version24 pages. Counts refer only to this official final PDF; appendix shorthand omits main 3.x numbering prefix.'
 if key=='aaai2024-generalization':
  p['proof_count_kind']='exact_manual_formal_pdf_approximate_derivation_inventory'
  p['proof_unit_type']='approximate analytic reasoning, not a complete numbered proof'
 if key=='neurips2023-difficulty-main':
  p['proof_sketch_count']=1;p['proof_sketch_pages']=[21]
  s=DOWNLOADS['neurips2023-difficulty-supplement']
  p['formal_supplements']=[{**s,'total_pages':22,'byte_identical_to_main':True,'counted_separately':False,'note':'Official supplemental URL serves same SHA256 22-page file as main; no duplicate proof counts.'}]
 if key=='aaai2025-monitoring':
  p['proof_count_kind']='exact_manual_in_acquired_formal_main_only; formal_supplement_unverified'
  p['proof_evidence']=[{'section':'Theorem 2.1 at PDF p3 points to proof in Appendix E, which is absent from the acquired official nine-page PDF','pdf_pages':[],'statement_pdf_pages':[3]}]
  p['supplement_status']='formal_supplement_missing'
  p['supplement_gap']='Official nine-page PDF omits referenced Appendix E and other appendices; publisher landing provides PDF/video but no acquired formal supplement. Overall proof count unverified.'
  p['acquired_main_proof_count']=0
  p['whole_paper_proof_count']=None
  p['proof_count']=None
  p['materials'][0]['role']='formal_main'
  p['materials'][0]['label']='正式正文PDF'
 if key in ['aaai2024-generalization','fitee2025-first-principles']:
  p['materials'][0]['role']='formal_main'
  p['materials'][0]['label']='正式正文PDF'
 if p.get('numbered_result_ids') is None:p['numbered_result_ids']=[]
 if not aid and key=='neurips2023-difficulty-main':p['numbered_result_ids']=['Theorem 1','Theorem 2','Theorem 3','Theorem 4','Proposition 1']
 if not aid and key=='aaai2025-monitoring':p['numbered_result_ids']=['Theorem 2.1']
 for ev in p['proof_evidence']:ev['location']=ev['section']
 p['authors']=old['authors']
 inventory.append({'id':p['duplicategroup'],'formal_id':key,'title':p['title'],'count_basis_version':p['count_basis_version'],'manual':True,
    'proof_count':p['proof_count'],'acquired_main_proof_count':nproof,'numbered_result_count':nresult,'proved_numbered_result_count':nproved,'proof_pages_or_span':spans,
  'proof_evidence':p['proof_evidence'],'numbered_result_ids':p['numbered_result_ids'],'recommendation':rec,'rationale':reason,
  'not_locally_proved_note':old['proof_evidence'][0]['location'] if aid else None})
 rows.append(p)

for m in read('journal-publication-evidence.json'):
 if m['status']!='publisher-deposited metadata acquired':continue
 year=m['published']['date-parts'][0][0];doi=m['doi'];title=m['title'][0]
 authors=[f"{a.get('given','')} {a.get('family','')}".strip() for a in m['authors']]
 identity=[a for a in m['authors'] if a.get('family')=='Zhang' and a.get('given')=='Quanshi']
 assert identity and any('Jiao Tong' in a.get('name','') for a in identity[0]['affiliation'])
 related={'tpami2024-taylor':'2303.01506','tpami2026-attribution-survey':'2508.07636'}.get(m['id'])
 p={'title':title,'year':year,'publication_year':year,'venue':m['journal'][0],'authors':authors,
  'source_type':'published','formal_publication_verified':True,'is_formal_version':False,'eligible_for_formal_candidate':False,
  'source_url':'https://doi.org/'+doi,'pdf_url':None,'formal_pdf':None,'local_pdf':None,'sha256':None,'total_pages':None,
  'version':'formal publication metadata verified; official full text not acquired','count_basis_version':None,
  'numbered_result_count':None,'proved_numbered_result_count':None,'proof_count':None,'proof_count_kind':'unverified_formal_full_text_not_acquired',
  'proof_evidence':[],'proof_pages_or_span':[],'formal_supplements':[],'recommendation':'uncertain',
  'status':'formal_publication_verified_formal_pdf_pending','formal_candidate_status':'formal_pdf_pending',
  'rationale':'正式出版DOI、作者及SJTU身份已由IEEE存入Crossref的元数据核实；正式PDF接口未取得全文，证明数量未核实，不能替用arXiv计数。',
  'authors_evidence':{'identity_status':'verified_publisher_metadata; formal_pdf_not_acquired','publisher_metadata_author':identity[0],'metadata_source':m['source_url'],'local_metadata':m['local_metadata']},
  'publication_evidence':m,'publication':{'venue':m['journal'][0],'year':year,'doi':doi,'volume':m['volume'],'issue':m['issue'],'pages':m['page'],'source_url':m['source_url']},
  'duplicategroup':'doi:'+doi.lower(),'arxiv_id':related,'candidate_confirmation':'not_yet_eligible_full_text_pending','formal_import_status':'not_imported','review_as_of':'2026-09-30','draft':False,
  'topic':BYID[related]['topic'] if related else 'published group paper / formal full text pending',
  'research_content':BYID[related]['research_content'] if related else '仅核实公开题名和出版元数据；尚未读取正式全文，研究内容及理论证明待核。',
  'supplement_status':'not_acquired','manual_evidence_file':None}
 if related:p['preprint_discovery_key']='arxiv:'+related
 rows.append(p)

discovery=read('discovery.json')
formal_arxiv={p['arxiv_id']:p for p in rows if p.get('arxiv_id')}
for e in discovery['entries']:
 if e['review_owner']!='recent':continue
 p=formal_arxiv.get(e['arxiv_id'])
 e['eligible_for_formal_candidate']=bool(p and p['eligible_for_formal_candidate'])
 e['formal_version_key']=p['duplicategroup'] if p else None
 e['formal_status']=p['formal_candidate_status'] if p else 'formal_publication_not_verified; preprint_excluded_by_user_constraint'
 e['formal_screening_record']=f'{REL}/papers.json' if p else None
 e.pop('recommendation',None)
 e['preprint_role']='discovery/history only; never substituted for formal PDF'
discovery['latest_scope_constraint']='Only officially published conference/journal PDFs and formally linked supplementary materials can enter candidate table; unverified/preprint-only records excluded.'
discovery['formal_recent_papers_file']=f'{REL}/papers.json'
discovery['formal_publisher_metadata_pending_pdf']=[p['duplicategroup'] for p in rows if not p['is_formal_version']]
write('discovery.json',discovery)

errors=[];checks=[]
for p in rows:
 if not p['is_formal_version']:
  assert p['proof_count'] is None and not p['eligible_for_formal_candidate'];continue
 q=ROOT/p['local_pdf'];assert q.is_file(),q
 digest=hashlib.sha256(q.read_bytes()).hexdigest();assert digest==p['sha256'],q
 a=read(f'text/{q.stem}.pages.json');assert len(a)==p['total_pages']
 ps=spanpages(p['proof_pages_or_span']);assert len(ps)==p['proof_page_count']
 assert all(1<=i<=p['total_pages'] for i in ps)
 assert p['numbered_result_count']==len(p['numbered_result_ids']),(p['title'],p['numbered_result_ids'])
 assert p['proved_numbered_result_count']<=p['numbered_result_count']
 if p['proof_count']:
  assert sum(u.get('units',0) for u in p['proof_evidence'])==p['proof_count']
  assert set(i for u in p['proof_evidence'] for i in u['pdf_pages']).issubset(set(ps))
 checks.append({'formal_id':q.stem,'local_pdf':p['local_pdf'],'exists':True,'sha256_match':True,'pdf_page_count_match':True,'identity_verified':True,'manual_proof_evidence':True})
counts=collections.Counter(p['recommendation'] for p in rows if p['is_formal_version'])
validation={'as_of':'2026-09-30','frozen':True,'scope':'formal_publications_only',
 'formal_pdf_papers':len(checks),'formally_published_pdf_pending':sum(not p['is_formal_version'] for p in rows),
 'formal_recommendation_counts':dict(counts),'formal_candidate_papers':sum(p['eligible_for_formal_candidate'] for p in rows),
 'errors':errors,'checks':checks,'all_formal_proof_counts_manually_rechecked':True,'no_arxiv_count_substitution':True,
 'all_candidates_pending_user_confirmation':True,'corpus_import_performed':False}
write('papers.json',rows);write('formal-proof-inventory.json',inventory);write('validation.json',validation)
write('formal-candidates.json',[p for p in rows if p['eligible_for_formal_candidate']])
write('formal-pending.json',[p for p in rows if p['formal_candidate_status'] in ['supplement_pending','formal_pdf_pending']])
write('formal-screened-low-priority.json',[p for p in rows if p['formal_candidate_status']=='screened_low_proof_priority'])

def spantext(p):return ', '.join(str(a) if a==z else f'{a}–{z}' for a,z in p['proof_pages_or_span']) or '—'
evidence=['# 近期正式版证据（截至2026-09-30）','',
 '用户最新要求只取正式版。本部分14篇正式公开PDF已逐篇核对，另4篇正式期刊元数据已核实、正式全文未取得。arXiv初筛保存在历史台账，不能替用其计数。候选仍待用户确认，没有正式导入。','',
 '计数分别表示独立编号陈述、本地有专门证明的编号目标、证明/推导块及含证明的PDF物理页，不能相加。正文与附录同一陈述去重；一个多部分Proof块计一次，独立Proof块分别计。引用定理、方法公式、数据解题例和未展开草图不计完整证明。计数是文件内容人工清点，不等于数学正确性全面审稿。', '',
 '|正式题名/来源|发表年及venue|证明/推导单元|独立编号结果|本地编号证明|PDF证明页|编号/章节定位|','|---|---|---:|---:|---:|---|---|']
for p in rows:
 if not p['is_formal_version']:continue
 count=str(p['proof_count'])
 if 'approximate' in p['proof_count_kind']:count+='（近似推导）'
 if p.get('formal_candidate_status')=='supplement_pending':count+='（仅正文，附件未核实）'
 ev='; '.join(u['section'] for u in p['proof_evidence'])
 evidence.append(f"|[{p['title']}]({p['source_url']})|{p['year']} {p['venue']}|{count}|{p['numbered_result_count']}|{p['proved_numbered_result_count']}|{spantext(p)}|{ev}|")
evidence+=['','ICLR2024 Sparse：34页正式版，B.7证明延续到27页；正文Theorem3在B.4误标Theorem6，按内容去重后10个编号目标及11个证明块。Generalizable：正式版23页，C/D证明在12–15页，未沿用24页arXiv版页码。',
 'NeurIPS2023 Difficulty：main与supplement URL下载SHA256相同，22页含同一附录，仅计一次；G.1–3三个定理证明加G.4完整关系推导=4单元，G.5回归三步草图另记1，不计完整证明。',
 'AAAI2025 Monitoring：仅取得9页正式正文，Theorem2.1明确指向未取得AppendixE；整体证明量未核实。AAAI2024 Generalization的1单元是正文近似方差分析，与完整编号定理证明区分。',
 '四篇待取得期刊PDF：Taylor TPAMI2024、Attribution Survey TPAMI2026、Attribute Obfuscation TPAMI2025、Introspective Math Word Problems TASLP2024。IEEE存入Crossref的题名、发表信息、ORCID及SJTU作者身份已核；官方PDF接口HTTP418，证明数均null，未用预印本补位。','',
 '原95条arXiv作者查询仅用于发现分母，近期36个主PDF全部已查；有2份首三页未给个人作者身份，不冒充PDF身份核实。正式14篇PDF均实际核实张拳石及SJTU身份。所有原始发现PDF保留，预印本不进入正式候选主表。数学疑点仅保留在原预印本调研记录，未影响正式候选建议。','']
(BASE/'evidence.md').write_text('\n'.join(evidence))
findings=['# 近期正式版候选筛查结果','',
 f"截至2026-09-30，已实查14篇正式版：优先建议{counts['recommend']}篇、次级参考{counts['secondary']}篇、正式附件待取得{counts['uncertain']}篇、证明较少{counts['low_priority']}篇。另有4篇正式期刊全文待取得，证明数量未核。只有取得并核对正式PDF的recommend/secondary共10篇进入待用户确认表。",'',
 '|题名|正式版|证明/推导单元|独立编号结果|PDF页|建议理由|','|---|---|---:|---:|---|---|']
for p in rows:
 if p['is_formal_version'] and p['recommendation']=='recommend':
  findings.append(f"|[{p['title']}]({p['source_url']})|{p['venue']} {p['year']}|{p['proof_count']}|{p['numbered_result_count']}|{spantext(p)}|{p['rationale']}|")
findings+=['','完整逐篇原文定位、研究内容、固定来源PDF/sha256及计数依据在papers.json与formal-proof-inventory.json，验证结果在validation.json。综述、基础技术说明及单个近似推导均明确区分；不是所有推荐项都称证明密集。',
 '未确证正式发表的预印本（包括2026最新符号pattern、百万Agent、水印、区域primitive等）只保留discovery；用户“只取正式版”要求优先于此前预印本推荐。未在网上取得附件不等于论文没有证明，未宣称检索绝无遗漏。','']
(BASE/'findings.md').write_text('\n'.join(findings))
for n in ['discovery-screening-evidence.md','discovery-screening-findings.md']:
 p=BASE/n
 text=p.read_text()
 text='> 历史调研：以下分类先于用户“只取正式版”约束；不作为当前收录建议。以papers.json及findings.md正式版结果为准。\n\n'+text
 text=text.replace('40篇公开PDF均核对了题名、作者及SJTU身份。','40篇公开PDF均实查；38篇首三页核对了张拳石及SJTU身份，2篇首三页个人作者身份未核。')
 text=text.replace('36篇近期arXiv主PDF全部取得、完整转换并核对身份；4篇venue-only同样核对公开PDF。没有待确认同名身份的40项已查记录；','36篇近期arXiv主PDF全部取得、完整转换；其中2份首三页缺个人作者身份，仅保留查询元数据。4篇venue-only核对公开PDF身份。')
 p.write_text(text)
print(json.dumps({k:v for k,v in validation.items() if k!='checks'},ensure_ascii=False,indent=2))
