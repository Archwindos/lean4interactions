#!/usr/bin/env python3
"""Merge frozen survey evidence into a formal-publication-only review table."""
import collections, copy, csv, hashlib, json, pathlib, re, subprocess
ROOT=pathlib.Path('/mnt/data2/wyh/lean4project')
BASE=ROOT/'research/paper-survey-20260930'
REL=BASE.relative_to(ROOT).as_posix()
def read(path):return json.loads((ROOT/path).read_text())
def write(path,obj):(ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def key(p):return p.get('duplicate_group') or p.get('duplicategroup') or 'title:'+p['title'].casefold()
def norm(s):return s.casefold() if s.startswith('doi:') else s

FILES=[f'{REL}/earlier/papers.json',f'{REL}/recent/screened-discovery-papers.json',
 f'{REL}/earlier/formal-candidates.json',f'{REL}/earlier/formal-pending.json',f'{REL}/recent/papers.json',
 f'{REL}/recent/formal-candidates.json',f'{REL}/recent/formal-pending.json']
INPUTS={f:read(f) for f in FILES}
CANDIDATES=[(f,p) for f in [f'{REL}/earlier/formal-candidates.json',f'{REL}/recent/formal-candidates.json'] for p in read(f)]
PENDING=[(f,p) for f in [f'{REL}/earlier/formal-pending.json',f'{REL}/recent/formal-pending.json'] for p in read(f)]
parent={}
def find(k):
 k=norm(k);parent.setdefault(k,k)
 if parent[k]!=k:parent[k]=find(parent[k])
 return parent[k]
def union(a,b):
 a,b=find(a),find(b)
 if a!=b:parent[b]=a

for f,rows in INPUTS.items():
 for p in rows:
  find(key(p))
  # These aliases were explicitly matched by official author-publication/DOI evidence.
  if p.get('preprint_discovery_key'):union(key(p),p['preprint_discovery_key'])
groups=collections.defaultdict(list)
for f,rows in INPUTS.items():
 for i,p in enumerate(rows):groups[find(key(p))].append({'source_file':f,'row_index':i,'record':p})
cand={find(key(p)):(f,p) for f,p in CANDIDATES}
pend={find(key(p)):(f,p) for f,p in PENDING}
assert len(cand)==len(CANDIDATES),'Duplicate formal candidate requires explicit merge review'
assert not (set(cand)&set(pend)),'Candidate/pending conflict'

CONTENT={
 'arxiv:2210.09020':'用DFT和圆周卷积分析卷积decoder的前向/反向传播，解释高频表示、零填充和频谱学习的缺陷。',
 'arxiv:2205.01940':'以信息论量化ReLU网络变换复杂度，证明复杂度与解缠关系，研究训练动态及复杂度控制。',
 'arxiv:2111.06206':'把DNN推理拆为稀疏交互概念并组织成因果图/And-Or图，证明任意mask输入的输出可重构。',
 'arxiv:2103.07364':'用多阶交互统一解释对抗攻击与防御，分析高阶交互扰动、低阶稳健特征及形状偏置。',
 'arxiv:2010.05045':'定义多变量Shapley交互和coalition的重要性，量化DNN记忆的原型特征及组内变量协同。',
 'arxiv:2007.04298':'用Shapley交互构建句子的可解释树，提出六种交互指标，并比较BERT、ELMo、LSTM等模型。',
 'arxiv:1906.04109':'量化逐层/逐像素信息丢弃，统一比较不同层和模型对输入信息的保留与删除。',
}

def materials(p):
 ms=copy.deepcopy(p.get('materials') or [])
 if not ms and p.get('formal_pdf') and p.get('local_pdf'):
  ms=[{**p['formal_pdf'],'role':'formal_main'}]
 if not ms and p.get('is_formal_version') and p.get('local_pdf') and p.get('sha256') and p.get('total_pages'):
  ms=[{'role':'formal_main','local_pdf':p['local_pdf'],'sha256':p['sha256'],'pdf_url':p['pdf_url'],'total_pages':p['total_pages']}]
 return ms

def formal_proof_locations(p):
 out=[];raw=p.get('proof_pages_or_span') or []
 if isinstance(raw,dict):raw=[raw]
 for s in raw:
  if isinstance(s,dict):
   role=s.get('file','formal_main');ps=s.get('pages') or s.get('span') or []
   section=s.get('section','')
  else:role='formal_main';ps=s;section=''
  if len(ps)!=2:raise ValueError((p['title'],s))
  out.append({'role':role,'start':ps[0],'end':ps[1],'section':section})
 return out

def venue(p):
 v=p.get('venue') or p.get('publication',{}).get('venue')
 if not v:v={'official:iccv2015':'ICCV 2015','official:guan19a':'ICML 2019'}.get(key(p),'正式出版记录待核')
 return v

combined=[]
for gid,sources in groups.items():
 tier='discovery_only'
 if gid in cand:f,p=cand[gid];tier='candidate'
 elif gid in pend:f,p=pend[gid];tier='pending_formal_material'
 else:
  formal=[s for s in sources if s['record'].get('is_formal_version')]
  selected=formal[-1] if formal else sources[-1]
  f,p=selected['source_file'],selected['record']
  if p.get('is_formal_version') and p.get('review_complete') and p.get('recommendation')=='low_priority':tier='formal_screened_low_priority'
 c=copy.deepcopy(p)
 c['canonical_key']=key(p);c['duplicate_group']=key(p)
 c['aliases']=sorted({key(s['record']) for s in sources})
 c['original_records']=sources
 c['selected_source_file']=f;c['selection_tier']=tier
 c['requires_user_confirmation']=tier=='candidate';c['formal_import_status']='not_imported'
 if tier in ['candidate','pending_formal_material','formal_screened_low_priority']:
  c['source_type']='published';c['publication_year']=p['year'];c['venue']=venue(p)
  c['formal_materials']=materials(p);c['formal_proof_locations']=formal_proof_locations(p)
  c['formal_pdf']=next((m for m in c['formal_materials'] if 'supplement' not in m.get('role','')),None)
  c['materials_total_pages']=sum(m['total_pages'] for m in c['formal_materials']) if c['formal_materials'] else None
  if c['formal_pdf']:c['total_pages']=c['formal_pdf']['total_pages']
  c['count_basis_version']=p.get('count_basis_version') or p['version']
  c['publication_evidence']=p.get('publication_evidence') or {'source_url':p['source_url'],'local_landing':p.get('formal_landing_snapshot'),'verification':p.get('formal_status')}
  if key(p) in CONTENT:c['research_content']=CONTENT[key(p)]
  if tier=='candidate':
   assert p.get('is_formal_version') and p.get('recommendation') in ['recommend','secondary']
   assert c['formal_materials'] and p['proof_count'] is not None
   assert p.get('proof_evidence') and re.search('manual|exact',p['proof_count_kind'])
  if tier=='pending_formal_material':
   c['whole_paper_proof_count']=None
   c['proof_count']=None
 else:
  c['source_type']='published_source_initial_screen_only' if p.get('is_formal_version') else 'preprint_or_unverified_author_copy_discovery'
  c['eligible_for_formal_candidate']=False
  c['historical_proof_count']=p.get('proof_count')
  c['historical_proof_count_kind']=p.get('proof_count_kind')
  c['proof_count']=None;c['proof_count_kind']='not_eligible_under_published_version_only_constraint'
  c['recommendation']='excluded_from_formal_candidates'
  c['formal_proof_locations']=[];c['formal_materials']=[]
 combined.append(c)

def sortcandidate(p):return (p['recommendation']!='recommend',-(p.get('proof_count') or 0),p['publication_year'],p['title'])
candidates=sorted([p for p in combined if p['selection_tier']=='candidate'],key=sortcandidate)
pending=sorted([p for p in combined if p['selection_tier']=='pending_formal_material'],key=lambda p:(-p['publication_year'],p['title']))
oldsummary=read(f'{REL}/summary.json') if (BASE/'summary.json').exists() else {}
idmap=oldsummary.get('stable_id_map',{})
def assign(rows,prefix):
 used=[int(x[len(prefix):]) for x in idmap.values() if x.startswith(prefix) and x[len(prefix):].isdigit()]
 n=max(used,default=0)
 for p in rows:
  k=p['canonical_key']
  if k not in idmap:n+=1;idmap[k]=f'{prefix}{n:02d}'
  p['candidate_id']=idmap[k]
assign(candidates,'F');assign(pending,'W')

def counttext(p):
 n=p.get('proof_count')
 if n is None:return '未核实'
 if 'lower_bound' in p['proof_count_kind']:return f'≥{n}'
 if 'approximate' in p['proof_count_kind']:return f'{n}（近似推导）'
 return str(n)
def locationtext(p):
 out=[]
 for s in p['formal_proof_locations']:
  label='补充PDF' if 'supplement' in s['role'] else 'PDF'
  nums=str(s['start']) if s['start']==s['end'] else f"{s['start']}–{s['end']}"
  out.append(label+nums)
 return '；'.join(out) or '—'
def materialtext(p):
 ms=p['formal_materials']
 if not ms:return '未取得'
 if len(ms)==1 and p['selection_tier']=='pending_formal_material':return f"正文{ms[0]['total_pages']}页；补充待取得/核实"
 if len(ms)==1:return f"{ms[0]['total_pages']}页"
 return '＋'.join(('补充' if 'supplement' in m.get('role','') else '正文')+str(m['total_pages']) for m in ms)+'页'
def escape(s):return str(s).replace('|','/').replace('\n',' ')
def citation(p):
 v=p['venue'];y=p['publication_year']
 if str(y) not in v:v=f'{v} {y}'
 return f"[{p['title']}]({p['source_url']})<br>{v}"

errors=[];warnings=[];checked={}
for p in combined:
 if p['selection_tier'] not in ['candidate','pending_formal_material','formal_screened_low_priority']:continue
 roles={m.get('role','formal_main'):m for m in p['formal_materials']}
 for m in p['formal_materials']:
  f=m['local_pdf'];q=ROOT/f
  if pathlib.Path(f).is_absolute() or not q.is_relative_to(ROOT):errors.append('nonrelative/outside PDF: '+f);continue
  if not q.is_file():errors.append('missing formal PDF: '+f);continue
  digest=hashlib.sha256(q.read_bytes()).hexdigest()
  if digest!=m['sha256']:errors.append('hash mismatch: '+f)
  info=subprocess.run(['pdfinfo',str(q)],capture_output=True,text=True,check=True).stdout
  n=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
  if n!=m['total_pages']:errors.append('material page mismatch: '+f)
  checked[f]={'local_pdf':f,'exists':True,'sha256':digest,'sha256_match':digest==m['sha256'],'actual_pages':n,'metadata_pages':m['total_pages']}
  if 'arxiv.org' in m.get('pdf_url',''):errors.append('arXiv substituted as formal material: '+f)
 for s in p['formal_proof_locations']:
  m=roles.get(s['role'])
  if m is None and s['role']=='formal_main':m=next((m for m in p['formal_materials'] if 'supplement' not in m.get('role','')),None)
  if m is None:errors.append('proof location material role missing: '+p['title']);continue
  if not 1<=s['start']<=s['end']<=m['total_pages']:errors.append('proof page outside formal material: '+p['title'])
 if p['selection_tier']=='candidate':
  if p['proof_count']>0 and not p['formal_proof_locations']:errors.append('candidate positive count without formal pages: '+p['title'])
  if not re.search('manual|exact',p['proof_count_kind']):errors.append('candidate has automatic count: '+p['title'])
  if not p.get('research_content'):errors.append('candidate lacks research content: '+p['title'])
  if p.get('numbered_result_count') is not None and p.get('proved_numbered_result_count') is not None and p['proved_numbered_result_count']>p['numbered_result_count']:errors.append('proved numbered count exceeds statements: '+p['title'])
assert not errors,errors

arxiv=read(f'{REL}/recent/discovery.json')['entries']
earlier_arxiv=read(f'{REL}/earlier/papers.arxiv-discovery.json')
recent_discovery=read(f'{REL}/recent/screened-discovery-papers.json')
arc_pdfs=[p for p in earlier_arxiv+recent_discovery if p.get('local_pdf') and key(p).startswith('arxiv:')]
excluded_arxiv=collections.Counter(p.get('status','') for p in earlier_arxiv if not p.get('local_pdf'))
individual=[p for p in combined if p.get('status') not in ['withdrawn_by_authors','edited_proceedings_html_not_individual_paper']]
summary={'as_of':'2026-09-30','scope':'officially published conference/journal versions and formal supplements only',
 'formal_candidates':len(candidates),'recommended':sum(p['recommendation']=='recommend' for p in candidates),
 'secondary':sum(p['recommendation']=='secondary' for p in candidates),'formal_material_pending':len(pending),
 'candidate_formal_pdf_materials':sum(len(p['formal_materials']) for p in candidates),
 'candidate_independent_papers':len(candidates),
 'formal_papers_with_acquired_main_pdf':sum(bool(p.get('formal_pdf')) for p in combined if p['source_type']=='published'),
 'formal_material_count_scope':'本轮正式版核查集合：冻结候选/材料缺口及近期人工实查的低证明项；另2篇仅自动初筛的官方全文保留发现层，不在核查计数内',
 'formal_pdf_materials_verified':len(checked),'distinct_formal_pdf_sha256_verified':len({m['sha256'] for m in checked.values()}),
 'full_ledger_work_groups':len(combined),'full_ledger_individual_work_groups':len(individual),
 'raw_source_record_snapshots':sum(len(x) for x in INPUTS.values()),
 'arxiv_discovery_records':len(arxiv),'arxiv_public_pdf_records_acquired':len(arc_pdfs),
 'arxiv_nonpdf_record_statuses':dict(excluded_arxiv),
 'not_a_claim_of_complete_internet_coverage':True,'all_candidates_pending_user_confirmation':True,'corpus_import_performed':False,
 'stable_id_map':idmap,'input_files':{f:{'rows':len(x),'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest()} for f,x in INPUTS.items()}}
validation={'as_of':'2026-09-30','frozen':True,'errors':errors,'warnings':warnings,
 'formal_candidate_papers_checked':len(candidates),'formal_candidate_source_type_published':all(p['source_type']=='published' for p in candidates),
 'formal_candidate_versions_verified':all(p.get('is_formal_version') for p in candidates),
 'no_preprint_count_substitution':True,'formal_candidates_manual_counts_only':True,
 'physical_materials_not_aggregate_page_counts':True,'formal_pdf_checks':list(checked.values()),
 'input_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in FILES}}
write(f'{REL}/combined-papers.json',combined);write(f'{REL}/summary.json',summary);write(f'{REL}/validation.json',validation)

with (BASE/'candidate-selection.csv').open('w',newline='') as stream:
 fields=['candidate_id','selection_tier','recommendation','title','publication_year','venue','research_content','proof_units','proof_count','proof_count_kind','numbered_result_count','proof_locations','formal_material_pages','source_url','pdf_url','rationale','user_confirmation','canonical_key']
 writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
 for p in candidates+pending:
  writer.writerow({f:p.get(f,'') for f in fields}|{'proof_units':counttext(p),'proof_locations':locationtext(p),
   'formal_material_pages':materialtext(p),'user_confirmation':'待确认' if p['selection_tier']=='candidate' else '待取得正式材料后再确认'})

doc=['# 张拳石公开论文：正式版候选确认表','',
 f"截至2026-09-30，按‘只取正式版’筛选，{len(candidates)}项具备正式材料并完成证明密度筛查：{summary['recommended']}项优先建议、{summary['secondary']}项次级或导读参考。另{len(pending)}项有正式出版记录，但正式全文、补充材料或其最终版身份仍有缺口，单列待取得。本轮未将新候选正式导入或展开逐篇重写/Lean形式化，已有试点成果另计。",'',
 '证明/推导单元按实际Proof块或独立证明小节计；编号结果是独立Theorem/Lemma/Proposition/Corollary陈述，包括注明引用的旧结果，两列不能相加。≥表示有具体页码支持的人工下界。页码均为各正式PDF的物理页；‘补充PDF’从补充文件第一页起算。Generalizable的2个单元按基础重要推荐，FITEE的0个单元按导读参考登记，Generalization的1个单元是近似推导，不能把所有候选统称证明密集论文。','',
 '## 优先建议（全部列出）','',
 '|稳定ID|正式论文及发表版|研究内容|证明/推导单元|独立编号结果|证明位置|正式材料页数|建议依据|用户确认|',
 '|---|---|---|---:|---:|---|---|---|---|']
def tablerow(p):
 return f"|{p['candidate_id']}|{citation(p)}|{escape(p['research_content'])}|{counttext(p)}|{p['numbered_result_count']}|{locationtext(p)}|{materialtext(p)}|{escape(p['rationale'])}|待确认|"
doc.extend(tablerow(p) for p in candidates if p['recommendation']=='recommend')
doc+=['','## 次级候选与导读参考','',
 '|稳定ID|正式论文及发表版|研究内容|证明/推导单元|独立编号结果|证明位置|正式材料页数|建议依据|用户确认|',
 '|---|---|---|---:|---:|---|---|---|---|']
doc.extend(tablerow(p) for p in candidates if p['recommendation']=='secondary')
doc+=['','## 正式材料待取得或待核实','',
 '下表整体证明数量均未核实，不以预印本或正文编号陈述数量代替。正文已取得的文件保留以便对齐，缺少的证明附件仍待取得。','',
 '|稳定ID|正式论文及发表版|已取得正式材料|证明数量|缺口与处理依据|',
 '|---|---|---|---|---|']
for p in pending:doc.append(f"|{p['candidate_id']}|{citation(p)}|{materialtext(p)}|未核实|{escape(p['rationale'])}|")
doc+=['','## 计数与检索边界','',
 'CVPR2023 Sparse的‘正文10＋补充27页’和NeurIPS2021 Robustness的‘正文14＋补充16页’是两个文件的材料规模，不能当作正文PDF本身的页数。NeurIPS2023 Difficulty主文/补充两个URL下载为同一SHA256文件，不重复计篇数或证明数。',
 'ICLR2024 Sparse按正式题名及34页文件登记，证明延续到PDF27；正文Theorem3在B.4误标Theorem6，按陈述内容去重。Generalizable按正式23页文件，证明在12–15页；Coalition按ICML2025正式24页版本。',
 '单元定位来源于逐篇正式版核查；本轮只核证明密度、版本和位置，没有完成每个证明的数学审校。下界计数及待取得材料会在用户确认范围后的逐篇流程细化。',
 '上述数量按每篇论文分别统计，尚未对跨论文共享的重构、Shapley等证明做命题对齐和去重，不能把各行相加当作公共Lean库的独立定理数。',
 f"本轮正式版核查集合含{summary['formal_papers_with_acquired_main_pdf']}篇已取得正文的论文、{summary['formal_pdf_materials_verified']}个不同正式PDF文件；其中待确认候选为17篇/19文件。另2项官方全文仅完成自动初筛，保留发现层，未据此称证明较少。", 
 f"检索记录另外保留95项arXiv作者索引及{summary['arxiv_public_pdf_records_acquired']}项取得的公开PDF记录，其余为撤回/重复撤回记录与两项HTML文集；它们仅用于发现，不进入正式候选。官方作者publicationlist、实验室主页及官方venue用于补漏；作者主页部分年份未更新，不能据此宣称网上绝无遗漏。",'',
 f"完整发现与排除台账见[full-ledger.md](../{REL}/full-ledger.md)，机器可读原始字段及选定正式版见[combined-papers.json](../{REL}/combined-papers.json)，审核选择可用[candidate-selection.csv](../{REL}/candidate-selection.csv)。所有正式文件的路径、SHA256、逐文件页数及证明页段已检查，验证错误为0。",'']
(ROOT/'docs/paper-candidates-20260930.md').write_text('\n'.join(doc))

ledger=['# 完整发现与筛选台账','',
 '本表按显式合并键去重，正式版与预印本证据保留在combined-papers.json的original_records。相近题名及期刊扩展不会自行并成同一证明；arXiv预印本和作者未核最终版的PDF不进入待确认正式主表。',
 f"共{len(combined)}个调研合并组，其中{len(individual)}个非撤回/非文集的独立作品组；这些数量不是正式候选篇数，也不是下载PDF或证明数量。17项正式候选与15项材料缺口由冻结的正式专用数组选择。",'',
 '|合并键/稳定ID|题名与选定来源|记录年份|角色|正式证明/推导数|处置依据|','|---|---|---:|---|---|---|']
for p in sorted(combined,key=lambda p:(-(p.get('year') or 0),p['title'])):
 label={'candidate':'正式待确认','pending_formal_material':'正式材料待取得/核实','formal_screened_low_priority':'正式全文已核，证明较少','discovery_only':'发现记录，排除正式主表'}[p['selection_tier']]
 count=counttext(p) if p['selection_tier']!='discovery_only' else '不采用历史预印本计数'
 reason=p.get('rationale') or p.get('status') or '未完成正式版身份核查'
 ledger.append(f"|{escape(p['canonical_key'])}{' / '+p['candidate_id'] if p.get('candidate_id') else ''}|[{escape(p['title'])}]({p['source_url']})|{p.get('year','')}|{label}|{count}|{escape(reason)}|")
ledger+=['','检索日期、作者身份边界、全部95项arXiv记录及额外正式来源见earlier/recent发现文件；本表不能证明作者全部论文均已穷尽。',
 '源数据文件SHA256以及实际PDF存在、哈希、页数和证明页范围检查在validation.json。对正式主表的全部计数使用人工定位口径；自动关键词命中只留原始发现字段。','']
(BASE/'full-ledger.md').write_text('\n'.join(ledger))
print(json.dumps({k:v for k,v in summary.items() if k not in ['stable_id_map','input_files']},ensure_ascii=False,indent=2))
for p in candidates:
 print(p['candidate_id'],p['title'],'|',p['version'],'|',counttext(p),'|',locationtext(p),flush=True)
