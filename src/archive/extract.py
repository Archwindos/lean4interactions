"""Conservative local candidate extraction; completeness always needs review."""
from __future__ import annotations

import re
from pathlib import Path

from .util import ArchiveError, digest_data, identifier, load_data, resolve_root, safe_path, sha256, utcnow, write_data, write_text

LABEL = re.compile(r"(?im)^\s*(?:#{1,6}\s*)?(?:\*\*)?((?:Theorem|Lemma|Proposition|Corollary|Property|Claim|Definition|Assumption|定理|引理|命题|推论|性质|定义|假设)\s*[A-Za-z]?\.?\d*(?:\.\d+)*[^\n]{0,100})")
TEX = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|claim|definition|assumption|property)\}(?:\[([^\]]*)\])?(.*?)\\end\{\1\}", re.S)


def _candidates(text: str, suffix: str) -> list[dict]:
    matches = list(TEX.finditer(text)) if suffix == ".tex" else []
    items = []
    if matches:
        for index, match in enumerate(matches):
            label = match.group(2) or f"{match.group(1)} (source occurrence {index + 1})"
            items.append({"label": label, "kind": match.group(1), "statement": match.group(3).strip(), "offset": match.start(), "line": text.count("\n", 0, match.start()) + 1})
    else:
        matches = list(LABEL.finditer(text))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            block = text[match.start():end].strip()
            label = match.group(1).strip().strip("*")
            kind = "definition" if re.match(r"(?i)(Definition|定义)", label) else "assumption" if re.match(r"(?i)(Assumption|假设)", label) else "claim"
            items.append({"label": label, "kind": kind, "statement": block[:20000], "offset": match.start(), "line": text.count("\n", 0, match.start()) + 1})
    return items


def extract_paper(root: str | Path | None, paper_id: str, version: str | None = None, *, collection: str = "public") -> dict:
    from .store import ArchiveStore
    root = resolve_root(root)
    paper_id = identifier(paper_id, "paper_id")
    store = ArchiveStore(root, collection=collection)
    paper = store.get_paper(paper_id, version)
    if not paper:
        raise ArchiveError(f"Unknown paper: {paper_id}")
    version = paper["version"]
    directory = safe_path(root, f"{store.corpus_prefix}/papers/{paper_id}/{version}")
    inventory = dict(paper["inventory"])
    previous_items = {item.get("claim_id"): item for item in inventory.get("items", [])}
    items = []
    issues = []
    extracted = []
    for entry in paper["manifest"].get("files", []):
        source = safe_path(root, directory / entry["path"], must_exist=True)
        if sha256(source) != entry.get("sha256"):
            raise ArchiveError(f"Source checksum changed: {entry['path']}")
        suffix = source.suffix.lower()
        chunks = []
        try:
            if suffix == ".pdf":
                from pypdf import PdfReader
                reader = PdfReader(source)
                for number, page in enumerate(reader.pages, 1):
                    chunks.append((number, page.extract_text() or ""))
                if not any(text.strip() for _, text in chunks):
                    issues.append(f"{entry['path']}: no PDF text; local OCR/manual review required")
            elif suffix in {".tex", ".md", ".markdown", ".txt"}:
                chunks = [(None, source.read_text(encoding="utf-8", errors="replace"))]
            else:
                continue
        except Exception as exc:
            issues.append(f"{entry['path']}: text extraction failed ({type(exc).__name__}: {exc})")
            continue
        text_content = "\n\n".join(f"[PDF page {page}]\n{text}" if page else text for page, text in chunks)
        text_relative = f"extracted/{Path(entry['path']).relative_to('sources').as_posix()}.txt"
        write_text(safe_path(root, directory / text_relative), text_content)
        extracted.append({"source_path": entry["path"], "text_path": text_relative, "source_sha256": entry["sha256"]})
        for page, text in chunks:
            for candidate in _candidates(text, suffix):
                claim_id = "claim-" + digest_data([paper_id, version, entry["path"], page, candidate["offset"], candidate["label"]])[:24]
                location = {"file": entry["path"], "pdf_page": page, "printed_page": None, "section": None, "line": candidate["line"] if suffix != ".pdf" else None, "offset": candidate["offset"]}
                claim_dir = safe_path(root, f"{store.corpus_prefix}/claims/{claim_id}")
                metadata_file = claim_dir / "metadata.yaml"
                if not metadata_file.exists():
                    metadata = {"schema_version": 1, "claim_id": claim_id, "paper_id": paper_id, "paper_version": version, "source_location": location, "original_label": candidate["label"], "kind": candidate["kind"], "theorem_ids": [], "proof_ids": [], "review_status": "candidate", "extraction_status": "candidate", "rewriting_status": "not_started", "alignment_status": "not_reviewed", "visibility": paper.get("visibility", "private"), "source_sha256": entry["sha256"], "issues": ["Automatically detected candidate; statement/proof boundaries and completeness require human review."]}
                    write_data(metadata_file, metadata)
                    write_text(claim_dir / "original.tex", candidate["statement"] + "\n")
                    write_data(claim_dir / "alignment.yaml", {"schema_version": 1, "status": "not_reviewed", "symbol_mapping": [], "evidence": []})
                    write_data(claim_dir / "review.yaml", {"schema_version": 1, "status": "pending", "issues": metadata["issues"]})
                item = previous_items.get(claim_id, {"claim_id": claim_id, "original_label": candidate["label"], "kind": candidate["kind"], "source_location": location, "review_status": "candidate", "disposition": "pending"})
                items.append(item)
    # Reviewed inventory entries remain in the denominator even if the detector changes.
    detected_ids = {item["claim_id"] for item in items}
    new_detected_ids = detected_ids - previous_items.keys()
    if new_detected_ids:
        if inventory.get("denominator_reviewed") is True:
            issues.append("New automatically detected candidates require renewed completeness review: " + ", ".join(sorted(new_detected_ids)))
        inventory.update(denominator_reviewed=False, completeness_status="not_reviewed")
    items.extend(item for cid, item in previous_items.items() if cid not in detected_ids)
    inventory.update({"schema_version": 1, "paper_id": paper_id, "paper_version": version, "items": items, "extraction_status": "candidates_generated", "extracted_at": utcnow(), "extracted_files": extracted, "issues": list(dict.fromkeys(inventory.get("issues", []) + issues + ["Completeness is not certified by automated extraction."]))})
    inventory.setdefault("completeness_status", "not_reviewed")
    inventory.setdefault("denominator_reviewed", False)
    write_data(directory / "inventory.yaml", inventory)
    return {"paper_id": paper_id, "version": version, "candidate_count": len(items), "completeness_status": inventory["completeness_status"], "issues": issues}
