#!/usr/bin/env python3
"""Build the inventory-driven full-paper reader, without altering the frozen v2 preview.

Only this script's output directory is served. No archive-store traversal, corpus
export, experimental proof, browser environment, or unpublished paper is copied.
"""
from __future__ import annotations

import copy
import hashlib
import html
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from input_manifest import load_manifest, project_path as guarded_project_path
from evidence_paths import EVIDENCE

ROOT = Path(__file__).resolve().parents[1]
WORK = Path(__file__).resolve().parent
SITE = WORK / "preview"
PAPER_IDS = set()
INPUTS: dict[str, dict] = {}
PUBLIC_FILES: dict[str, dict] = {}
LEAN_WHITELIST = {"propext", "Classical.choice", "Quot.sound"}
VERIFICATION_CHECKS: list[dict] = []
PROOF_REGISTRY: dict[str,dict] = {}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> None:
    INPUTS[path.relative_to(ROOT).as_posix()] = {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}


def project_file(path: str | Path) -> Path:
    relative = Path(path)
    if len(relative.parts)>1 and relative.parts[0]=="corpus" and relative.parts[1] in {"papers","claims","theorems","issues","reviews"}:
        raise ValueError("Inactive legacy corpus is not a reader input")
    result = guarded_project_path(path).resolve()
    if not result.is_relative_to(ROOT) or not result.is_file():
        raise ValueError(f"Expected an existing project file: {path}")
    if Path(path).is_absolute() or (ROOT / path).is_symlink():
        raise ValueError(f"Only ordinary project-relative files are supported: {path}")
    return result


def read_json(path: Path) -> dict:
    record(path)
    return json.loads(path.read_text(encoding="utf-8"))


