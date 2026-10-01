"""Freeze discovery separately from the user's formal-version-only candidate table."""
from pathlib import Path
import copy,hashlib,json,re,subprocess
from collections import Counter
import build_papers
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent.parent
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def evidence(section,pages,ids,detail,file='formal_main'):
 return dict(section=section,pdf_pages=pages,identifiers=ids,detail=detail,file=file)
def locators(directory):
 hits=[]
 for p in json.loads((directory/'pages.json').read_text()):
  for l in p['text'].splitlines():
   if re.search(r'\b(?:[Pp]roof|[Dd]erivation|Theorem|Lemma|Proposition|Corollary)\b',l):hits.append({'page':p['page'],'text':l.strip()})
 return hits

# Further manual discovery inspections. These are not accepted-version counts.
build_papers.MANUAL.update({
 '1901.09546':dict(recommendation='recommend',topic='complex-valued equivariance / privacy',proof_count=5,proof_count_kind='manual_exact_distinct_proof_units',numbered_result_count=0,proof_pages_or_span={'span':[11,11],'kind':'proof-bearing appendix page'},proof_evidence=[evidence('A',[11,11],'Operation groups 1–5','Five algebraic proofs: convolution, ReLU, batch normalization, pooled Avg/Max/Dropout, skip connection. Six operation types do not mean six proof units.','arxiv')],rationale='ICLR2020相关论文；此计数仅指已下载的arXiv v2，不作为正式版计数。'),
 '1906.04109':dict(recommendation='secondary',topic='information discarding / information bottleneck',proof_count=2,proof_count_kind='manual_lower_bound',numbered_result_count=0,proof_pages_or_span={'span':[12,13],'kind':'proof-bearing appendix span'},proof_evidence=[evidence('B,C',[12,13],'Equation 4; concentration / information-bottleneck relation','At least two explicit derivation sections, not two numbered theorems.','arxiv')],rationale='已实际读附录B/C推导；正式ICML2022另取得PDF并重核。'),
 '1901.02413':dict(recommendation='secondary',topic='interpretable convolutional networks',proof_count=2,proof_count_kind='manual_exact_explicit_proof_blocks',numbered_result_count=0,proof_pages_or_span={'span':[15,16],'kind':'proof-bearing appendix span'},proof_evidence=[evidence('Appendix',[15,16],'Proof of Equations 4 and 5','Two explicit equation proof sections. TPAMI final publication version has not been independently acquired.','arxiv')],rationale='两段显式证明；计数不能移植到未取得的TPAMI正式版。'),
 '1710.00935':dict(recommendation='low_priority',topic='interpretable convolutional networks',proof_count=2,proof_count_kind='manual_lower_bound',numbered_result_count=0,proof_pages_or_span={'span':[11,11],'kind':'equation-derivation appendix page'},proof_evidence=[evidence('Proof of equations',[11,11],'gradient and entropy decomposition','Two equation derivations; no large independent theorem-proof appendix.','arxiv')],rationale='已读证明附录，至少两段推导；正式CVPR版尚未独立取得。'),
 '1708.03911':dict(recommendation='low_priority',topic='graph mining / active annotation',proof_count=1,proof_count_kind='manual_lower_bound',numbered_result_count=0,proof_pages_or_span={'span':[14,14],'kind':'objective-function derivation appendix page'},proof_evidence=[evidence('Appendix objective function',[14,14],'graph-mining objective','One inspected multi-line objective derivation; not a numbered theorem.','arxiv')],rationale='实际目标函数推导至少一单元；正式CVIU版未独立取得。'),
})
build_papers.main('papers.arxiv-discovery.base.json')
discovery=json.loads((ROOT/'papers.arxiv-discovery.base.json').read_text())
byid={p['duplicate_group'].split(':')[-1]:p for p in discovery}
for i,note,pages,n in [
 ('2106.10938','PDF3/6有Propositions1–2，但主要通过可视化和实验验证；性质证明另指supplement，此12页版未包含。',[3,6],2),
 ('2009.05423','Theorem1明确引自Hein/Guo，Theorem2声明省略证明并引用独立supp；此9页版未含该附件。同标题后期期刊作者名单改变，不能自动移植其证明。',[3,3],2),
 ('2007.04298','arXiv9页正文引用独立附录；随后取得AAAI2021正式10页版，第8页确有3个实际证明。',[4,4],0),
 ('2010.05045','arXiv9页版引用supplement；正式AAAI2021第9–10页另有一段关系推导，已独立读取。',[5,5],0),
 ('2010.14978','此7页技术note主要列定义与性质，PDF1明确说明完整证明在另一论文；不据题名与抽象将其判为多证明。',[1,6],None),
 ('2111.03505','已读正文的supp引用及PDF20附录B/C，给出revised-vMF/MLE及EM公式但未建立完整独立证明清单。',[4,20],None),
 ('1911.09017','已读PDF5的计算/方差说明及PDF14附录性质；大量图表和评价结果，未建立完整独立证明清单。',[5,14],None),
 ('2003.08365','已读10页方法/实验版，未见独立证明附录；仍不把关键词无命中写成证明数0。',[1,10],None),
]:
 p=next(x for x in discovery if x['duplicate_group']=='arxiv:'+i)
 p['status']='pdf_manually_screened_significant_locators_no_complete_proof_inventory'
 p['rationale']=note;p['proof_evidence']=[evidence('manual prescreen',pages,'see note',note,'arxiv')]
 p['numbered_result_count']=n
