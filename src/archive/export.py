"""Portable static snapshots generated exclusively from the selected store view."""
from __future__ import annotations

import html
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlencode, urlsplit

from .search import _documents
from .store import ArchiveStore
from .util import ArchiveError, safe_path, utcnow, write_data, write_text


def _page_route(url: str) -> str:
    split = urlsplit(url)
    path = unquote(split.path)
    versions = parse_qs(split.query, keep_blank_values=True).get("version")
    if path.startswith("/papers/") and versions:
        return path + "?" + urlencode({"version": versions[-1]})
    return path


def export_site(root=None, output: str | Path = "build/site", public: bool = True, collection: str = "public") -> dict:
    from .http_client import LocalAppClient
    from .web import create_app
    store = ArchiveStore(root, collection=collection if public else "private")
    destination = safe_path(store.root, output)
    if destination.exists() and any(destination.iterdir()):
        raise ArchiveError("Export destination must be empty; choose a new output directory for each snapshot")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".export-", dir=destination.parent))
    routes = {"/": "index.html", "/papers": "papers.html", "/theorems": "theorems.html", "/library": "library.html", "/search": "search.html", "/issues": "issues.html"}
    for paper in store.list_papers():
        routes[f"/papers/{paper['paper_id']}"] = f"papers/{paper['paper_id']}.html"
        for version in paper.get("versions", []):
            value = version["version"]
            route = f"/papers/{paper['paper_id']}?" + urlencode({"version": value})
            routes[route] = f"papers/{paper['paper_id']}/{value}.html"
    for theorem in store.list_theorems():
        routes[f"/theorems/{theorem['theorem_id']}"] = f"theorems/{theorem['theorem_id']}.html"
        for proof in theorem.get("proofs", []):
            routes[f"/proofs/{proof['proof_id']}"] = f"proofs/{proof['proof_id']}.html"
    for claim in store.list_claims():
        routes[f"/claims/{claim['claim_id']}"] = f"claims/{claim['claim_id']}.html"
    for issue in store.list_issues():
        routes[f"/issues/{issue['issue_id']}"] = f"issues/{issue['issue_id']}.html"
    for declaration in store.load_catalog().get("declarations", []):
        routes[f"/library/{declaration['name']}"] = f"library/{declaration['name']}.html"
    exported, omitted = [], []
    try:
        with LocalAppClient(create_app(root=store.root, store=store, public=public)) as client:
            for route, filename in routes.items():
                split_route = urlsplit(route)
                request_url = quote(split_route.path, safe="/") + ("?" + split_route.query if split_route.query else "")
                response = client.get(request_url)
                if response.status_code == 404 and route == "/issues":
                    continue
                if response.status_code != 200:
                    raise ArchiveError(f"Export route failed: {route} ({response.status_code})")
                def rewrite(match):
                    attribute, url = match.group(1), html.unescape(match.group(2))
                    split = urlsplit(url)
                    if split.scheme or split.netloc or not split.path.startswith("/"):
                        return match.group(0)
                    path = unquote(split.path)
                    if path.startswith("/static/"):
                        target = path.lstrip("/")
                    elif path.startswith("/files/"):
                        relative = path.removeprefix("/files/")
                        source = safe_path(store.root, relative, must_exist=True)
                        allowed = client.get(quote(path, safe="/")).status_code == 200
                        if not allowed:
                            omitted.append(path)
                            return f'{attribute}="#unavailable-in-this-export"'
                        target = "files/" + relative
                        target_file = staging / target
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        if relative == "catalog/library.json":
                            write_data(target_file, store.load_catalog())
                        else:
                            shutil.copyfile(source, target_file)
                    else:
                        target = routes.get(_page_route(url))
                        if not target:
                            omitted.append(path)
                            return f'{attribute}="#unavailable-in-this-export"'
                    relative_url = os.path.relpath(target, Path(filename).parent.as_posix()).replace(os.sep, "/")
                    if split.fragment:
                        relative_url += "#" + split.fragment
                    return f'{attribute}="{html.escape(relative_url, quote=True)}"'
                page = re.sub(r'(href|src|action)="([^"]*)"', rewrite, response.text)
                write_text(staging / filename, page)
                exported.append(filename)
        static = safe_path(store.root, "web/static")
        if static.exists():
            for path in static.rglob("*"):
                safe_path(store.root, path)
            shutil.copytree(static, staging / "static")
        documents = [{"kind": kind, "id": entity_id, "title": title, "content": content,
                      "url": routes.get("/library/" + entity_id if kind == "declaration" else _page_route(url), "index.html")}
                     for kind, entity_id, title, content, url in _documents(store)]
        write_data(staging / "search-index.json", documents)
        data = json.dumps(documents, ensure_ascii=False).replace("<", "\\u003c")
        search_page = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>离线检索</title><link rel="stylesheet" href="static/archive.css"><body><main><p><a href="index.html">档案首页</a></p><h1>离线检索</h1><p>检索此快照中的归档内容与原编号；结果来自已保存的条目。</p><input id="q" type="search" aria-label="搜索内容" placeholder="中文、English、Theorem 1"><div id="results"></div></main><script id="data" type="application/json">''' + data + '''</script><script>const docs=JSON.parse(document.getElementById('data').textContent);const q=document.getElementById('q');const results=document.getElementById('results');function search(){results.replaceChildren();const tokens=q.value.toLowerCase().trim().split(/\\s+/).filter(Boolean);if(!tokens.length)return;for(const d of docs.filter(d=>tokens.every(t=>(d.title+' '+d.content+' '+d.id).toLowerCase().includes(t))).slice(0,100)){const p=document.createElement('p'),a=document.createElement('a');a.href=d.url;a.textContent=d.title+' ['+d.kind+']';p.append(a,document.createElement('br'),document.createTextNode(d.content.slice(0,220)));results.append(p);}}q.addEventListener('input',search);</script></body></html>'''
        write_text(staging / "search.html", search_page)
        write_data(staging / "export-manifest.json", {"schema_version": 1, "generated_at": utcnow(), "public": public, "pages": exported, "search_documents": len(documents), "omitted_links": sorted(set(omitted))})
        if destination.exists():
            destination.rmdir()
        os.rename(staging, destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return {"status": "exported", "public": public, "output": destination.relative_to(store.root).as_posix(), "page_count": len(exported), "search_documents": len(documents), "omitted_links": sorted(set(omitted))}
