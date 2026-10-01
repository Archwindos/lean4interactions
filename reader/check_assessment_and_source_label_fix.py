#!/usr/bin/env python3
"""Check the precise final metadata/label delta against the completed full matrix."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from check_preview import ROOT, WORK, EVIDENCE, sync_playwright

IDS = {'decoder-backpropagation', 'decoder-geometric-sum'}
SELECTORS = ('#reader-panel .source-links,#reader-panel .source-notes,'
             '#reader-panel details>summary,#reader-panel figcaption,'
             '#reader-panel .error-message,#reader-panel .original-section>h2:first-child')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def main(base):
    baseline_path = EVIDENCE / 'assessment-and-label-fix-baseline.json'
    previous_path = EVIDENCE / 'twelve-paper-browser-before-assessment-fix.json'
    baseline = json.loads(baseline_path.read_text())
    previous = json.loads(previous_path.read_text())
    manifest = json.loads((EVIDENCE / 'build-manifest.json').read_text())
    data = json.loads((WORK / 'preview/data.public.json').read_text())
    source = json.loads((ROOT / 'corpus/public/reader/icml2023-decoder/content.json').read_text())
    inventory = json.loads((ROOT / 'corpus/public/reader/icml2023-decoder/inventory.json').read_text())
    paths = [WORK / 'preview' / name for name in ('data.public.json', 'data.public.js', 'reader.js', 'reader.css')]
    paths += [baseline_path, previous_path, EVIDENCE / 'build-manifest.json', Path(__file__).resolve(),
              ROOT / 'corpus/public/reader/icml2023-decoder/content.json',
              ROOT / 'corpus/public/reader/icml2023-decoder/inventory.json']
    hashes = lambda: {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    before = hashes()
    checks, errors, external, screenshots = [], [], [], []
    def check(name, value, detail=None):
        checks.append({'name': name, 'passed': bool(value), 'detail': detail})
    def changed_fields(row, old):
        return [k for k in set(old) | set(row) if old.get(k) != (digest(row[k]) if k in row else None)]

    check('full-matrix-report-byte-bound', before[previous_path.relative_to(ROOT).as_posix()] == baseline['browser_report_sha256'])
    failures = [c for c in previous['checks'] if not c['passed']]
    check('prior-failures-all-source-labels', failures and all(c['name'].startswith('english-source-labels:') for c in failures))
    check('source-331-decodes-in-full-matrix', previous['source_pages_decoded'] == 331)
    diffs = {}
    for label, rows, old, allowed in (
        ('source', source['results'], baseline['source_result_field_hashes'],
         {'statement_assessment', 'rewrite_status', 'rewrite_role', 'scope_label', 'translations'}),
        ('inventory', inventory['entries'], baseline['inventory_entry_field_hashes'],
         {'statement_assessment', 'rewrite_status', 'rewrite_role'}),
    ):
        check(label + '-stable-ids', {r['id'] for r in rows} == set(old))
        diffs[label] = {}
        for row in rows:
            fields = changed_fields(row, old[row['id']])
            if fields: diffs[label][row['id']] = fields
            check(label + '-allowed-delta:' + row['id'], not fields or row['id'] in IDS and set(fields) <= allowed, fields)
            if label == 'source' and row['id'] in IDS:
                english = {k: v for k, v in row.get('translations', {}).get('en', {}).items() if k != 'scope_label'}
                check('source-English-proof-byte-fingerprint:' + row['id'], digest(english) == baseline['source_english_without_scope_label'][row['id']])
    for label, obj, old, excluded in (
        ('source', source, baseline['source_root_hashes'], {'results'}),
        ('inventory', inventory, baseline['inventory_root_hashes'], {'entries'}),
    ):
        check(label + '-all-other-fields-unchanged', {k: digest(v) for k, v in obj.items() if k not in excluded} == old)
    rows = {r['id']: r for r in data['math']['results']}
    check('all-355-result-ids-retained', set(rows) == set(baseline['result_hashes']))
    diffs['preview'] = {}
    for ident, row in rows.items():
        if ident not in IDS:
            check('unaffected-result-unchanged:' + ident, digest(row) == baseline['result_hashes'][ident])
        else:
            fields = changed_fields(row, baseline['changed_result_field_hashes'][ident])
            diffs['preview'][ident] = fields
            allowed = {'statement_assessment', 'rewrite_status', 'rewrite_role', 'scope_label', 'translations',
                       'source_semantic_status', 'reading_status', 'original_rewrite_status'}
            check('preview-allowed-delta:' + ident, set(fields) <= allowed, fields)
            english = {k: v for k, v in row.get('translations', {}).get('en', {}).items() if k != 'scope_label'}
            check('preview-English-proof-byte-fingerprint:' + ident, digest(english) == baseline['preview_english_without_scope_label'][ident])
    check('all-shared-proofs-and-math-metadata-unchanged', {k: digest(v) for k, v in data['math'].items() if k != 'results'} == baseline['math_root_hashes'])
    check('all-other-public-data-unchanged', {k: digest(v) for k, v in data.items() if k not in {'math', 'inventories', 'coverage'}} == baseline['public_root_hashes'])
    assets = {r['path']: r['sha256'] for r in manifest['public_file_allowlist']}
    for path, expected in baseline['source_asset_hashes'].items():
        target = WORK / 'preview' / path
        check('unchanged-formal-PDF-or-image:' + path, assets.get(path) == expected and hashlib.sha256(target.read_bytes()).hexdigest() == expected)
    check('CSS-unchanged', before['reader/preview/reader.css'] == baseline['original_css_sha256'])
    ui = (WORK / 'preview/reader.js').read_text()
    for addition in baseline['ui_dictionary_additions']:
        check('UI-addition-present:' + digest(addition), ui.count(addition) == 1)
        ui = ui.replace(addition, '', 1)
    check('UI-only-eight-reviewed-translation-keys', hashlib.sha256(ui.encode()).hexdigest() == baseline['original_ui_sha256'])
    cases = {}
    for failure in failures:
        _, ident, tab = failure['name'].split(':')
        cases.setdefault(ident, set()).add(tab)
    with sync_playwright() as engine:
        browser = engine.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1440, 'height': 1050})
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        origin = urlparse(base)
        def route(request):
            url = urlparse(request.request.url)
            if url.scheme in ('http', 'https') and (url.hostname, url.port) != (origin.hostname, origin.port):
                external.append(request.request.url); request.abort()
            else: request.continue_()
        context.route('**/*', route)
        for path in paths[:4]:
            served = hashlib.sha256(urlopen(base + path.relative_to(WORK / 'preview').as_posix()).read()).hexdigest()
            check('served-current-byte:' + path.name, served == before[path.relative_to(ROOT).as_posix()])
        page.goto(base, wait_until='load')
        page.evaluate("localStorage.setItem('proof-reader-language','en')")
        for number, (ident, tabs) in enumerate(cases.items(), 1):
            row = rows[ident]
            page.goto(base + 'papers/' + row['paper_id'] + '/results/' + ident + '/', wait_until='load')
            page.wait_for_selector('h1')
            for tab in sorted(tabs):
                page.locator('#tab-' + tab).click()
                page.locator('#reader-panel details').evaluate_all('xs=>xs.forEach(x=>x.open=true)')
                leftovers = page.locator(SELECTORS).evaluate_all("xs=>xs.map(x=>{const y=x.cloneNode(true);y.querySelectorAll('.katex,code,pre,.raw-source,#language-select').forEach(z=>z.remove());return y.textContent}).filter(x=>/[\u3400-\u9fff]/.test(x))")
                check('english-source-labels:' + ident + ':' + tab, not leftovers, leftovers)
                check('source-math:' + ident + ':' + tab, not page.evaluate('window.READER_MATH_ERRORS||[]'))
                check('source-layout:' + ident + ':' + tab, page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            if number % 40 == 0: print('Affected English source results checked: ' + str(number), flush=True)
        for language in ('zh', 'en'):
            page.evaluate('(x)=>localStorage.setItem("proof-reader-language",x)', language)
            for ident in sorted(IDS):
                row = rows[ident]
                page.goto(base + 'papers/' + row['paper_id'] + '/results/' + ident + '/', wait_until='load')
                page.wait_for_selector('h1')
                expected = row['scope_label'] if language == 'zh' else row['translations']['en']['scope_label']
                check('visible-original-domain:' + language + ':' + ident, expected in page.locator('.result-meta').inner_text(), expected)
                check('not-mislabelled-refuted:' + language + ':' + ident, '复合陈述中的一部分有反例' not in page.locator('.result-meta').inner_text() and 'A clause of the compound statement is refuted' not in page.locator('.result-meta').inner_text())
                check('domain-page-math:' + language + ':' + ident, not page.evaluate('window.READER_MATH_ERRORS||[]'))
                page.locator('#tab-lean').click()
                expected_role = 'theorem_proof' if ident == 'decoder-backpropagation' else 'partial_component'
                check('machine-role-retained:' + language + ':' + ident, row['verification_role'] == expected_role and page.locator('.lean-map').count() > 0)
                page.locator('#tab-rewrite').click()
                image = EVIDENCE / ('twelve-domain-fix-' + language + '-' + ident + '.png')
                page.screenshot(path=str(image))
                screenshots.append({'path': image.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(image.read_bytes()).hexdigest()})
                page.goto(base + 'papers/icml2023-decoder/', wait_until='load'); page.wait_for_selector('h1')
                link = page.locator('[data-result="' + ident + '"]')
                check('directory-domain-label:' + language + ':' + ident, expected in link.inner_text())
        browser.close()
    after = hashes()
    check('no-JS-errors', not errors, errors); check('no-external-requests', not external, external)
    check('snapshot-unchanged-during-delta-check', before == after)
    for item in manifest['inputs']:
        target = ROOT / item['path']
        check('current-build-input:' + item['path'], target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256'])
    report = {'status': 'passed' if all(c['passed'] for c in checks) else 'failed',
              'scope': 'Affected-only actual Chromium checks plus complete byte/field fingerprint carry-forward. The previous full matrix retained its 412 source-label failures; this report rechecks those exact panels and two domain labels. Formal PDFs/images were compared bytewise, not decoded a second time. No new mathematical proof or Lean compilation.',
              'recorded_at': datetime.now(timezone.utc).isoformat(), 'previous_report': previous_path.relative_to(ROOT).as_posix(),
              'snapshot_hashes': {'before': before, 'after': after}, 'changed_result_ids': sorted(IDS),
              'field_differences': diffs, 'affected_source_panels': len(failures), 'affected_source_results': len(cases),
              'unchanged_source_assets': len(baseline['source_asset_hashes']), 'screenshots': screenshots,
              'checks': checks, 'js_errors': errors, 'external_requests': external}
    (EVIDENCE / 'twelve-paper-assessment-and-source-label-delta.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    failed = [c for c in checks if not c['passed']]
    print(json.dumps({'status': report['status'], 'checks': len(checks), 'failed': len(failed), 'failures': failed[:10]}, ensure_ascii=False))
    return int(bool(failed))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--base', default='http://127.0.0.1:8004/')
    raise SystemExit(main(parser.parse_args().base))