for p in discovery:
 i=p['version'].split(':')[-1].split('v')[0]
 if i in ['1901.07538','1901.06978']:
  full={'1901.07538':'1805.07468','1901.06978':'1804.10272'}[i]
  p['duplicate_group']='arxiv:'+full;p['related_full_paper']='arxiv:'+full
  p['status']='extended_abstract_same_work_not_extra_full_paper'
  p['rationale']='作者列表和首页明确为同一工作的extended abstract；不与全文重复按独立工作计数。'
write('papers.arxiv-discovery.json',discovery)

manifests=[]
for name in ['venue-source-index.json','formal-source-index.json','formal-supp-source-index.json']:
 manifests+=json.loads((ROOT/name).read_text())
files={r['key']:r for r in manifests if r['kind']=='pdf' and r['status']=='ok'}
def material(key,role):
 r=files[key]
 return dict(role=role,pdf_url=r['url'],local_pdf=r['local_file'],sha256=r['sha256'],total_pages=r['total_pages'])
FORMAL={
 '2111.06206':dict(title='Defining and Quantifying the Emergence of Sparse Concepts in DNNs',year=2023,venue='CVPR 2023',landing='sparse-cvpr2023',keys=['sparse-cvpr2023-main','sparse-cvpr2023-supp'],count=12,kind='manual_exact_distinct_proof_units',numbered=5,recommendation='recommend',inventory='Theorems1–5. Repeated declarations and necessity/sufficiency parts are not extra results.',proofs=[evidence('C',[3,3],'Theorem1','Necessity and sufficiency together form one distinct proof unit.','formal_supplement'),evidence('D.1',[4,5],'7 unnumbered Harsanyi properties','Seven separate property proofs, not seven numbered theorems.','formal_supplement'),evidence('D.2',[6,11],'Theorems5,2,3,4','Four actual theorem proofs, with statement repeats collapsed.','formal_supplement')],rationale='正式CVPR正文10页+补充27页，人工重核5个独立编号定理和12个实际证明单元；本轮优先正式收录候选。'),
 '2210.09020':dict(title='Defects of Convolutional Decoder Networks in Frequency Representation',year=2023,venue='ICML 2023',landing='decoder-icml2023',keys=['decoder-icml2023'],count=9,kind='manual_lower_bound',numbered=8,recommendation='recommend',inventory='Theorems3.2,4.2–4.5; Corollaries3.3–3.4; LemmaA.1.',proofs=[evidence('A/A.1–A.7',[11,25],'5 Theorems; 2 Corollaries; LemmaA.1; Assumption4.1 derivation','Official PDF proof starts inspected on pages11,12,14,15,18,19,21,22,23,24. Theorem4.2 multiple parts are collapsed; at least nine independent proof/derivation units.')],rationale='正式ICML2023 PDF34页，证明与相关推导位于PDF11–25；已在正式文件人工核页与独立结果。'),
 '2205.01940':dict(title='Towards Theoretical Analysis of Transformation Complexity of ReLU DNNs',year=2022,venue='ICML 2022',landing='transformation-icml2022',keys=['transformation-icml2022'],count=10,kind='manual_exact_proof_blocks',numbered=0,recommendation='recommend',inventory='No numbered theorem/lemma/proposition/corollary; Properties1–3 are recorded separately.',proofs=[evidence('B.1–B.4',[13,15],'Properties1–3 and information/disentanglement relations','Official PDF has 3 Proof blocks on page13, 4 on page14, 3 on page15. No theorem count is inferred from those 10 blocks.')],rationale='正式ICML2022 PDF22页；10段显式证明虽无Theorem编号，仍应纳入多证明候选。'),
 '2103.07364':dict(title='A Unified Game-Theoretic Interpretation of Adversarial Robustness',year=2021,venue='NeurIPS 2021',landing='robustness-neurips2021',keys=['robustness-neurips2021-main','robustness-neurips2021-supp'],count=15,kind='manual_lower_bound',numbered=1,recommendation='recommend',inventory='Proposition1 only; most proof units establish unnumbered properties.',proofs=[evidence('B.1–B.4',[2,7],'5 interaction properties;4 multiorder Shapley properties;2 relations;Proposition1 and converse','13 actual blocks read in official supplementary PDF; main/appendix statement repetition does not add numbered results.','formal_supplement'),evidence('D,G',[8,9],'meaning of ΔI;attribution-detector utility','Two additional explicit proof blocks. The H dropout derivation is not included in the lower bound.','formal_supplement')],rationale='正式NeurIPS2021正文14页+补充16页，至少15段证明。Landing/BibTeX标题为Towards a Unified Game-Theoretic View of Adversarial Perturbations and Robustness，正式PDF仍用本标题；已核作者与论文身份。'),
 '2007.04298':dict(title='Building Interpretable Interaction Trees for Deep NLP Models',year=2021,venue='AAAI 2021',landing='trees-aaai',keys=['trees-aaai2021'],count=3,kind='manual_exact_distinct_proof_units',numbered=0,recommendation='secondary',inventory='Three unnumbered equation-relation proofs.',proofs=[evidence('Appendix',[8,8],'Eq5;Eq6/7;Eq8','Three titled proofs: elementary-component relation, fine-grained two-set interactions, recursive interaction-benefit decomposition.')],rationale='正式AAAI10页版包含arXiv9页版没有的3段实际证明；数量中等，核心相关次级候选。'),
 '2010.05045':dict(title='Interpreting Multivariate Shapley Interactions in DNNs',year=2021,venue='AAAI 2021',landing='multivariate-aaai',keys=['multivariate-aaai2021'],count=1,kind='manual_exact_inspected_appendix_unit',numbered=0,recommendation='secondary',inventory='One unnumbered elementary-interaction relation derivation.',proofs=[evidence('Appendix relationship',[9,10],'B([A]) / elementary interaction components','The actual algebra on page10 establishes one relation, despite lacking a Proof heading. Other independent supplements were not acquired.')],rationale='正式AAAI10页已核1段关系推导；保留核心定义的次级候选，不能声称此版证明很多。'),
 '1906.04109':dict(title='Quantification and Analysis of Layer-wise and Pixel-wise Information Discarding',year=2022,venue='ICML 2022',landing='discarding-icml2022',keys=['discarding-icml2022'],count=2,kind='manual_lower_bound',numbered=0,recommendation='secondary',inventory='Unnumbered equation/information-theoretic derivations.',proofs=[evidence('B,C',[12,13],'Equation4;concentration/information-bottleneck relation','Two complete explicit sections read in the official35-page PDF. A and F contain additional mathematical explanations not included in the conservative lower bound.')],rationale='正式ICML35页已核至少2类推导，属于信息论相关次级；不把总页数当证明页数。'),
}
htmls={r['key']:r for r in manifests if r['kind']=='html'}
FORMAL_AUTHORS={
 '2111.06206':['Jie Ren','Mingjie Li','Qirui Chen','Huiqi Deng','Quanshi Zhang'],
 '2210.09020':['Ling Tang','Wen Shen','Zhanpeng Zhou','Yuefeng Chen','Quanshi Zhang'],
 '2205.01940':['Jie Ren','Mingjie Li','Meng Zhou','Shih-Han Chan','Quanshi Zhang'],
 '2103.07364':['Jie Ren','Die Zhang','Yisen Wang','Lu Chen','Zhanpeng Zhou','Yiting Chen','Xu Cheng','Xin Wang','Meng Zhou','Jie Shi','Quanshi Zhang'],
 '2007.04298':['Die Zhang','Hao Zhang','Huilin Zhou','Xiaoyi Bao','Da Huo','Ruizhao Chen','Xu Cheng','Mengyue Wu','Quanshi Zhang'],
 '2010.05045':['Hao Zhang','Yichen Xie','Longjie Zheng','Die Zhang','Quanshi Zhang'],
 '1906.04109':['Haotian Ma','Hao Zhang','Fan Zhou','Yinqing Zhang','Quanshi Zhang'],
 '2205.15146':['Zhanpeng Zhou','Wen Shen','Huixin Chen','Ling Tang','Yuefeng Chen','Quanshi Zhang'],
 '2205.15130':['Xu Cheng','Hao Zhang','Yue Xin','Wen Shen','Quanshi Zhang'],
 '1911.09040':['Wen Shen','Binbin Zhang','Shikun Huang','Zhihua Wei','Quanshi Zhang'],
}
papers=[]
for d in discovery:
 p=copy.deepcopy(d);i=d['version'].split(':')[-1].split('v')[0]
 p['discovery_record']='papers.arxiv-discovery.json#arxiv:'+i
 p['first_public_year']=d['year'];p['is_formal_version']=False
 p['formal_status']='formal_publication_or_exact_accepted_version_not_confirmed'
 p['recommendation']='low_priority';p['status']='discovery_only_not_formal_candidate'
 p['rationale']='仅保留作者索引发现记录；用户只取正式版，此arXiv文件不进入待收录主表。'
 p['proof_evidence']=[];p['proof_count']=None;p['numbered_result_count']=None;p['proof_pages_or_span']=None
 p['numbered_result_inventory']=None
 p['automatic_screen']['source_version']=d['version']
 p['proof_count_kind']='not_a_formal_version_counts_kept_in_arxiv_discovery_ledger'
 if i in FORMAL:
  f=FORMAL[i];m=[material(k,'formal_main' if j==0 else 'formal_supplement') for j,k in enumerate(f['keys'])]
  p.update(title=f['title'],year=f['year'],venue=f['venue'],source_url=htmls[f['landing']]['url'],pdf_url=m[0]['pdf_url'],version=f['venue']+' venue-hosted published PDF(s); artifact SHA256 pinned',local_pdf=m[0]['local_pdf'],sha256=m[0]['sha256'],total_pages=m[0]['total_pages'],total_material_pages=sum(x['total_pages'] for x in m),materials=m,proof_evidence=f['proofs'],proof_count_kind=f['kind'],proof_count=f['count'],numbered_result_count=f['numbered'],numbered_result_inventory=f['inventory'],proof_pages_or_span=[{'file':x['file'],'pages':x['pdf_pages'],'section':x['section']} for x in f['proofs']],recommendation=f['recommendation'],rationale=f['rationale'],status='formal_pdf_manually_reviewed_for_proof_structure_not_correctness',is_formal_version=True,formal_status='published_venue_pdf_verified',authors_evidence={'source':htmls[f['landing']]['url'],'pdf_page':1,'files':[x['local_pdf'] for x in m],'note':'正式PDF首页题名/作者已核对；不依据错置网页anchor猜论文身份。'})
  if i=='2205.01940':p['other_numbered_properties']=3
  if i=='2103.07364':p['published_landing_title']='Towards a Unified Game-Theoretic View of Adversarial Perturbations and Robustness'
  p['formal_landing_snapshot']=htmls[f['landing']]['local_file']
  p['authors']=FORMAL_AUTHORS[i]
 if i in build_papers.EXCLUDED:
  p['status'],p['rationale']=build_papers.EXCLUDED[i];p['formal_status']=p['status']
 papers.append(p)

