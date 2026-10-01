#!/usr/bin/env python3
"""Verify one real cold source-page render with the project Poppler and Chromium."""
import functools
import hashlib
import json
import subprocess
import threading
from datetime import datetime,timezone
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from check_preview import ROOT,WORK,EVIDENCE,sync_playwright
from evidence_paths import input_hashes
from input_manifest import load_manifest,project_path

def main():
 manifest=load_manifest()
 item=next(row for row in manifest['papers'] if row['paper_id']=='iclr2024-sparse')
 metadata_path=project_path(item['metadata_path'])
 source=json.loads(metadata_path.read_text())['sources'][0]
 pdf=project_path(source['local_path']);page_number=13
 executable=ROOT/'.conda-env/bin/pdftoppm'
 if not executable.is_file():raise RuntimeError('Project Poppler missing; run scripts/bootstrap.sh.')
 version=subprocess.run([str(executable),'-v'],capture_output=True,text=True,check=True)
 folder=ROOT/'.tmp/reader-render-environment';folder.mkdir(parents=True,exist_ok=True)
 target=folder/(source['id']+'-p13.png')
 target.unlink(missing_ok=True)
 command=[str(executable),'-f',str(page_number),'-l',str(page_number),'-r','110','-png','-singlefile',str(pdf),str(target.with_suffix(''))]
 render=subprocess.run(command,capture_output=True,text=True)
 if render.returncode or not target.is_file():raise RuntimeError('Actual cold-page render failed: '+render.stderr)
 class Handler(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(folder)))
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 try:
  base='http://127.0.0.1:'+str(server.server_port)+'/'
  with sync_playwright() as p:
   browser=p.chromium.launch(headless=True,args=['--no-sandbox']);page=browser.new_page()
   page.goto(base,wait_until='load')
   response=page.request.get(base+target.name)
   served_hash=hashlib.sha256(response.body()).hexdigest();response_ok=response.ok;response.dispose()
   decoded=page.evaluate('''async path=>{const image=new Image();image.src=path;await image.decode();return {width:image.naturalWidth,height:image.naturalHeight,same_origin:new URL(image.src).origin===location.origin};}''',target.name)
   browser.close()
 finally:
  server.shutdown();server.server_close();thread.join(timeout=5)
 image_hash=hashlib.sha256(target.read_bytes()).hexdigest()
 install_path=ROOT/'.tmp/poppler-conda-install.json'
 installed=json.loads(install_path.read_text()) if install_path.is_file() else {}
 packages=[{'name':row['name'],'version':row['version'],'build':row.get('build_string',row.get('build')),'channel':row.get('channel')} for row in installed.get('actions',{}).get('LINK',[])]
 report={'status':'passed' if response_ok and served_hash==image_hash and decoded['same_origin'] and decoded['width']>0 and decoded['height']>0 else 'failed',
  'scope':'one_actual_cold_formal_source_page_project_dependency_and_same_origin_decode_not_mathematical_review',
  'recorded_at':datetime.now(timezone.utc).isoformat(),'source_id':source['id'],'pdf_page':page_number,
  'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'source_metadata_hash_matches':hashlib.sha256(pdf.read_bytes()).hexdigest()==source['sha256'],
  'renderer':{'path':executable.relative_to(ROOT).as_posix(),'version':(version.stdout+version.stderr).strip(),'sha256':hashlib.sha256(executable.read_bytes()).hexdigest()},
  'cold_render':{'cached_image_existed_at_render':False,'exit_code':render.returncode,'render_dpi':110,'image_sha256':image_hash,'served_image_sha256':served_hash,'decoded':decoded},
  'installation':{'status':'passed' if installed.get('success') else 'already_available_or_not_recorded','prefix':'.conda-env','package_cache':'.cache/conda/pkgs','configuration_search_disabled':True,'replaced_packages':len(installed.get('actions',{}).get('UNLINK',[])),'linked_packages':packages},
  'input_hashes':input_hashes(Path(__file__).resolve(),WORK/'check_preview.py',WORK/'evidence_paths.py',WORK/'input_manifest.py',ROOT/'environment.yml',ROOT/'scripts/env.sh',ROOT/'scripts/bootstrap.sh',ROOT/'locks/python-conda-linux-64.txt',ROOT/'corpus/public/reader/input-manifest.json',metadata_path,pdf)}
 if not report['source_metadata_hash_matches']:report['status']='failed'
 (EVIDENCE/'render-environment-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'renderer':report['renderer']['version'],'cold_page':source['id']+':'+str(page_number),'decoded':decoded,'linked_packages':len(packages)},ensure_ascii=False))
 return int(report['status']!='passed')

if __name__=='__main__':raise SystemExit(main())
