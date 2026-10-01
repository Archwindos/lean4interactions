/* Public formal sources only. Source text is always inserted through DOM text nodes. */
(function () {
  "use strict";
  const language = localStorage.getItem("proof-reader-language") === "en" ? "en" : "zh";
  window.READER_LANGUAGE = language;
  document.documentElement.lang = language === "en" ? "en" : "zh-CN";
  const selector = document.getElementById("language-select");
  selector.value = language;
  selector.addEventListener("change", () => {localStorage.setItem("proof-reader-language", selector.value); location.reload();});
  function overlay(base, en) {
    if (Array.isArray(base) && Array.isArray(en)) {
      if (base.length && base.every(x=>x && typeof x==="object" && x.id)) {
        const byId=new Map(en.map(x=>[x.id,x])); return base.map(x=>overlay(x,byId.get(x.id)||{}));
      }
      return en.map((x,i)=>overlay(base[i],x));
    }
    if (base && typeof base==="object" && en && typeof en==="object" && !Array.isArray(en)) {
      const result={...base}; for(const [key,value] of Object.entries(en))result[key]=overlay(base[key],value); return result;
    }
    return en;
  }
  function localized(value) {
    if(Array.isArray(value))return value.map(localized);
    if(value && typeof value==="object") {
      const base=Object.fromEntries(Object.entries(value).filter(([k])=>k!=="translations").map(([k,v])=>[k,localized(v)]));
      return language==="en" && value.translations && value.translations.en ? overlay(base,value.translations.en) : base;
    }
    return value;
  }
  const D = localized(window.READER_V2_DATA);
  const UI = {
    "论文与证明":"Papers and proofs", "论文":"Papers", "符号表":"Symbols", "给 AI 与维护者":"For AI and maintainers", "跳到正文":"Skip to content", "本次范围":"Current scope",
    "公开正式论文 · 中文证明阅读原型":"Published papers · Bilingual proof reader", "相关符号":"Related symbols", "全部论文":"All papers", "筛选论文":"Filter papers", "搜索符号或含义":"Search symbols or meanings", "搜索符号":"Search symbols", "没有匹配的符号。":"No matching symbols.",
    "原文":"Source", "中文重写":"Rewritten proof", "证明重写":"Rewritten proof", "完整证明":"Complete proof", "证明整理中":"Proof in progress", "原文与覆盖范围":"Source and coverage", "完整说明":"Complete explanation", "范围说明":"Scope explanation",
    "原命题有反例":"Counterexample to the original statement", "复合陈述中的一部分有反例":"A clause of the compound statement is refuted", "原陈述有反例记录，范围待核对":"Counterexample recorded; scope under review", "原等式待判定 · 分析子断言有反例":"Parent equation unassessed · counterexample to a subclaim", "定义、方法或经验材料":"Definitions, methods or empirical material", "定义、方法与实验":"Definitions, methods and experiments", "命题与推导":"Statements and derivations",
    "近似主张与适用条件":"Approximation claims and conditions", "已证明的子范围":"Proved subcomponent", "完整共享证明":"Complete shared proof", "共享证明":"Shared proof", "本篇适配":"Paper adaptation", "论文适配":"Paper adaptation", "条件与定义":"Conditions and definitions", "假设":"Assumptions", "定义":"Definitions", "证明范围":"Proof scope", "数学陈述":"Mathematical statement", "证明正文":"Proof text", "原命题":"Original statement", "原证明":"Original proof", "查看原文":"View source",
    "搜索本论文定理编号、标题或关键词":"Search theorem labels, titles or keywords in this paper", "搜索论文、定理编号或关键词":"Search papers, theorem labels or keywords", "搜索本论文":"Search this paper", "搜索论文与结果":"Search papers and results", "没有匹配条目。":"No matching entries.",
    "正式补充材料":"Formal supplement", "正式论文":"Formal paper", "返回论文列表":"Back to papers", "未找到这一阅读页":"Reading page not found", "阅读数据未能加载。":"Reading data did not load.", "Lean 对照已编译":"Lean comparison compiled", "尚未形式化":"Not formalized", "Lean 证据待更新":"Lean evidence is stale", "Lean 证据未取得":"Lean evidence unavailable", "分项Lean证据已验证":"Lean subcomponent verified", "反例已验证；其范围见下方":"Counterexample verified; see scope below",
    "反例的数学内容":"Counterexample", "原文问题":"Source issue", "完整核验记录 ↗":"Complete review record ↗", "核验数据 ↗":"Review data ↗", "使用这个符号的结果":"Results using this symbol", "相关公共定义 →":"Related public definition →", "域：":"Domain: ", "；作用域：":"; scope: ", "空集约定：":"Empty-set convention: ", "基线约定：":"Baseline convention: ", "对应关系：":"Correspondence: ", "Lean 定义： ":"Lean definition: ", "返回 ":"Back to ", "PDF 第 ":"PDF page ", " 页":"",
    "定义一致":"Same definition", "仅记号不同":"Renaming", "去输出基线的变体":"Centered variant", "由原定义导出":"Derived quantity", "定义或公式冲突":"Definition or formula conflict", "语义对齐说明":"Semantic alignment note", "定义关系待核对":"Definition relation under review",
    "按定义、域与作用域对照论文原符号。点击一行查看定义、空集约定与出处。":"Compare the original notation by definition, domain and scope. Open a row to inspect its definition, empty-set convention and sources."
  };
  Object.assign(UI,{"完整证明": "Complete proof", "完整说明": "Complete explanation", "证明整理中": "Proof in progress", "中文证明": "Proof", "中文说明": "Explanation", "证明与范围": "Proof and scope", "反例与说明": "Counterexample and explanation", "记号与条件": "Notation and conditions", "查看本证明的符号定义": "Definitions used in this proof", "命题": "Statement", "证明思路": "Proof idea", "查看 Lean 对照 ↗": "View Lean comparison ↗", "公共命题": "Shared statement", "公共证明的记号与条件": "Notation and conditions for the shared proof", "论文定义与公共证明的对应": "Paper definitions and shared-proof adaptation", "反例与原命题问题": "Counterexample and original-statement issue", "分项证明与问题": "Component proof and issues", "陈述与适用条件": "Statement and conditions", "已证明的范围": "Proved scope", "一个具体例子": "A concrete example", "本证明的适用范围": "Scope of this proof", "补充材料 ↗": "Supplement ↗", "正式论文 ↗": "Formal paper ↗", "本论文符号对照 →": "Notation for this paper →", "定义、假设、方法与实验（": "Definitions, assumptions, methods and experiments (", "项）": " items)", "原文核验范围": "Source-review scope", "核验说明": "Review explanation", "公共数学结果": "Shared mathematical result", "阅读内容": "Reading content", "← 论文目录": "← Paper directory", "下一结果": "Next result", "当前位置": "Current location", "继续阅读": "Continue reading", "原命题与反例": "Original statement and counterexample", "复合陈述中的问题": "Issue in a compound statement", "分析子断言有反例；父结论未判定": "Counterexample to an analysis subclaim; parent conclusion unassessed", "原文记号与适用范围": "Source notation and scope", "定义与算法的边界": "Definitions and algorithm boundaries", "原证明的错误步骤": "Incorrect step in the original proof"});
  Object.assign(UI,{
    "实际 Lean 类型":"Actual Lean type", "当前编译记录 · ":"Current compilation record · ", "验证报告 ↗":"Verification report ↗", "源码第 ":"Source line ", " 行 ↗":" ↗", "返回中文证明的这一步":"Return to this proof step", "此结果尚未提供已编译的 Lean 对照。":"A compiled Lean comparison is not available for this result.", "所列声明已编译；实际验证范围见下方类型与报告。":"The listed declarations compiled; the actual verification scope is shown by the types and reports below.", "本论文与 Lean 的逐步对应":"Paper steps and Lean declarations", "公共证明与 Lean 的逐步对应":"Shared-proof steps and Lean declarations", "对应步骤 ":"Corresponding step ", "该声明尚未取得当前编译报告、实际类型和源码位置；本步不宣称已形式化。":"A current compilation report, actual type and source location are not available for this declaration; this step does not claim formalization.", "对应的数学陈述":"Corresponding mathematical statement", "被检验的原陈述":"Original statement being checked", "原陈述与本次验证范围":"Original statement and verified scope", "反例针对的子断言":"Subclaim targeted by the counterexample", "实际反例命题：":"Actual counterexample statement: ", "错误子句的反例：":"Counterexample to the incorrect clause: ", "实际Lean类型：":"Actual Lean type: ", "实际反例命题与 Lean 类型":"Actual counterexample statement and Lean type", "实际分项命题与 Lean 类型":"Actual subcomponent statement and Lean type", "完整 Lean 类型陈述":"Full Lean type", "已编译的论文适配":"Compiled paper adapter", "论文适配源码":"Paper adapter source", "目前只有声明级对应，尚未给出逐步代码对照。":"Only declaration-level correspondence is available; a stepwise code comparison has not been supplied.", "Lean 源文件":"Lean source file", "编译与公理检查记录":"Compilation and axiom audit", "公共 Lean 源文件":"Shared Lean source file", "Lean 编码说明":"Lean encoding note", "反例检验的是下列分析子断言；上方父陈述的整体结论没有因此被判定为错误。":"This counterexample checks the analysis subclaim below; it does not classify the complete parent conclusion as false."
  });
  Object.assign(UI,{"论文概览":"Paper overview","本论文符号对照":"Notation for this paper","Lean 对照":"Lean comparison","论文目录":"Paper directory","论文与定理目录":"Paper and theorem directory","从论文，读到完整证明":"Read the complete proof behind each paper","阅读论文 →":"Read paper →","选择一篇正式论文，查看其中的命题、中英双语证明与 Lean 对照。采用规范符号，并保留论文原记号对照，把省略的推导逐步展开。":"Choose a formal paper to read its statements, bilingual proofs and Lean comparisons. Proofs use canonical notation and retain a comparison with the original paper notation, expanding omitted derivations step by step.","查看第 ":"View step "," 步的 Lean 对照":" in Lean","原文数学核验":"Source mathematics review","原文数学问题":"Source mathematical issues","部分范围的 Lean 证据通过":"Lean evidence verified for a partial scope","部分范围的 Lean 证据未取得":"Lean evidence unavailable for the partial scope"});
  Object.assign(UI,{"原文核验":"Source review"});
  function ui(value) {
    if(language!=="en" || typeof value!=="string")return value;
    if(UI[value])return UI[value];
    let result=value;for(const [zh,en] of Object.entries(UI).sort((a,b)=>b[0].length-a[0].length))if(result.includes(zh))result=result.split(zh).join(en);return result;
  }
  if(language==="en") {
    for(const node of document.querySelectorAll(".skip-link,.brand,#papers-nav,#symbols-nav,#about-nav,.site-footer span,.site-footer a")) {
      for(const text of Array.from(node.childNodes).filter(n=>n.nodeType===Node.TEXT_NODE))text.textContent=ui(text.textContent);
    }
  }
  const app = document.getElementById("app");
  window.READER_MATH_ERRORS = [];
  if (!D) { app.textContent = "阅读数据未能加载。"; return; }
  const papers = D.papers || [];
  const results = D.math.results || [];
  const sharedProofs = D.math.shared_proofs || [];
  const paperMap = new Map(papers.map(p => [p.id, p]));
  const resultMap = new Map(results.map(r => [r.id, r]));
  const sharedMap = new Map((Array.isArray(sharedProofs) ? sharedProofs : Object.values(sharedProofs)).map(p => [p.id, p]));
  const sources = new Map(papers.flatMap(p => p.sources || []).map(s => [s.id, s]));
  let currentResult = null;
  let currentShared = null;
  let activeTab = "rewrite";
  let activeStep = null;
  let renderedProofSteps = new Map();
  function stepIdentity(step){step=resolvedStep(step);return JSON.stringify([step.id,step.body_md,step.formula_tex]);}
  function commonProofUrl(proof){return '/proofs/'+encodeURIComponent(proof.id)+'/';}
  function sharedFor(result){return asList(result.shared_proof_ids||result.shared_proof_id).map(id=>sharedMap.get(id)).filter(Boolean);}
  function proofLocations(){
    const map=new Map();for(const [prefix,proof] of [['paper',currentResult],...sharedFor(currentResult).map((p,i)=>[i===0?'shared':'shared-'+i,p])]){
      asList(proof&&proof.proof_steps).forEach((raw,i)=>{const step=resolvedStep(raw),key=stepIdentity(step);if(!map.has(key))map.set(key,{id:stepAnchor(prefix,step.id,i),prefix,stepId:step.id});});
    }return map;
  }
  function resolvedStep(step,seen){
    const ref=step.shared_step_ref||step.result_step_ref;if(!ref)return step;
    seen=seen||new Set();const key=(ref.proof_id||ref.result_id)+':'+ref.step_id;if(seen.has(key))return step;seen.add(key);
    const proof=sharedMap.get(ref.proof_id)||resultMap.get(ref.result_id);const found=asList(proof&&proof.proof_steps).find(s=>s.id===ref.step_id);
    return found?{...resolvedStep(found,seen),id:step.id,title:step.title||found.title}:step;
  }

  function el(tag, text, attrs) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = ui(String(text));
    for (const [key, value] of Object.entries(attrs || {})) if (value !== undefined && value !== null) node.setAttribute(key, ui(String(value)));
    return node;
  }
  function a(text, href, attrs) { return el("a", text, {href, ...(attrs || {})}); }
  function paperUrl(id) { return "/papers/" + encodeURIComponent(id) + "/"; }
  function resultUrl(result) { return result.paper_id ? paperUrl(result.paper_id) + "results/" + encodeURIComponent(result.id) + "/" : "/library/" + encodeURIComponent(result.id) + "/"; }
  function asList(value) { return value === undefined || value === null ? [] : Array.isArray(value) ? value : [value]; }
  function textValue(value) { if (typeof value === "string") return value; if (!value) return ""; return value.text_md || value.body_md || value.text || value.label || value.explanation || value.title || ""; }
  function math(container) {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(container, {
      delimiters: [{left:"$$",right:"$$",display:true}, {left:"\\[",right:"\\]",display:true}, {left:"\\(",right:"\\)",display:false}, {left:"$",right:"$",display:false}],
      throwOnError:false, trust:false, strict:"ignore", ignoredClasses:["code-panel", "raw-source", "formula-fallback"],
      errorCallback:message => window.READER_MATH_ERRORS.push(String(message))
    });
  }
  function formula(tex, parent, display) {
    if (!tex) return;
    const node = el(display === false ? "span" : "div", null, {class:display === false ? "inline-formula" : "math-block"});
    parent.append(node);
    try { window.katex.render(String(tex), node, {displayMode:display !== false, throwOnError:true, trust:false, strict:"ignore"}); }
    catch (error) { node.textContent = String(tex); node.classList.add("formula-fallback"); window.READER_MATH_ERRORS.push(String(error)); }
  }
  function inline(text, parent) {
    // Support only safe prose formatting. Mathematical delimiters remain literal
    // until local KaTeX consumes them; arbitrary HTML never enters the document.
    const tokens = /(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^\s)]+\))/g;
    let offset = 0, match;
    while ((match = tokens.exec(String(text)))) {
      parent.append(document.createTextNode(String(text).slice(offset, match.index)));
      const token = match[0];
      if (token[0] === "`") parent.append(el("code", token.slice(1, -1)));
      else if (token.startsWith("**")) parent.append(el("strong", token.slice(2, -2)));
      else {
        const link = /^\[([^\]]+)\]\(([^)]+)\)$/.exec(token);
        if (link && /^(https?:\/\/|\/files\/|#)/.test(link[2])) parent.append(a(link[1], link[2], link[2].startsWith("http") ? {target:"_blank",rel:"noopener"} : {}));
        else parent.append(document.createTextNode(token));
      }
      offset = tokens.lastIndex;
    }
    parent.append(document.createTextNode(String(text).slice(offset)));
  }
  function markdown(text, parent) {
    text=String(text||"");
    if (!text) return;
    const blocks = String(text).replace(/\r\n/g,"\n").split(/\n\s*\n/);
    for (let block of blocks) {
      block = block.trim(); if (!block) continue;
      if (block.startsWith("```")) {
        const code = block.replace(/^```[^\n]*\n?/m, "").replace(/\n?```$/, "");
        parent.append(el("pre", code, {class:"code-panel"})); continue;
      }
      const heading = /^(#{1,6})\s+([\s\S]+)$/.exec(block);
      if (heading) { const h = el("h3", null, {class:"md-heading"}); inline(heading[2], h); parent.append(h); continue; }
      const lines = block.split("\n");
      if (lines.every(line => /^\s*(?:[-*]|\d+[.)])\s+/.test(line))) {
        const list = el(/^\s*\d+/.test(lines[0]) ? "ol" : "ul", null, {class:"markdown-list"});
        for (const line of lines) { const li = el("li"); inline(line.replace(/^\s*(?:[-*]|\d+[.)])\s+/, ""), li); list.append(li); }
        parent.append(list); continue;
      }
      const p = el("p"); inline(block, p); parent.append(p);
    }
    math(parent);
  }
  function paragraph(text, parent, attrs) { const p = el("p", null, attrs); inline(ui(String(text)), p); parent.append(p); math(p); return p; }
  function venueLabel(paper) { return paper.venue_label || (String(paper.venue||"").includes(String(paper.year)) ? paper.venue : [paper.venue, paper.year].filter(Boolean).join(" ")); }
  function shortTitle(paper) { return paper.short_title || paper.title; }
  function paperResults(paper) { return results.filter(r => r.paper_id === paper.id); }
  function isComplete(result) { return result.reading_status === "complete"; }
  function readingLabel(result) {
    if(result.rewrite_status==='complete_with_definition_only_counterexample')return result.scope_label||'显示定义版本的反例；最优选择版本未反驳';
    if(result.rewrite_status==='complete_with_original_domain_issue')return result.scope_label||'原定义域内证明与未定义范围说明';
    if(result.statement_assessment === 'refuted')return '原命题有反例';
    if(result.statement_assessment === 'partially_refuted')return '复合陈述中的一部分有反例';
    if(result.statement_assessment === 'counterexample_recorded')return '原陈述有反例记录，范围待核对';
    if(result.statement_assessment==='scope_under_review'&&asList(result.clause_assessments).some(c=>c.status==='refuted'))return '原等式待判定 · 分析子断言有反例';
    if(!result.proof_target)return '定义、方法或经验材料';
    if(result.rewrite_role==='statement_scope_explanation')return (result.scope_label||'近似主张与适用条件')+(result.reading_status==='scope_explanation_complete'?' · 完整说明':' · 范围说明');
    if(result.rewrite_role==='partial_component')return '已证明的子范围 · '+leanLabel(result.lean||{});
    return isComplete(result)?'完整证明 · '+leanLabel(result.lean||{}):result.rewrite_status==='in_progress'?'证明整理中':'原文与覆盖范围';
  }
  function resultGroup(result){return !result.proof_target?'定义、方法与实验':'命题与推导';}
  function searchLabels(result){
    const entries=asList(D.inventories).flatMap(i=>i.entries||[]).filter(e=>asList(result.inventory_ids).includes(e.id));
    return [result.title,result.original_label,...asList(result.aliases),...entries.flatMap(e=>[e.original_label,...asList(e.aliases)])].filter(Boolean);
  }
  function normalizedSearch(text){return String(text||'').toLowerCase().replace(/\s+/g,'');}
  function searchBox(parent,paper){
    const box=el('div',null,{class:'paper-search'});const input=el('input',null,{type:'search',placeholder:paper?'搜索本论文定理编号、标题或关键词':'搜索论文、定理编号或关键词','aria-label':paper?'搜索本论文':'搜索论文与结果'});const output=el('div',null,{class:'search-results',hidden:''});box.append(input,output);parent.append(box);
    input.addEventListener('input',()=>{output.replaceChildren();const query=normalizedSearch(input.value);output.hidden=!query;if(!query)return;
      if(!paper)for(const p of papers){if(normalizedSearch(p.title+' '+shortTitle(p)).includes(query)){const row=a('',paperUrl(p.id));row.append(el('span',venueLabel(p),{class:'search-source'}),el('strong',p.title));output.append(row);}}
      const found=results.filter(r=>(!paper||r.paper_id===paper.id)&&normalizedSearch(searchLabels(r).join(' ')).includes(query));
      for(const r of found){const p=paperMap.get(r.paper_id);const row=a('',resultUrl(r),{'data-search-result':r.id});row.append(el('span',[p&&venueLabel(p),r.original_label].filter(Boolean).join(' · '),{class:'search-source'}),el('strong',r.title));output.append(row);}if(!output.childNodes.length)paragraph('没有匹配条目。',output);
    });return input;
  }
  function relatedSymbols(result,parent){
    const ids=asList(result.symbol_ids);if(!ids.length)return;
    const row=el('div',null,{class:'related-symbols'});row.append(el('span','相关符号'));
    const known=D.symbols||[];
    for(const id of ids){const sym=known.find(s=>s.id===id||s.canonical_id===id);if(!sym)continue;const link=a('', '/symbols/?paper='+result.paper_id+'#'+encodeURIComponent(sym.canonical_id||sym.id));formula(sym.canonical_tex,link,false);link.setAttribute('title',sym.name_zh||sym.id);row.append(link);}
    parent.append(row);
  }
  function symbolsPage(){
    document.getElementById('symbols-nav').setAttribute('aria-current','page');
    const main=el('main',null,{class:'about-page symbols-page',id:'main',tabindex:'-1'});main.append(el('h1','符号表'));
    paragraph('按定义、域与作用域对照论文原符号。点击一行查看定义、空集约定与出处。',main);
    const controls=el('div',null,{class:'symbol-controls'});const select=el('select',null,{'aria-label':'筛选论文'});select.append(el('option','全部论文',{value:''}));for(const p of papers)select.append(el('option',shortTitle(p),{value:p.id}));select.value=new URLSearchParams(location.search).get('paper')||'';
    const search=el('input',null,{type:'search',placeholder:'搜索符号或含义','aria-label':'搜索符号'});controls.append(select,search);main.append(controls);const body=el('div',null,{class:'symbols-list'});main.append(body);
    const labels={same_definition:'定义一致',renaming:'仅记号不同',centered_variant:'去输出基线的变体',derived_quantity:'由原定义导出',conflict:'定义或公式冲突',pending_alignment:'语义对齐说明'};
    function draw(){body.replaceChildren();const query=search.value.toLowerCase();const list=(D.symbols||[]).filter(s=>(!select.value||asList(s.paper_mappings).some(m=>m.paper_id===select.value))&&JSON.stringify(s).toLowerCase().includes(query));
      for(const sym of list){const card=el('details',null,{class:'symbol-card',id:sym.canonical_id||sym.id});const summary=el('summary');const glyph=el('span',null,{class:'symbol-glyph'});formula(sym.canonical_tex,glyph,false);summary.append(glyph,el('span',sym.name_zh||sym.id,{class:'symbol-name'}));const names=[...new Set(asList(sym.paper_mappings).map(m=>shortTitle(paperMap.get(m.paper_id)||{title:m.paper_id})))];summary.append(el('span',names.join(' · '),{class:'symbol-papers'}));card.append(summary);
        const detail=el('div',null,{class:'symbol-detail'});formula(sym.definition_tex,detail);markdown(sym.description_md,detail);paragraph('域：'+textValue(sym.type_or_domain)+'；作用域：'+textValue(sym.scope),detail,{class:'source-notes'});
        if(sym.parent_concept_id)detail.append(a('相关公共定义 →','/symbols/#'+sym.parent_concept_id,{class:'source-link'}));
        if(sym.empty_set_convention)markdown('空集约定：'+sym.empty_set_convention,detail);if(sym.baseline_convention)markdown('基线约定：'+sym.baseline_convention,detail);
        for(const map of asList(sym.paper_mappings).filter(m=>!select.value||m.paper_id===select.value)){const p=paperMap.get(map.paper_id);const row=el('div',null,{class:'symbol-mapping'});row.append(el('h3',p?shortTitle(p):map.paper_id));if(/无独立原符号|no separate|same as/i.test(map.original_tex||''))paragraph(map.original_tex,row);else formula(map.original_tex,row,false);formula(map.original_definition_tex,row);paragraph('对应关系：'+(labels[map.relation_type]||'定义关系待核对'),row,{class:'source-notes'});if(map.conflict_note)markdown(map.conflict_note,row);sourceLinks({source_refs:[{source_id:map.source_id,locations:asList(map.pdf_pages).map(n=>({pdf_page:n,label:'PDF 第 '+n+' 页'}))}]},row);detail.append(row);}
        const used=results.filter(r=>asList(r.symbol_ids).includes(sym.id));if(used.length){detail.append(el('h3','使用这个符号的结果'));const links=el('div',null,{class:'symbol-results'});for(const r of used)links.append(a(r.title,resultUrl(r)));detail.append(links);}
        if(asList(sym.lean_names).length){const names=el('p',null,{class:'source-notes'});names.append(document.createTextNode('Lean 定义： '));for(const name of sym.lean_names)names.append(el('code',name));detail.append(names);}card.append(detail);body.append(card);}
      math(body);if(!list.length)paragraph('没有匹配的符号。',body);
      if(location.hash){const selected=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(selected){selected.open=true;setTimeout(()=>selected.scrollIntoView({block:'start'}),0);}}
    }select.addEventListener('change',()=>{history.replaceState(null,'','/symbols/'+(select.value?'?paper='+select.value:''));draw();});search.addEventListener('input',draw);window.addEventListener('hashchange',draw);app.append(main);draw();
  }
  function sourceLabel(source) { return source.label || (source.kind === "supplement" ? "正式补充材料" : "正式论文"); }
  function sourceHref(source, page) { return source.public_path + (page ? "#page=" + page : ""); }
  function referenceSource(ref) { return sources.get(typeof ref === "string" ? ref : ref.source_id || ref.id); }
  function referenceLocations(ref) {
    if (typeof ref === "string") return [];
    if (ref.locations) return asList(ref.locations);
    if (ref.location) return asList(ref.location);
    return [ref];
  }
  function locationLabel(location) {
    if (typeof location === "string") return location;
    return location.label || location.description || [location.section, location.theorem, location.pdf_page ? "PDF 第 " + location.pdf_page + " 页" : location.page ? "第 " + location.page + " 页" : ""].filter(Boolean).join(" · ");
  }
  function sourceLinks(result, parent, purpose) {
    const row = el("div", null, {class:"source-links"});
    const seen = new Set();
    for (const ref of result.source_refs || []) {
      const source = referenceSource(ref); if (!source || !source.public_path) continue;
      let locations = referenceLocations(ref);
      if (purpose && locations.some(x => typeof x === "object" && (x.role || x.kind || x.purpose))) {
        const selected = locations.filter(x => typeof x === "string" || String(x.role || x.kind || x.purpose).includes(purpose));
        if (!selected.length) continue;
        locations = selected;
      }
      if (!locations.length) locations = [{}];
      for (const location of locations) {
        const page = typeof location === "object" ? location.pdf_page || location.page || asList(location.pdf_pages)[0] : null;
        const label = locationLabel(location);
        const href = sourceHref(source, page);
        const key = href + label; if (seen.has(key)) continue; seen.add(key);
        row.append(a(sourceLabel(source) + (label ? " · " + label : "") + " ↗", href, {class:"source-link",target:"_blank",rel:"noopener"}));
      }
    }
    if (row.childNodes.length) parent.append(row);
  }
  function resultNumber(result, paper) {
    const descriptor = paper && asList(paper.results).find(r => r.id === result.id);
    return result.original_number || result.source_label || (descriptor && (descriptor.original_number || descriptor.source_label || descriptor.number)) || String(result.original_label||'').split(';')[0] || (paper && /^[^：:]+[：:]/.test(result.title) ? result.title.split(/[：:]/)[0] : "");
  }
  function directoryTitle(result,paper){const number=resultNumber(result,paper);if(number&&result.title.startsWith(number)&&/^[：:]/.test(result.title.slice(number.length)))return result.title.slice(number.length+1).trim();return result.title;}
  function leanLabel(lean) {
    if (!lean) return "尚未形式化";
    return lean.label || (["verified","compiled","passed"].includes(lean.status) ? "Lean 对照已编译" : "尚未形式化");
  }
  function getLean(result, shared) { return result.lean || (shared && shared.lean) || {}; }
  function home() {
    document.getElementById("papers-nav").setAttribute("aria-current","page");
    const main = el("main", null, {class:"home",id:"main",tabindex:"-1"});
    const head = el("div", null, {class:"home-head"});
    head.append(el("p","READ THE PROOF",{class:"eyebrow"}),el("h1","从论文，读到完整证明"));
    paragraph("选择一篇正式论文，查看其中的命题、中英双语证明与 Lean 对照。采用规范符号，并保留论文原记号对照，把省略的推导逐步展开。",head,{class:"intro"}); main.append(head);
    searchBox(main);const list = el("div", null, {class:"paper-list"});
    for (const paper of papers) {
      const row = el("article", null, {class:"paper-row","data-paper":paper.id});
      row.append(el("div",venueLabel(paper),{class:"venue"}));
      const content = el("div"); const h = el("h2"); h.append(a(paper.title,paperUrl(paper.id))); content.append(h);
      paragraph(paper.intro || paper.description || paper.summary || "",content,{class:"paper-description"});
      row.append(content,a("阅读论文 →",paperUrl(paper.id),{class:"read-link"}));list.append(row);
    }
    main.append(list);
    paragraph(language==='en'?`The directory covers ${D.papers.length} formal papers, including main text, appendices and supplements. Each result records the scope of its source, rewritten proof and Lean evidence.`:`目录覆盖 ${D.papers.length} 篇正式论文的正文、附录与补充材料。每条独立说明原文整理、重写证明与 Lean 的实际范围。`,main,{class:"home-note"});
    app.append(main);
  }
  function shell(paper, result) {
    const wrapper = el("div", null, {class:"reader-shell"});
    const sidebar = el("aside", null, {class:"sidebar","aria-label":"论文与定理目录"});
    const selector = el("details", null, {class:"paper-selector",id:"paper-selector"});
    const summary = el("summary"); const summaryText = el("span",shortTitle(paper)); summaryText.append(el("span",venueLabel(paper),{class:"current-venue"})); summary.append(summaryText);selector.append(summary);
    const options = el("div", null, {class:"paper-options"});
    for (const p of papers) { const link = a(shortTitle(p),paperUrl(p.id),{"aria-current":p.id === paper.id ? "page" : null});link.append(el("small",venueLabel(p)));options.append(link); }
    selector.append(options);sidebar.append(selector);
    const toggle = el("button","论文目录",{type:"button",class:"directory-toggle",id:"directory-toggle","aria-expanded":"false","aria-controls":"directory"});toggle.append(el("span","⌄",{"aria-hidden":"true"}));sidebar.append(toggle);
    const directory = el("nav", null, {class:"directory",id:"directory","aria-label":"论文目录"});
    directory.append(a("论文概览",paperUrl(paper.id),{"aria-current":result ? null : "page"}));
    directory.append(a("本论文符号对照","/symbols/?paper="+paper.id));
    for(const label of ['命题与推导','定义、方法与实验']){
      const grouped=paperResults(paper).filter(r=>resultGroup(r)===label);if(!grouped.length)continue;
      let target=directory;
      if(label==='定义、方法与实验'){target=el('details',null,{class:'directory-extra'});target.append(el('summary',label));directory.append(target);}else directory.append(el("p",label,{class:"directory-label"}));
      for (const r of grouped) { const link = a("",resultUrl(r),{"data-result":r.id,"aria-current":result && result.id === r.id ? "page" : null});const number=resultNumber(r,paper);if(number)link.append(el("span",number,{class:"theorem-number"}));link.append(el("span",directoryTitle(r,paper)));target.append(link); }
    }
    sidebar.append(directory);
    const sideSources=el("div",null,{class:"side-sources"});for(const source of paper.sources || [])sideSources.append(a(source.kind === "supplement" ? "补充材料 ↗" : "正式论文 ↗",sourceHref(source),{target:"_blank",rel:"noopener"}));sidebar.append(sideSources);
    toggle.addEventListener("click",()=>{const open=toggle.getAttribute("aria-expanded")!=="true";toggle.setAttribute("aria-expanded",String(open));directory.classList.toggle("mobile-open",open);});
    const main = el("main",null,{class:"reader-main",id:"main",tabindex:"-1"});
    const breadcrumb=el("nav",null,{class:"breadcrumb","aria-label":"当前位置"});breadcrumb.append(a("论文", "/"),el("span","/",{"aria-hidden":"true"}),a(shortTitle(paper),paperUrl(paper.id)));
    if(result)breadcrumb.append(el("span","/",{"aria-hidden":"true"}),el("span",resultNumber(result,paper)||"证明"));main.append(breadcrumb);
    wrapper.append(sidebar,main);app.append(wrapper);return main;
  }
  function paperPage(paper) {
    const main=shell(paper);
    main.append(el("p",venueLabel(paper),{class:"eyebrow"}),el("h1",paper.title,{class:"paper-title"}));
    if(paper.authors&&paper.authors.length)paragraph(asList(paper.authors).map(textValue).join(" · "),main,{class:"paper-authors"});
    paragraph(paper.intro||paper.description||paper.summary||"",main,{class:"paper-abstract"});
    const pdfs=el("div",null,{class:"source-links"});for(const source of paper.sources||[])pdfs.append(a(sourceLabel(source)+" ↗",sourceHref(source),{class:"source-link",target:"_blank",rel:"noopener"}));main.append(pdfs);
    paragraph(paper.scope||"正文与附录的全部数学清单；各条实际完成范围分别记录。",main,{class:"scope-note"});
    const tools=el('div',null,{class:'directory-tools'});tools.append(a('本论文符号对照 →','/symbols/?paper='+paper.id));main.append(tools);
    searchBox(main,paper);const list=el("div",null,{class:"result-list"});const extra=el('details',null,{class:'source-entry-list'});extra.append(el('summary','定义、假设、方法与实验（'+paperResults(paper).filter(r=>!r.proof_target).length+'项）'));const extraList=el('div',null,{class:'result-list'});extra.append(extraList);
    for(const result of paperResults(paper)){
      const link=a("",resultUrl(result),{"data-result":result.id});const number=resultNumber(result,paper);if(number)link.append(el("span",number,{class:"result-number"}));
      link.append(el("h2",directoryTitle(result,paper)));link.append(el("span",readingLabel(result),{class:"result-blurb"}));(result.proof_target?list:extraList).append(link);
    }
    main.append(list,extra);
  }
  function conditions(result, parent, title) {
    const assumptions=asList(result.assumptions),definitions=asList(result.definitions);
    if(!assumptions.length&&!definitions.length)return;
    const section=el("section",null,{class:"notation-section"});section.append(el("h2",title||"记号与条件"));
    const shared=definitions.filter(item=>item&&item.definition_origin==='symbol_registry');
    const local=definitions.filter(item=>!shared.includes(item));
    function appendItem(item,target,isAssumption){const block=el("div",null,{class:isAssumption?"condition":"definition-item"});markdown(textValue(item),block);for(const tex of asList(item.formula_tex))formula(tex,block);target.append(block);}
    for(const item of assumptions)appendItem(item,section,true);
    for(const item of local)appendItem(item,section,false);
    if(shared.length){const details=el('details',null,{class:'proof-symbol-definitions'});details.append(el('summary','查看本证明的符号定义'));for(const item of shared)appendItem(item,details,false);section.append(details);}
    parent.append(section);
  }
  function statement(result,parent,label) {
    const block=el("section",null,{class:"statement-block"});block.append(el("p",label||"命题",{class:"section-label"}));
    markdown(result.statement_md||result.statement_zh_md||"",block);for(const tex of asList(result.display_statement_tex||result.statement_tex))formula(tex,block);
    parent.append(block);
  }
  function overview(result,parent) {
    if(!result.overview)return;
    const box=el("section",null,{class:"proof-idea"});box.append(el("h2","证明思路"));for(const text of asList(result.overview))markdown(textValue(text),box);parent.append(box);
  }
  function stepAnchor(prefix,id,index) { return prefix+"-"+String(id||index+1).replace(/[^a-zA-Z0-9_-]/g,"-"); }
  function proofSteps(proof,parent,prefix,title) {
    const steps=asList(proof.proof_steps);if(!steps.some(s=>!renderedProofSteps.has(stepIdentity(s))))return;
    if(title)parent.append(el("h2",title,{class:"complete-proof-heading"}));
    steps.forEach((step,index)=>{
      step=resolvedStep(step);const identity=stepIdentity(step);if(renderedProofSteps.has(identity))return;
      const id=stepAnchor(prefix,step.id,index);const section=el("section",null,{class:"proof-step",id,"data-step-id":step.id||index+1,"data-proof-prefix":prefix});
      renderedProofSteps.set(identity,{id,prefix,stepId:step.id});
      const head=el("h3");head.append(el("span",index+1,{class:"step-number"}),el("span",step.title||"",{class:"step-title"}));section.append(head);
      markdown(step.body_md||step.body||"",section);for(const tex of asList(step.formula_tex))formula(tex,section);
      if(step.justification){const note=el("div",null,{class:"justification"});markdown(textValue(step.justification),note);section.append(note);}
      if(asList(step.lean_refs).length || matchingStepMap(step.id,prefix).length){const button=el("button","查看 Lean 对照 ↗",{type:"button",class:"step-to-lean","aria-label":"查看第 "+(index+1)+" 步的 Lean 对照"});button.addEventListener("click",()=>{activeStep={id:String(step.id||index+1),prefix,anchor:id};setTab("lean");const match=document.querySelector('.lean-map[data-step-id="'+CSS.escape(activeStep.id)+'"]');if(match)match.scrollIntoView({block:"start"});});section.append(button);}
      parent.append(section);
    });
  }
  function matchingStepMap(stepId,prefix) {
    const common=prefix.startsWith('shared')?sharedFor(currentResult)[prefix==='shared'?0:Number(prefix.slice(7))]:null;
    const lean=common?common.lean:getLean(currentResult,currentShared);
    return asList(lean&&lean.step_map).filter(item=>String(item.step_id||item.id||item.proof_step_id)===String(stepId));
  }
  function caveats(result,parent) {
    const items=asList(result.caveats);if(!items.length)return;
    const detail=el("details",null,{class:"caveats"});detail.append(el("summary","本证明的适用范围"));const body=el("div",null,{class:"caveat-body"});for(const item of items)markdown(textValue(item),body);detail.append(body);parent.append(detail);
  }
  function relatedPapers(result,parent) {
    if(!result.shared_proof_id)return;
    const related=results.filter(r=>r.id!==result.id&&r.paper_id&&r.shared_proof_id===result.shared_proof_id);
    if(!related.length)return;
    const text=el("p",null,{class:"shared-intro"});text.append(document.createTextNode("另见这些论文： "));
    for(const r of related){const p=paperMap.get(r.paper_id);if(p)text.append(a(venueLabel(p)+" · "+shortTitle(p),resultUrl(r)));}parent.append(text);
  }
  function rewritePanel() {
    renderedProofSteps = new Map();
    const parent=el("div",null,{class:"proof-prose"});
    statement(currentResult,parent);
    conditions(currentResult,parent);
    overview(currentResult,parent);
    proofSteps(currentResult,parent,"paper",currentResult.rewrite_role==='counterexample'?'反例与原命题问题':currentResult.rewrite_role==='partial_proof_with_refuted_clause'?'分项证明与问题':currentResult.rewrite_role==='statement_scope_explanation'?'陈述与适用条件':currentResult.rewrite_role==='partial_component'?'已证明的范围':currentShared ? "论文定义与公共证明的对应" : "完整证明");
    const sharedList=asList(currentResult.shared_proof_ids||currentResult.shared_proof_id).map(id=>sharedMap.get(id)).filter(Boolean);
    for(const [index,shared] of sharedList.entries()){
      if(!asList(shared.proof_steps).some(s=>!renderedProofSteps.has(stepIdentity(s)))){const p=el('p',null,{class:'shared-intro'});p.append(a((shared.title||'公共证明')+'（本页已展开） ↗',commonProofUrl(shared)));parent.append(p);continue;}
      parent.append(el("h2",shared.title||"公共证明",{class:"shared-proof-heading"}));
      statement(shared,parent,"公共命题");conditions(shared,parent,"公共证明的记号与条件");overview(shared,parent);proofSteps(shared,parent,index===0?'shared':'shared-'+index,"完整证明");
    }
    const example=currentResult.example_md || (currentShared&&currentShared.example_md);
    if(example){const section=el("section",null,{class:"example"});section.append(el("h3","一个具体例子"));markdown(example,section);parent.append(section);}
    caveats(currentResult,parent);relatedPapers(currentResult,parent);return parent;
  }
  function issueNote(result,parent) {
    for(const issue of asList(result.issues||result.issue_refs)){
      if(!issue||typeof issue!=="object")continue;
      const text=issue.text_md||issue.summary||issue.title;if(!text)continue;
      if(issue.classification === "source_proof_step_issue"&&Array.isArray(issue.affected_result_ids)&&!issue.affected_result_ids.includes(result.id)){const p=el("p",null,{class:"source-notes"});if(issue.public_path)p.append(a("完整 AND/OR 定理的原证明另有核验记录 ↗",issue.public_path,{class:"source-link",target:"_blank",rel:"noopener"}));parent.append(p);continue;}
      const box=el("div",null,{class:issue.classification === "notation_alignment_note"?"source-notes":"error-message"});markdown(text,box);
      if(issue.public_path)box.append(a("查看原文核验记录 ↗",issue.public_path,{class:"source-link",target:"_blank",rel:"noopener"}));parent.append(box);
    }
  }
  function originalPanel(proof) {
    const parent=el("div",null,{class:"proof-prose"});
    const value=proof ? currentResult.original_proof_md : currentResult.original_statement_md;
    const note=proof ? currentResult.original_proof_note : currentResult.original_statement_note;
    paragraph(note||(proof?"下文是原证明推导的中文说明；原文请查看对应的正式 PDF 或展开原文页。":"下文呈现原命题的公式与中文说明；正式原文请查看对应 PDF 或展开原文页。"),parent,{class:"source-notes"});
    const dedicatedProof=asList(currentResult.source_refs).some(ref=>referenceLocations(ref).some(loc=>loc.role==='proof'));
    if(proof&&!dedicatedProof)paragraph(language==='en'?'No separate proof page is inventoried for this item. The linked formal PDF pages give the statement or derivation context.':'本条未登记独立的原证明页。下列正式 PDF 位置提供命题或推导上下文。',parent,{class:'source-notes'});
    sourceLinks(currentResult,parent,proof&&dedicatedProof?"proof":"statement");
    if(proof||!isComplete(currentResult))issueNote(currentResult,parent);
    sourcePageImages(currentResult,parent,proof&&dedicatedProof?"proof":"statement");
    if(value){const section=el("section",null,{class:"original-section"});section.append(el("h2",proof?(currentResult.original_proof_heading||"原证明数学内容与译文"):(currentResult.original_statement_heading||"原命题数学内容与译文")));
      if(String(value).includes('```text')){paragraph('精确数学转录正在整理；下方原始抽取仅作辅助，请对照上方正式PDF页。',section,{class:'source-notes'});const details=el('details',null,{class:'raw-extraction'});details.append(el('summary','辅助：原始文本抽取'));const raw=el('div');markdown(value,raw);details.append(raw);section.append(details);}
      else markdown(value,section);parent.append(section);}
    else paragraph("本页未转录这一部分的完整原文，请查看上方正式 PDF 的对应位置。",parent,{class:"source-notes"});
    for(const asset of (D.formula_transcripts||{})[currentResult.paper_id]||[]){const details=el("details",null,{class:"lean-details original-tex"});details.append(el("summary","查看选定公式的 TeX 转录"));const body=el("div");paragraph("按正式 PDF 核对的公式摘录，含命题与证明片段；这是项目转录，未取得作者 TeX 源码。",body,{class:"source-notes"});body.append(a("下载公式转录 TeX ↗",asset.public_path,{class:"source-link",target:"_blank",rel:"noopener"}),el("pre",asset.raw_text,{class:"code-panel raw-source"}));details.append(body);parent.append(details);}
    return parent;
  }
  function sourcePageImages(result,parent,purpose){
    const images=[];const seen=new Set();
    for(const ref of result.source_refs||[]){const source=referenceSource(ref);if(!source)continue;for(const location of referenceLocations(ref)){
      if(typeof location!=="object"||location.role&&location.role!==purpose)continue;const page=location.pdf_page||location.page;const path=source.page_images&&source.page_images[String(page)];if(!path||seen.has(path))continue;seen.add(path);images.push({source,page,path});
    }}
    if(!images.length)return;
    const details=el("details",null,{class:"original-pages"});details.append(el("summary","查看正式 PDF 原文页（"+images.length+" 页）"));
    for(const {source,page,path} of images){const figure=el("figure");const caption=el("figcaption");caption.append(a(sourceLabel(source)+" · PDF 第 "+page+" 页 ↗",sourceHref(source,page),{target:"_blank",rel:"noopener"}));figure.append(caption,el("img",null,{src:path,alt:sourceLabel(source)+" PDF 第 "+page+" 页原文",loading:"lazy"}));details.append(figure);}parent.append(details);
  }
  function code(value,parent) { if(!value)return;const pre=el("pre",null,{class:"code-panel"});pre.append(el("code",String(value)));parent.append(pre); }
  function leanStatement(lean,parent,result) {
    const role=lean.evidence_role||result.verification_role;
    const statementBlock=el("section",null,{class:"lean-statement"});statementBlock.append(el("h2",role==='counterexample'?'被检验的原陈述':role==='partial_component'?'原陈述与本次验证范围':'对应的数学陈述'));
    const tex=lean.display_statement_tex||lean.statement_tex||result.display_statement_tex||result.statement_tex;for(const item of asList(tex))formula(item,statementBlock);markdown(lean.statement_md||"",statementBlock);parent.append(statementBlock);
    if(result.rewrite_status==='complete_with_definition_only_counterexample')paragraph(language==='en'?'This counterexample targets a decomposition allowed by the displayed definition; it does not refute the global optimal-selection version.':'反例针对显示定义允许的分解；全局最优选解版本尚未判定。',statementBlock,{class:'source-notes'});
    else if(role==='counterexample'&&result.statement_assessment!=='refuted')paragraph('反例检验的是下列分析子断言；上方父陈述的整体结论没有因此被判定为错误。',statementBlock,{class:'source-notes'});
    if(role==='counterexample'&&(result.analysis_clause_tex||lean.counterexample_statement_tex)){statementBlock.append(el('h3','反例针对的子断言'));formula(result.analysis_clause_tex||lean.counterexample_statement_tex,statementBlock);}
  }
  function leanMap(lean,parent,prefix,proof) {
    const locations=proofLocations();const map=asList(lean.step_map).filter(item=>{const step=asList(proof.proof_steps).find(s=>String(s.id)===String(item.step_id||item.proof_step_id||item.id));if(!step)return true;const where=locations.get(stepIdentity(step));return !where||where.prefix===prefix;});if(!map.length)return;
    parent.append(el("h2",prefix === "shared" ? "公共证明与 Lean 的逐步对应" : "本论文与 Lean 的逐步对应"));
    map.forEach((item,index)=>{
      const stepId=String(item.step_id||item.proof_step_id||item.id||index+1);
      const section=el("section",null,{class:"lean-map","data-step-id":stepId,"data-proof-prefix":prefix,id:"lean-"+prefix+"-"+stepId});
      const step=asList(proof.proof_steps).find(s=>String(s.id)===stepId);
      section.append(el("h3",item.title||step&&step.title||"对应步骤 "+(index+1)));
      markdown(item.explanation_md||item.explanation||item.text_md||item.description||"",section);
      if(item.declaration){const declaration=el("p",null,{class:"lean-declarations"});declaration.append(el("code",asList(item.declaration).join(", ")));section.append(declaration);}
      if(item.signature){paragraph('实际 Lean 类型',section,{class:'source-notes'});code(item.signature,section);}
      code(item.lean_excerpt||item.lean_code||item.code||"",section);
      if(item.evidence_status==='current'){const provenance=el('p',null,{class:'source-notes'});provenance.append(document.createTextNode(ui('当前编译记录 · ')));if(item.public_report_path)provenance.append(a('验证报告 ↗',item.public_report_path,{target:'_blank',rel:'noopener'}));if(item.public_source_path)provenance.append(document.createTextNode(' · '),a('源码第 '+item.line+' 行 ↗',item.public_source_path,{target:'_blank',rel:'noopener'}));section.append(provenance);}
      else paragraph('该声明尚未取得当前编译报告、实际类型和源码位置；本步不宣称已形式化。',section,{class:'source-notes'});
      const button=el("button","返回中文证明的这一步",{type:"button",class:"step-to-lean return-step"});button.addEventListener("click",()=>{const where=step&&proofLocations().get(stepIdentity(step));setTab("rewrite");const target=document.getElementById(where?where.id:stepAnchor(prefix,stepId,index));if(target){target.scrollIntoView({block:"start"});target.setAttribute("tabindex","-1");target.focus({preventScroll:true});}});section.append(button);parent.append(section);
    });
  }
  function leanPanel() {
    const parent=el("div");const lean=getLean(currentResult,currentShared);
    const intro=el("div",null,{class:"lean-intro"});intro.append(el("h2",leanLabel(lean)));markdown(ui(lean.scope||(lean.compiled?"所列声明已编译；实际验证范围见下方类型与报告。":"此结果尚未提供已编译的 Lean 对照。")),intro);parent.append(intro);
    leanStatement(lean,parent,currentResult);
    const declarations=asList(lean.declarations);
    if(declarations.length){const row=el("div",null,{class:"lean-declarations"});for(const declaration of declarations)row.append(el("code",typeof declaration === "string" ? declaration : declaration.name||declaration.declaration||""));parent.append(row);}
    for(const decl of asList(lean.actual_declarations)){const details=el('details',null,{class:'lean-details actual-declaration'});details.append(el('summary',(lean.evidence_role==='counterexample'?'实际反例命题：':lean.evidence_components&&asList(lean.evidence_components.counterexample_clauses).includes(decl.name)?'错误子句的反例：':'实际Lean类型：')+decl.name));const body=el('div');code(decl.signature,body);details.append(body);parent.append(details);}
    if(lean.statement){const details=el("details",null,{class:"lean-details"});details.append(el("summary",lean.evidence_role==='counterexample'?'实际反例命题与 Lean 类型':lean.evidence_role==='partial_component'?'实际分项命题与 Lean 类型':'完整 Lean 类型陈述'));const body=el("div");code(lean.statement,body);details.append(body);parent.append(details);}
    if(lean.adapter_code){parent.append(el("h3",lean.compiled?"已编译的论文适配":"论文适配源码"));code(lean.adapter_code,parent);}
    leanMap(lean,parent,"paper",currentResult);
    sharedFor(currentResult).forEach((shared,index)=>{const sharedLean=shared.lean;if(sharedLean)leanMap(sharedLean,parent,index===0?'shared':'shared-'+index,shared);});
    if(!asList(lean.step_map).length&&!(currentShared&&asList(currentShared.lean&&currentShared.lean.step_map).length)){paragraph("目前只有声明级对应，尚未给出逐步代码对照。",parent,{class:"source-notes"});}
    const evidence=el("div",null,{class:"lean-evidence"});
    for(const item of [lean.public_source_path&&{path:lean.public_source_path,label:"Lean 源文件"},lean.public_report_path&&{path:lean.public_report_path,label:"编译与公理检查记录"},currentShared&&currentShared.lean&&currentShared.lean.public_source_path&&{path:currentShared.lean.public_source_path,label:"公共 Lean 源文件"}].filter(Boolean))evidence.append(a(item.label+" ↗",item.path,{target:"_blank",rel:"noopener"}));
    parent.append(evidence);
    if(lean.encoding_note){const details=el("details",null,{class:"lean-details"});details.append(el("summary","Lean 编码说明"));const body=el("div");markdown(lean.encoding_note,body);details.append(body);parent.append(details);}
    return parent;
  }
  function scopePanel(){
    const parent=el("div",null,{class:"proof-prose"});parent.append(el("h2","原文核验范围"));
    markdown(currentResult.overview||"本条已纳入全篇清单；原文整理、中文重写与形式化的交付状态分别记录。",parent);
    if(currentResult.source_material_summary_md)markdown(currentResult.source_material_summary_md,parent);
    issueNote(currentResult,parent);sourceLinks(currentResult,parent);caveats(currentResult,parent);
    return parent;
  }
  function setTab(tab,focus) {
    activeTab=tab;
    for(const button of document.querySelectorAll(".tab")){const selected=button.dataset.tab===tab;button.setAttribute("aria-selected",String(selected));button.setAttribute("tabindex",selected?"0":"-1");}
    const panel=document.getElementById("reader-panel");panel.replaceChildren();panel.setAttribute("aria-labelledby","tab-"+tab);
    panel.append(tab === "rewrite" ? rewritePanel() : tab === "statement" ? originalPanel(false) : tab === "original-proof" ? originalPanel(true) : tab === "scope" ? scopePanel() : leanPanel());
    if(focus)document.getElementById("tab-"+tab).focus();
    const fragment=tab === "rewrite" ? "" : "#"+tab;history.replaceState(null,"",location.pathname+fragment);
  }
  function resultPage(result) {
    currentResult=result;currentShared=sharedMap.get(result.shared_proof_id)||null;
    const paper=paperMap.get(result.paper_id);let main;
    if(paper)main=shell(paper,result);else{main=el("main",null,{class:"about-page",id:"main",tabindex:"-1"});main.append(el("nav",null,{class:"breadcrumb"}));main.firstChild.append(a("论文","/"),el("span","/"),el("span","公共数学结果"));app.append(main);}
    const head=el("header",null,{class:"result-head"});const number=resultNumber(result,paper);if(number&&!result.title.startsWith(number))head.append(el("p",number,{class:"eyebrow"}));head.append(el("h1",result.title));
    const meta=el("div",null,{class:"result-meta"});if(paper)meta.append(el("span",venueLabel(paper)));meta.append(el("span",readingLabel(result)));head.append(meta);main.append(head);
    relatedSymbols(result,main);
    const tabs=el("div",null,{class:"tabs",role:"tablist","aria-label":"阅读内容"});
    const hasText=asList(result.proof_steps).length>0;
    const labels=result.is_shared_proof?[["rewrite","完整证明"],["lean","Lean 对照"]]:hasText?[["rewrite",result.rewrite_role==='statement_scope_explanation'?'中文说明':result.rewrite_role==='partial_component'||result.rewrite_role==='partial_proof_with_refuted_clause'?'证明与范围':result.rewrite_role==='counterexample'?'反例与说明':'中文证明'],["statement","原命题"],["original-proof","原证明"],["lean","Lean 对照"]]:[["statement","原命题"],["original-proof","原证明"],["scope","核验说明"]];
    labels.forEach(([id,label],index)=>{
      const button=el("button",label,{type:"button",role:"tab",class:"tab",id:"tab-"+id,"data-tab":id,"aria-controls":"reader-panel","aria-selected":"false",tabindex:"-1"});
      button.addEventListener("click",()=>setTab(id));button.addEventListener("keydown",event=>{if(!["ArrowLeft","ArrowRight","Home","End"].includes(event.key))return;event.preventDefault();const next=event.key === "Home" ? 0 : event.key === "End" ? labels.length-1 : (index+(event.key === "ArrowRight" ? 1 : -1)+labels.length)%labels.length;setTab(labels[next][0],true);});tabs.append(button);
    });
    main.append(tabs,el("section",null,{id:"reader-panel",class:"reading-panel",role:"tabpanel",tabindex:"0"}));
    const requested=location.hash.slice(1);setTab(labels.some(([id])=>id===requested)?requested:labels[0][0]);
    const next=el("nav",null,{class:"next-result","aria-label":"继续阅读"});
    if(paper){next.append(a("← 论文目录",paperUrl(paper.id)));const ordered=paperResults(paper);const following=ordered[ordered.findIndex(r=>r.id===result.id)+1];if(following){const link=a("",resultUrl(following));link.append(el("span","下一结果",{class:"next-label"}),el("span",following.title+" →"));next.append(link);}}
    main.append(next);
  }
  function about() {
    document.getElementById("about-nav").setAttribute("aria-current","page");
    const main=el("main",null,{class:"about-page",id:"main",tabindex:"-1"});main.append(el("p","FOR AGENTS & MAINTAINERS",{class:"eyebrow"}),el("h1","让每一步都可回到出处"));
    paragraph("阅读页连接正式原文、规范命题、公共证明和 Lean 对照。论文之间复用一个公共证明，各篇保留自己的定义、原定理位置与适配过程。",main);
    main.append(el("h2","从论文到可核验的结果"));
    const table=el("table");const header=el("tr");header.append(el("th","对象"),el("th","承载的内容"));const thead=el("thead");thead.append(header);table.append(thead);const tbody=el("tbody");
    for(const [name,description] of [["正式来源","会议正式正文、补充材料、版本及文件哈希。"],["论文中的命题","原文位置、核对转录、定义与假设。"],["公共证明","规范陈述、完整推导及被哪些论文采用。"],["论文适配","把论文符号与规范命题逐步连接。"],["Lean 与证据","实际声明、编译范围、源码和验证记录。"]]){const row=el("tr");row.append(el("td",name),el("td",description));tbody.append(row);}table.append(tbody);main.append(table);
    main.append(el("h2","给 AI 的只读入口"));paragraph("数据包和命令行工具支持查找论文、追溯来源、检索公共结果与读取验证证据；新增论文按同一关系结构接入。",main);
    const docs=el("div",null,{class:"docs-links"});for(const item of D.documentation||[])docs.append(a(item.label+" ↗",item.public_path,{target:"_blank",rel:"noopener"}));main.append(docs);
    if(D.library_artifacts){const artifacts=D.library_artifacts,details=el('details',null,{class:'caveats'});details.append(el('summary','公共库 '+artifacts.version+' 的源码与验证记录'));const links=el('div',null,{class:'docs-links'});links.append(a('当前验证报告 ↗',artifacts.report,{target:'_blank',rel:'noopener'}));for(const item of [...asList(artifacts.source_files),...asList(artifacts.command_logs)])links.append(a((item.label||item.path.split('/').pop())+' ↗',item.public_path,{target:'_blank',rel:'noopener'}));details.append(links);main.append(details);}
    if(D.cli_example)code(D.cli_example,main);
    main.append(el("h2","本次范围",{id:"scope"}));
    paragraph("全文目录来自逐页清单，包含命题、推导、定义、算法与经验材料。完整重写和 Lean 验证按每条证据确定；原证明修正与原命题反例分别展示。",main);
    for(const p of papers)paragraph(venueLabel(p)+"："+(p.scope||"选定结果的中文重写。"),main,{class:"scope-note"});
    const library=results.filter(r=>!r.paper_id);if(library.length){main.append(el("h2","补充公共结果"));for(const r of library){const p=el("p");p.append(a(r.title,resultUrl(r)));main.append(p);}}
    if(asList(D.review_records).length){main.append(el("h2","原文数学问题"));
      const groups=[['原命题反例与复合句的错误子句',r=>['refuted','partially_refuted'].includes(r.assessment_status)],['分析子断言反例（父结论尚未判定）',r=>r.issue_type==='analysis_subclause_counterexample'],['陈述定义域、反例记录与待判定范围',r=>!['refuted','partially_refuted'].includes(r.assessment_status)&&['statement_counterexample','statement_partial_counterexample','statement_alignment_or_scope'].includes(r.issue_type)],['原证明步骤与推导问题',r=>!['refuted','partially_refuted'].includes(r.assessment_status)&&!['analysis_subclause_counterexample','statement_counterexample','statement_partial_counterexample','statement_alignment_or_scope'].includes(r.issue_type)]];
      for(const [title,predicate] of groups){const records=D.review_records.filter(predicate);if(!records.length)continue;main.append(el('h3',title));for(const issue of records){const p=el('p');p.append(a(issue.title,issue.public_path));main.append(p);}}
    }
    main.append(el('h2','公共证明'));for(const proof of sharedMap.values()){const p=el('p');p.append(a(proof.title,commonProofUrl(proof)));main.append(p);}
    app.append(main);
  }
  function reviewPage(review){
    const main=el("main",null,{class:"about-page proof-prose",id:"main",tabindex:"-1"});
    const paper=paperMap.get(review.paper_id)||paperMap.get(asList(review.affected_result_ids).map(id=>resultMap.get(id)).filter(Boolean).map(r=>r.paper_id)[0]);
    const breadcrumb=el("nav",null,{class:"breadcrumb"});breadcrumb.append(a("论文","/"),el("span","/"));if(paper)breadcrumb.append(a(shortTitle(paper),paperUrl(paper.id)),el('span','/'));breadcrumb.append(el("span","原文核验"));main.append(breadcrumb);
    const categories={statement_counterexample:'原命题与反例',statement_partial_counterexample:'复合陈述中的问题',analysis_subclause_counterexample:'分析子断言有反例；父结论未判定',statement_alignment_or_scope:'原文记号与适用范围',definition_or_algorithm_boundary:'定义与算法的边界',proof_step_error:'原证明的错误步骤'};
    main.append(el("p",categories[review.issue_type]||'原文数学核验',{class:"eyebrow"}),el("h1",review.title));
    markdown(review.text_md||review.summary_md||review.problem_md||review.description_md||review.analysis_md||'',main);
    const formalRefs=[];
    for(const ref of review.source_refs||[]){const source=sources.get(ref.source_id);if(!source)continue;for(const loc of referenceLocations(ref)){const page=loc.pdf_page;if(!page)continue;const p=el("p");p.append(a(sourceLabel(source)+" · PDF 第 "+page+" 页 ↗",sourceHref(source,page),{class:"source-link",target:"_blank",rel:"noopener"}));main.append(p);formalRefs.push({source_id:ref.source_id,locations:[{pdf_page:page,role:"proof"}]});}}
    if(formalRefs.length)sourcePageImages({source_refs:formalRefs},main,"proof");
    if(review.original_conditions_tex||review.original_assertion_tex){main.append(el("h2","原文位置与断言"));formula(review.original_conditions_tex,main);formula(review.original_assertion_tex,main);}
    if(review.counterexample){const counter=review.counterexample;main.append(el("h2","核验例子"));const sets=["N","T","L"].filter(key=>Array.isArray(counter[key])).map(key=>key+"=\\{"+counter[key].join(",")+"\\}").join(",\\quad ");formula(sets,main);markdown(counter.explanation_md,main);}
    if(review.case4_note){const note=review.case4_note;main.append(el("h2","同段推导的求和范围"));formula(note.original_conditions_tex,main);formula(note.original_range_tex,main);markdown(note.problem_md,main);markdown(note.impact_md,main);}
    if(review.original_full_formula_tex){main.append(el("h2","正文与附录的记号"));formula(review.original_full_formula_tex,main);formula(review.original_and_subformula_tex,main);markdown(review.definition_convention_md,main);}
    if(review.impact_md){main.append(el("h2","影响范围"));markdown(review.impact_md,main);}
    if(review.original_formula_tex){main.append(el('h2','保留的原式'));formula(review.original_formula_tex,main);}
    if(review.evidence_md){main.append(el('h2','具体核验依据'));markdown(review.evidence_md,main);}
    if(review.analysis_formula_tex){main.append(el('h2','条件与数学核对'));formula(review.analysis_formula_tex,main);}
    if(review.counterexample_md){main.append(el('h2','反例'));markdown(review.counterexample_md,main);}
    if(review.counterexample_tex){main.append(el('h2','反例的数学内容'));formula(review.counterexample_tex,main);}
    paragraph(review.fix_authorization==='proof_only_granted'?'已授权忠实修正证明；原命题及其假设保持，错误命题单列。用户逐项审阅状态另行记录。':'授权与审阅状态见本条记录；原命题及假设保持。',main,{class:"source-notes"});
    const downloads=el("div",null,{class:"docs-links"});downloads.append(a("完整核验记录 ↗","/files/source-issues.md",{target:"_blank",rel:"noopener"}),a("核验数据 ↗","/files/source-issues.json",{target:"_blank",rel:"noopener"}));main.append(downloads);
    for(const id of review.affected_result_ids||[]){const r=resultMap.get(id);if(r){const p=el('p');p.append(a('返回 '+r.title+' →',resultUrl(r)+'#original-proof'));main.append(p);}}app.append(main);
  }
  const kind=document.body.dataset.pageKind||"home";
  if(kind === "paper"&&paperMap.has(document.body.dataset.paperId))paperPage(paperMap.get(document.body.dataset.paperId));
  else if(kind === "result"&&resultMap.has(document.body.dataset.resultId))resultPage(resultMap.get(document.body.dataset.resultId));
  else if(kind === 'shared'&&sharedMap.has(document.body.dataset.proofId))resultPage(sharedMap.get(document.body.dataset.proofId));
  else if(kind === "about")about();
  else if(kind === 'symbols')symbolsPage();
  else if(kind === "review"&&(D.review_records||[]).some(r=>r.id===document.body.dataset.reviewId))reviewPage(D.review_records.find(r=>r.id===document.body.dataset.reviewId));
  else if(kind === "home")home();
  else{const main=el("main",null,{class:"missing",id:"main"});main.append(el("h1","未找到这一阅读页"),a("返回论文列表","/"));app.append(main);}
})();
