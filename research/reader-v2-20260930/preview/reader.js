/* Public formal sources only. Source text is always inserted through DOM text nodes. */
(function () {
  "use strict";
  const D = window.READER_V2_DATA;
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

  function el(tag, text, attrs) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = String(text);
    for (const [key, value] of Object.entries(attrs || {})) if (value !== undefined && value !== null) node.setAttribute(key, String(value));
    return node;
  }
  function a(text, href, attrs) { return el("a", text, {href, ...(attrs || {})}); }
  function paperUrl(id) { return "/papers/" + encodeURIComponent(id) + "/"; }
  function resultUrl(result) { return result.paper_id ? paperUrl(result.paper_id) + "results/" + encodeURIComponent(result.id) + "/" : "/library/" + encodeURIComponent(result.id) + "/"; }
  function asList(value) { return value === undefined || value === null ? [] : Array.isArray(value) ? value : [value]; }
  function textValue(value) { if (typeof value === "string") return value; if (!value) return ""; return value.text_md || value.text || value.label || value.explanation || value.title || ""; }
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
  function paragraph(text, parent, attrs) { const p = el("p", null, attrs); inline(String(text), p); parent.append(p); math(p); return p; }
  function venueLabel(paper) { return paper.venue_label || (String(paper.venue||"").includes(String(paper.year)) ? paper.venue : [paper.venue, paper.year].filter(Boolean).join(" ")); }
  function shortTitle(paper) { return paper.short_title || paper.title; }
  function paperResults(paper) { return results.filter(r => r.paper_id === paper.id); }
  function isComplete(result) { return result.reading_status === "complete"; }
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
    return result.original_number || result.source_label || (descriptor && (descriptor.original_number || descriptor.source_label || descriptor.number)) || (paper && /^[^：:]+[：:]/.test(result.title) ? result.title.split(/[：:]/)[0] : "");
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
    paragraph("选择一篇正式论文，查看其中的命题、中文证明与 Lean 对照。公式沿用论文记号，并把省略的推导逐步展开。",head,{class:"intro"}); main.append(head);
    const list = el("div", null, {class:"paper-list"});
    for (const paper of papers) {
      const row = el("article", null, {class:"paper-row","data-paper":paper.id});
      row.append(el("div",venueLabel(paper),{class:"venue"}));
      const content = el("div"); const h = el("h2"); h.append(a(paper.title,paperUrl(paper.id))); content.append(h);
      paragraph(paper.intro || paper.description || paper.summary || "",content,{class:"paper-description"});
      row.append(content,a("阅读论文 →",paperUrl(paper.id),{class:"read-link"}));list.append(row);
    }
    main.append(list);
    paragraph("本次呈现三篇论文中的选定结果；每篇的阅读页说明具体范围。",main,{class:"home-note"});
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
    for(const [complete,label] of [[true,"选定结果"],[false,"原文核验"]]){
      const grouped=paperResults(paper).filter(r=>isComplete(r)===complete);if(!grouped.length)continue;
      directory.append(el("p",label,{class:"directory-label"}));
      for (const r of grouped) { const link = a("",resultUrl(r),{"data-result":r.id,"aria-current":result && result.id === r.id ? "page" : null});const number=resultNumber(r,paper);if(number)link.append(el("span",number,{class:"theorem-number"}));link.append(el("span",directoryTitle(r,paper)));directory.append(link); }
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
    paragraph(paper.scope||"本次只呈现下列已重写结果，尚未完成整篇论文的证明目录。",main,{class:"scope-note"});
    const list=el("div",null,{class:"result-list"});
    for(const result of paperResults(paper)){
      const link=a("",resultUrl(result),{"data-result":result.id});const number=resultNumber(result,paper);if(number)link.append(el("span",number,{class:"result-number"}));
      link.append(el("h2",directoryTitle(result,paper))); const lean=getLean(result,sharedMap.get(result.shared_proof_id));link.append(el("span",isComplete(result)?"完整中文证明 · "+leanLabel(lean):"原命题与原证明 · 对齐待核验",{class:"result-blurb"}));list.append(link);
    }
    main.append(list);
  }
  function conditions(result, parent, title) {
    const assumptions=asList(result.assumptions),definitions=asList(result.definitions);
    if(!assumptions.length&&!definitions.length)return;
    const section=el("section",null,{class:"notation-section"});section.append(el("h2",title||"记号与条件"));
    for(const item of [...assumptions,...definitions]){const block=el("div",null,{class:assumptions.includes(item)?"condition":"definition-item"});markdown(textValue(item),block);for(const tex of asList(item.formula_tex))formula(tex,block);section.append(block);}
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
    const steps=asList(proof.proof_steps);if(!steps.length)return;
    if(title)parent.append(el("h2",title,{class:"complete-proof-heading"}));
    steps.forEach((step,index)=>{
      const id=stepAnchor(prefix,step.id,index);const section=el("section",null,{class:"proof-step",id,"data-step-id":step.id||index+1,"data-proof-prefix":prefix});
      const head=el("h3");head.append(el("span",index+1,{class:"step-number"}),el("span",step.title||"",{class:"step-title"}));section.append(head);
      markdown(step.body_md||step.body||"",section);for(const tex of asList(step.formula_tex))formula(tex,section);
      if(step.justification){const note=el("div",null,{class:"justification"});markdown(textValue(step.justification),note);section.append(note);}
      if(asList(step.lean_refs).length || matchingStepMap(step.id,prefix).length){const button=el("button","查看 Lean 对照 ↗",{type:"button",class:"step-to-lean","aria-label":"查看第 "+(index+1)+" 步的 Lean 对照"});button.addEventListener("click",()=>{activeStep={id:String(step.id||index+1),prefix,anchor:id};setTab("lean");const match=document.querySelector('.lean-map[data-step-id="'+CSS.escape(activeStep.id)+'"]');if(match)match.scrollIntoView({block:"start"});});section.append(button);}
      parent.append(section);
    });
  }
  function matchingStepMap(stepId,prefix) {
    const lean=prefix === "shared" && currentShared ? currentShared.lean : getLean(currentResult,currentShared);
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
    const parent=el("div",null,{class:"proof-prose"});
    statement(currentResult,parent);
    conditions(currentResult,parent);
    overview(currentResult,parent);
    proofSteps(currentResult,parent,"paper",currentShared ? "论文命题的适配" : "完整证明");
    if(currentShared){
      parent.append(el("h2",currentShared.title||"公共证明",{class:"shared-proof-heading"}));
      statement(currentShared,parent,"公共命题");conditions(currentShared,parent,"公共证明的记号与条件");overview(currentShared,parent);proofSteps(currentShared,parent,"shared","完整证明");
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
    sourceLinks(currentResult,parent,proof?"proof":"statement");
    if(proof||!isComplete(currentResult))issueNote(currentResult,parent);
    sourcePageImages(currentResult,parent,proof?"proof":"statement");
    if(value){const section=el("section",null,{class:"original-section"});section.append(el("h2",proof?(currentResult.original_proof_heading||"原证明的中文说明"):(currentResult.original_statement_heading||"原命题的公式与说明")));markdown(value,section);parent.append(section);}
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
    const statementBlock=el("section",null,{class:"lean-statement"});statementBlock.append(el("h2","对应的数学陈述"));
    const tex=lean.display_statement_tex||lean.statement_tex||result.display_statement_tex||result.statement_tex;for(const item of asList(tex))formula(item,statementBlock);markdown(lean.statement_md||"",statementBlock);parent.append(statementBlock);
  }
  function leanMap(lean,parent,prefix,proof) {
    const map=asList(lean.step_map);if(!map.length)return;
    parent.append(el("h2",prefix === "shared" ? "公共证明与 Lean 的逐步对应" : "本论文与 Lean 的逐步对应"));
    map.forEach((item,index)=>{
      const stepId=String(item.step_id||item.proof_step_id||item.id||index+1);
      const section=el("section",null,{class:"lean-map","data-step-id":stepId,"data-proof-prefix":prefix,id:"lean-"+prefix+"-"+stepId});
      const step=asList(proof.proof_steps).find(s=>String(s.id)===stepId);
      section.append(el("h3",item.title||step&&step.title||"对应步骤 "+(index+1)));
      markdown(item.explanation_md||item.explanation||item.text_md||item.description||"",section);
      if(item.declaration){const declaration=el("p",null,{class:"lean-declarations"});declaration.append(el("code",asList(item.declaration).join(", ")));section.append(declaration);}
      code(item.lean_excerpt||item.lean_code||item.code||"",section);
      const button=el("button","返回中文证明的这一步",{type:"button",class:"step-to-lean return-step"});button.addEventListener("click",()=>{setTab("rewrite");const target=document.getElementById(stepAnchor(prefix,stepId,index));if(target){target.scrollIntoView({block:"start"});target.setAttribute("tabindex","-1");target.focus({preventScroll:true});}});section.append(button);parent.append(section);
    });
  }
  function leanPanel() {
    const parent=el("div");const lean=getLean(currentResult,currentShared);
    const intro=el("div",null,{class:"lean-intro"});intro.append(el("h2",leanLabel(lean)));markdown(lean.scope||"此结果尚未提供已编译的 Lean 对照。",intro);parent.append(intro);
    leanStatement(lean,parent,currentResult);
    const declarations=asList(lean.declarations);
    if(declarations.length){const row=el("div",null,{class:"lean-declarations"});for(const declaration of declarations)row.append(el("code",typeof declaration === "string" ? declaration : declaration.name||declaration.declaration||""));parent.append(row);}
    if(lean.statement){const details=el("details",null,{class:"lean-details"});details.append(el("summary","完整 Lean 类型陈述"));const body=el("div");code(lean.statement,body);details.append(body);parent.append(details);}
    if(lean.adapter_code){parent.append(el("h3",lean.compiled?"已编译的论文适配":"论文适配源码"));code(lean.adapter_code,parent);}
    leanMap(lean,parent,"paper",currentResult);
    if(currentShared&&currentShared.lean){const sharedLean=currentShared.lean;if(sharedLean.adapter_code&&sharedLean.adapter_code!==lean.adapter_code){parent.append(el("h3","公共声明"));code(sharedLean.adapter_code,parent);}leanMap(sharedLean,parent,"shared",currentShared);}
    if(!asList(lean.step_map).length&&!(currentShared&&asList(currentShared.lean&&currentShared.lean.step_map).length)){paragraph("目前只有声明级对应，尚未给出逐步代码对照。",parent,{class:"source-notes"});}
    const evidence=el("div",null,{class:"lean-evidence"});
    for(const item of [lean.public_source_path&&{path:lean.public_source_path,label:"Lean 源文件"},lean.public_report_path&&{path:lean.public_report_path,label:"编译与公理检查记录"},currentShared&&currentShared.lean&&currentShared.lean.public_source_path&&{path:currentShared.lean.public_source_path,label:"公共 Lean 源文件"}].filter(Boolean))evidence.append(a(item.label+" ↗",item.path,{target:"_blank",rel:"noopener"}));
    parent.append(evidence);
    if(lean.encoding_note){const details=el("details",null,{class:"lean-details"});details.append(el("summary","Lean 编码说明"));const body=el("div");markdown(lean.encoding_note,body);details.append(body);parent.append(details);}
    return parent;
  }
  function scopePanel(){
    const parent=el("div",null,{class:"proof-prose"});parent.append(el("h2","原文核验范围"));
    markdown(currentResult.overview||"完整 AND/OR 联合命题的原文对齐尚待核验。附录 C(1) 的 AND 子结论有独立的中文证明与 Lean 对照。",parent);
    issueNote(currentResult,parent);sourceLinks(currentResult,parent);caveats(currentResult,parent);
    const completed=results.find(r=>r.paper_id===currentResult.paper_id&&isComplete(r));if(completed){const p=el("p");p.append(a("阅读附录 C(1) 的完整 AND 子结论 →",resultUrl(completed)));parent.append(p);}return parent;
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
    const meta=el("div",null,{class:"result-meta"});if(paper)meta.append(el("span",venueLabel(paper)));meta.append(el("span",isComplete(result)?"完整中文证明":"原文对齐待核验"));if(isComplete(result))meta.append(el("span",leanLabel(getLean(result,currentShared))));head.append(meta);main.append(head);
    const tabs=el("div",null,{class:"tabs",role:"tablist","aria-label":"阅读内容"});
    const labels=isComplete(result)?[["rewrite","中文证明"],["statement","原命题"],["original-proof","原证明"],["lean","Lean 对照"]]:[["statement","原命题"],["original-proof","原证明"],["scope","核验说明"]];
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
    if(D.cli_example)code(D.cli_example,main);
    main.append(el("h2","本次范围",{id:"scope"}));
    paragraph("本原型展示三篇公开正式论文的选定结果。它没有宣称整篇论文全部重写或全部形式化；每一结果的 Lean 页面单独说明编译所覆盖的数学内容。",main);
    for(const p of papers)paragraph(venueLabel(p)+"："+(p.scope||"选定结果的中文重写。"),main,{class:"scope-note"});
    const library=results.filter(r=>!r.paper_id);if(library.length){main.append(el("h2","补充公共结果"));for(const r of library){const p=el("p");p.append(a(r.title,resultUrl(r)));main.append(p);}}
    if(D.issues&&D.issues.length){main.append(el("h2","原文核验记录"));for(const issue of D.issues){const p=el("p");p.append(a(issue.label||"待确认的原文疑点",issue.public_path,{target:"_blank",rel:"noopener"}));main.append(p);}}
    app.append(main);
  }
  function reviewPage(review){
    const main=el("main",null,{class:"about-page proof-prose",id:"main",tabindex:"-1"});
    const breadcrumb=el("nav",null,{class:"breadcrumb"});breadcrumb.append(a("论文","/"),el("span","/"),a("跨模型通用交互",paperUrl("iclr2024-generalizable")),el("span","/"),el("span","原文核验"));main.append(breadcrumb);
    main.append(el("p",review.classification === "notation_alignment_note"?"原文记号对齐":"原证明的具体疑点",{class:"eyebrow"}),el("h1",review.title));
    markdown(review.text_md,main);
    const formalRefs=[];
    for(const ref of review.source_refs||[]){const source=sources.get(ref.source_id);if(!source)continue;const page=ref.pdf_page;const p=el("p");p.append(a(sourceLabel(source)+" · PDF 第 "+page+" 页 ↗",sourceHref(source,page),{class:"source-link",target:"_blank",rel:"noopener"}));main.append(p);formalRefs.push({source_id:ref.source_id,locations:[{pdf_page:page,role:"proof"}]});}
    if(formalRefs.length)sourcePageImages({source_refs:formalRefs},main,"proof");
    if(review.original_conditions_tex||review.original_assertion_tex){main.append(el("h2","原文位置与断言"));formula(review.original_conditions_tex,main);formula(review.original_assertion_tex,main);}
    if(review.counterexample){const counter=review.counterexample;main.append(el("h2","核验例子"));const sets=["N","T","L"].filter(key=>Array.isArray(counter[key])).map(key=>key+"=\\{"+counter[key].join(",")+"\\}").join(",\\quad ");formula(sets,main);markdown(counter.explanation_md,main);}
    if(review.case4_note){const note=review.case4_note;main.append(el("h2","同段推导的求和范围"));formula(note.original_conditions_tex,main);formula(note.original_range_tex,main);markdown(note.problem_md,main);markdown(note.impact_md,main);}
    if(review.original_full_formula_tex){main.append(el("h2","正文与附录的记号"));formula(review.original_full_formula_tex,main);formula(review.original_and_subformula_tex,main);markdown(review.definition_convention_md,main);}
    if(review.impact_md){main.append(el("h2","影响范围"));markdown(review.impact_md,main);}
    paragraph("该记录等待用户确认；原命题与原证明保持原样。",main,{class:"source-notes"});
    const downloads=el("div",null,{class:"docs-links"});downloads.append(a("完整核验记录 ↗","/files/source-issues.md",{target:"_blank",rel:"noopener"}),a("核验数据 ↗","/files/source-issues.json",{target:"_blank",rel:"noopener"}));main.append(downloads);
    const parent=results.find(r=>r.id==="iclr2024-generalizable-andor");if(parent){const p=el("p");p.append(a("返回 Theorem 2 原证明 →",resultUrl(parent)+"#original-proof"));main.append(p);}app.append(main);
  }
  const kind=document.body.dataset.pageKind||"home";
  if(kind === "paper"&&paperMap.has(document.body.dataset.paperId))paperPage(paperMap.get(document.body.dataset.paperId));
  else if(kind === "result"&&resultMap.has(document.body.dataset.resultId))resultPage(resultMap.get(document.body.dataset.resultId));
  else if(kind === "about")about();
  else if(kind === "review"&&(D.review_records||[]).some(r=>r.id===document.body.dataset.reviewId))reviewPage(D.review_records.find(r=>r.id===document.body.dataset.reviewId));
  else if(kind === "home")home();
  else{const main=el("main",null,{class:"missing",id:"main"});main.append(el("h1","未找到这一阅读页"),a("返回论文列表","/"));app.append(main);}
})();