# Published but the accepted PDF, or its actual proof attachment, is unavailable.
PENDING={
 '2010.04055':('A Unified Approach to Interpreting and Boosting Adversarial Transferability',2021,'ICLR2021','X76iqnUbBjz',None,None),
 '2009.11729':('Interpreting and Boosting Dropout from a Game-Theoretic View',2021,'ICLR2021','Jacdvfjicf7',None,None),
 '1901.09546':('Interpretable Complex-Valued Neural Networks for Privacy Protection',2020,'ICLR2020','SHDG97ukaIH',None,None),
 '2105.10719':('Can We Faithfully Represent Masked States to Compute Shapley Values on a DNN?',2023,'ICLR2023','YV8tP7bW6Kt',None,None),
 '2111.06236':('Discovering and Explaining the Representation Bottleneck of DNNs',2022,'ICLR2022','iRCUlgmdfHJ',None,None),
 '2205.15146':('Batch Normalization Is Blind to the First and Second Derivatives of the Loss',2024,'AAAI2024','29978','bn-aaai2024',3),
 '2205.15130':('Clarifying the Behavior and the Difficulty of Adversarial Training',2024,'AAAI2024','29032','advtrain-aaai2024',7),
 '1911.09040':('3D-Rotation-Equivariant Quaternion Neural Networks',2020,'ECCV2020','3539','quaternion-eccv2020-main',None),
}
for i,(title,year,venue,oid,key,numbered) in PENDING.items():
 p=next(x for x in papers if x['discovery_record'].endswith('arxiv:'+i));p['title']=title;p['year']=year;p['venue']=venue
 p['recommendation']='uncertain';p['status']='published_formal_proof_material_pending';p['formal_status']='published_pdf_unavailable' if key is None else 'published_main_obtained_proof_supplement_not_obtained'
 p['proof_count']=None;p['numbered_result_count']=numbered;p['proof_count_kind']='formal_proof_inventory_unverified_missing_material'
 if venue.startswith('ICLR'):
  p.update(source_url=f'https://openreview.net/forum?id={oid}',pdf_url=f'https://openreview.net/pdf?id={oid}',local_pdf=None,sha256=None,total_pages=None,version=venue+' accepted version, PDF not acquired',is_formal_version=False)
  p['rationale']='正式发表已由作者publication与官方OpenReview公开论文记录交叉识别；网页PDF/API/API2均403，web.open亦官方browser challenge。arXiv证明数保留在发现台账，不能替代正式版。'
 else:
  m=material(key,'formal_main');p.update(pdf_url=m['pdf_url'],local_pdf=m['local_pdf'],sha256=m['sha256'],total_pages=m['total_pages'],materials=[m],version=venue+' venue-hosted main PDF, proof supplement not acquired',is_formal_version=True)
  p['authors']=FORMAL_AUTHORS[i]
  p['authors_evidence']={'source':m['pdf_url'],'pdf_page':1,'file':m['local_pdf'],'note':'正式PDF首页题名及作者顺序人工核对；引用附录与实际证明分开。'}
  if venue.startswith('AAAI'):
   landing={'2205.15146':'bn-aaai2024','2205.15130':'advtrain-aaai2024'}[i]
   p['source_url']=htmls[landing]['url'];p['formal_landing_snapshot']=htmls[landing]['local_file']
   p['rationale']='正式正文9页已核：首页及编号结果可定位，实际证明引用Appendices。官方第二galley经下载确认是Underline会议报告，不是证明supplement。不得照搬旧arXiv附录计数。'
   p['numbered_result_inventory']='Formal main PDF only: Theorems1–2; Corollary1. Referenced appendices not acquired.' if i=='2205.15146' else 'Formal main PDF only: Theorems1–6; Lemma1. Referenced appendix results/proofs not acquired.'
   p['proof_evidence']=[evidence('Main statements',[2,7],'Theorems1–2+Corollary1' if i=='2205.15146' else 'Theorems1–6+Lemma1','These are statement counts only; referenced proof appendices have not been obtained.')]
  else:
   p['source_url']=htmls['quaternion-eccv2020']['url'];p['formal_landing_snapshot']=htmls['quaternion-eccv2020']['local_file']
   p['rationale']='正式ECCV2020正文17页已取得；arXiv21页版的4类操作证明在额外附录中，不在此正式正文中，正式附件未取得。'
