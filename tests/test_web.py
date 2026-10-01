"""Route and privacy integration tests; all mathematics here is synthetic."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml
from archive.http_client import LocalAppClient

from archive.util import digest_data, sha256
from archive.web import _safe_markdown, create_app

_clients=[]
def TestClient(app):
    client=LocalAppClient(app);_clients.append(client);return client

@pytest.fixture(autouse=True)
def stop_local_servers():
    yield
    for client in _clients:client.close()
    _clients.clear()

PROJECT = Path(__file__).resolve().parents[1]


def write_yaml(root: Path, relative: str, data: dict) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


@pytest.fixture
def archive_root(tmp_path: Path) -> Path:
    root = tmp_path / "archive"
    root.mkdir()
    shutil.copytree(PROJECT / "web", root / "web")
    for paper_id, visibility, title in [
        ("public-test", "public", "测试公开论文"),
        ("private-test", "private", "秘密测试手稿"),
    ]:
        source = root / f"corpus/{visibility}/papers/{paper_id}/v1/sources/paper.tex"
        source.parent.mkdir(parents=True)
        source.write_text("Synthetic test material", encoding="utf-8")
        write_yaml(root, f"corpus/{visibility}/papers/{paper_id}/v1/manifest.yaml", {
            "schema_version": 1, "paper_id": paper_id, "version": "v1",
            "title": title, "authors": ["测试作者"], "visibility": visibility,
            "source_type": "manual", "publication_status": "unpublished",
            "files": [{"path": "sources/paper.tex", "sha256": sha256(source)}],
        })
        claim_id = paper_id + "-claim"
        write_yaml(root, f"corpus/{visibility}/papers/{paper_id}/v1/inventory.yaml", {
            "schema_version": 1, "denominator_reviewed": False,
            "completeness_status": "not_reviewed",
            "items": [{"claim_id": claim_id, "kind": "theorem"}],
        })
        write_yaml(root, f"corpus/{visibility}/claims/{claim_id}/metadata.yaml", {
            "schema_version": 1, "claim_id": claim_id, "paper_id": paper_id,
            "paper_version": "v1", "original_label": "Theorem TEST",
            "source_location": {"section": "测试节", "pdf_page": 2},
            "theorem_ids": ["test-result"], "proof_ids": ["test-proof"],
            "visibility": visibility, "alignment_status": "pending",
        })
        (root / f"corpus/{visibility}/claims/{claim_id}/original.tex").write_text("x = x", encoding="utf-8")
    write_yaml(root, "corpus/public/theorems/test-result/metadata.yaml", {
        "schema_version": 1, "theorem_id": "test-result", "title": "测试自反结论",
        "summary": "仅用于页面测试", "assumptions": ["x 是一个实数"],
        "visibility": "public", "lean_declarations": ["Test.self"],
    })
    (root / "corpus/public/theorems/test-result/statement.tex").write_text("x=x", encoding="utf-8")
    write_yaml(root, "corpus/public/theorems/test-result/proofs/test-proof/metadata.yaml", {
        "schema_version": 1, "proof_id": "test-proof", "theorem_id": "test-result",
        "title": "测试分步证明", "visibility": "public", "lean_declarations": ["Test.self"],
        "lean_dependencies": ["Test.self"],
        "steps": [{"id": "step-1", "title": "自反性", "lean_declarations": ["Test.self"]},
                  {"id": "step-2", "title": "未登记步骤", "lean_declarations": ["Test.missing"]}],
    })
    (root / "corpus/public/theorems/test-result/proofs/test-proof/proof.zh.md").write_text(
        '# 第一步\n\n<a id="step-1"></a>\n\n依据自反性，$x=x$。\n\n<script>alert(\'unsafe\')</script>', encoding="utf-8",
    )
    write_yaml(root, "corpus/public/theorems/private-derived/metadata.yaml", {
        "schema_version": 1, "theorem_id": "private-derived", "title": "秘密派生结果",
        "visibility": "public", "derived_from": ["private-test-claim"],
    })
    write_yaml(root, "corpus/private/issues/test-issue.yaml", {
        "schema_version": 1, "issue_id": "test-issue", "title": "测试问题",
        "paper_id": "private-test", "visibility": "private",
        "original_statement": "测试原文", "problem": "测试疑似问题",
        "user_confirmation": "pending", "fix_authorization": "pending",
        "evidence": "测试证据，不是真实数学审查",
    })
    source = root / "lean/HarsanyiLib/Harsanyi/Test.lean"
    source.parent.mkdir(parents=True)
    source.write_text("theorem Test.self (x : Nat) : x = x := rfl\n", encoding="utf-8")
    records = [{"path": source.relative_to(root).as_posix(), "sha256": sha256(source)}]
    fingerprint = digest_data(records)
    report = root / "reports/lean/test/report.json"
    report.parent.mkdir(parents=True)
    report.write_text(json.dumps({
        "schema_version": 1, "build_id": "synthetic-test-only", "status": "passed",
        "source_files": records, "source_fingerprint": fingerprint,
        "commands": [{"argv": ["synthetic-test"], "exit_code": 0, "log_path": "reports/lean/test/build.log"}],
        "declarations": [{"name": "Test.self", "status": "passed", "axioms": []}],
    }), encoding="utf-8")
    (report.parent / "build.log").write_text("Synthetic test log", encoding="utf-8")
    catalog = root / "catalog/library.json"
    catalog.parent.mkdir()
    catalog.write_text(json.dumps({
        "schema_version": 1, "library": "SyntheticTest", "library_version": "test",
        "source_fingerprint": fingerprint, "verification_report": "reports/lean/test/report.json",
        "declarations": [{
            "name": "Test.self", "module": "Harsanyi.Test", "signature": "(x : Nat) : x = x",
            "theorem_id": "test-result", "proof_id": "test-proof", "visibility": "public",
            "source_path": records[0]["path"], "line": 1, "axioms": [],
        }],
    }), encoding="utf-8")
    return root


def test_main_routes_and_local_formula_assets(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root))
    for route in [
        "/", "/papers", "/papers/public-test", 
        "/theorems", "/theorems/test-result", "/proofs/test-proof",
        "/claims/public-test-claim", "/library", "/library/Test.self",
        "/issues", "/search",
    ]:
        response = client.get(route)
        assert response.status_code == 200, (route, response.text)
        assert '<html lang="zh-CN">' in response.text
    for asset in [
        "/static/archive.css", "/static/archive-math.js", "/static/vendor/katex/katex.min.js",
        "/static/vendor/katex/katex.min.css", "/static/vendor/katex/contrib/auto-render.min.js",
        "/static/vendor/katex/fonts/KaTeX_Main-Regular.woff2",
    ]:
        assert client.get(asset).status_code == 200, asset
    page = client.get("/").text
    assert "https://cdn" not in page and "unpkg.com" not in page


def test_search_title_author_id_and_claim(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root))
    for query, expected in [
        ("测试公开", "public-test"), ("测试作者", "public-test"),
        ("public-test", "public-test"), ("Theorem TEST", "public-test-claim"),
    ]:
        page = client.get("/search", params={"q": query})
        assert page.status_code == 200 and expected in page.text
    assert "/library/Test.self" in client.get("/search?q=Test.self").text
    assert client.get("/search", params={"q": "a" * 501}).status_code == 400


def test_shared_proof_has_bidirectional_source_links(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root))
    proof = client.get("/proofs/test-proof").text
    assert "/claims/public-test-claim" in proof and "/claims/private-test-claim" not in proof
    assert "/theorems/test-result" in proof and "/library/Test.self" in proof
    claim = client.get("/claims/public-test-claim").text
    assert "/proofs/test-proof" in claim and "/theorems/test-result" in claim
    assert "待处理" in claim and "尚未形式化" in claim


def test_proof_body_escapes_untrusted_html(archive_root: Path) -> None:
    page = TestClient(create_app(root=archive_root)).get("/proofs/test-proof").text
    assert "<script>alert" not in page
    assert "&lt;script&gt;alert" in page
    assert 'id="step-1"' in page


def test_step_markers_are_strict_unique_and_do_not_enable_html() -> None:
    body = _safe_markdown('''# 说明

<a id="step-1"></a>
一个实际步骤。
<a id="step-1"></a>
<a id="step-4" onclick="alert(1)"></a>
<a id="unsafe"></a>
<script>alert(1)</script>
```html
<a id="step-2"></a>
```
''')
    assert body.count('id="step-1"') == 1
    assert 'id="auto-step-1"' in body
    assert 'id="step-2"' not in body and 'id="step-4"' not in body
    assert "<script" not in body and "<a " not in body
    assert "&lt;script&gt;" in body and "onclick=&quot;" in body


def test_step_links_resolve_actual_api_source_and_reverse_explanation(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root,public=False))
    page = client.get("/proofs/test-proof").text
    assert 'href="#step-1"' in page
    assert 'href="/library/Test.self#signature"' in page
    assert 'href="/library/Test.self#source"' in page
    assert 'href="#step-2"' not in page and 'href="/library/Test.missing"' not in page
    assert "正文尚无对应步骤锚点" in page and "API 目录尚无此声明" in page
    api = client.get("/library/Test.self").text
    assert 'id="signature"' in api and 'id="source"' in api
    assert 'href="/proofs/test-proof#step-1"' in api
    assert "theorem Test.self" in api
    public_page = TestClient(create_app(root=archive_root, public=True)).get("/proofs/test-proof").text
    assert 'href="/library/Test.self#signature"' in public_page
    assert 'href="/library/Test.self#source"' not in public_page
    assert "Test.missing" not in public_page


def test_stale_report_never_displays_current_validation(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root))
    assert "已过期" not in client.get("/library/Test.self").text
    (archive_root / "lean/HarsanyiLib/Harsanyi/Test.lean").write_text("-- changed\n", encoding="utf-8")
    assert "已过期" in client.get("/library/Test.self").text
    assert "已过期" in client.get("/theorems/test-result").text


def test_file_route_rejects_escape_symlink_and_metadata(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root,public=False))
    assert client.get("/files/lean/HarsanyiLib/Harsanyi/Test.lean").status_code == 200
    for path in [
        "/files/%2E%2E/PLAN.md", "/files/lean/%2E%2E/%2E%2E/PLAN.md",
        "/files//etc/passwd", "/files/corpus/claims/public-test-claim/metadata.yaml",
        "/files/.conda-env/bin/python", "/papers/%5Cbad",
    ]:
        assert client.get(path).status_code == 404, path
    # An outside-root link points to another synthetic file within pytest's
    # project-local temporary parent, never to a user's/system secret.
    outside = archive_root.parent / "outside.txt"
    outside.write_text("outside fixture", encoding="utf-8")
    (archive_root / "reports/escape.txt").symlink_to(outside)
    assert client.get("/files/reports/escape.txt").status_code == 404


def test_public_routes_remove_private_and_derived_metadata(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root, public=True))
    for route in ["/", "/papers", "/theorems", "/theorems/test-result", "/proofs/test-proof", "/library", "/issues", "/search?q=秘密"]:
        response = client.get(route)
        assert response.status_code == 200
        assert "private-test" not in response.text
        assert "秘密" not in response.text or route.startswith("/search")
        assert "private-derived" not in response.text
    for route in ["/papers/private-test", "/claims/private-test-claim", "/theorems/private-derived", "/issues/test-issue"]:
        assert client.get(route).status_code == 404
    assert client.get("/files/reports/lean/test/report.json").status_code == 404
    assert client.get("/files/lean/HarsanyiLib/Harsanyi/Test.lean").status_code == 404
    assert client.get("/files/catalog/library.json").status_code == 200


def test_issue_page_keeps_confirmation_and_fix_authorization_separate(archive_root: Path) -> None:
    client = TestClient(create_app(root=archive_root,public=False))
    page = client.get("/issues/test-issue").text
    assert "用户确认" in page and "修正授权" in page
    assert "测试原文" in page and "测试证据" in page
    assert "<button" not in page


def test_independent_claim_evidence_is_local_scoped_and_privacy_filtered(archive_root: Path) -> None:
    claim_id = "private-test-claim"
    relative = f"corpus/private/claims/{claim_id}/lean"
    base = archive_root / relative
    base.mkdir()
    source = base / "Adapter.lean"
    source.write_text("theorem Private.adapter : 1 = 1 := rfl\n", encoding="utf-8")
    (base / "build.log").write_text("Synthetic private adapter test", encoding="utf-8")
    (base / "unlisted.json").write_text('{"private": "unlisted"}', encoding="utf-8")
    (base / "sources").mkdir()
    (base / "sources/unlisted.json").write_text('{}', encoding="utf-8")
    records = [{"path": f"{relative}/Adapter.lean", "sha256": sha256(source)}]
    report = {"status": "passed", "source_files": records, "source_fingerprint": digest_data(records),
              "commands": [{"exit_code": 0, "log_path": f"{relative}/build.log"}],
              "declarations": [{"name": "Private.adapter", "status": "passed", "axioms": []}]}
    (base / "report.json").write_text(json.dumps(report), encoding="utf-8")
    metadata = archive_root / f"corpus/private/claims/{claim_id}/metadata.yaml"
    data = yaml.safe_load(metadata.read_text())
    data.update(verification_report=f"{relative}/report.json", lean_declarations=["Private.adapter"])
    write_yaml(archive_root, metadata.relative_to(archive_root).as_posix(), data)
    client = TestClient(create_app(root=archive_root,public=False))
    page = client.get(f"/claims/{claim_id}").text
    assert "独立论文应用验证" in page and "通过" in page
    for name in ("report.json", "Adapter.lean", "build.log"):
        assert f'href="/files/{relative}/{name}"' in page
        assert client.get(f"/files/{relative}/{name}").status_code == 200
    for name in ("unlisted.json", "sources/unlisted.json"):
        assert client.get(f"/files/{relative}/{name}").status_code == 404
    public = TestClient(create_app(root=archive_root, public=True))
    assert public.get(f"/claims/{claim_id}").status_code == 404
    for name in ("report.json", "Adapter.lean", "build.log"):
        assert public.get(f"/files/{relative}/{name}").status_code == 404


def test_static_export_preserves_versions_steps_and_public_visibility(archive_root: Path) -> None:
    from archive.export import export_site
    v1 = archive_root / "corpus/public/papers/public-test/v1"
    for version, title, visibility in [("v2", "公开论文第二版", "public"), ("v3", "版本私有手稿", "private")]:
        base = archive_root / f"corpus/{visibility}/papers/public-test/{version}"
        shutil.copytree(v1, base)
        metadata = yaml.safe_load((base / "manifest.yaml").read_text())
        metadata.update(version=version, title=title, visibility=visibility)
        write_yaml(archive_root, (base / "manifest.yaml").relative_to(archive_root).as_posix(), metadata)
        write_yaml(archive_root, (base / "inventory.yaml").relative_to(archive_root).as_posix(), {"items": [], "denominator_reviewed": False})
    export_site(root=archive_root, output="build/test-local-export",public=False)
    export_site(root=archive_root, output="build/test-public-export", public=True)
    local = archive_root / "build/test-local-export"
    public = archive_root / "build/test-public-export"
    assert "版本私有手稿" in (local / "papers/public-test.html").read_text()
    assert (local / "papers/public-test/v3.html").is_file()
    assert "公开论文第二版" in (public / "papers/public-test.html").read_text()
    assert "测试公开论文" in (public / "papers/public-test/v1.html").read_text()
    assert "公开论文第二版" in (public / "papers/public-test/v2.html").read_text()
    assert not (public / "papers/public-test/v3.html").exists()
    assert 'href="../papers/public-test/v1.html"' in (public / "claims/public-test-claim.html").read_text()
    proof = (public / "proofs/test-proof.html").read_text()
    assert 'href="../library/Test.self.html#signature"' in proof
    assert 'href="../proofs/test-proof.html#step-1"' in (public / "library/Test.self.html").read_text()
    index = json.loads((public / "search-index.json").read_text())
    assert next(row for row in index if row["kind"] == "declaration")["url"] == "library/Test.self.html"
    for path in public.rglob("*"):
        if path.suffix in {".html", ".json"}:
            text = path.read_text()
            assert "private-test" not in text and "版本私有手稿" not in text
