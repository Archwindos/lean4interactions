#!/usr/bin/env python3
"""Freeze the recent public-paper evidence inventory; no corpus import."""
import collections
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path('/mnt/data2/wyh/lean4project')
BASE = ROOT / 'research/paper-survey-20260930/recent'
REL = BASE.relative_to(ROOT).as_posix()

def read(name):
    return json.loads((BASE / name).read_text())

def write(name, obj):
    (BASE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

CONTENT = {
 '2609.06483': ('parameter pruning / AND-OR interactions', '研究参数剪枝怎样改变DNN的交互表示、交互阶数和泛化特征；比较剪枝策略及不同模型，附录给出AND/OR输出重构。'),
 '2608.06839': ('symbolic patterns / emergence / monotonicity / smoothness', '总结符号pattern涌现、稀疏交互及网络推理的数学条件与实验现象；正文讨论单调性、平滑性和交互阶数上界，详细理论推导指向未取得的Supplementary Note 1。'),
 '2606.08129': ('cross-LLM consistency / shared interactions', '以共享AND/OR交互衡量不同LLM的推理一致性；附录用Möbius变换重构逻辑模型，主体比较共享和模型独有的交互。'),
 '2605.29801': ('agent safety / scalable guardrail / data purification', '提出轻量Agent安全防护框架AgentDoG1.5、分类引导的数据引擎和基于影响函数的数据净化，报告模型与基准评测。'),
 '2605.17967': ('LLM supervised fine-tuning / interactions', '用交互表示区分SFT的效果，解释看似矛盾的SFT有效性结论；本地理论主要是AND/OR/组合输出精确重构。'),
 '2605.17770': ('reasoning models / entropy / gradients', '分析大推理模型内部熵与梯度之间的关系及entropy-gradient inversion现象；附录给出softmax、Cauchy–Schwarz和logit梯度推导。'),
 '2605.13148': ('generalization / decision-pattern shift', '用训练与测试之间的决策pattern变化理解泛化；正文在其固定其他logit的分析设定下给出交叉熵及Taylor近似关系。'),
 '2605.11410': ('EEG foundation models / representation audit', '审计EEG基础模型对脑信号信息的捕获，设计EEG词典、特征解释与因果消融及跨任务评测。'),
 '2605.11404': ('million-agent emergence / Aumann-Shapley attribution', '研究百万Agent系统涌现的可扩展归因；分析精确离散归因的困难，提出连续Aumann–Shapley方法并验证归因公理。'),
 '2604.06628': ('reasoning SFT / conditional generalization experiments', '系统研究推理SFT泛化与优化、数据及模型能力的条件关系，包含大量实验、任务实例和完整结果表。'),
 '2601.18491': ('agent safety / diagnostic guardrails', '提出AgentDoG诊断式安全防护、细粒度风险分类和数据集/基准，通过诊断案例与实验评估Agent风险。'),
 '2512.18607': ('interaction bottleneck / discovery / modulation', '扩展交互瓶颈研究，分析神经网络不同阶数交互的表示偏好及调制方法；正文含定理与推论，证明指定在未取得的补充材料。'),
 '2510.13080': ('diffusion models / hallucination counting', '研究扩散生成中的幻觉数量估计与评价，给出计数方法和实验；正文中的proof词命中来自参考文献标题。'),
 '2508.07636': ('attribution theory / survey / method unification', '从理论角度综述深度网络归因解释、方法统一、解释合理性与理论评价，作为已有理论工作的导读与索引。'),
 '2505.06993': ('generalization metrics / technical report', '技术报告讨论DNN泛化能力的量化与分析，引用交互精确重构；五页公开PDF未包含文中提及的附录C。'),
 '2505.01007': ('watermark robustness / fine-tuning / Fourier analysis', '在频域分析神经网络水印抗微调能力，研究DFT结构、缩放/置换及相关抵抗条件；附录包含多个独立数学证明。'),
 '2502.10162': ('generalization / symbolic interaction dynamics', '用符号交互重访DNN泛化能力，连接交互学习动态、噪声与泛化；主要本地证明是精确重构，另有从前作导入的理论解。'),
 '2502.08625': ('parameter randomness / confusing samples / interaction representations', '研究低层参数随机性对混淆样本和交互表示的影响；附录证明AND/OR交互的精确重构，其余以提取和实验为主。'),
 '2410.04421': ('image generation / regional primitives / OR interactions', '把图像生成的区域primitive分解为OR逻辑特征分量，研究分量等价表示、可加性及输出重构。'),
 '2410.09083': ('LLM judgment / inference-pattern correctness', '用交互逻辑模型评价LLM作出判断时的推理模式正确性，结合判断任务实验与精确重构/稀疏模型推论。'),
 '2409.08712': ('layerwise knowledge / feature interactions', '把知识定义和交互提取扩展到神经网络中间层，追踪逐层知识的保留、增加与丢失，含两个编号理论目标。'),
 '2407.19198': ('symbolic interaction learning / two-phase dynamics / noise', '解释DNN学习符号交互的两阶段动态，分析参数噪声、Taylor触发函数、交互阶数与最优回归权重。'),
 '2405.11880': ('LLM in-context reasoning / memorization decomposition', '将LLM的上下文推理效果和记忆效果拆解为AND/OR交互，给出分解的精确重构并比较不同效果。'),
 '2405.10262': ('overfitting onset / two-phase interaction dynamics', '用交互的两阶段动态解释DNN开始学习过拟合特征的时点，推导随机交互的纺锤形分布和组件交互支持。'),
 '2402.13055': ('in-context learning / semantic induction heads', '定义关系指标并通过阈值、格式、pattern与token分类实验识别语义induction heads，解释上下文学习。'),
 '2401.16318': ('generalizable primitives / AND-OR interactions / universal matching', '定义并提取可泛化的AND/OR交互primitive，分析任意mask输入的精确重构和交互方差，验证primitive跨模型或输入的泛化。'),
 '2310.09838': ('Go game / interaction explanation / noise variance', '用AND/OR交互解释围棋网络的决策并支持人类学习，包含交互关系、输出重构、噪声方差及饱和性分析。'),
 '2309.13411': ('coalition attribution / AND-OR reallocation / Shapley axioms', '指出将单变量归因直接相加可能与coalition归因冲突，构建coalition的AND/OR分配并证明相关定理和归因公理。'),
 '2305.01939': ('sparse symbolic concepts / combinatorial proof / interaction bounds', '在明确网络条件下研究稀疏符号交互的涌现，构造组合矩阵关系、阶数/数量上界，并连接多种Shapley指标。'),
 '2304.13312': ('AND-OR definitions / extraction / technical note', '基础技术说明定义AND/OR交互及其提取优化，陈述与Shapley类指标的关系，但八页公开PDF没有专门证明块。'),
 '2304.01811': ('HarsanyiNet / exact Shapley values / neural architecture', '设计HarsanyiNet使一次前向传播精确计算Shapley值，证明网络交互结构与归因关系，并推广到CNN构造。'),
 '2304.01083': ('LLM logic / symbolic concepts / empirical explanation', '探索LLM推理逻辑是否可分解为符号概念，以交互提取和实证解释为主，引用精确重构定理。'),
 '2303.01506': ('Taylor interactions / attribution unification', '用Taylor交互统一14种归因方法，分别建立各方法与交互项的对应关系，包含16个独立编号理论目标及证明。'),
 '2302.13095': ('Bayesian neural networks / uncertainty / interaction complexity', '研究BNN为何避免复杂且扰动敏感的概念，连接交互阶数、Taylor展开、随机变量矩及回归权重。'),
 '2302.13091': ('generalization / interactive concepts / approximate variance analysis', '用交互概念解释DNN泛化，给出Taylor和扰动矩公式及近似方差增长分析，并开展实证验证；公开正文没有专门完整证明附录。'),
 '2302.13080': ('symbolic concepts / sparsity / transferability / empirical validation', '从稀疏性、跨输入或模型可迁移性、判别能力及语义意义四方面实证检验DNN是否编码符号概念。'),
}

NUMBERED = {
 '2303.01506': ['Proposition 1'] + [f'Theorem {i}' for i in range(1,16)],
 '2305.01939': [f'Theorem {i}' for i in range(1,7)] + [f'Lemma {i}' for i in range(1,5)],
 '2309.13411': ['Theorem 3.2','Theorem 3.3','Theorem 3.4','Theorem 3.6','Corollary 3.5','Corollary 3.7','Corollary 3.8'],
 '2304.01811': ['Theorem 1','Theorem 2','Theorem 3','Theorem 4','Lemma 1'],
 '2302.13095': ['Lemma 2.1'] + [f'Theorem 2.{i}' for i in range(2,7)] + ['Proposition G.1'],
 '2407.19198': [f'Theorem {i}' for i in range(1,6)] + ['Lemma 1','Lemma 2','Lemma 3','Proposition 1'],
 '2401.16318': ['Theorem 1','Theorem 2','Theorem 3','Proposition 1'],
 '2405.11880': ['Theorem 1','Theorem 2','Lemma 1'],
 '2409.08712': ['Theorem 3.3','Lemma 3.4'],
 '2410.04421': ['Theorem 1-α','Theorem 1-β','Theorem 2'],
 '2410.09083': ['Theorem 1'],
 '2310.09838': ['Theorem 1','Theorem 2','Theorem 3','Corollary 4'],
 '2505.01007': ['Theorem 3.1','Theorem 3.2','Theorem 3.5','Theorem 3.6','Corollary 3.3','Proposition 3.4','Lemma A.1'],
 '2605.11404': ['Theorem 1','Lemma 1','Proposition 1'],
 '2502.10162': ['Theorem 2.1','Theorem 2.3'],
 '2502.08625': ['Theorem 2.1'],
 '2405.10262': ['Theorem 1','Theorem 2','Theorem 3'],
 '2304.13312': ['Theorem 1','Theorem 2','Theorem 3'],
 '2304.01083': ['Theorem 1'],
 '2505.06993': ['Theorem 1'],
 '2512.18607': ['Theorem 1','Theorem 2','Corollary 1'],
 '2302.13091': ['Theorem 1','Lemma 1','Theorem 2'],
}

OFFICIAL_VENUES = {
 '2305.01939': ('ICLR',2024,'http://qszhang.com/index.php/publications/'),
 '2401.16318': ('ICLR',2024,'http://qszhang.com/index.php/publications/'),
 '2302.13091': ('AAAI',2024,'http://qszhang.com/index.php/publications/'),
 '2302.13095': ('ICML',2023,'http://qszhang.com/index.php/publications/'),
 '2303.01506': ('IEEE TPAMI',2024,'http://qszhang.com/index.php/publications/'),
 '2304.01811': ('ICML',2023,'https://proceedings.mlr.press/v202/chen23s.html'),
 '2302.13080': ('ICML',2023,'https://proceedings.mlr.press/v202/li23at.html'),
 '2309.13411': ('ICML',2025,'https://proceedings.mlr.press/v267/zheng25d.html'),
 '2407.19198': ('NeurIPS',2024,'https://arxiv.org/abs/2407.19198v2'),
 '2409.08712': ('ICML',2024,'https://arxiv.org/abs/2409.08712v1'),
 '2402.13055': ('ACL',2024,'https://arxiv.org/abs/2402.13055v2'),
 '2604.06628': ('COLM',2026,'https://arxiv.org/abs/2604.06628v2'),
}

def pages_for(spans):
    return sorted({i for a,z in spans for i in range(a,z+1)})

def identity(version, metadata_source):
    p=BASE/'text'/f'{version}.pages.json'
    a=read(f'text/{version}.pages.json')
    lines=[]
    for e in a[:3]:
        for line in e['text'].splitlines():
            if re.search(r'Quanshi|QUANSHI|Quanshi ZHANG|Jiao|SJTU|sjtu|zqs1022',line):
                line=line.strip()
                if line and line not in lines:
                    lines.append(line)
    verified=any(re.search(r'Quanshi|QUANSHI',s) for s in lines) and any(re.search(r'Jiao|sjtu|SJTU',s) for s in lines)
    return {'metadata_source':metadata_source,'pdf_pages_checked':[e['page'] for e in a[:3]],
      'pdf_identity_lines':lines[:20],'local_text':p.relative_to(ROOT).as_posix(),
      'verification':'PDF author name plus SJTU affiliation/email and matching group coauthors verified' if verified else 'Author query metadata matches group coauthors, but inspected first three PDF pages do not provide individual-author identity evidence',
      'identity_status':'verified_public_pdf' if verified else 'metadata_only_not_verified_in_checked_PDF_pages',
      'identity_sources':['http://qszhang.com/index.php/publications/','https://jhc.sjtu.edu.cn/people/members/quanshi-zhang.html']}

papers=read('papers.json')
manual=read('manual-review.json')
for p in papers:
    aid=p['arxiv_id']
    p['topic'],p['research_content']=CONTENT[aid]
    p['numbered_result_ids']=NUMBERED.get(aid,[])
    p['numbered_result_count_kind']='exact_manual_distinct_numbered_statements_in_acquired_pdf'
    p['proved_numbered_result_count_kind']='numbered_targets_with_local_dedicated_proof_blocks; cited statements not treated as locally proved'
    p['proof_count_scope']='acquired public PDF version only; no claim of complete supplementary-material retrieval or proof correctness'
    p['count_method']='Manual inspection of text page by page and proof/appendix context; raw marker hits are leads only. Main/appendix restatements collapsed by statement content.'
    p['manual_evidence_file']=f'{REL}/manual-review.json'
    p['proof_count_unit']='dedicated proof block or clearly separated derivation subsection; separately headed parts counted separately, a single multipart Proof block counted once'
    p['authors_evidence']=identity(p['version'],'arxiv-author.atom plus PDF title/author/affiliation')
    p['first_public_year_basis']='arXiv first-submitted timestamp'
    p['supplement_status']='proof-bearing appendices included in acquired PDF' if p['proof_count'] else 'no separate supplement relied on in this acquired-PDF count'
    p['draft']=False
    p['review_complete']=True
    p['candidate_confirmation']='pending'
    p['formal_import_status']='not_imported'
    p['publication']=None
    if aid in OFFICIAL_VENUES:
        v,y,u=OFFICIAL_VENUES[aid]
        p['publication']={'venue':v,'year':y,'source_url':u,'verification':'author official publication list or PDF venue header, not inferred from arXiv submission year'}
    p['source_versions']=[]

for aid in ['2302.13091','2605.17770','2605.13148']:
    p=next(p for p in papers if p['arxiv_id']==aid)
    p['proof_count_kind']='exact_manual_derivation_unit_inventory'
    p['proof_unit_type']='approximate/theoretical derivation; not a numbered complete proof'

for aid,detail in {
 '2608.06839':'Methods PDF p14 points to Supplementary Note 1; no such file acquired from public arXiv record. Overall proof density remains unverified.',
 '2512.18607':'PDF pp9–10 explicitly point to supplementary proofs of Theorems 1–2; no supplementary file acquired. Overall proof density remains unverified.',
 '2505.06993':'PDF p4 mentions Appendix C, which is not part of the acquired five-page report. Proofs in any external attachment not verified.',
}.items():
    p=next(p for p in papers if p['arxiv_id']==aid)
    p['supplement_status']='missing_or_unavailable_in_acquired_public_record'
    p['supplement_gap']=detail
    p['proof_count_kind']='exact_manual_inventory_in_acquired_main_pdf_only; supplements_unverified'

go=next(p for p in papers if p['arxiv_id']=='2310.09838')
go['rationale']='围棋网络交互解释有4个本地证明/推导小节，适合作为应用与基础matching复用候选；另有待用户复核数学疑点，未据此降低建议级别。'
go['mathematical_issue_refs']=[f'{REL}/mathematical-issues.json#arxiv:2310.09838']
manual['2310.09838']['rationale']=go['rationale']

vdownloads={v['id']:v for v in read('venue-downloads.json')+read('extra-downloads.json')}

def additional_version(aid,key,source,venue,year,note):
    p=next(p for p in papers if p['arxiv_id']==aid)
    d=vdownloads[key]
    n=len(read(f'text/{key}.pages.json'))
    p['source_versions'].append({**d,'source_url':source,'version':f'{venue} {year} official publication PDF','total_pages':n,'note':note,'duplicategroup':p['duplicategroup']})

additional_version('2309.13411','icml2025-coalition','https://proceedings.mlr.press/v267/zheng25d.html','ICML',2025,'Official final 24-page PDF; same title, three authors and Appendix C–G proof inventory as acquired arXiv v3. Earlier v1/v2 are smaller preliminary versions; counts belong to acquired v3/final, not all versions.')
additional_version('2304.01811','icml2023-harsanyinet','https://proceedings.mlr.press/v202/chen23s.html','ICML',2023,'Official final 22-page PDF; same local proof inventory as acquired arXiv v2, counted as one paper.')
additional_version('2302.13080','icml2023-symbolic-concepts','https://proceedings.mlr.press/v202/li23at.html','ICML',2023,'Official final 18-page empirical paper; no dedicated theorem proof verified; counted as one paper with arXiv v3.')

EXTRAS=[
 {
  'id':'neurips2023-difficulty-main','title':'Towards the Difficulty for a Deep Neural Network to Learn Concepts of Different Complexities','year':2023,
  'authors':['Dongrui Liu','Huiqi Deng','Xu Cheng','Qihan Ren','Kangrui Wang','Quanshi Zhang'],
  'source_url':'https://papers.neurips.cc/paper_files/paper/2023/hash/8143b8c73073a9a23b9c18e400066471-Abstract-Conference.html',
  'version':'NeurIPS 2023 official publication PDF','duplicategroup':'venue:neurips2023:8143b8c73073a9a23b9c18e400066471',
  'publication':{'venue':'NeurIPS','year':2023},
  'numbered_result_ids':['Theorem 1','Theorem 2','Theorem 3','Theorem 4','Proposition 1'],
  'numbered_result_count':5,'proved_numbered_result_count':3,'proof_count':4,'proof_pages_or_span':[[17,21]],
  'evidence':'Appendix G.1 pp17–18 Theorem 2; G.2 pp18–19 Theorem 3; G.3 p20 Theorem 4; G.4 pp20–21 unnumbered derivation linking concepts and multi-order interactions = four proof/derivation units. G.5 p21 only lists a three-step regression argument (one sketch excluded from proof_count). Theorem 1 is cited; Proposition 1 is a stated independent-variable factorization without a separate proof.',
  'topic':'concept complexity / learning difficulty / perturbation variance',
  'research_content':'理论解释复杂交互概念为何难学，分析Taylor触发函数的扰动方差、概念二值激活、与多阶交互的关系及简化回归模型的学习困难。',
  'recommendation':'recommend','rationale':'3个本地编号证明加1个完整关系推导，理论涉及Taylor、随机变量和组合求和；回归草图另记，避免夸大证明完整性。',
  'proof_sketch_count':1,'proof_sketch_pages':[21],
 },
 {
  'id':'aaai2025-monitoring','title':'Monitoring Primitive Interactions During the Training of DNNs','year':2025,
  'authors':['Jie Ren','Xinhao Zheng','Jiyu Liu','Andrew Lizarraga','Ying Nian Wu','Liang Lin','Quanshi Zhang'],
  'source_url':'https://ojs.aaai.org/index.php/AAAI/article/view/34223',
  'version':'AAAI 2025 official nine-page publication PDF','duplicategroup':'doi:10.1609/aaai.v39i19.34223',
  'publication':{'venue':'AAAI','year':2025,'doi':'10.1609/aaai.v39i19.34223','published':'2025-04-11'},
  'numbered_result_ids':['Theorem 2.1'],'numbered_result_count':1,'proved_numbered_result_count':0,'proof_count':0,'proof_pages_or_span':[],
  'evidence':'Main PDF p3 Theorem 2.1 (universal matching of feature interactions) points to a proof in Appendix E. The official nine-page PDF does not include Appendix E or its other referenced appendices. No supplementary file acquired from official landing page.',
  'topic':'training dynamics / feature interaction primitives / PCA',
  'research_content':'将主成分特征分量作为交互变量，监测训练中primitive交互的出现、增强或减弱，并以稀疏重构和实验研究学习效率。',
  'recommendation':'uncertain','rationale':'有明确编号理论并声称附录证明，但已取得官方PDF缺少Appendix E，须补查公开附件再判断证明数量。',
  'supplement_status':'missing_or_unavailable_in_acquired_public_record',
  'supplement_gap':'Publisher nine-page PDF omits referenced Appendix E (Theorem 2.1 proof); no public supplementary file acquired.',
 },
 {
  'id':'acl2026-nonliteral','title':'Challenging the Explanation Based on Preceding Tokens: Discovering Transferable Non-Literal Biasing','year':2026,
  'authors':['Yuchen Huang','Junpeng Zhang','Quanshi Zhang'],
  'source_url':'https://aclanthology.org/2026.acl-short.52/',
  'version':'ACL 2026 short-paper official publication PDF','duplicategroup':'doi:10.18653/v1/2026.acl-short.52',
  'publication':{'venue':'ACL (short papers)','year':2026,'doi':'10.18653/v1/2026.acl-short.52','published':'2026-07'},
  'numbered_result_ids':[],'numbered_result_count':0,'proved_numbered_result_count':0,'proof_count':0,'proof_pages_or_span':[],
  'evidence':'PDF pp1–9 includes method, experiments, limitations, references and supplemental cases; preceding-token bias is demonstrated experimentally. No numbered theorem/lemma/proposition or dedicated proof/derivation block verified.',
  'topic':'LLM explanations / preceding-token bias / empirical study',
  'research_content':'发现语义无关的先前token可独立偏置LLM答案，且偏置可迁移到移除原推理证据的prompt；通过替换token和迁移实验验证。',
  'recommendation':'low_priority','rationale':'公开全文及附录已实查，研究以非字面偏置实验为主，没有本地数学证明块。',
 },
 {
  'id':'fitee2025-first-principles','title':'Towards the first principles of explaining DNNs: interactions explain the learning dynamics','year':2025,
  'authors':['Huilin Zhou','Qihan Ren','Junpeng Zhang','Quanshi Zhang'],
  'source_url':'https://doi.org/10.1631/FITEE.2401025',
  'version':'FITEE 2025 26(7):1017–1026 official publication PDF','duplicategroup':'doi:10.1631/FITEE.2401025',
  'publication':{'venue':'Frontiers of Information Technology & Electronic Engineering','year':2025,'doi':'10.1631/FITEE.2401025','volume':'26(7)','pages':'1017–1026'},
  'numbered_result_ids':[],'numbered_result_count':0,'proved_numbered_result_count':0,'proof_count':0,'proof_pages_or_span':[],
  'evidence':'Official PDF pp1–10, Personal View: discusses interaction axioms, phenomenon explanations, attribution/adversarial method unification and two-phase dynamics using prior results. No independent numbered theorem/lemma/proposition or dedicated local proof appendix verified.',
  'topic':'interaction first principles / learning dynamics / perspective',
  'research_content':'Personal View讨论交互解释能否构成DNN解释的第一性原理，串联公理、泛化/对抗/瓶颈现象、归因方法统一及两阶段学习动态。',
  'recommendation':'secondary','rationale':'研究体系导览与相关论文索引的重要参考，单独标明没有本地新证明，不能用综述总页数代替证明密度。',
 },
]

for e in EXTRAS:
    key=e.pop('id')
    ev=e.pop('evidence')
    d=vdownloads[key]
    pdf=ROOT/d['local_pdf']
    n=len(read(f'text/{key}.pages.json'))
    p={**e,'pdf_url':d['pdf_url'],'local_pdf':d['local_pdf'],'sha256':d['sha256'],'total_pages':n,
     'authors_evidence':identity(key,e['source_url']),
     'proof_evidence':[{'location':ev,'pdf_pages':pages_for(e['proof_pages_or_span'])}],
     'proof_count_kind':'exact_manual_inventory_of_proof_units' if e['recommendation']!='uncertain' else 'exact_manual_inventory_in_acquired_main_pdf_only; supplements_unverified',
     'proof_page_count':len(pages_for(e['proof_pages_or_span'])),
     'proof_count_unit':'dedicated proof block or clearly separated complete derivation subsection; theorem restatements, cited assertions and incomplete sketches not counted',
     'numbered_result_count_kind':'exact_manual_distinct_numbered_statements_in_acquired_pdf',
     'proved_numbered_result_count_kind':'numbered_targets_with_local_dedicated_proof_blocks; cited statements not treated as locally proved',
     'proof_count_scope':'acquired public PDF only; no claim of complete supplementary-material retrieval or proof correctness',
     'count_method':'Manual inspection of full public PDF and proof/appendix context, not automatic marker-hit count.',
     'status':'screened_public_pdf_pending_user_confirmation',
     'first_public_year_basis':'official venue publication year; no earlier arXiv version found in the 95-entry author query',
     'review_as_of':'2026-09-30','draft':False,'review_complete':True,
     'candidate_confirmation':'pending','formal_import_status':'not_imported','arxiv_id':None,'source_versions':[],
     'manual_evidence_file':f'{REL}/manual-review.json'}
    p.setdefault('supplement_status','no separate supplement relied on in this acquired-PDF count')
    p['publication']['source_url']=e['source_url']
    p['publication']['verification']='official venue landing page and acquired PDF front matter'
    if key=='neurips2023-difficulty-main':
        p['source_versions'].append({**vdownloads['neurips2023-difficulty-supplement'],
          'version':'NeurIPS 2023 official supplemental URL','total_pages':n,
          'note':'Byte-identical SHA256 to main PDF: includes the same appendix; not an additional paper or additional proof count.',
          'duplicategroup':p['duplicategroup']})
    manual[p['duplicategroup']]={k:p[k] for k in ['numbered_result_count','proved_numbered_result_count','proof_count','proof_pages_or_span','recommendation','rationale']}
    manual[p['duplicategroup']]['evidence']=ev
    papers.append(p)

discovery=read('discovery.json')
for e in discovery['entries']:
    match=next((p for p in papers if p.get('arxiv_id')==e['arxiv_id']),None)
    if match:
        e['identity_status']=match['authors_evidence']['identity_status']
        e['status']='screened_public_pdf'
        e['paper_evidence_file']=f'{REL}/papers.json'
        e['recommendation']=match['recommendation']
        e['duplicategroup']=match['duplicategroup']
    elif e['review_owner']=='earlier':
        e['status']='handed_to_earlier_screening_agent; see earlier ledger'
discovery['coverage_limits']='Author query is a reproducible 95-entry discovery index, not all publications. Personal homepage stops around 2024; lab homepage is older. Venue-only discoveries recorded separately; no assertion of Internet-wide completeness.'
discovery['venue_only_entries']=[{k:p[k] for k in ['title','year','authors','source_url','duplicategroup','publication','recommendation','status']} for p in papers if not p.get('arxiv_id')]
discovery['additional_unverified_leads']=[{
 'title':'An Introspective Data Augmentation Method for Training Math Word Problem Solvers',
 'year':2024,'authors':['Jinghui Qin','Zhongzhan Huang','Ying Zeng','Quanshi Zhang','Liang Lin'],
 'doi':'10.1109/TASLP.2024.3408067','source_url':'https://doi.org/10.1109/TASLP.2024.3408067',
 'metadata_url':'https://dblp1.uni-trier.de/rec/journals/taslp/QinHZZL24.html',
 'publication':'IEEE/ACM Transactions on Audio, Speech and Language Processing 32:3113–3127 (2024)',
 'identity_status':'metadata ORCID matches official public PDF identity 0000-0002-6108-2738; PDF author/affiliation not yet verified',
 'pdf_url':None,'proof_count':None,'numbered_result_count':None,
 'status':'public_full_text_not_acquired; not one of 40 PDF-screened recent papers',
 'duplicategroup':'doi:10.1109/TASLP.2024.3408067',
}]
discovery['official_recent_publication_blocks_file']=f'{REL}/author-publications-recent-blocks.json'
discovery['identity_exclusion_rule']='Do not accept a name-only search hit. Recent included PDFs must identify Quanshi Zhang together with SJTU affiliation/email or corresponding-author line and group coauthors. Unverified leads remain separate. No inspected recent query PDF was excluded as a namesake.'

for filename in ['downloads.json','venue-downloads.json','extra-downloads.json']:
    ds=read(filename)
    for d in ds:
        if d.get('local_pdf'):
            q=pathlib.Path(d['local_pdf'])
            if q.is_absolute(): d['local_pdf']=q.relative_to(ROOT).as_posix()
    write(filename,ds)

errors=[]
hash_count=0
for p in papers:
    q=ROOT/p['local_pdf']
    if not q.is_file(): errors.append(f"missing PDF: {p['local_pdf']}");continue
    if hashlib.sha256(q.read_bytes()).hexdigest()!=p['sha256']: errors.append(f"hash mismatch {p['local_pdf']}")
    hash_count+=1
    if p['numbered_result_count']!=len(p['numbered_result_ids']): errors.append(f"numbered ID count {p['title']}")
    if p['proved_numbered_result_count']>p['numbered_result_count']: errors.append(f"proved count {p['title']}")
    ps=pages_for(p['proof_pages_or_span'])
    if ps and (min(ps)<1 or max(ps)>p['total_pages']): errors.append(f"page bounds {p['title']}")
    if p['proof_page_count']!=len(ps): errors.append(f"page count {p['title']}")
    if p['proof_count']>0 and not ps: errors.append(f"proof missing pages {p['title']}")
    if len(read(f"text/{q.stem}.pages.json"))!=p['total_pages']: errors.append(f"PDF page count {p['title']}")
    for v in p['source_versions']:
        qv=ROOT/v['local_pdf']
        if not qv.is_file() or hashlib.sha256(qv.read_bytes()).hexdigest()!=v['sha256']: errors.append(f"version PDF/hash {v['local_pdf']}")
        hash_count+=1
assert len(papers)==40
assert not errors, errors
for p in papers:
    p['pre_constraint_recommendation']=p['recommendation']
    p['eligible_for_formal_candidate']=False
    p['scope']='historical acquired-PDF discovery screening; superseded by published-version-only candidate filter'
write('screened-discovery-papers.json',papers)
write('manual-review.json',manual)
write('discovery.json',discovery)

counts=collections.Counter(p['recommendation'] for p in papers)
validation={'as_of':'2026-09-30','frozen':False,'scope':'historical discovery screening, not formal-only candidates','papers':40,'arxiv_recent_papers':36,'venue_only_papers':4,
 'recommendation_counts':dict(counts),'additional_unverified_metadata_leads':1,
 'pdfs_checked_with_exists_sha256_and_page_bounds':hash_count,
 'primary_pdf_identity_verified':sum(p['authors_evidence']['identity_status']=='verified_public_pdf' for p in papers),'errors':errors,'all_paths_relative':True,
 'all_candidates_require_user_confirmation':True,'corpus_import_performed':False,
 'recommend_keys':[p['arxiv_id'] or p['duplicategroup'] for p in papers if p['recommendation']=='recommend']}
write('discovery-screening-validation.json',validation)

def spantext(p):
    return ', '.join(str(a) if a==z else f'{a}–{z}' for a,z in p['proof_pages_or_span']) or '—'

evidence=['# 2023–2026公开论文逐篇证据（截至2026-09-30）','',
 '本文件和papers.json是候选调研，尚待用户确认；没有正式收录、证明重写或Lean形式化。40篇公开PDF均核对了题名、作者及SJTU身份。', '',
 '## 计数口径','',
 '- 编号结果数：论文中独立的Theorem/Lemma/Proposition/Corollary陈述，含明确引用的旧结果；正文与附录复述按内容合并。编号相同但内容不同的陈述分别处理。',
 '- 本地有专门证明的编号目标：上述编号目标中在已取PDF有对应专门Proof块或证明小节的数量；引用旧结果不当成本地证明。',
 '- 证明/推导单元：专门Proof块或清楚分隔的证明/推导小节；同一个多部分Proof块计一次，分别设标题的部分分别计。非编号完整推导可以计入，但引文、公式定义、任务解题数据和未展开的草图不算完整证明。',
 '- 2302.13091、2605.17770、2605.13148的一个单元各为近似/理论推导，已单独标注；不声称它们是完整编号定理证明。',
 '- 证明页数：含实际证明/所登记推导内容的PDF物理页去重；不是印刷页码、章节页总和或正文总页数。边界页可能同时包含实验。',
 '- 自动proof-hits只用于定位。所有列出的计数经正文/附录上下文人工检查，不等同数学正确性全面审稿；也未核实不可得附件。',
 '- pdftotext中的\\x0f可能来自数学字体，不按整个文本formfeed分割。精确分页来自pdfinfo及逐页pdftotext -f/-l，保存于text/*.pages.json。','',
 '## 独立论文证据','',
 '|合并键|题名及公开来源|首发年|编号结果|本地编号证明|证明/推导单元|证明PDF页|附录/编号证据|',
 '|---|---|---:|---:|---:|---:|---|---|']
for p in papers:
    key=p['arxiv_id'] or p['duplicategroup']
    unit=str(p['proof_count'])
    if p['proof_count_kind']=='exact_manual_derivation_unit_inventory':unit+='（推导）'
    if p.get('supplement_gap'):unit+='（仅已取PDF，附件未核实）'
    evidence.append(f"|{key}|[{p['title']}]({p['source_url']})|{p['year']}|{p['numbered_result_count']}|{p['proved_numbered_result_count']}|{unit}|{spantext(p)}|{p['proof_evidence'][0]['location'].replace('|','/')}|")
evidence+=['','## 版本及附件边界','',
 'Coalition：首发2023，正式ICML2025；计数依据arXiv 2309.13411v3（2026-02-24更新）和ICML2025完整24页版本，不把2026更新算新论文。HarsanyiNet及Does a Neural Network Really Encode Symbolic Concepts的PMLR版与arXiv版在source_versions登记，分别仅算一篇。',
 'NeurIPS2023 Difficulty的main与supplement两个官方URL下载为相同SHA256文件，均为含附录22页，既不算第二篇也不把证明重复相加。G.5回归论证只列步骤，另记sketch=1；G.1–G.3和G.4共4个证明/完整推导单元。',
 '2305.01939：主文Theorem 3稀疏上界在Appendix B.4 p20误标Theorem 6，实际Shapley–Taylor Theorem 6在p25是另一陈述。按陈述内容去重后10个编号结果，不把同号混合或重复算入。',
 '最新2608.06839的Supplementary Note 1、2512.18607的supplementary materials、AAAI2025 Monitoring的Appendix E均未取得；只能列已取PDF的局部计数，整体证明密度未核实。2505.06993正文提及Appendix C，但五页PDF不含该附录。',
 '2512.18607是旧交互瓶颈研究的期刊扩展候选，与早期ICLR2022论文相关，未按题名相近自动合并。arXiv管理员提示2502.10162与2407.19198存在文字重叠；两篇保留独立候选，并标共享/扩展关系供后续命题对齐。','',
 '## 文件、身份与数学疑点','',
 'papers.json包含全部40行、相对PDF/逐页文本路径、sha256、具体证明位置、研究内容、正式发表年份（有核对证据时）及待用户确认状态。validation.json检查主PDF及四份额外版本的存在/哈希、页数和计数基本约束。',
 '95项作者Atom完整原样保存为arxiv-author.atom；discovery.json保留全部95项，再单列4篇venue-only和1项全文未取得的TASLP元数据线索。早期59项由earlier代理处理。',
 'mathematical-issues.json仅记录围棋论文Appendix G Eq18–19的待复核疑点：有限差分消去要求同一二次多项式且系数不随子集改变，Taylor余项和系数定义仍须审查。问题确认、修改授权均pending，未断言已确认论文错误，未改命题。','']
(BASE/'discovery-screening-evidence.md').write_text('\n'.join(evidence))

findings=['# 近期候选筛查结果（冻结版）','',
 f"截至2026-09-30，本部分实查36篇首次arXiv公开于2023–2026的论文和4篇额外官方发表论文，共40篇独立候选；建议优先{counts['recommend']}、次级{counts['secondary']}、附件待核实{counts['uncertain']}、证明较少或未见本地证明{counts['low_priority']}。没有将候选正式导入。",'',
 '## 建议优先候选（全部列出）','',
 '|合并键|题名|研究内容|证明/推导单元|编号结果|PDF页|建议依据|',
 '|---|---|---|---:|---:|---|---|']
for p in papers:
    if p['recommendation']=='recommend':
        findings.append(f"|{p['arxiv_id'] or p['duplicategroup']}|[{p['title']}]({p['source_url']})|{p['research_content']}|{p['proof_count']}|{p['numbered_result_count']}|{spantext(p)}|{p['rationale']}|")
findings+=['','## 完整性限制','',
 '36篇近期arXiv主PDF全部取得、完整转换并核对身份；4篇venue-only同样核对公开PDF。没有待确认同名身份的40项已查记录；TASLP2024另一条仅有DOI/ORCID元数据的线索保留discovery，不算已实查。',
 '作者Atom的95项是可复现检索分母，不等于作者全部发表论文。官方个人publicationlist更新到约2024；实验室主页更旧且部分Paper链接错复用。补充检索使用arXiv、PMLR、NeurIPS、AAAI、ACL及FITEE官方来源，但不宣称网上绝无遗漏。',
 '2608.06839、2512.18607、AAAI2025 Monitoring的公开正文明确指向未取得附件，整体证明数量待查；2505.06993也有正文提及但未提供附录C的缺口。',
 '综述/基础技术说明（2304.13312、2508.07636、FITEE2025）保留为secondary：用于研究内容与理论体系导读，本地proof=0不能列为证明密集成果。',
 '没有按研究题目淘汰LLM、Agent、EEG或系统论文；均以实际正文和附录核查结果分类。推荐级别是调研建议，是否收录仍待用户确认。','']
(BASE/'discovery-screening-findings.md').write_text('\n'.join(findings))
print(json.dumps(validation,ensure_ascii=False,indent=2))