for p in papers:
 if p['discovery_record'].endswith(('arxiv:2207.11694','arxiv:2112.00980','arxiv:2006.13016')):
  p['rationale']='当前查到的作者publication/OpenReview作者记录仍列arXiv/CoRR，未确证对应正式会议/期刊版本；不进入用户要求的正式候选。此结论不表示永未发表。'

TITLES={
 'pami2016':('Object Discovery: Soft Attributed Graph Mining',2016),
 'tist2015':('From RGB-D Images to RGB Images: Single Labeling for Mining Visual Models',2015),
 'iccv2015':('Mining And-Or Graphs for Graph Matching and Object Discovery',2015),
 'cvpr14graph':('Attributed Graph Mining and Matching: An Attempt to Define and Extract Soft Attributed Patterns',2014),
 'iccv2013':('Learning Graph Matching: Oriented to Category Modeling from Cluttered Scenes',2013),
 'cvpr2013':('Category Modeling from just a Single Labeling: Use Depth Information to Guide the Learning of 2D Models',2013),
 'tist2016song_prediction':('Prediction and Simulation of Human Mobility Following Natural Disasters',2016),
 'neuralcom2013':('Unsupervised Skeleton Extraction and Motion Capture from Kinect Video via 3D Deformable Matching',2013),
 'intelligentsystem2013':('Intelligent System for Human Behavior Analysis and Reasoning Following Large-Scale Disasters',2013),
 'tist2013song_fully':('A Fully Online and Unsupervised System for Large and High Density Area Surveillance: Tracking, Semantic Scene Learning and Abnormality Detection',2013),
 'InformationFusion2012':('A Novel Dynamic Model for Multiple Pedestrians Tracking in Extremely Crowded Scenarios',2012),
 'aaai2015song':('A Simulator of Human Emergency Mobility following Disasters: Knowledge Transfer from Big Disaster Data',2015),
 'cvpr2014reconstruction':('When 3D Reconstruction Meets Ubiquitous RGB-D Images',2014),
 'icra2014':('Start from Minimum Labeling: Learning of 3D Object Models and Point Labeling from a Large and Complex Environment',2014),
 'KDD2014':('Prediction of Human Emergency Behavior and their Mobility following Large-scale Disaster',2014),
 'AAAI2014':('Intelligent System for Urban Emergency Management During Large-scale Disaster',2014),
 'ICRA13':('Unsupervised 3D Category Discovery and Point Labeling from a Large Urban Environment',2013),
 'KDD2013':('Modeling and Probabilistic Reasoning of Population Evacuation During Large-scale Disaster',2013),
 'ICRA12':('Laser-based Intelligent Surveillance and Abnormality Detection in Extremely Crowded Scenarios',2012),
 'icra2009':('Moving Object Classification using Horizontal Laser Scan Data',2009),
 'ling22a':('Exploring Image Regions Not Well Encoded by an INN',2022),
 'interpretable-gan-aaai2022':('Interpretable Generative Adversarial Networks',2022),
 'guan19a':('Towards a Deep and Unified Understanding of Deep Neural Models in NLP',2019),
}
official=json.loads((ROOT/'official-acquisition-index.json').read_text())
for a in official:
 if not a.get('local_pdf'):continue
 key=Path(a['local_pdf']).parent.name
 if key=='iccv2015_supplementary':continue
 title,year=TITLES[key];hits=locators(ROOT/'official-papers'/key)
 p=dict(title=title,year=year,first_public_year=None,authors_evidence={'source':a['source_url'],'pdf_page':1,'first_page_text':a['first_page'],'note':'Public author publication entry and PDF title/byline matched. Pre-2016 items are author career publications, not automatically SJTU-lab-affiliated work.'},source_url=a['source_url'],pdf_url=a['pdf_url'],version='public author-hosted copy; exact final publication version not independently verified' if key not in ['ling22a','interpretable-gan-aaai2022','guan19a'] else 'venue-hosted published PDF; SHA256 pinned',local_pdf=a['local_pdf'],sha256=a['sha256'],total_pages=a['total_pages'],proof_evidence=[],proof_count_kind='not_counted_automatic_prescreen_only',proof_count=None,numbered_result_count=None,proof_pages_or_span=None,topic='author-publication boundary / method and applications',recommendation='uncertain',rationale='公开PDF逐页粗筛完成；无高证明定位信号不等于已证明为0。作者托管副本的最终正式版本身份未独立核实，不能直接进入正式候选主表。',status='official_author_copy_prescreen_final_version_unverified',duplicate_group='official:'+key,is_formal_version=key in ['ling22a','interpretable-gan-aaai2022','guan19a'],formal_status='published_venue_pdf_prescreen_only' if key in ['ling22a','interpretable-gan-aaai2022','guan19a'] else 'author_publication_found_exact_final_version_unverified',automatic_screen={'kind':'estimate_locator_not_count_of_proofs','keyword_line_hits':len(hits),'locator_pages':sorted({x['page'] for x in hits})},discovery_index_text=a.get('index_text'))
 if key=='iccv2015':
  m=material('graph-iccv2015-main','formal_main');p.update(pdf_url=m['pdf_url'],local_pdf=m['local_pdf'],sha256=m['sha256'],total_pages=m['total_pages'],materials=[m],source_url=htmls['graph-iccv2015']['url'],version='ICCV2015 venue-hosted published main PDF; author supplement not venue-verified',is_formal_version=True,formal_status='published_main_obtained_author_supplement_role_unverified',status='published_formal_proof_material_pending')
  sup=next(x for x in official if x['pdf_url'].endswith('iccv2015_supplementary.pdf'))
  p['author_supplement_discovery']={k:sup[k] for k in ['pdf_url','local_pdf','sha256','total_pages']}
  p['author_supplement_discovery'].update(proof_count=3,proof_count_kind='manual_exact_titled_proof_sections',proof_pages_or_span=[2,11],sections=['2 Proof of Operation1','3 Proof of Operation3','4 Proof of Operation4'],note='Three actual sections read, but the formal-venue landing only links the main PDF. Kept separate under the user’s strict final-version rule.')
  p['rationale']='正式ICCV主文9页已取得；作者官网另有18页Supplementary包含3段长证明（PDF2–11），但本轮未从正式venue确认该附件的最终版身份，故不将它计入正式证明数。'
  p['venue']='ICCV2015'
 if key in ['tist2015','tist2013song_fully','InformationFusion2012']:
  p['rationale']='人工核对证明关键词均在指向外部文献的说明中，不能算本论文独立证明；没有完整本地证明清单，数值留空。'
  p['status']='reference_proof_locator_manually_checked_final_version_unverified'
 if key=='guan19a':
  p['rationale']='正式ICML2019主文10页已取得；个人主页链接的Microsoft全文/补充403，猜测PMLR supplement路径404。未取得附件，不能依据正文或摘要断言完整证明数。'
  p['formal_status']='published_main_obtained_external_full_supplement_unavailable'
  p['venue']='ICML2019'
  p['materials']=[dict(role='formal_main',pdf_url=p['pdf_url'],local_pdf=p['local_pdf'],sha256=p['sha256'],total_pages=p['total_pages'])]
 if key=='ling22a':p['venue']='AISTATS2022'
 if key=='interpretable-gan-aaai2022':p['venue']='AAAI2022'
 if key=='tist2013song_fully':p['version_note']='Author-hosted PDF has 2012 draft citation placeholders; personal publication list says journal2013. Exact final published PDF not confirmed.'
 write('official-papers/'+key+'/prescreen.json',{'title':title,'locator_hits':hits,'count_kind':'estimate_locator_not_count_of_proofs'})
 papers.append(p)

