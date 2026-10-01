#!/usr/bin/env python3
"""Inspect the real static multi-paper reader in the existing local Chromium."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
SITE = WORK / "preview"
EVIDENCE = WORK / "evidence"
OLD_TOOLS = ROOT / "research/reader-redesign-20260930/browser-tools"
sys.path.insert(0, str(OLD_TOOLS / "python"))
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(OLD_TOOLS / "browsers")
from playwright.sync_api import sync_playwright

checks: list[dict] = []


def check(name: str, passed: bool, evidence: object = None) -> None:
    item = {"name": name, "passed": bool(passed)}
    if evidence is not None:
        item["evidence"] = evidence
    checks.append(item)
    if not passed:
        raise AssertionError(name)


def result_url(result: dict) -> str:
    return (f"papers/{result['paper_id']}/results/{result['id']}/" if result.get("paper_id") else f"library/{result['id']}/")


def main(base: str) -> None:
    data = json.loads((SITE / "data.public.json").read_text(encoding="utf-8"))
    manifest = json.loads((EVIDENCE / "build-manifest.json").read_text(encoding="utf-8"))
    result_by_id = {r["id"]: r for r in data["math"]["results"]}
    shared_value = data["math"].get("shared_proofs", [])
    shared_by_id = {r["id"]: r for r in shared_value if isinstance(shared_value, list)} if isinstance(shared_value, list) else shared_value
    primary = [next(r for r in data["math"]["results"] if r.get("paper_id") == p["id"] and r["reading_status"] == "complete") for p in data["papers"]]
    screenshots = []
    requests = []
    external = []
    errors = []
    source_records = [s for p in data["papers"] for s in p["sources"]]
    for item in manifest["pages"]:
        with urlopen(base + item["path"], timeout=10) as response:
            check("static-page:" + item["path"], response.status == 200)
    for source in source_records:
        with urlopen(base.rstrip("/") + source["public_path"], timeout=15) as response:
            checksum = hashlib.sha256(response.read()).hexdigest()
            check("formal-source-hash:" + source["id"], response.status == 200 and checksum == source["sha256"], {"sha256": checksum})
    for item in data.get("documentation", []):
        with urlopen(base.rstrip("/") + item["public_path"], timeout=10) as response:
            check("agent-documentation:" + item["label"], response.status == 200)
    for path in ("evidence/build-manifest.json", "math/experimental/IndependentOR.lean", "data/math-content.json", "corpus/", "inbox/"):
        try:
            with urlopen(base + path, timeout=10) as response:
                status = response.status
        except HTTPError as error:
            status = error.code
        check("only-preview-is-served:" + path, status == 404, {"http_status":status})
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width":1440,"height":1050}, device_scale_factor=1)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        allowed = urlparse(base)

        def route(request_route):
            url = urlparse(request_route.request.url)
            requests.append(request_route.request.url)
            if url.scheme in {"http", "https"} and (url.hostname != allowed.hostname or url.port != allowed.port):
                external.append(request_route.request.url)
                request_route.abort()
            else:
                request_route.continue_()

        context.route("**/*", route)

        def layout(label: str):
            dimensions = page.evaluate("({viewport:innerWidth,document:document.documentElement.scrollWidth})")
            check("no-page-horizontal-overflow:" + label, dimensions["document"] <= dimensions["viewport"], dimensions)
            check("math-renders-without-errors:" + label, not page.evaluate("window.READER_MATH_ERRORS"), page.evaluate("window.READER_MATH_ERRORS"))

        def screenshot(name: str, full: bool = False):
            path = EVIDENCE / name
            page.screenshot(path=str(path), full_page=full, animations="disabled")
            screenshots.append({"path":path.relative_to(WORK).as_posix(),"url":page.url,"viewport":page.viewport_size,"full_page":full,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})

        page.goto(base, wait_until="networkidle")
        check("three-distinct-papers-in-library", page.locator(".paper-row").count() == 3 and len({p["id"] for p in data["papers"]}) == 3)
        check("paper-links-have-independent-paths", all(page.locator(f'.paper-row[data-paper="{p["id"]}"] h2 a').get_attribute("href") == f'/papers/{p["id"]}/' for p in data["papers"]))
        layout("library-desktop")
        screenshot("01-papers-desktop.png")
        page.locator(".paper-row h2 a").first.click()
        check("paper-navigation-opens-real-document", page.url.endswith("/papers/"+data["papers"][0]["id"]+"/") and page.locator("h1").inner_text() == data["papers"][0]["title"])
        screenshot("02-cvpr-paper-desktop.png")

        for index, (paper, result) in enumerate(zip(data["papers"], primary), 1):
            if index > 1:
                page.locator(".paper-selector summary").click()
                page.locator(f'.paper-options a[href="/papers/{paper["id"]}/"]').click()
            check("paper-switch:" + paper["id"], page.locator("h1").inner_text() == paper["title"] and f'/papers/{paper["id"]}/' in page.url)
            check("scope-is-local-to-paper:" + paper["id"], page.locator(".scope-note").count() == 1)
            page.locator(f'.result-list a[data-result="{result["id"]}"]').click()
            check("direct-result-url:" + result["id"], page.url == base + result_url(result) and "?" not in page.url)
            check("chinese-proof-opens-by-default:" + result["id"], page.locator("#tab-rewrite").get_attribute("aria-selected") == "true")
            shared = shared_by_id.get(result.get("shared_proof_id"), {})
            expected = len(result.get("proof_steps", [])) + len(shared.get("proof_steps", []))
            check("complete-proof-all-steps-visible:" + result["id"], expected > 0 and page.locator(".proof-step").count() == expected and page.evaluate("[...document.querySelectorAll('.proof-step')].every(x=>!x.closest('details')&&getComputedStyle(x).display!=='none')"), {"steps":expected})
            check("paper-notation-does-not-show-lean-encoding:" + result["id"], "DecidableEq" not in page.locator("#reader-panel").inner_text())
            check("math-is-rendered-in-proof:" + result["id"], page.locator("#reader-panel .katex").count() >= 4)
            check("paper-specific-original-title-retained:" + result["id"], page.locator("h1").inner_text() == result["title"])
            layout(result["id"] + "-desktop")
            screenshot(f"0{index+2}-{paper['id']}-proof-desktop.png")
            if index == 1:
                page.locator(".proof-step[data-proof-prefix='shared']").nth(2).scroll_into_view_if_needed()
                screenshot("17-common-proof-middle-desktop.png")
                page.evaluate("scrollTo(0,0)")
            for tab, field in [("statement", "original_statement_md"), ("original-proof", "original_proof_md")]:
                page.locator("#tab-" + tab).click()
                check("formal-original-readable:" + result["id"] + ":" + tab, bool(result.get(field)) and page.locator("#reader-panel .original-section").count() == 1 and page.locator("#reader-panel .katex").count() > 0)
                check("formal-original-pdf-location-linked:" + result["id"] + ":" + tab, page.locator("#reader-panel .source-link[href*='#page=']").count() > 0)
                check("no-preprint-as-formal-source:" + result["id"] + ":" + tab, "arxiv" not in " ".join(page.locator("#reader-panel a").evaluate_all("xs=>xs.map(x=>x.href)")))
                check("source-text-format-is-disclosed:" + result["id"] + ":" + tab, bool(page.locator(".source-notes").first.inner_text()))
                layout(result["id"] + "-" + tab)
            if index == 2:
                screenshot("06-sparse-original-proof-desktop.png")
                page.locator(".original-pages summary").click()
                page.locator(".original-pages img").first.wait_for()
                page.wait_for_function("[...document.querySelectorAll('.original-pages img')].every(x=>x.complete&&x.naturalWidth>0)")
                check("actual-official-pdf-page-is-readable-inline", page.locator(".original-pages img").count() == 1)
                screenshot("16-sparse-official-source-page-desktop.png", full=True)
                page.locator(".original-pages summary").click()
            if index == 1:
                page.locator(".original-tex summary").click()
                asset = data["formula_transcripts"][result["paper_id"]][0]
                check("pdf-transcription-tex-is-byte-preserving-in-dom", page.locator(".original-tex .raw-source").text_content() == asset["raw_text"])
                check("transcription-is-not-misrepresented-as-author-source", "未取得作者 TeX 源码" in page.locator(".original-tex").inner_text())
                page.locator(".original-tex summary").click()
            page.locator("#tab-lean").click()
            lean = result.get("lean", shared.get("lean", {}))
            check("compiled-adapter-is-exact-text:" + result["id"], bool(lean.get("adapter_code")) and lean["adapter_code"] in page.locator("#reader-panel .code-panel").all_text_contents())
            check("lean-scope-is-explicit:" + result["id"], bool(lean.get("scope")) and bool(page.locator(".lean-intro").inner_text()))
            check("actual-step-map-readable:" + result["id"], page.locator(".lean-map").count() > 0)
            layout(result["id"] + "-lean")
            if index == 2:
                screenshot("07-sparse-lean-desktop.png")
            page.locator(".return-step").first.click()
            check("lean-to-chinese-step-return:" + result["id"], page.locator("#tab-rewrite").get_attribute("aria-selected") == "true" and page.locator(".proof-step:focus").count() == 1)
            page.locator(".step-to-lean").first.click()
            check("chinese-step-to-lean-navigation:" + result["id"], page.locator("#tab-lean").get_attribute("aria-selected") == "true")
            page.locator("#tab-lean").focus()
            page.keyboard.press("Home")
            check("keyboard-tab-navigation:" + result["id"], page.locator("#tab-rewrite").get_attribute("aria-selected") == "true")

        pending = [r for r in data["math"]["results"] if r.get("paper_id") and r["reading_status"] != "complete"]
        for result in pending:
            page.goto(base + result_url(result), wait_until="networkidle")
            check("pending-original-has-no-completion-claim:" + result["id"], page.locator("#tab-rewrite,#tab-lean").count() == 0 and "完整中文证明" not in page.locator(".result-meta").inner_text())
            check("pending-f11-has-specific-issue-evidence", page.locator(".error-message .source-link").count() > 0)
            page.locator("#tab-original-proof").click()
            layout("pending-f11-original")
            screenshot("08-generalizable-original-review-desktop.png")
            page.locator("#tab-scope").click()
            check("pending-f11-links-complete-and-component", page.locator("#reader-panel a[href*='iclr2024-generalizable-and/']").count() > 0)
            evidence_path = page.locator("#reader-panel .error-message .source-link").first.get_attribute("href")
            page.goto(base.rstrip("/")+evidence_path, wait_until="networkidle")
            check("f11-issue-link-opens-specific-evidence-page", page.locator("h1").inner_text() == data["review_records"][0]["title"] and page.get_by_role("heading",name="核验例子",exact=True).count() == 1)
            page.locator(".original-pages summary").click()
            page.wait_for_function("[...document.querySelectorAll('.original-pages img')].every(x=>x.complete&&x.naturalWidth>0)")
            check("f11-issue-page-has-live-official-source-image", page.locator(".original-pages img").count() == 1 and page.locator(".original-pages a[href*='#page=14']").count() == 1)
            layout("f11-specific-issue-evidence")
            screenshot("19-generalizable-specific-evidence-desktop.png")

        page.goto(base + "about/", wait_until="networkidle")
        check("maintenance-content-has-separate-page", page.get_by_role("heading", name="给 AI 的只读入口", exact=True).count() == 1 and page.locator(".docs-links a").count() >= 3)
        layout("about-desktop")
        screenshot("09-for-agents-desktop.png")

        # All generated result pages, including CVPR uniqueness and the public
        # baseline convention, must work from a copied link in a fresh navigation.
        for result in data["math"]["results"]:
            page.goto(base + result_url(result), wait_until="networkidle")
            check("every-result-direct-link:" + result["id"], page.locator("h1").inner_text() == result["title"])
            layout("direct-"+result["id"])

        page.set_viewport_size({"width":390,"height":844})
        page.goto(base, wait_until="networkidle")
        layout("library-mobile")
        screenshot("10-papers-mobile.png")
        for index, result in enumerate(primary, 1):
            page.goto(base + result_url(result), wait_until="networkidle")
            layout(result["id"] + "-mobile")
            check("mobile-proof-does-not-collapse-full-text:" + result["id"], page.locator(".proof-step").count() > 0)
            screenshot(f"{10+index:02d}-{result['paper_id']}-proof-mobile.png")
            if index == 2:
                page.locator(".proof-step[data-proof-prefix='shared']").nth(2).scroll_into_view_if_needed()
                screenshot("18-common-proof-middle-mobile.png")
                page.evaluate("scrollTo(0,0)")
            page.locator("#directory-toggle").click()
            check("mobile-directory-operates:" + result["id"], page.locator("#directory").is_visible())
            page.locator("#directory a").first.click()
            check("mobile-navigation-closes-directory:" + result["id"], not page.locator("#directory").is_visible())
            page.goto(base + result_url(result) + "#lean", wait_until="networkidle")
            check("direct-lean-anchor:" + result["id"], page.locator("#tab-lean").get_attribute("aria-selected") == "true")
            layout(result["id"] + "-lean-mobile")
            if index == 2:
                screenshot("14-sparse-lean-mobile.png")
            page.locator("#tab-original-proof").click()
            layout(result["id"] + "-original-mobile")
        if pending:
            page.goto(base + result_url(pending[0]) + "#original-proof", wait_until="networkidle")
            layout("f11-review-mobile")
            screenshot("15-generalizable-original-review-mobile.png")
        # Deliberately inject a source string into the in-memory public snapshot:
        # both HTML syntax and raw TeX must remain inert text and local math.
        hostile='<img src=x onerror="window.readerInjected=true">\\(x<y\\)'
        first = primary[0]
        page.goto(base + result_url(first), wait_until="networkidle")
        page.evaluate("([id,text])=>{window.READER_V2_DATA.math.results.find(x=>x.id===id).original_statement_md=text;window.readerInjected=false;}", [first["id"],hostile])
        page.locator("#tab-statement").click()
        check("source-html-remains-safe-text", page.locator("#reader-panel .original-section img").count() == 0 and not page.evaluate("window.readerInjected") and "<img" in page.locator("#reader-panel .original-section").inner_text())
        check("no-javascript-errors", not errors, errors)
        check("no-external-browser-requests", not external, external)
        browser_version = browser.version
        browser.close()

    baseline = json.loads((EVIDENCE / "production-baseline.json").read_text(encoding="utf-8"))
    changed = [name for name, checksum in baseline["files"].items() if not (ROOT / name).is_file() or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != checksum]
    check("production-corpus-and-lean-originals-unchanged", not changed, {"files_checked":len(baseline["files"]),"changed":changed})
    check("public-snapshot-excludes-private-and-experimental", all(marker not in (SITE / "data.public.json").read_text(encoding="utf-8") for marker in ("manual-maintext","inbox/","/experimental/","library-or-reconstruction")))
    html_pages = list(SITE.rglob("*.html"))
    check("multipage-content-is-actual-static-pages", len(html_pages) == len(manifest["pages"]) and sum(p["kind"] == "paper" for p in manifest["pages"]) == 3)
    summary = {"generated_at":datetime.now(timezone.utc).isoformat(),"status":"passed","base_url":base,"browser":browser_version,"paper_count":3,
               "paper_result_pages":sum(bool(r.get("paper_id")) for r in data["math"]["results"]),"rewritten_paper_results":sum(bool(r.get("paper_id")) and r["reading_status"] == "complete" for r in data["math"]["results"]),
               "check_count":len(checks),"checks":checks,"screenshots":screenshots,"external_requests":external,"javascript_errors":errors,"request_count":len(requests),
               "limits":["Selected results from three formal papers; full-paper rewriting and formalization are not claimed.","F11 full AND/OR theorem remains pending; only Appendix C(1) fixed-x AND component is fully rewritten and has an adapter.","Experimental independent OR work is excluded from the served snapshot."]}
    (EVIDENCE / "browser-checks.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    failure_path = EVIDENCE / "browser-checks-failure.json"
    if failure_path.exists():
        failure_path.unlink()  # Previous generated attempt; the final report is current.
    print(json.dumps({key:summary[key] for key in ("status","paper_count","paper_result_pages","rewritten_paper_results","check_count","browser")},ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url",default="http://127.0.0.1:8002/")
    args = parser.parse_args()
    try:
        main(args.base_url.rstrip("/")+"/")
    except Exception as error:
        EVIDENCE.mkdir(parents=True,exist_ok=True)
        (EVIDENCE / "browser-checks-failure.json").write_text(json.dumps({"error":str(error),"checks":checks},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        raise
