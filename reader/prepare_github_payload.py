#!/usr/bin/env python3
"""Prepare Git Data payloads from an audited exact index, without Git mutations."""
from __future__ import annotations
import argparse,base64,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def git(*args):return subprocess.run(['git',*args],cwd=ROOT,check=True,stdout=subprocess.PIPE).stdout

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='.tmp/github-publish')
    parser.add_argument('--base-commit',default='HEAD',help='Use EMPTY to avoid reuse; otherwise a local base whose blobs may be reused only after the publisher confirms that remote Git contains it.')
    parser.add_argument('--inline-max-bytes',type=int,default=65536)
    args=parser.parse_args()
    output=(ROOT/args.output).resolve()
    if not output.is_relative_to(ROOT/'.tmp') or output==ROOT/'.tmp':raise ValueError('Payload output must be a dedicated project .tmp subdirectory')
    if output.exists() and any(output.iterdir()):raise ValueError('Use an empty payload directory; previous publication evidence is retained')
    if args.inline_max_bytes<0:raise ValueError('inline-max-bytes must be nonnegative')
    output.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/check-publication.py'),'--report',str(output/'index-audit.json')],cwd=ROOT,check=True)
    index=ROOT/'.git/index';initial=hashlib.sha256(index.read_bytes()).hexdigest()
    base=None if args.base_commit=='EMPTY' else git('rev-parse',args.base_commit+'^{commit}').decode().strip()
    base_blobs=set() if base is None else {entry.split(b'\t',1)[0].split()[2].decode() for entry in git('ls-tree','-rz','--full-tree',base).split(b'\0') if entry and entry.split(b'\t',1)[0].split()[1]==b'blob'}
    entries=[];required={};reuse=set();inline_count=0;indexed=[]
    for entry in git('ls-files','-s','-z').split(b'\0'):
        if not entry:continue
        header,path=entry.split(b'\t',1);mode,sha,stage=header.decode().split();path=path.decode('utf-8')
        if stage!='0' or mode not in {'100644','100755'}:raise ValueError('Unsupported/unmerged index entry: '+path)
        indexed.append({'path':path,'mode':mode,'sha':sha,'stage':0})
        row={'path':path,'mode':mode,'type':'blob'}
        if sha in base_blobs:row['sha']=sha;reuse.add(sha)
        else:
            data=git('cat-file','blob',sha)
            if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=sha:raise ValueError('Blob integrity failure: '+path)
            try:text=data.decode('utf-8');is_text='\0' not in text
            except UnicodeDecodeError:text=None;is_text=False
            if is_text and len(data)<=args.inline_max_bytes:row['content']=text;inline_count+=1
            else:
                row['sha']=sha
                item=required.setdefault(sha,{'sha':sha,'size_bytes':len(data),'kind':'utf8_text' if is_text else 'binary','paths':[],'encoding':'utf-8' if is_text else 'base64'})
                item['paths'].append(path)
                if len(item['paths'])==1:
                    folder=output/'blobs';folder.mkdir(exist_ok=True)
                    payload={'content':text if is_text else base64.b64encode(data).decode('ascii'),'encoding':item['encoding']}
                    payload_path=folder/(sha+'.json');payload_path.write_text(json.dumps(payload,ensure_ascii=False)+'\n')
                    item['api_payload_path']=payload_path.relative_to(ROOT).as_posix()
        entries.append(row)
    if hashlib.sha256(index.read_bytes()).hexdigest()!=initial:raise ValueError('Index changed during payload preparation; discard this attempt')
    (output/'flat-index.json').write_text(json.dumps(indexed,ensure_ascii=False,indent=2)+'\n')
    tree_path=output/'tree-entries.json';tree_path.write_text(json.dumps({'tree':entries},ensure_ascii=False)+'\n')
    blobs=list(required.values())
    report={'status':'prepared_pending_remote_base_confirmation_and_blob_upload','scope':'read_only_exact_index_no_stage_commit_push_or_network','index_sha256':initial,'local_base_commit':base,'remote_contains_base_not_assumed':True,'tree_entry_count':len(entries),'tree_payload_path':tree_path.relative_to(ROOT).as_posix(),'tree_payload_bytes':tree_path.stat().st_size,'reused_base_unique_blobs':len(reuse),'inline_utf8_entries':inline_count,'inline_max_bytes':args.inline_max_bytes,'new_unique_upload_blobs':blobs,'new_binary_unique_blobs':[b for b in blobs if b['kind']=='binary'],'required_blob_upload_bytes':sum(b['size_bytes'] for b in blobs),'publisher_must_verify_returned_blob_sha':True}
    (output/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','index_sha256','tree_entry_count','inline_utf8_entries','reused_base_unique_blobs','required_blob_upload_bytes']},ensure_ascii=False))
if __name__=='__main__':main()