write('papers.json',papers)
write('formal-candidates.json',[p for p in papers if p['is_formal_version'] and p['recommendation'] in ['recommend','secondary']])
write('formal-pending.json',[p for p in papers if p['status']=='published_formal_proof_material_pending' or p['formal_status']=='published_main_obtained_external_full_supplement_unavailable'])

# Map every enumerated PDF-linked personal-list block; no-link modules are an explicit coverage boundary.
blocks=json.loads((ROOT/'publication-index/publication-blocks.json').read_text());mapping=[]
early_ids={p['version'].split(':')[-1].split('v')[0] for p in discovery}
for j,b in enumerate(blocks,1):
 ids=sorted(set(re.findall(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})',str(b['links']))))
 matches=[]
 for i in ids:matches.append({'mergekey':'arxiv:'+i,'owner':'earlier' if i in early_ids else 'recent'})
 if not matches:
  urls=[x['url'] for x in b['links']]
  for p in papers:
   if p.get('discovery_index_text')==b['text'] or p['pdf_url'] in urls:matches.append({'mergekey':p['duplicate_group'],'owner':'earlier'})
  if any('camera_paper_with_supp_3.pdf' in u for u in urls):matches=[{'mergekey':'official:guan19a','owner':'earlier','note':'Microsoft original download403; matched accepted PMLR title/byline'}]
 mapping.append({'block_number':j,'index_text':b['text'],'links':b['links'],'title_mapping':matches,'status':'mapped' if matches else 'unmapped_requires_followup'})
write('publication-index/title-mapping.json',mapping)

errors=[];pdfs={};required=['title','year','authors_evidence','source_url','pdf_url','version','local_pdf','sha256','total_pages','proof_evidence','proof_count_kind','proof_count','proof_pages_or_span','topic','recommendation','rationale','status','duplicate_group']
for p in papers:
 missing=[k for k in required if k not in p]
 if missing:errors.append({'title':p['title'],'missing':missing})
 if p['recommendation'] in ['recommend','secondary'] and not p['is_formal_version']:errors.append({'title':p['title'],'error':'nonformal candidate'})
 if p.get('materials') and p['total_pages']!=p['materials'][0]['total_pages']:errors.append({'title':p['title'],'error':'primary PDF page-count metadata mismatch'})
 if 'total_material_pages' in p and p['total_material_pages']!=sum(m['total_pages'] for m in p['materials']):errors.append({'title':p['title'],'error':'aggregate material page-count metadata mismatch'})
 for m in p.get('materials',[]) or ([p] if p.get('local_pdf') else []):
  path=PROJECT/m['local_pdf']
  if not path.is_file():errors.append({'title':p['title'],'error':'missing file','file':str(path)});continue
  sha=hashlib.sha256(path.read_bytes()).hexdigest()
  if sha!=m['sha256']:errors.append({'title':p['title'],'error':'SHA mismatch'})
  if m.get('materials') is None:pdfs[str(path)]=sha
 for e in p['proof_evidence']:
  if p['is_formal_version'] and p.get('materials'):
   target=next((x for x in p['materials'] if x['role']==e.get('file')),None)
   if target and not(1<=e['pdf_pages'][0]<=e['pdf_pages'][1]<=target['total_pages']):errors.append({'title':p['title'],'error':'proof page out of bounds','evidence':e})
stats={'index_records':len(discovery),'arxiv_pdf_materials':sum(bool(p['local_pdf']) for p in discovery),'nonarxiv_individual_paper_records':len(TITLES),'ledger_records':len(papers),'formal_candidates':len(json.loads((ROOT/'formal-candidates.json').read_text())),'formal_candidate_tiers':dict(Counter(p['recommendation'] for p in papers if p['is_formal_version'] and p['recommendation'] in ['recommend','secondary'])),'formal_pending_rows':len(json.loads((ROOT/'formal-pending.json').read_text())),'personal_list_pdf_linked_blocks':len(mapping),'personal_list_mapped_blocks':sum(x['status']=='mapped' for x in mapping),'pdf_material_files':sum(1 for d in ['papers','official-papers','venue-papers'] for x in (ROOT/d).rglob('*.pdf')),'unique_work_mergekeys_in_ledger':len({p['duplicate_group'] for p in papers}),'validation_errors':errors,'count_note':'Index records, work mergekeys, downloaded files, accepted-version candidates and supplements are different denominators. The arXiv author query is not a complete list of all lab papers.'}
all_pdf_paths=[p for d in ['papers','official-papers','venue-papers'] for p in (ROOT/d).rglob('*.pdf')]
stats.update(distinct_downloaded_pdf_sha256=len({hashlib.sha256(p.read_bytes()).hexdigest() for p in all_pdf_paths}),formal_publications_with_at_least_main_pdf=sum(p['is_formal_version'] for p in papers),formal_candidate_pdf_materials=sum(len(p.get('materials',[])) for p in papers if p['is_formal_version'] and p['recommendation'] in ['recommend','secondary']),individual_work_groups_excluding_withdrawn_and_edited_collections=len({p['duplicate_group'] for p in papers if p['status'] not in ['withdrawn_by_authors','edited_proceedings_html_not_individual_paper']}))
write('survey-qa.json',stats)
print(json.dumps(stats,ensure_ascii=False,indent=2))
