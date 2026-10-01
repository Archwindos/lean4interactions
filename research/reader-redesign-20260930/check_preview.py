#!/usr/bin/env python3
"""Exercise the actual local prototype in Chromium and record bounded evidence."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "research/reader-redesign-20260930"
SITE = WORK / "preview"
EVIDENCE = WORK / "evidence"
BASE = "http://127.0.0.1:8001/"
DATA = json.loads((SITE / "data.public.json").read_text(encoding="utf-8"))
checks: list[dict] = []


def check(name: str, condition: bool, evidence: object = None) -> None:
    row = {"name": name, "passed": bool(condition)}
    if evidence is not None:
        row["evidence"] = evidence
    checks.append(row)
    if not condition:
        raise AssertionError(name)


def main() -> None:
    screenshots = []
    requests = []
    forbidden = []
    errors = []
    for file in ["", "reader.css", "reader.js", "data.public.js", "vendor/katex/katex.min.js",
                 "vendor/katex/katex.min.css", "vendor/katex/contrib/auto-render.min.js",
                 "vendor/katex/fonts/KaTeX_Main-Regular.woff2", "files/cvpr2023-main.pdf", "files/cvpr2023-supplement.pdf",
                 "files/formal-edition-evidence.json", "files/proof-reconstruction-v1.md", "files/core-verification-excerpt.json"]:
        with urlopen(BASE + file, timeout=12) as r:
            check("http:" + (file or "index.html"), r.status == 200, {"status": r.status, "content_type": r.headers.get("Content-Type")})

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1440, "height": 1050}, device_scale_factor=1,
                                      permissions=["clipboard-read", "clipboard-write"])
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))

        def request(route):
            u = urlparse(route.request.url)
            requests.append(route.request.url)
            if u.scheme in {"http", "https"} and (u.hostname != "127.0.0.1" or u.port != 8001):
                forbidden.append(route.request.url)
                route.abort()
            else:
                route.continue_()

        context.route("**/*", request)

        def screenshot(name):
            path = EVIDENCE / name
            page.screenshot(path=str(path), full_page=True, animations="disabled")
            screenshots.append({"path": path.relative_to(WORK).as_posix(), "case": page.url,
                                "viewport": page.viewport_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})

        def clean_layout(name):
            dimensions = page.evaluate("({width:innerWidth, scrollWidth:document.documentElement.scrollWidth})")
            check("no-horizontal-page-scroll:" + name, dimensions["scrollWidth"] <= dimensions["width"], dimensions)
            check("no-math-render-errors:" + name, page.evaluate("window.READER_MATH_ERRORS.length") == 0,
                  page.evaluate("window.READER_MATH_ERRORS"))

        page.goto(BASE, wait_until="networkidle")
        check("overview-discloses-unreviewed-formal-completeness", page.get_by_text("正式完整证明目录：尚未核对", exact=True).count() == 1)
        check("overview-keeps-formal-materials-and-results-separate", page.get_by_text("片段已对照的数学结果", exact=True).count() == 1 and page.get_by_text("正式正文与补充材料页数", exact=True).count() == 1)
        check("formal-overview-does-not-relabel-old-v6-counts", "18 条" not in page.locator("#page-content").inner_text() and DATA["inventory"]["source_record_count"] is None)
        clean_layout("overview-desktop")
        screenshot("01-overview-desktop.png")

        page.locator(".overview-card a[data-case=reconstruction]").click()
        page.locator("#reader-panel .proof-step").first.wait_for()
        check("real-shared-reconstruction-proof-is-readable-in-page", page.locator("#reader-panel .proof-step").count() == 4,
              page.locator("#reader-panel .proof-step p").all_text_contents())
        check("math-reading-conditions-do-not-expose-lean-encoding", "相等关系可判定" not in page.locator("#reader-panel .proof-body").inner_text() and "有限子集" in page.locator("#reader-panel .proof-body").inner_text())
        check("proof-copy-keeps-authoritative-steps", all(
            re.sub(r"^\d+\.\s", "", block.strip()) in page.locator("#reader-panel .proof-body").inner_text()
            for block in DATA["proofs"]["proof-reconstruction-v1"]["body"].split("\n\n")
            if re.match(r"^\d+\.\s", block)))
        clean_layout("reconstruction-desktop")
        screenshot("02-reconstruction-desktop.png")

        page.get_by_role("tab", name="原命题", exact=True).click()
        check("original-statement-default-is-math-rendered", page.locator("#original-source-view .katex").count() >= 3)
        clean_layout("original-statement")
        screenshot("03-original-statement-desktop.png")
        check("auxiliary-tex-origin-not-misrepresented", "不是 CVPR 作者源码" in page.locator("#reader-panel").inner_text())
        page.get_by_role("button", name="原样辅助 TeX", exact=True).click()
        check("raw-tex-byte-preserving-dom-text", page.locator("#original-source-view pre").text_content() == DATA["original"]["reconstruction_statement"]["raw"])
        page.get_by_role("button", name="复制辅助 TeX", exact=True).click()
        clipboard = page.evaluate("navigator.clipboard.readText()")
        check("copy-tex-exactly-preserves-source", clipboard == DATA["original"]["reconstruction_statement"]["raw"],
              {"characters": len(clipboard), "source_sha256": hashlib.sha256(clipboard.encode()).hexdigest()})
        check("raw-tex-is-not-json-quoted", not clipboard.startswith('"') and "\\begin{theorem}" in clipboard)

        page.get_by_role("tab", name="原证明", exact=True).click()
        check("original-proof-has-math-and-full-source-boundary", page.locator("#original-source-view .katex").count() >= 8)
        clean_layout("original-proof")
        screenshot("04-original-proof-desktop.png")
        page.get_by_role("button", name="原样辅助 TeX", exact=True).click()
        check("original-proof-raw-preserves-both-components", page.locator("#original-source-view pre").text_content() == DATA["original"]["theorem1_proof"]["raw"])

        page.get_by_role("tab", name="中文重写", exact=True).click()
        page.locator("#step-3 button").click()
        check("step-to-actual-lean-declaration", page.get_by_role("tab", name="Lean 结果", exact=True).get_attribute("aria-selected") == "true" and page.get_by_role("heading", name="Harsanyi.reconstruction", exact=True).count() == 1)
        check("step-map-precision-disclosed", "尚未提供步骤到代码行的精确对应" in page.locator("#reader-panel").inner_text())
        page.locator("#lean-encoding summary").click()
        check("lean-encoding-condition-retained-in-lean-tab", "相等关系可判定" in page.locator("#lean-encoding").inner_text())
        page.locator("#lean-encoding summary").click()
        clean_layout("lean-result")
        screenshot("05-lean-desktop.png")
        page.get_by_role("button", name="返回对应中文步骤", exact=True).click()
        check("lean-to-proof-return", page.locator("#step-3").is_visible())
        page.locator(".jump-next a").click()
        check("real-uniqueness-proof-readable", page.locator("#reader-panel .proof-step").count() == 3)
        clean_layout("uniqueness")

        page.locator(".directory-link[data-case=shapley]").click()
        check("incomplete-theorem-discloses-unwritten", page.get_by_text("尚未重写", exact=True).count() >= 1)
        check("incomplete-theorem-does-not-invent-rewrite-or-lean-tabs", page.get_by_role("tab", name="中文重写", exact=True).count() == 0 and page.get_by_role("tab", name="Lean 结果", exact=True).count() == 0)
        check("candidate-original-math-readable", page.locator("#original-source-view .katex").count() >= 2)
        clean_layout("candidate-desktop")
        screenshot("06-unwritten-desktop.png")
        page.get_by_role("tab", name="原证明的位置", exact=True).click()
        check("candidate-has-formal-original-proof-location", page.get_by_role("link", name="打开正式补充材料第 6 页 ↗", exact=True).get_attribute("href").endswith("#page=6"))
        page.get_by_role("tab", name="处理进度", exact=True).click()
        check("candidate-lean-not-formalized", "尚未形式化" in page.locator("#reader-panel").inner_text())

        page.goto(BASE + "?case=reference", wait_until="networkidle")
        check("prose-reference-not-presented-as-independent-theorem", page.get_by_text("正文引用 · 非独立定理", exact=True).count() >= 1)
        check("candidate-not-labeled-as-math-error", "数学问题待确认" not in page.locator("#page-content").inner_text())
        check("pdf-text-source-format-disclosed", "正式 PDF 自动提取" in page.locator("#page-content").inner_text())
        check("formal-reference-retains-extracted-text", page.locator("#original-source-view pre").text_content() == DATA["formal_reference_text"])
        clean_layout("reference-desktop")
        screenshot("07-prose-reference-desktop.png")
        page.get_by_role("button", name="辅助TeX上下文", exact=True).click()
        check("reference-can-read-actual-author-tex", page.locator("#original-source-view pre").text_content() == DATA["original"]["complaint_context"]["raw"])

        check("legacy-cases-not-in-formal-navigation", page.locator("#directory [data-case=dummy], #directory [data-case=inventory]").count() == 0)
        for old_case in ["inventory", "dummy"]:
            page.goto(BASE + "?case=" + old_case, wait_until="networkidle")
            check("old-direct-url-is-explicit-history:" + old_case, page.get_by_role("heading", name="旧版审计入口", exact=True).count() == 1 and "不能作为 CVPR 2023 正式版" in page.locator("#page-content").inner_text())
        page.goto(BASE + "?case=reconstruction", wait_until="networkidle")
        page.get_by_role("button", name="状态与管理帮助", exact=True).click()
        check("generic-authorization-help-is-confined-to-dialog", page.get_by_role("dialog").is_visible() and "取得具体修改授权" in page.get_by_role("dialog").inner_text())
        page.get_by_role("button", name="关闭帮助", exact=True).click()
        check("keyboard-tabs-operate", page.locator("#tab-rewrite").focus() is None)
        page.keyboard.press("ArrowRight")
        check("keyboard-arrow-selects-original", page.locator("#tab-statement").get_attribute("aria-selected") == "true")

        # A hostile source string must stay visible as text, not become DOM/HTML.
        hostile='<img src=x onerror="window.previewInjected=true">\\(x<y\\)'
        page.evaluate("text => { window.READER_DATA.original.reconstruction_statement.raw=text; window.previewInjected=false; }",hostile)
        page.get_by_role("tab", name="中文重写", exact=True).click()
        page.get_by_role("tab", name="原命题", exact=True).click()
        check("source-html-is-escaped-in-reading-mode", page.locator("#original-source-view img").count() == 0 and not page.evaluate("window.previewInjected"))
        page.get_by_role("button", name="原样辅助 TeX", exact=True).click()
        check("source-html-is-escaped-in-raw-mode", page.locator("#original-source-view pre").text_content() == hostile and page.locator("#original-source-view img").count() == 0)

        page.set_viewport_size({"width":390,"height":844})
        page.goto(BASE + "?case=reconstruction", wait_until="networkidle")
        clean_layout("reconstruction-mobile")
        screenshot("08-reconstruction-mobile.png")
        page.get_by_role("button", name="章节与定理目录", exact=False).click()
        check("mobile-directory-operates", page.locator("#directory").is_visible())
        page.locator(".directory-link[data-case=shapley]").click()
        clean_layout("candidate-mobile")
        screenshot("09-unwritten-mobile.png")
        check("mobile-directory-collapses-after-navigation", not page.locator("#directory").is_visible())

        check("no-javascript-page-errors", not errors, errors)
        check("no-external-requests", not forbidden, forbidden)
        browser_version = browser.version
        browser.close()

    baseline = json.loads((EVIDENCE / "production-baseline.json").read_text())
    changed = [path for path, digest in baseline["files"].items()
               if not (ROOT / path).is_file() or hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest]
    check("production-corpus-web-and-lean-unchanged", not changed, {"files_checked":len(baseline["files"]), "changed":changed})
    # Only a narrow public snapshot directory is served; browser tools/evidence stay outside it.
    check("served-snapshot-excludes-private-paper-identifiers", "manual-maintext" not in (SITE / "data.public.json").read_text())
    for record in DATA["formal_edition_audit"]["sources"]:
        if record["key"] in {"sparse-cvpr2023-main", "sparse-cvpr2023-supp"}:
            copied = "cvpr2023-main.pdf" if record["key"].endswith("main") else "cvpr2023-supplement.pdf"
            check("official-pdf-sha-matches-acquired-source:" + record["key"], hashlib.sha256((SITE / "files" / copied).read_bytes()).hexdigest() == record["sha256"])
    record = {"generated_at":datetime.now(timezone.utc).isoformat(),"status":"passed" if all(x["passed"] for x in checks) else "failed",
              "checks":checks,"check_count":len(checks),"browser":browser_version,"base_url":BASE,"screenshots":screenshots,
              "external_requests":forbidden,"javascript_errors":errors,"request_count":len(requests),
              "limits":["Screenshots cover one official CVPR paper and two viewport widths, not the production site or full corpus.",
                        "Auxiliary TeX is arXiv v6, explicitly labeled; official PDF is authoritative. Full official inventory and corpus migration are incomplete.",
                        "Existing Lean report was rechecked; no new Lean build or new mathematical proof was produced."]}
    (EVIDENCE / "browser-checks.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":record["status"],"checks":len(checks),"screenshots":len(screenshots),"browser":browser_version},ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        (EVIDENCE / "browser-checks-failure.json").write_text(json.dumps({"error":str(error),"checks":checks},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        raise
