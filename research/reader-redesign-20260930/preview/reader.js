/* Public, read-only prototype. Text nodes retain source TeX; KaTeX trust is false. */
(function () {
  "use strict";
  const D = window.READER_DATA;
  const CASES = {
    reconstruction: {title:"Theorem 1 · 全模式精确重构", position:"§3.1 · Theorem 1", proof:"proof-reconstruction-v1", claim:"claim-e15edb3df777058b68a8489c", statement:"reconstruction_statement", pages:"3", pdf:"cvpr2023-main.pdf", image:"official-main-page-03.png", sourceText:"CVPR 2023 正文第 3 页（20282）· 原证明：补充材料 C，第 3 页"},
    uniqueness: {title:"Theorem 1 · 重构系数唯一", position:"补充材料 C · 唯一性", proof:"proof-reconstruction-unique-v1", claim:"claim-9cd974272d015aded7b577c6", statement:"appendix_statement", pages:"2", pdf:"cvpr2023-supplement.pdf", image:"official-supp-page-02.png", sourceText:"CVPR 2023 补充材料 C · 陈述第 2 页，原证明第 3 页"},
    shapley: {title:"Theorem 2 · 与 Shapley value 的联系", position:"§3.1 · Theorem 2", claim:"claim-a31904cefdbc9e0a9374c802", statement:"shapley_statement", pages:"4", pdf:"cvpr2023-main.pdf", image:"official-main-page-04.png", sourceText:"CVPR 2023 正文第 4 页（20283）· 原证明：补充材料 D.2，第 6 页起"},
    reference: {title:"正文中对 Theorem 1 的引用", position:"§3.2 · 正文引用", claim:"claim-114147f1447e7138f450971e", pages:"4", pdf:"cvpr2023-main.pdf", sourceText:"CVPR 2023 正文第 4 页，右栏 · 稀疏化和基线优化的讨论"},
    overview: {title:"论文概览", position:"论文概览"},
    legacy: {title:"旧版审计入口", position:"历史审计 · 非正式版目录"},
  };
  let state = {case:"overview", tab:null, mode:"reading", focusStep:null};
  let toastTimer;
  window.READER_MATH_ERRORS = [];

  function node(tag, text, attrs) {
    const n = document.createElement(tag);
    if (text !== undefined && text !== null) n.textContent = text;
    Object.entries(attrs || {}).forEach(([k,v]) => n.setAttribute(k,v));
    return n;
  }
  function esc(x) {return String(x === undefined || x === null ? "" : x).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);}
  function math(root) {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(root, {delimiters:[
      {left:"$$",right:"$$",display:true},{left:"\\[",right:"\\]",display:true},
      {left:"$",right:"$",display:false},{left:"\\(",right:"\\)",display:false}],
      throwOnError:false,trust:false,strict:"ignore",ignoredClasses:["raw-source","lean-code","formula-fallback"],
      errorCallback:(message) => window.READER_MATH_ERRORS.push(message)});
  }
  function formula(tex, container, display) {
    try {window.katex.render(tex,container,{displayMode:display,throwOnError:true,trust:false,strict:"ignore"});}
    catch (err) {container.textContent = tex;container.classList.add("formula-fallback");window.READER_MATH_ERRORS.push(String(err));}
  }
  function prose(tag, text, className) {
    const p = node(tag,null,{class:className || ""});
    let rest = text;
    const code = /`([^`]+)`/g;
    let m, last = 0;
    while ((m=code.exec(text))) {
      p.append(document.createTextNode(text.slice(last,m.index)), node("code",m[1]));
      last = code.lastIndex;
    }
    rest = text.slice(last);p.append(document.createTextNode(rest));math(p);return p;
  }
  function markdown(text, target, isProof) {
    let nextStep = null;
    text.split(/\n\s*\n/).forEach(block => {
      block = block.trim();if (!block) return;
      const marker = /^<a id="(step-[1-9][0-9]*)"><\/a>$/.exec(block);
      if (marker) {nextStep = marker[1];return;}
      if (block.startsWith("# ")) {if (!isProof) target.append(prose("h3",block.slice(2)));return;}
      if (block.startsWith("## ")) {target.append(prose("h3",block.slice(3)));return;}
      if (isProof && block.startsWith("命题：")) return;
      if (isProof && block.startsWith("前提：")) {
        let condition=block.slice(3);const encodingPrefix="变量类型 α 的相等关系可判定；";
        if(condition.startsWith(encodingPrefix))condition=condition.slice(encodingPrefix.length);
        target.append(node("h3","适用条件"),prose("p",condition));return;
      }
      if (isProof && block.startsWith("证明思路：")) {target.append(node("h3","证明思路"),prose("p",block.slice(5)));return;}
      const numbered = /^(\d+)\.\s([\s\S]*)/.exec(block);
      if (isProof && numbered) {
        const section = node("section",null,{class:"proof-step",id:nextStep || "proof-step-"+numbered[1],"data-number":numbered[1]});
        section.append(prose("p",numbered[2]));
        section.append(node("button","Lean ↗",{type:"button",class:"step-code","data-step":nextStep || "step-"+numbered[1],"aria-label":"查看步骤 "+numbered[1]+" 对应的 Lean 声明"}));
        target.append(section);nextStep=null;return;
      }
      if (isProof && block.startsWith("来源与对齐：")) {
        const d=node("details",null,{class:"auxiliary"});d.append(node("summary","共享证明原文件的范围说明"),prose("p",block,"source-note"));target.append(d);return;
      }
      target.append(prose("p",block,isProof && block.startsWith("Lean 关键声明：") ? "source-note" : "markdown-block"));
    });
  }
  // Only presentation commands are removed. Mathematical content is not inferred
  // from PDF text. Raw mode and copy use the original, untouched source string.
  function unwrapPresentation(text) {
    for (const command of ["emph","textbf","textit"]) {
      let search=0;
      while (true) {
        const start=text.indexOf("\\"+command+"{",search);if(start<0)break;
        const brace=start+command.length+1;let depth=1,end=brace+1;
        while(end<text.length && depth) {if(text[end]==="{" && text[end-1]!=="\\")depth++;if(text[end]==="}" && text[end-1]!=="\\")depth--;end++;}
        if(depth)break;
        const content=text.slice(brace+1,end-1);text=text.slice(0,start)+content+text.slice(end);search=start+content.length;
      }
    }
    return text;
  }
  function readableTex(raw, target) {
    let text=raw.replace(/\\label\{[^}]+\}/g,"")
      .replace(/\\begin\{theorem\}(?:\[[^\]]*\])?/g,"").replace(/\\end\{theorem\}/g,"")
      .replace(/\\begin\{manualtheorem\}\{\d+\}(?:\[[^\]]*\])?/g,"").replace(/\\end\{manualtheorem\}/g,"")
      .replace(/\\(?:begin|end)\{small\}/g,"").replace(/\\(?:small|noindent|normalfont)\b/g,"")
      .replace(/\\vspace\{[^}]+\}/g,"")
      .replace(/\\cite\{harsanyi1963simplified\}/g,"[29]").replace(/\\cite\{shapley1953value\}/g,"[56]")
      .replace(/\\cite\{([^}]+)\}/g,"[$1]")
      .replace(/\\ref\{fig:causal-graph\}/g,"1").replace(/\\ref\{th:(?:app-)?harsanyi-faithful\}/g,"1")
      .replace(/\\ref\{th:app-harsanyi-shapley-value\}/g,"2");
    text=unwrapPresentation(text).replace(/\{\s*(\$[^$]+\$)\s*\}/g,"$1");
    const pattern=/\\begin\{(equation\*?|align\*?)\}([\s\S]*?)\\end\{\1\}|\\\[([\s\S]*?)\\\]/g;
    let last=0,m;
    function paragraphs(s) {
      s.split(/\n\s*\n/).forEach(part=>{
        part=part.replace(/\s*\n\s*/g," ").replace(/~/g," ").trim();if(!part)return;
        target.append(prose(/^(?:Proof for |\(Basis step\)|\(Induction step\))/.test(part) && part.length<65?"h4":"p",part));
      });
    }
    while((m=pattern.exec(text))) {
      paragraphs(text.slice(last,m.index));
      const box=node("div",null,{class:"math-block"});
      const tex=m[3] || (/^align/.test(m[1]) ? "\\begin{aligned}"+m[2]+"\\end{aligned}" : m[2]);
      formula(tex.trim(),box,true);target.append(box);last=pattern.lastIndex;
    }
    paragraphs(text.slice(last));
  }
  function notice(title, text, cls) {
    const n=node("div",null,{class:cls || "quiet-notice"});n.append(node("strong",title),node("p",text));return n;
  }
  function sourcePanel(excerpt, parent, options) {
    options=options||{};
    parent.append(notice("正式原文以 CVPR 2023 PDF 为准","下面的辅助 TeX 来自 arXiv v6，不是 CVPR 作者源码。此处数学陈述或证明片段已与正式 PDF 对照；文献编号和公式编号仍保留辅助来源的编号。"));
    const toolbar=node("div",null,{class:"raw-toolbar"});
    const switcher=node("div",null,{class:"segmented","aria-label":"原文显示方式"});
    switcher.append(node("button",options.plain ? "正式PDF提取文本" : "辅助数学排版",{type:"button","data-mode":"reading","aria-pressed":state.mode==="reading"?"true":"false"}),
                    node("button",options.plain ? "辅助TeX上下文" : "原样辅助 TeX",{type:"button","data-mode":"source","aria-pressed":state.mode==="source"?"true":"false"}));
    toolbar.append(switcher,node("button",options.plain && state.mode==="reading" ? "复制提取文本" : "复制辅助 TeX",{type:"button",class:"copy-button",id:"copy-source"}));
    parent.append(toolbar);
    const raw=options.plain && state.mode==="reading" ? options.plain : excerpt.raw;
    const wrapper=node("div",null,{class:state.mode==="source" || options.plain ? "raw-source" : "tex-reading",id:"original-source-view"});
    if (state.mode==="source" || options.plain) wrapper.append(node("pre",raw));else readableTex(excerpt.raw,wrapper);
    parent.append(wrapper);
    const caption=options.plain && state.mode==="reading" ? "当前文字来自正式 PDF 自动提取，不是原 TeX；原论文页可从上方打开。" :
      "辅助来源：arXiv:2111.06206v6 · "+excerpt.label+"。复制逐字保留辅助 TeX；不是 CVPR 2023 原源码。";
    parent.append(node("p",caption,{class:"render-caption"}));
    if(options.officialImage){const image=node("details",null,{class:"auxiliary"});image.append(node("summary","查看正式 PDF 的原页面"),node("img",null,{src:"files/official-pages/"+options.officialImage,alt:"CVPR 2023 正式 PDF 对应原页",style:"display:block;width:100%;height:auto"}));parent.append(image);}
    document.getElementById("copy-source").onclick=()=>copy(raw);
  }
  async function copy(text) {
    try {await navigator.clipboard.writeText(text);toast("已复制原文");}
    catch (_) {
      const t=node("textarea",text,{"aria-label":"待复制原文"});document.body.append(t);t.select();
      const ok=document.execCommand("copy");t.remove();toast(ok ? "已复制原文" : "浏览器未允许复制；可在源码框中选择全文。");
    }
  }
  function toast(message) {const t=document.getElementById("toast");t.textContent=message;t.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.hidden=true,2500);}
  function setLocation() {
    const p=new URLSearchParams();p.set("case",state.case);if(state.tab)p.set("tab",state.tab);if(state.mode==="source")p.set("mode","source");
    history.pushState(null,"","?"+p.toString());
  }
  function activateCase(name) {
    if(!CASES[name])return;state={case:name,tab:null,mode:"reading",focusStep:null};setLocation();render();
    document.getElementById("directory").classList.remove("mobile-open");document.getElementById("directory-toggle").setAttribute("aria-expanded","false");
    window.scrollTo(0,0);
  }
  function header(target, spec, type) {
    target.append(node("p",type==="complete" ? "已重写的证明" : type==="pending" ? "待核对的定理" : type==="reference" ? "来源片段" : "数学疑点",{class:"eyebrow"}),node("h1",spec.title));
    const row=node("div",null,{class:"badge-row"});
    if(type==="complete")row.append(node("span","已有中文重写",{class:"badge good"}),node("span","正式片段已对照",{class:"badge good"}),node("span",D.proofs[spec.proof].declaration.verification_status==="passed" ? "公共 Lean 已验证" : "Lean 尚未验证",{class:D.proofs[spec.proof].declaration.verification_status==="passed" ? "badge good" : "badge pending"}));
    if(type==="pending")row.append(node("span","已提取待核对",{class:"badge pending"}),node("span","尚未重写",{class:"badge pending"}));
    if(type==="reference")row.append(node("span","正文引用 · 非独立定理",{class:"badge"}),node("span","正式目录待核对",{class:"badge pending"}));
    if(type==="issue")row.append(node("span","范围疑点 · 等待确认",{class:"badge pending"}));
    target.append(row);
    const strip=node("div",null,{class:"source-strip"});strip.append(node("span",spec.sourceText),node("a","打开正式 PDF ↗",{href:"files/"+spec.pdf+"#page="+spec.pages,target:"_blank",rel:"noopener"}));target.append(strip);
  }
  function tabs(target, definitions, current) {
    const bar=node("div",null,{class:"reader-tabs",role:"tablist","aria-label":"证明阅读内容"});
    definitions.forEach(([id,title])=>bar.append(node("button",title,{type:"button",id:"tab-"+id,role:"tab","aria-selected":id===current?"true":"false","aria-controls":"reader-panel",tabindex:id===current?"0":"-1","data-tab":id})));
    bar.addEventListener("keydown",event=>{
      if(!["ArrowRight","ArrowLeft","Home","End"].includes(event.key))return;
      event.preventDefault();const index=definitions.findIndex(x=>x[0]===state.tab);
      const next=event.key==="Home"?0:event.key==="End"?definitions.length-1:(index+(event.key==="ArrowRight"?1:-1)+definitions.length)%definitions.length;
      state.tab=definitions[next][0];state.mode="reading";setLocation();render();document.getElementById("tab-"+state.tab).focus();
    });
    target.append(bar);const panel=node("section",null,{id:"reader-panel",class:"reader-panel",role:"tabpanel","aria-labelledby":"tab-"+current});target.append(panel);return panel;
  }
  function complete(target,spec) {
    const proof=D.proofs[spec.proof];header(target,spec,"complete");
    const definitions=[["rewrite","中文重写"],["statement","原命题"],["original-proof","原证明"],["lean","Lean 结果"]];
    if(!definitions.some(x=>x[0]===state.tab))state.tab="rewrite";
    const panel=tabs(target,definitions,state.tab);
    if(state.tab==="rewrite") {
      const box=node("div",null,{class:"statement-box"});box.append(node("p","统一记号下的命题"));const f=node("div");formula(proof.statement.trim(),f,true);box.append(f);panel.append(box);
      const body=node("article",null,{class:"proof-body"});markdown(proof.body,body,true);panel.append(body);
      panel.append(node("p","本页直接引用档案中已有的共享中文证明。原论文的双重求和 / 基数归纳证明与项目证明的方法分别保留。",{class:"source-note"}));
      const def=node("details",null,{class:"auxiliary"});def.append(node("summary","正式片段的定义与空集基线对照"));
      def.append(node("p","正式正文固定 DNN、输入和掩蔽基线，取 g(S)=v(x_S)。全模式集合包含空集；补充材料的基例保留 w_empty=v(x_empty)。本次对照没有加入零基线条件。",{class:"markdown-block"}),node("a","查看本次逐段对照依据",{href:"files/formal-edition-evidence.json",target:"_blank",rel:"noopener"}));panel.append(def);
      const common=node("details",null,{class:"auxiliary"});common.append(node("summary","共享证明的来源与复用"));
      common.append(node("p","当前中文证明来自既有公共库。正式正文 Theorem 1 与补充材料 C 的数学核心已在本次展示审计中对照；正式版 corpus 迁移和全篇目录核对尚未完成。",{class:"markdown-block"}));
      common.append(node("a","下载已有共享证明的原文件",{href:"files/"+spec.proof+".md",download:spec.proof+".md"}));panel.append(common);
      if(state.case==="reconstruction") {
        const deps=node("details",null,{class:"auxiliary"});deps.append(node("summary","展开所用引理：增加变量公式与空集基线"));
        D.dependency_proofs.forEach(dep=>{deps.append(node("h3",dep.title));markdown(dep.body,deps,false);});panel.append(deps);
      }
      const jump=node("div",null,{class:"jump-next"});jump.append(node("span",state.case==="reconstruction"?"附录 C 还包含唯一性结论":"正文 Theorem 1 的重构结论"),node("a",state.case==="reconstruction"?"接着读：重构系数唯一 →":"返回：全模式精确重构 →",{href:"?case="+(state.case==="reconstruction"?"uniqueness":"reconstruction"),"data-case":state.case==="reconstruction"?"uniqueness":"reconstruction"}));panel.append(jump);
    } else if(state.tab==="statement") {
      if(state.case==="uniqueness")panel.append(notice("原文边界","附录 C 的 Theorem 1 同时陈述重构与唯一性。这里完整保留这段陈述；当前中文重写阅读的是其中的唯一性部分。"));
      sourcePanel(D.original[spec.statement],panel,{officialImage:spec.image});
    } else if(state.tab==="original-proof") {
      panel.append(notice("正式补充材料 C 的原证明","CVPR 2023 补充材料第 3 页同时包含重构与唯一性证明。下面采用已对照数学内容的辅助 TeX 排版，可以展开查看正式 PDF 原页。"));
      sourcePanel(D.original.theorem1_proof,panel,{officialImage:"official-supp-page-03.png"});
    } else lean(panel,proof);
  }
  function lean(panel,proof) {
    panel.append(notice("验证范围：公共定理","已有报告验证的是下列公共声明。正式 Theorem 1 的数学核心已经本次片段对照；正式版档案尚未迁移，本页没有把公共库报告当作新的论文适配构建。"));
    const encoding=node("details",null,{class:"auxiliary",id:"lean-encoding"});encoding.append(node("summary","Lean 编码约定"),node("p",proof.theorem.assumptions[0],{class:"markdown-block"}),node("p","公共库在 Lean 中用可判定相等关系处理有限子集。这是声明的编码参数；数学阅读页保留有限集合与实值函数等条件。权威证明和原假设字段保持原样。",{class:"small-body"}));panel.append(encoding);
    const list=node("ul",null,{class:"validation-list"});
    [["实际构建与公理检查",D.verification.effective_status==="passed"?"通过":"未通过"],["源码与报告",D.verification.effective_status==="passed"?"本次快照读取时匹配":"状态需重新核查"],["允许的公理",proof.declaration.axioms.join(" · ")],["验证版本","Lean 4.24.0 · mathlib v4.24.0"]].forEach(([a,b])=>{const li=node("li");li.append(node("span",a),node("strong",b));list.append(li);});panel.append(list);
    panel.append(node("h3",proof.declaration.name),node("pre",proof.declaration.signature,{class:"lean-code"}));
    if(state.focusStep)panel.append(node("p","来自中文步骤 "+state.focusStep.replace("step-","")+"。现有映射对应整条声明，尚未提供步骤到代码行的精确对应。",{class:"small-body"}));
    panel.append(node("h3","已验证源码"));const code=node("pre",null,{class:"lean-code",id:"lean-source"});
    proof.source.raw.split("\n").forEach((line,index)=>{const n=node("span",null,{class:"code-line"});n.append(node("span",String(proof.source.first+index),{class:"line-no"}),document.createTextNode(line));code.append(n);});panel.append(code);
    const links=node("div",null,{class:"small-link-line"});links.append(node("a","查看已有验证证据",{href:"files/core-verification-excerpt.json",target:"_blank",rel:"noopener"}),node("a","下载完整公共源码",{href:"files/Mobius.lean",download:"Mobius.lean"}),node("button","返回对应中文步骤",{type:"button",class:"text-button",id:"return-proof"}));panel.append(links);
    panel.append(node("p","验证记录来自 "+D.verification.report_path+"；原型生成时重新核验源码哈希，本次未重新执行 Lean 构建。",{class:"render-caption"}));
    document.getElementById("return-proof").onclick=()=>{state.tab="rewrite";setLocation();render();const step=state.focusStep && document.getElementById(state.focusStep);if(step)step.scrollIntoView({block:"center"});};
  }
  function pending(target,spec) {
    header(target,spec,"pending");target.append(notice("尚未重写","已经找到原论文的定理陈述和证明位置，尚未完成原文边界核对、命题对齐和中文重写。可以直接阅读原命题与原论文。"));
    const defs=[["statement","原命题"],["proof-location","原证明的位置"],["progress","处理进度"]];if(!defs.some(x=>x[0]===state.tab))state.tab="statement";
    const panel=tabs(target,defs,state.tab);
    if(state.tab==="statement")sourcePanel(D.original.shapley_statement,panel,{officialImage:"official-main-page-04.png"});
    if(state.tab==="proof-location") {
      panel.append(node("h3","正式补充材料 D.2 · Theorem 2"),node("p","正式补充材料的 PDF 第 6 页开始给出原证明。当前仍未核对整份证明的完整边界，不把局部上下文当成完整提取成果。",{class:"small-body"}));
      const links=node("div",null,{class:"small-link-line"});links.append(node("a","打开正式补充材料第 6 页 ↗",{href:"files/cvpr2023-supplement.pdf#page=6",target:"_blank",rel:"noopener"}));panel.append(links);
    }
    if(state.tab==="progress") {
      panel.append(node("h3","下一步：核对原陈述与原证明的范围"));
      const row=node("div",null,{class:"progress-row"});[["提取","已提取待核对"],["中文重写","尚未重写"],["Lean","尚未形式化"]].forEach(([a,b])=>{const c=node("div",null,{class:"progress-cell"});c.append(node("small",a),node("strong",b,{class:"pending"}));row.append(c);});panel.append(row);
      panel.append(node("p","公共库中已经有若干 Shapley 相关结果，但尚无本条目与这些结果的已核对关系。因此这里不展示公共证明或已验证标签。",{class:"small-body"}));
    }
  }
  function reference(target,spec) {
    header(target,spec,"reference");target.append(notice("这是正文引用","原文正在讨论如何利用 Theorem 1 去除弱模式并优化基线。这段文字引用已有定理，没有声明新的独立定理；当前正式记录仍待整理。"));
    target.append(node("p","可以回到真正的 Theorem 1 阅读重构命题和已有中文证明。",{class:"small-body"}),node("a","阅读 Theorem 1 · 全模式精确重构 →",{href:"?case=reconstruction","data-case":"reconstruction",class:"primary-button"}));
    const panel=node("section",null,{class:"reader-panel section-rule"});target.append(panel);sourcePanel(D.original.complaint_context,panel,{plain:D.formal_reference_text});
  }
  function overview(target) {
    target.append(node("p","示例论文 · 正式会议版",{class:"eyebrow"}),node("h1",D.paper.title),node("p",D.paper.authors.join(" · ")+" · CVPR 2023 · CVF公开版本",{class:"paper-byline"}));
    target.append(node("p","仅收录正式会议或期刊版及其官方补充材料。当前用 CVPR 2023 的正文 10 页、补充材料 27 页演示阅读；正式全篇目录和 corpus 迁移尚未完成。",{class:"lede"}));
    const stats=node("div",null,{class:"stats-band"});[["2","片段已对照的数学结果"],["10 + 27","正式正文与补充材料页数"],["待核对","正式完整定理与证明目录"]].forEach(([a,b])=>{const x=node("div");x.append(node("strong",a),node("span",b));stats.append(x);});target.append(stats);
    const grid=node("div",null,{class:"overview-grid"});
    const read=node("section",null,{class:"overview-card"});read.append(node("span","可以直接阅读",{class:"card-label"}),node("h2","Theorem 1 · 重构与唯一性"),node("p","正式正文与补充材料的数学核心已对照，复用已有两份中文证明与公共 Lean 结果。完整论文审核仍待进行。"),node("a","阅读中文重写 →",{class:"primary-button",href:"?case=reconstruction","data-case":"reconstruction"}));
    const p=node("section",null,{class:"overview-card"});p.append(node("span","尚未完成",{class:"card-label"}),node("h2","Theorem 2 · Shapley value"),node("p","已找到原文，尚未重写；先展示原命题和原证明位置，处理进度可以展开查看。"),node("a","阅读原命题 →",{class:"simple-link",href:"?case=shapley","data-case":"shapley"}));grid.append(read,p);target.append(grid);
    const small=node("div",null,{class:"small-body"});small.append(node("h3","这次对照覆盖到哪里？"),node("p","Theorem 1 的正式陈述、定义、重构与唯一性证明片段已对照。Theorem 2 只核到正式陈述与原证明位置，尚未重写。正式版全篇的定理、性质、未编号论证及证明总数尚未统计，不沿用旧 arXiv 候选数。"));target.append(small);
    target.append(node("h2","按原论文编号阅读"));
    const table=node("table",null,{class:"toc-table"});table.innerHTML='<thead><tr><th>章节与编号</th><th>结论</th><th>当前阅读状态</th></tr></thead><tbody><tr><td>正式正文 · Theorem 1</td><td><a href="?case=reconstruction" data-case="reconstruction">全模式精确重构</a></td><td>已有重写 · 正式片段已对照</td></tr><tr><td>正式补充 C · Theorem 1</td><td><a href="?case=uniqueness" data-case="uniqueness">重构系数唯一</a></td><td>已有重写 · 正式片段已对照</td></tr><tr><td>正式正文 · Theorem 2</td><td><a href="?case=shapley" data-case="shapley">与 Shapley value 的联系</a></td><td>尚未重写</td></tr></tbody>';target.append(table);
    const links=node("div",null,{class:"small-link-line"});links.append(node("a","CVPR 2023 正文 · 10 页",{href:"files/cvpr2023-main.pdf",target:"_blank",rel:"noopener"}),node("a","正式补充材料 · 27 页",{href:"files/cvpr2023-supplement.pdf",target:"_blank",rel:"noopener"}),node("a","查看本次片段对照证据",{href:"files/formal-edition-evidence.json",target:"_blank",rel:"noopener"}));target.append(links);
  }
  function render() {
    const spec=CASES[state.case] || CASES.overview;
    document.title=spec.title+" · 论文证明阅读预览";
    document.getElementById("breadcrumb-position").textContent=spec.position;
    document.querySelectorAll(".directory-link[data-case]").forEach(a=>{const selected=a.dataset.case===state.case;a.classList.toggle("active",selected);if(selected)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current");});
    if(state.case==="reference")document.getElementById("pending-sources").open=true;
    const target=document.getElementById("page-content");target.replaceChildren();
    document.getElementById("toast").hidden=true;
    if(spec.proof)complete(target,spec);else if(state.case==="shapley")pending(target,spec);else if(state.case==="reference")reference(target,spec);else if(state.case==="legacy") {
      target.append(node("p","历史审计",{class:"eyebrow"}),node("h1","旧版审计入口"),notice("此链接不属于正式版数学目录","原先的 18 条来源记录及 Dummy 问题来自 arXiv v6 的历史审计，不能作为 CVPR 2023 正式版的计数或审核结果。旧证据保留在项目审计文件中，尚未完成正式版迁移。"),node("a","返回 CVPR 2023 正式版示例 →",{href:"?case=overview","data-case":"overview",class:"primary-button"}));
    } else overview(target);
    document.getElementById("snapshot-date").textContent="内容快照 "+D.snapshot_at.slice(0,10)+" · 方案尚未应用到正式站点";
  }
  function fromURL() {
    const p=new URLSearchParams(location.search);const requested=p.get("case");state={case:["inventory","dummy"].includes(requested)?"legacy":CASES[requested]?requested:"overview",tab:p.get("tab"),mode:p.get("mode")==="source"?"source":"reading",focusStep:null};render();
  }
  document.addEventListener("click",event=>{
    const c=event.target.closest("[data-case]");if(c && !event.ctrlKey && !event.metaKey && !event.shiftKey){event.preventDefault();activateCase(c.dataset.case);return;}
    const tab=event.target.closest("[data-tab]");if(tab){state.tab=tab.dataset.tab;state.mode="reading";state.focusStep=null;setLocation();render();document.getElementById("tab-"+state.tab).focus();return;}
    const mode=event.target.closest("[data-mode]");if(mode){state.mode=mode.dataset.mode;setLocation();render();return;}
    const step=event.target.closest("[data-step]");if(step){state.focusStep=step.dataset.step;state.tab="lean";setLocation();render();document.getElementById("lean-source").scrollIntoView({block:"center"});}
  });
  document.getElementById("side-summary").innerHTML='<div class="side-counter"><strong class="counter-emphasis">2 个</strong>正式片段已对照结果</div><div class="side-counter"><strong>10 + 27 页</strong>正式材料</div><p>正式完整证明目录：尚未核对</p>';
  document.getElementById("pending-count").textContent="· 待核对";
  document.getElementById("paper-button").onclick=()=>{const p=document.getElementById("paper-list");p.hidden=!p.hidden;document.getElementById("paper-button").setAttribute("aria-expanded",String(!p.hidden));};
  document.getElementById("choose-paper").onclick=()=>{activateCase("overview");document.getElementById("paper-list").hidden=true;document.getElementById("paper-button").setAttribute("aria-expanded","false");};
  document.getElementById("directory-toggle").onclick=()=>{const d=document.getElementById("directory");const open=d.classList.toggle("mobile-open");document.getElementById("directory-toggle").setAttribute("aria-expanded",String(open));};
  document.getElementById("help-button").onclick=()=>document.getElementById("help-dialog").showModal();
  document.getElementById("close-help").onclick=()=>document.getElementById("help-dialog").close();
  document.getElementById("help-dialog").addEventListener("click",event=>{if(event.target===event.currentTarget){const r=event.currentTarget.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)event.currentTarget.close();}});
  window.addEventListener("popstate",fromURL);fromURL();
})();