def publish(source: Path, target: str, *, expected: str | None = None) -> str:
    if source.is_symlink() or not source.is_relative_to(ROOT):
        raise ValueError("Source must be an ordinary file inside this project")
    value = digest(source)
    if expected and value != expected:
        raise ValueError(f"Pinned source hash changed: {source.relative_to(ROOT)}")
    destination = SITE / target
    if not destination.resolve().is_relative_to(SITE):
        raise ValueError("Output escaped the preview directory")
    previous = PUBLIC_FILES.get(target)
    if previous and previous["sha256"] != value:
        raise ValueError(f"Different public sources would overwrite {target}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    record(source)
    PUBLIC_FILES[target] = {"path": target, "source": source.relative_to(ROOT).as_posix(), "sha256": value}
    return "/" + target


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verify_lean(lean: dict) -> dict:
    """Reuse the package's source/declaration/axiom checks, never a UI flag."""
    report_path = lean.get("report_path")
    names = [item if isinstance(item, str) else item.get("name", item.get("declaration")) for item in lean.get("declarations", [])]
    result = {"status": "unavailable", "declarations": names, "reasons": []}
    if not isinstance(report_path, str) or not report_path:
        result["reasons"].append("verification report is missing")
        return result
    try:
        report_file = project_file(report_path)
        report = read_json(report_file)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        result["reasons"].append(str(error))
        return result
    # Inspect configured report paths before the historical verifier can open
    # any source bytes. The public reader rejects private and inactive corpora.
    for source in report.get("source_files", []):
        try:
            project_file(source["path"])
        except (ValueError, KeyError) as error:
            result["reasons"].append(str(error))
            return result
    helper_path = WORK / "architecture/v2_verification_helper.py"
    record(helper_path)
    spec = importlib.util.spec_from_file_location("reader_v2_package_verifier", helper_path)
    helper = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(helper)
    node = {"id": "reader-verification", "path": report_path, "scope": lean.get("scope", "selected declaration"),
            "expected_declarations": names, "visibility": "public"}
    package = helper.PaperPackage(root=ROOT, manifest={"verification_reports": [node]}, math_content={"results": [], "shared_proofs": []})
    package_evidence = package.report_evidence(node["id"])
    result["package_evidence"] = package_evidence
    if package_evidence["freshness"] == "stale":
        result["status"] = "stale"
    elif package_evidence["compilation"] == "passed" and package_evidence["axiom_audit"] == "passed" and package_evidence["freshness"] == "current":
        result["status"] = "verified"
    else:
        result["reasons"].append(package_evidence.get("reason", "compilation or axiom audit did not pass"))
    commands = report.get("commands", [])
    if not any("lean" in command.get("argv", []) and any("audit" in str(arg).lower() for arg in command.get("argv", [])) and command.get("exit_code") == 0 for command in commands):
        result["reasons"].append("no successful declaration/axiom audit command")
    source_rows = report.get("source_files", [])
    for row in source_rows:
        try:
            record(project_file(row["path"]))
        except (ValueError, KeyError, OSError):
            pass  # The shared helper records missing or modified sources as stale.
    declared = {item["name"]: item for item in report.get("declarations", [])}
    for name in names:
        if name in declared and declared[name].get("source_path") not in {row.get("path") for row in source_rows}:
            result["reasons"].append(f"declaration source was not fingerprinted: {name}")
    if result["reasons"] and result["status"] == "verified":
        result["status"] = "unavailable"
    result["source_fingerprint"] = report.get("source_fingerprint")
    result["report_sha256"] = digest(report_file)
    return result


def public_lean(lean: dict) -> None:
    lean["requested_compilation_status"]=lean.get("status")
    explicitly_unformalized = lean.get("status") == "not_formalized" and not lean.get("declarations") and not lean.get("report_path")
    verification = verify_lean(lean)
    VERIFICATION_CHECKS.append(verification)
    lean["status"] = "not_formalized" if explicitly_unformalized else verification["status"]
    lean["compiled"] = verification["status"] == "verified"
    lean["label"] = "尚未形式化" if explicitly_unformalized else {"verified": "Lean 对照已编译", "stale": "Lean 证据待更新", "unavailable": "Lean 证据未取得"}[verification["status"]]
    lean["verification"] = verification
    if lean.get('report_path') and (ROOT/lean['report_path']).is_file():
        report=read_json(project_file(lean['report_path']));wanted=set(verification['declarations'])
        lean['actual_declarations']=[{k:row[k] for k in ('name','signature','source_path','line','axioms','kind') if k in row} for row in report.get('declarations',[]) if row['name'] in wanted]
    if lean.get('evidence_role')=='counterexample':lean['label']='反例已验证；其范围见下方' if lean['compiled'] else '反例证据未取得'
    if lean.get('evidence_role')=='partial_component':lean['label']='部分范围的 Lean 证据通过' if lean['compiled'] else '部分范围的 Lean 证据未取得'
    for key, label in (("source_path", "source"), ("report_path", "report")):
        path = lean.get(key)
        if not isinstance(path, str) or not path:
            continue
        # These paths are supplied by the mathematical reviewer. Experimental
        # OR work is deliberately outside the downloadable/readable snapshot.
        current_public_report=json.loads((ROOT/'catalog/library.json').read_text()).get('verification_report')
        allowed = path.startswith("lean/HarsanyiLib/Harsanyi/") or path.startswith("research/reader-v2-20260930/math/") or path.startswith("research/full-proof-integration-20260930/") or path.startswith("corpus/public/reader/") or (key=='report_path' and path==current_public_report)
        if not allowed or "/experimental/" in path:
            raise ValueError(f"Non-public Lean artifact requested: {path}")
        if not (ROOT / path).is_file():
            continue
        source = project_file(path)
        lean["public_" + key] = publish(source, "files/lean/" + digest(source)[:12] + "-" + source.name)
    # Kept in provenance outside the served data; reader code names are useful,
    # machine paths and build directories are not part of the reading flow.
    lean.pop("source_path", None)
    lean.pop("report_path", None)

def enrich_step_maps(math_content: dict) -> None:
    """Make every referenced compiled declaration visible at the requested step."""
    rows={}; provenance={}
    all_proofs=math_content.get('results',[])+math_content.get('shared_proofs',[])
    catalog=read_json(ROOT/'catalog/library.json')
    paths={p.get('lean',{}).get('report_path') for p in all_proofs if p.get('lean',{}).get('report_path')}
    current_public_report=catalog.get('verification_report')
    if current_public_report:paths.add(current_public_report)
    # Prefer the current public-library report for common declarations. Paper
    # adapters retain the actual report that compiled their own exact types.
    for path in sorted(paths,key=lambda p:(p!=current_public_report,p)):
        if not (ROOT/path).is_file():continue
        report=read_json(project_file(path))
        verification=verify_lean({'report_path':path,'declarations':[r['name'] for r in report.get('declarations',[])],
                                  'scope':'actual declarations referenced by proof steps'})
        if verification['status']!='verified':continue
        source_hashes={r['path']:r['sha256'] for r in report['source_files']}
        for row in report.get('declarations',[]):
            name=row['name']
            if name in rows:continue
            rows[name]=row
            provenance[name]={'report_path':path,'report_sha256':verification['report_sha256'],
                              'source_fingerprint':report['source_fingerprint'],'source_sha256':source_hashes.get(row.get('source_path')),
                              'freshness':'current','compilation':'passed','axiom_audit':'passed'}
    def resolved(step,seen=None):
        ref=step.get('shared_step_ref') or step.get('result_step_ref')
        if not ref:return step
        key=(ref.get('proof_id',ref.get('result_id')),ref['step_id']);seen=seen or set()
        if key in seen:return step
        target=next((s for s in PROOF_REGISTRY.get(key[0],{}).get('proof_steps',[]) if s.get('id')==key[1]),step)
        return resolved(target,seen|{key})
    def attach_actual(item):
        name=item.get('declaration');row=rows.get(name) if isinstance(name,str) else None
        if not row:
            item['evidence_status']='unavailable'
            item.setdefault('explanation','尚未取得该声明的实际类型与源码记录；本步不宣称已形式化。');return
        path=row.get('source_path');line=row.get('line');item.update(source_path=path,line=line,signature=row.get('signature'))
        if path and isinstance(line,int) and line>0 and row.get('signature') and (ROOT/path).is_file():
            source=project_file(path);record(source);lines=source.read_text().splitlines();start=line-1;end=len(lines)
            if start>=end:raise ValueError(f'Declaration line outside current source: {name}')
            for j in range(start+1,len(lines)):
                if re.match(r'^(?:@\[[^]]+\]\s*)?(?:noncomputable\s+)?(?:def|abbrev|theorem|lemma|structure)\s+',lines[j]):end=j;break
            item['lean_excerpt']='\n'.join(lines[start:end]).strip()
            evidence=provenance[name]
            if digest(source)!=evidence['source_sha256']:raise ValueError(f'Declaration source changed during build: {name}')
            if not (path.startswith('lean/HarsanyiLib/Harsanyi/') or path.startswith('research/full-proof-integration-20260930/') or path.startswith('research/reader-v2-20260930/math/') or path.startswith('corpus/public/reader/')) or '/experimental/' in path:
                raise ValueError(f'Step requested a non-public source: {name}')
            report_file=project_file(evidence['report_path'])
            item.update(evidence_status='current',evidence=evidence,
                        public_source_path=publish(source,'files/lean/'+digest(source)[:12]+'-'+source.name),
                        public_report_path=publish(report_file,'files/lean/'+digest(report_file)[:12]+'-'+report_file.name))
        else:
            item['evidence_status']='unavailable'
            item['explanation']='该声明缺少当前实际类型或源码行号；本步不宣称已形式化。'
    for proof in all_proofs:
        lean=proof.setdefault('lean',{'status':'not_formalized','declarations':[]})
        maps=lean.setdefault('step_map',[]);known={(m.get('step_id'),m.get('declaration')) for m in maps if isinstance(m.get('declaration'),str)}
        for item in maps:attach_actual(item)
        for raw in proof.get('proof_steps',[]):
            step=resolved(raw)
            for ref in step.get('lean_refs',[]):
                name=ref if isinstance(ref,str) else ref.get('declaration',ref.get('name'))
                if not name or (raw.get('id'),name) in known:continue
                item={'step_id':raw.get('id'),'title':step.get('title',''),'declaration':name,'explanation':'本步调用该声明。其参数和前提见下面实际Lean类型；本条编译范围仍由顶部状态说明。'}
                attach_actual(item)
                maps.append(item);known.add((raw.get('id'),name))


def proof_body_present(proof: dict) -> bool:
    steps = proof.get("proof_steps", [])
    def body(step,visited):
        if not isinstance(step,dict):return False
        if str(step.get('body_md','')).strip() or step.get('formula_tex'):return True
        ref=step.get('shared_step_ref') or step.get('result_step_ref')
        if not ref:return False
        key=(ref.get('proof_id',ref.get('result_id')),ref.get('step_id'))
        if key in visited:return False
        source=next((s for s in PROOF_REGISTRY.get(key[0],{}).get('proof_steps',[]) if s.get('id')==key[1]),{})
        return body(source,visited|{key})
    return bool(steps) and all(body(step,set()) for step in steps)


def status_complete(result: dict, shared_by_id: dict[str, dict]) -> bool:
    # Reading completeness is separate from original-statement alignment. Only
    # an explicit positive rewrite status and actual proof text can establish it.
    if result.get("rewrite_status") != "complete" or not (result.get("statement_tex") or result.get("statement_md")):
        return False
    if result.get('rewrite_role','proof')!='proof':return False
    shared_ids = result.get("shared_proof_ids") or ([result["shared_proof_id"]] if result.get("shared_proof_id") else [])
    if shared_ids:
        return proof_body_present(result) and all(shared_by_id.get(s,{}).get("rewrite_status") == "complete" and proof_body_present(shared_by_id.get(s,{})) for s in shared_ids)
    return proof_body_present(result)


def check_status_contract() -> list[dict]:
    proof = {"id": "reviewed-proof", "rewrite_status": "complete", "proof_steps": [{"body_md": "A complete public derivation."}]}
    shared = {proof["id"]: proof}
    cases = [
        ("not_started with a candidate proof id is pending", {"rewrite_status": "not_started", "shared_proof_id": proof["id"], "statement_tex": "x=x", "proof_steps": [{"body_md": "candidate adaptation"}]}, False),
        ("unknown rewrite status with proof id is pending", {"rewrite_status": "unknown", "shared_proof_id": proof["id"], "statement_tex": "x=x", "proof_steps": [{"body_md": "candidate adaptation"}]}, False),
        ("complete metadata without actual body is pending", {"rewrite_status": "complete", "statement_tex": "x=x", "shared_proof_id": proof["id"]}, False),
        ("complete component with real shared body is complete", {"rewrite_status": "complete", "shared_proof_id": proof["id"], "statement_tex": "x=x", "proof_steps": [{"body_md": "explicit component adaptation"}]}, True),
    ]
    records = []
    for name, candidate, expected in cases:
        actual = status_complete(candidate, shared)
        if actual != expected:
            raise AssertionError(name)
        records.append({"name": name, "passed": True, "reading_status": "complete" if actual else "pending"})
    return records


def check_lean_contract(math_data: dict) -> list[dict]:
    reviewed = next((result["lean"] for result in math_data.get("results", []) if result.get("lean", {}).get("report_path") and result["lean"].get("declarations")), None)
    if not reviewed or not (ROOT / reviewed['report_path']).is_file():
        return [{"name":"unavailable reports cannot claim verified Lean","passed":True}]
    report = json.loads(project_file(reviewed["report_path"]).read_text(encoding="utf-8"))
    checks = []
    current = verify_lean(reviewed)
    if current["status"] != "verified":
        # A later source edit must downgrade the evidence, not prevent a reading
        # snapshot from being built. Negative fixtures need a current baseline.
        return [{"name": "non-current evidence is not advertised as compiled", "passed": current["status"] in {"stale", "unavailable"}, "effective_status": current["status"]}]
    checks.append({"name": "current compiled declaration and approved axioms are verified", "passed": True})
    with tempfile.TemporaryDirectory(prefix="lean-status-fixtures-", dir=EVIDENCE) as fixture_dir:
        fixture = Path(fixture_dir) / "report.json"
        variants = []
        stale = copy.deepcopy(report)
        stale["source_files"][0]["sha256"] = "0" * 64
        variants.append(("stale source cannot inherit compiled metadata", stale, reviewed["declarations"], "stale"))
        failed = copy.deepcopy(report)
        failed["commands"][0]["exit_code"] = 1
        variants.append(("failed command cannot inherit compiled metadata", failed, reviewed["declarations"], "unavailable"))
        bad_axiom = copy.deepcopy(report)
        selected = {item if isinstance(item, str) else item.get("name") for item in reviewed["declarations"]}
        for declaration in bad_axiom["declarations"]:
            if declaration["name"] in selected:
                declaration["axioms"].append("sorryAx")
        variants.append(("unapproved axiom cannot inherit compiled metadata", bad_axiom, reviewed["declarations"], "unavailable"))
        variants.append(("missing exact declaration cannot inherit compiled metadata", report, ["ReaderV2.missing_declaration"], "unavailable"))
        for name, altered, names, expected in variants:
            fixture.write_text(json.dumps(altered, ensure_ascii=False), encoding="utf-8")
            candidate = {**reviewed, "status": "verified", "compiled": True, "report_path": fixture.relative_to(ROOT).as_posix(), "declarations": names}
            actual = verify_lean(candidate)["status"]
            if actual != expected:
                raise AssertionError(name)
            checks.append({"name": name, "passed": True, "effective_status": actual})
        INPUTS.pop(fixture.relative_to(ROOT).as_posix(), None)
    return checks


def build(allow_incomplete_language=False,allow_incomplete_content=False) -> dict:
    global PAPER_IDS
    configured=load_manifest(read_json)
    PAPER_IDS={item['paper_id'] for item in configured['papers']}
    record(WORK/'input_manifest.py')
    record(WORK/'evidence_paths.py')
    record(Path(__file__).resolve())
    SITE.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    aggregate_report=read_json(EVIDENCE/'aggregate-report.json')
    for bound in aggregate_report['inputs']:
        path=project_file(bound['path'])
        if digest(path)!=bound['sha256']:raise ValueError('Aggregate input changed; rebuild aggregate: '+bound['path'])
        record(path)
    for path,expected in aggregate_report['output_sha256'].items():
        if digest(project_file(path))!=expected:raise ValueError('Aggregate output changed: '+path)
    paper_data = read_json(WORK / "data/papers.json")
    math_data = read_json(WORK / "data/math-content.json")
    papers = copy.deepcopy(paper_data["papers"])
    math_content = {key: copy.deepcopy(math_data[key]) for key in ("schema_version", "language", "notation", "shared_proofs", "results") if key in math_data}
    contract_checks = check_status_contract() + check_lean_contract(math_data)
    full_data=read_json(WORK / 'data/full-content.json')
    from check_completion import completion_report
    completion=completion_report(full_data)
    write_json(EVIDENCE/'content-completion-checks.json',completion)
    record(WORK/'check_completion.py')
    preservation_baseline=WORK/'evidence/six-paper-preservation-baseline.json'
    if preservation_baseline.is_file():record(preservation_baseline)
    if completion['inventory_contract_errors']:raise ValueError('Invalid proof denominator: '+ '; '.join(completion['inventory_contract_errors'][:20]))
    if completion['incomplete'] and not allow_incomplete_content:raise ValueError('Unfinished proof targets: '+', '.join(x['id'] for x in completion['incomplete']))
    from bilingual import validate_translations
    language_check=validate_translations(full_data,strict=not allow_incomplete_language)
    record(WORK/'bilingual.py')
    PROOF_REGISTRY.update({p['id']:p for p in math_content.get('results',[])+math_content.get('shared_proofs',[])})
    shared_value = math_content.get("shared_proofs", [])
    shared_by_id = {proof["id"]: proof for proof in shared_value} if isinstance(shared_value, list) else shared_value
    if len(papers) != len(PAPER_IDS) or {p["id"] for p in papers} != PAPER_IDS:
        raise ValueError("This snapshot must contain precisely the configured formal papers")
    page_requests: dict[str, set[int]] = {}
    for result in math_content.get("results", []):
        for ref in result.get("source_refs", []):
            if isinstance(ref, str):
                continue
            source_id = ref.get("source_id", ref.get("id"))
            for location in ref.get("locations", []):
                page = location.get("pdf_page") if isinstance(location, dict) else None
                if isinstance(page, int):
                    page_requests.setdefault(source_id, set()).add(page)
    source_page_records = []
    # Official PDFs have independent page numbering; every inventoried
    # page has a real inline source image, including reference/nonproof pages.
    for inventory in full_data['inventories']:
        for audit in inventory['page_audit']:
            page_requests.setdefault(audit['source_id'],set()).add(audit['pdf_page'])
    enrich_step_maps(math_content)
    page_cache_path = EVIDENCE / "source-pages-manifest.json"
    page_cache = json.loads(page_cache_path.read_text(encoding="utf-8")).get("pages", []) if page_cache_path.exists() else []
    accepted_cache_path=WORK/'evidence/source-pages-manifest.json'
    accepted_cache=json.loads(accepted_cache_path.read_text()).get('pages',[]) if accepted_cache_path.exists() else []
    for paper in papers:
        if paper.get("visibility") != "public" or paper.get("publication_status") != "published":
            raise ValueError(f"Non-public or non-formal paper: {paper['id']}")
        for source in paper["sources"]:
            if source.get("visibility") != "public" or source.get("publication_status") != "published":
                raise ValueError(f"Non-public or non-formal source: {source['id']}")
            source_file = project_file(source["local_path"])
            source["public_path"] = publish(source_file, "files/papers/" + source["id"] + ".pdf", expected=source["sha256"])
            source["page_images"] = {}
            for page_number in sorted(page_requests.get(source["id"], set())):
                if not 1 <= page_number <= source["total_pages"]:
                    raise ValueError(f"PDF page outside formal source: {source['id']}:{page_number}")
                cache_image = EVIDENCE / "source-pages" / f"{source['id']}-p{page_number:02}.png"
                cached=next((item for item in page_cache if item['source_id']==source['id'] and item['pdf_page']==page_number and item['pdf_sha256']==source['sha256']),None)
                if cached and cached.get('cache_path'):cache_image=guarded_project_path(cached['cache_path'],required=False)
                valid = cache_image.exists() and any(item["source_id"] == source["id"] and item["pdf_page"] == page_number and item["pdf_sha256"] == source["sha256"] and item["image_sha256"] == digest(cache_image) for item in page_cache)
                if not valid:
                    accepted=WORK/'evidence/source-pages'/cache_image.name
                    reused=next((item for item in accepted_cache if item['source_id']==source['id'] and item['pdf_page']==page_number and item['pdf_sha256']==source['sha256'] and accepted.is_file() and item['image_sha256']==digest(accepted)),None)
                    if reused:cache_image=accepted;valid=True
                if not valid:
                    cache_image=EVIDENCE/'source-pages'/f"{source['id']}-p{page_number:02}.png"
                    cache_image.parent.mkdir(parents=True, exist_ok=True)
                    subprocess.run(["pdftoppm", "-f", str(page_number), "-l", str(page_number), "-r", "110", "-png", "-singlefile", str(source_file), str(cache_image.with_suffix(""))], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                source["page_images"][str(page_number)] = publish(cache_image, "files/source-pages/" + cache_image.name)
                source_page_records.append({"source_id": source["id"], "pdf_page": page_number, "pdf_sha256": source["sha256"], "render_dpi": 110, "image_sha256": digest(cache_image),'cache_path':cache_image.relative_to(ROOT).as_posix()})
            source.pop("local_path", None)
        for key in ("candidate_id", "selection_status", "review_status", "user_approval_status", "version_label"):
            paper.pop(key, None)
    all_results = math_content.get("results", [])
    math_content["results"] = [r for r in all_results if r.get("publication_status") != "experimental_not_published" and r.get("status") != "experimental_not_published" and r.get("id") != "library-or-reconstruction"]
    source_ids = {s["id"] for p in papers for s in p["sources"]}
    transcript_by_paper: dict[str, list[dict]] = {}
    excerpt_metadata = WORK / "data/source-excerpts/metadata.json"
    if excerpt_metadata.exists():
        excerpts = read_json(excerpt_metadata)
        seen_transcripts = set()
        for excerpt in excerpts.get("excerpts", []):
            path = excerpt.get("transcription_path")
            if not path or path in seen_transcripts or excerpt.get("paper_id") not in PAPER_IDS:
                continue
            if excerpt.get("visibility") != "public" or excerpt.get("source_id") not in source_ids:
                raise ValueError("A formula transcript is outside the formal source whitelist")
            seen_transcripts.add(path)
            source = project_file(path)
            public_path = publish(source, "files/transcripts/" + source.name, expected=excerpt.get("transcription_sha256"))
            transcript_by_paper.setdefault(excerpt["paper_id"], []).append({"public_path": public_path, "raw_text": source.read_text(encoding="utf-8"), "label": "选定公式的 PDF 核对转录", "source_format": "agent_transcription_not_author_tex"})
    for result in math_content["results"]:
        if result.get("paper_id") not in PAPER_IDS | {None}:
            raise ValueError(f"Unexpected paper id: {result['id']}")
        for ref in result.get("source_refs", []):
            source_id = ref if isinstance(ref, str) else ref.get("source_id", ref.get("id"))
            if source_id not in source_ids:
                raise ValueError(f"Unknown formal source: {result['id']}: {source_id}")
        if result.get("rewrite_status") not in {"complete", "not_started", "in_progress", "blocked_by_source_issue", "not_applicable", "statement_refuted", "not_a_proof_target", "complete_empirical_explanation", "complete_external_reference_explanation", "complete_with_scope_issue", "complete_with_definition_only_counterexample", "complete_with_original_domain_issue"}:
            raise ValueError(f"Explicit rewrite_status is required: {result['id']}")
        result["reading_status"] = "complete" if status_complete(result, shared_by_id) else "pending"
        if result.get('rewrite_status') in {'complete','complete_with_scope_issue','complete_with_definition_only_counterexample','complete_with_original_domain_issue'} and result.get('rewrite_role') in {'statement_scope_explanation','partial_component','partial_proof_with_refuted_clause'} and proof_body_present(result):
            result['reading_status']='scope_explanation_complete'
        if result["rewrite_status"] == "complete" and result["reading_status"] != "complete":
            if result['reading_status']!='scope_explanation_complete':
                result['rewrite_status']='in_progress'
                result['completion_check_note']='完整共享证明或适配正文尚未交付。'
        if result.get("lean"):
            public_lean(result["lean"])
            if result.get('verification_role')=='counterexample':
                result['lean']['verification_role']='counterexample'
                result['lean']['label']='反例已验证；原命题未证明' if result['lean']['compiled'] else '反例核验；原命题未证明'
    shared_proofs = math_content.get("shared_proofs", [])
    for proof in shared_proofs if isinstance(shared_proofs, list) else shared_proofs.values():
        proof['is_shared_proof']=True
        proof['proof_target']=True
        proof['reading_status']='complete' if proof.get('rewrite_status')=='complete' and proof_body_present(proof) else 'pending'
        if proof.get("lean"):
            public_lean(proof["lean"])
    for paper in papers:
        complete = [r for r in math_content["results"] if r.get("paper_id") == paper["id"] and r["reading_status"] == "complete"]
        paper['complete_rewrite_count']=len(complete)

    documentation = []
    for source_name, label, target in [
        ("docs/paper-agent-data-model.md", "数据关系与 Paper2Agent 参考", "files/paper-agent-data-model.md"),
        ("docs/agent-extension-workflow.md", "新增论文的处理流程", "files/agent-extension-workflow.md"),
        ("docs/library-api.md", "独立公共模块与准确适用条件", "files/library-api.md"),
        ("docs/ai-use-library.md", "AI 调用公共库与实际消费示例", "files/ai-use-library.md"),
        ("reader/architecture/paper_agent.py", "只读命令行工具（项目内运行）", "files/paper_agent.py"),
        ("reader/architecture/v2_verification_helper.py", "源指纹与声明证据检查", "files/v2_verification_helper.py"),
        ("reader/architecture/agent-package.json", "可核验的数据包", "files/agent-package.json"),
        ("reader/architecture/package.schema.json", "数据包结构定义", "files/package.schema.json"),
        ("reader/architecture/full-content.schema.json", "全文内容结构定义", "files/full-content.schema.json"),
        ("reader/data/full-content.json", "全篇目录与数学内容", "files/full-content.json"),
        ("corpus/public/reader/input-manifest.json", "显式正式论文配置", "files/input-manifest.json"),
        ("catalog/library.json", "公共库真实API目录", "files/library.json"),
        ("docs/math-conventions.md", "数学记号约定", "files/math-conventions.md"),
        ("docs/human-to-lean.md", "中文证明到Lean对照", "files/human-to-lean.md"),
        ("docs/reviews/full-integration-root-crosscheck-20260930.md", "根代理独立交叉核对记录", "files/root-crosscheck.md"),
    ]:
        source = ROOT / source_name
        if source.exists():
            documentation.append({"label": label, "public_path": publish(source, target)})
    # Export individual artifacts pinned by the actual current catalog. Never
    # publish a report directory or traverse an unrelated archive/inbox.
    catalog=read_json(ROOT/'catalog/library.json')
    library_report_path=catalog['verification_report']
    library_report_file=project_file(library_report_path)
    library_report=read_json(library_report_file)
    library_artifacts={'version':catalog['library_version'],
                       'report':publish(library_report_file,'files/lean/'+digest(library_report_file)[:12]+'-'+library_report_file.name),
                       'source_files':[],'command_logs':[]}
    used_sources={d['source_path'] for d in catalog['declarations']}
    used_sources.add('lean/HarsanyiLib/Harsanyi.lean')
    for row in library_report['source_files']:
        if row['path'] not in used_sources:continue
        source=project_file(row['path'])
        library_artifacts['source_files'].append({'path':row['path'],'sha256':row['sha256'],
            'public_path':publish(source,'files/lean/'+digest(source)[:12]+'-'+source.name,expected=row['sha256'])})
    for command in library_report['commands']:
        path=command.get('log_path')
        if not path:continue
        source=project_file(path)
        if source.parent!=library_report_file.parent:raise ValueError('Command log is outside the selected public report')
        library_artifacts['command_logs'].append({'label':source.name,'sha256':digest(source),
            'public_path':publish(source,'files/lean/'+digest(source)[:12]+'-'+source.name)})
    issue_data = []
    issues_path = WORK / "math/issues.json"
    if issues_path.exists():
        issues = read_json(issues_path)
        issue_data = issues.get("issues", []) + issues.get("alignment_notes", []) if isinstance(issues, dict) else issues
        publish(issues_path, "files/source-issues.json")
        if (WORK / "math/issues.md").exists():
            publish(WORK / "math/issues.md", "files/source-issues.md")
        for issue in issue_data:
            issue["public_path"] = "/reviews/" + issue["id"] + "/"
        issue_map = {i["id"]: i for i in issue_data}
        for result in math_content["results"]:
            refs = result.get("issue_refs", result.get("issues", result.get("related_issue_ids", [])))
            if result["reading_status"] != "complete":
                refs = list(refs) + list(result.get("alignment_note_ids", []))
            mapped = []
            for ref in refs:
                issue_id = ref if isinstance(ref, str) else ref.get("id", ref.get("issue_id"))
                issue = copy.deepcopy(issue_map.get(issue_id, ref if isinstance(ref, dict) else {}))
                if issue:
                    issue["public_path"] = issue.get("public_path", "/files/source-issues.md")
                    mapped.append(issue)
            if mapped:
                result["issues"] = mapped

    requested_failures=[p['id'] for p in math_content['results']+math_content['shared_proofs'] if p.get('lean',{}).get('requested_compilation_status') in {'verified','compiled','passed','partial_scope_verified','counterexample_verified','partial'} and not p['lean'].get('compiled')]
    stale_step_failures=[p['id']+':'+str(m.get('step_id')) for p in math_content['results']+math_content['shared_proofs'] if p.get('lean',{}).get('requested_compilation_status') in {'verified','compiled','passed','partial_scope_verified','counterexample_verified','partial'} for m in p['lean'].get('step_map',[]) if m.get('declaration') and m.get('evidence_status')!='current']
    write_json(EVIDENCE/'requested-lean-checks.json',{'status':'failed' if requested_failures or stale_step_failures else 'passed','unavailable_requested_compilations':requested_failures,'noncurrent_requested_steps':stale_step_failures})
    if not allow_incomplete_content and (requested_failures or stale_step_failures):raise ValueError('Requested Lean evidence is not current: '+', '.join((requested_failures+stale_step_failures)[:20]))
    from lean_english import attach_lean_english
    lean_language_check=attach_lean_english(math_content)
    record(WORK/'lean_english.py')
    write_json(EVIDENCE/'lean-bilingual-checks.json',lean_language_check)
    if not allow_incomplete_language and lean_language_check['missing']:raise ValueError('Incomplete English evidence explanations: '+', '.join(lean_language_check['missing'][:20]))
    data = {"schema_version": "3.0", "papers": papers, "math": math_content, "documentation": documentation,
            'inventories':full_data['inventories'],'coverage':full_data['coverage'],'symbols':full_data['symbols'],
            'library_artifacts':library_artifacts,
            "formula_transcripts": transcript_by_paper,
            "issues": [{"label": i.get("title", i.get("id")), "public_path": i["public_path"]} for i in issue_data],
            "review_records": issue_data,
            "cli_example": "python reader/architecture/paper_agent.py search Shapley"}
    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    if any(marker in serialized for marker in ("manual-maintext", "inbox/", "unpublished", "/experimental/")):
        raise ValueError("Private or experimental identifier reached the served reading data")
    write_json(SITE / "data.public.json", data)
    (SITE / "data.public.js").write_text("window.READER_V2_DATA = " + serialized.replace("</", "<\\/") + ";\n", encoding="utf-8")
    for filename in ("reader.js", "reader.css"):
        publish(WORK / "ui" / filename, filename)
    template = (WORK / "ui/index.html").read_text(encoding="utf-8")
    record(WORK / "ui/index.html")
    pages = []

    def page(relative: str, title: str, kind: str, **route: str) -> None:
        destination = SITE / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        attrs = " ".join(f'data-{key.replace("_", "-")}="{html.escape(value, quote=True)}"' for key, value in {"page_kind": kind, **route}.items())
        content = template.replace("<body>", "<body " + attrs + ">").replace("<title>论文与证明</title>", "<title>" + html.escape(title) + " · 论文与证明</title>")
        destination.write_text(content, encoding="utf-8")
        pages.append({"path": relative, "kind": kind, "title": title, **route})

    page("index.html", "论文", "home")
    page("about/index.html", "给 AI 与维护者", "about")
    page("symbols/index.html", "符号表", "symbols")
    for paper in papers:
        page(f"papers/{paper['id']}/index.html", paper["title"], "paper", paper_id=paper["id"])
    for result in math_content["results"]:
        paper_id = result.get("paper_id")
        path = f"papers/{paper_id}/results/{result['id']}/index.html" if paper_id else f"library/{result['id']}/index.html"
        page(path, result["title"], "result", result_id=result["id"], **({"paper_id": paper_id} if paper_id else {}))
    for proof in shared_proofs:
        page(f"proofs/{proof['id']}/index.html",proof['title'],'shared',proof_id=proof['id'])
    for issue in issue_data:
        page(f"reviews/{issue['id']}/index.html", issue["title"], "review", review_id=issue["id"])
    # Only the small, already-local KaTeX distribution is copied. Browser runtimes
    # and installed Python packages remain in the old tooling directory.
    vendor = ROOT / "web/static/vendor/katex"
    if not (vendor / "katex.min.js").exists():
        raise ValueError("Local KaTeX distribution is unavailable")
    for source in vendor.rglob("*"):
        if source.is_file() and source.suffix in {".js", ".css", ".woff2", ".woff", ".ttf", ".txt"}:
            publish(source, "vendor/katex/" + source.relative_to(vendor).as_posix())
    allowed = {p["path"] for p in pages} | set(PUBLIC_FILES) | {"data.public.js", "data.public.json"}
    stale = [p for p in SITE.rglob("*") if p.is_file() and p.relative_to(SITE).as_posix() not in allowed]
    for path in stale:
        path.unlink()  # Generated preview copies only; never any original source.
    generated = datetime.now(timezone.utc).isoformat()
    complete_count = sum(r["reading_status"] == "complete" and bool(r.get("proof_target")) and r.get("rewrite_role")=="proof" and bool(r.get("paper_id")) for r in math_content["results"])
    record_value = {"generated_at": generated, "visibility": "public", "paper_count": len(papers), "result_page_count": len(math_content["results"]),
                    "rewritten_paper_result_count": complete_count, "pages": pages, "inputs": sorted(INPUTS.values(), key=lambda x: x["path"]),
                    "public_file_allowlist": sorted(PUBLIC_FILES.values(), key=lambda x: x["path"]), "private_or_experimental_exported": False}
    write_json(EVIDENCE / "build-manifest.json", record_value)
    write_json(page_cache_path, {"pages": source_page_records})
    write_json(EVIDENCE / "status-contract-checks.json", {"status": "passed", "checks": contract_checks, "lean_verification": VERIFICATION_CHECKS})
    baseline_path = EVIDENCE / "production-baseline.json"
    if not baseline_path.exists():
        watched = {}
        for directory in ("src/archive", "web", "corpus/public", "lean/HarsanyiLib/Harsanyi", "lean/PaperProofs/PaperProofs"):
            for path in sorted((ROOT / directory).rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    watched[path.relative_to(ROOT).as_posix()] = digest(path)
        write_json(baseline_path, {"generated_at": generated, "files": watched})
    return {"status": "built", "papers": len(papers), "result_pages": len(math_content["results"]), "rewritten_paper_results": complete_count,
            "preview": str(SITE), "shared_proofs": len(shared_proofs)}


if __name__ == "__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--allow-incomplete-content',action='store_true',help='Development preview only; rejects unfinished proof targets by default.')
    parser.add_argument('--allow-incomplete-language',action='store_true',help='Development preview only; do not claim bilingual acceptance.')
    print(json.dumps(build(**vars(parser.parse_args())), ensure_ascii=False))
