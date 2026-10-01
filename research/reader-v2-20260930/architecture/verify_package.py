#!/usr/bin/env python3
"""Fixed local verification commands; not exposed as an agent tool."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from paper_agent import BASE, PROJECT_ROOT, PaperPackage, digest, fingerprint


def main():
    output_dir = BASE / "verification"
    output_dir.mkdir(exist_ok=True)
    rel = BASE.relative_to(PROJECT_ROOT).as_posix()
    commands = [
        ("build-package", [sys.executable,f"{rel}/build_package.py"],0),
        ("validate", [sys.executable,f"{rel}/paper_agent.py","validate"],0),
        ("integrity-tests", [sys.executable,"-m","unittest","discover","-s",rel,"-p","test_paper_agent.py","-v"],0),
        ("query", [sys.executable,f"{rel}/paper_agent.py","query","--paper","iclr2024-sparse"],0),
        ("get-result", [sys.executable,f"{rel}/paper_agent.py","get-result","cvpr2023-reconstruction"],0),
        ("dependencies", [sys.executable,f"{rel}/paper_agent.py","dependencies","iclr2024-generalizable-and","--depth","2"],0),
        ("parent-status", [sys.executable,f"{rel}/paper_agent.py","verification-status","iclr2024-generalizable-andor"],0),
        ("selected-resource", [sys.executable,f"{rel}/paper_agent.py","get-resource","res-proof-finite-mobius-reconstruction-v2"],0),
        ("closed-parameters", [sys.executable,f"{rel}/paper_agent.py","invoke","query",'{"text":"","shell":"not-executed"}'],2),
    ]
    records = []
    for name,argv,expected in commands:
        proc=subprocess.run(argv,cwd=PROJECT_ROOT,text=True,capture_output=True,shell=False)
        log=output_dir/f"{name}.log"
        log.write_text(proc.stdout+proc.stderr,encoding="utf-8")
        records.append({"name":name,"cwd":str(PROJECT_ROOT),"argv":argv,"exit_code":proc.returncode,
                        "expected_exit_code":expected,"passed":proc.returncode==expected,
                        "log_path":log.relative_to(PROJECT_ROOT).as_posix()})
    package=PaperPackage()
    inputs = [BASE/name for name in ["paper_agent.py","build_package.py","test_paper_agent.py","verify_package.py",
                                      "package.schema.json","agent-package.json","source-alignment-review.md"]]
    inputs += [PROJECT_ROOT / package.data["data_files"][key] for key in package.data["data_files"]]
    inputs += [PROJECT_ROOT / source["local_path"] for source in package.data["sources"]]
    inputs += [PROJECT_ROOT / path for path in ["docs/paper-agent-data-model.md","docs/agent-extension-workflow.md",
                                                "research/reader-v2-20260930/math/verification/report.json",
                                                "research/reader-v2-20260930/math/issues.json",
                                                "research/reader-v2-20260930/math/lean/ReaderAdapters.lean"]]
    source_files=[{"path":path.relative_to(PROJECT_ROOT).as_posix(),"sha256":digest(path)}
                  for path in sorted(set(inputs),key=str)]
    status="passed" if all(c["passed"] for c in records) else "failed"
    report={"schema_version":"2.0","status":status,"generated_at":datetime.now(timezone.utc).isoformat(),
            "scope":"local package integrity and read-only tools; independent source alignment record is separate",
            "commands":records,"source_files":source_files,"source_fingerprint":fingerprint(source_files),
            "validation":package.validate(),"integrity_test_count":12,
            "negative_cases":["private derivatives/edges/resources excluded","stale source hashes",
                              "failed command","missing declaration","missing axioms","sorryAx rejected",
                              "unsupported schema keyword","foreign-key/version mismatch","duplicate appearance semantics",
                              "closed tool parameters","unsafe path/symlink rejected","component does not verify parent"],
            "mcp_server_implemented":False,"production_migration_implemented":False,
            "private_test_data":"in-memory synthetic records only; no unpublished user file accessed",
            "source_alignment_review":f"{rel}/source-alignment-review.md"}
    (output_dir/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":status,"commands":len(records),"integrity_tests":12,
                      "report_path":(output_dir/"report.json").relative_to(PROJECT_ROOT).as_posix()},ensure_ascii=False))
    return 0 if status=="passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
