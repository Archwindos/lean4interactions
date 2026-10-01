#!/usr/bin/env python3
"""Idempotent physical split; originals are retained as ignored legacy evidence."""
from __future__ import annotations
import argparse, hashlib, json, shutil, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return yaml.safe_load(path.read_text()) or {}
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def migrate(root=ROOT):
 root=Path(root).resolve();corpus=root/'corpus';routes={};objects={'public':{},'private':{}}
 paper_public={}
 for manifest in sorted((corpus/'papers').glob('*/*/manifest.yaml')):
  d=read(manifest);key=(d.get('paper_id'),d.get('version'));paper_public[key]=d.get('visibility')=='public' and d.get('publication_status') not in {'unpublished','private'}
  routes[manifest.parent]='public' if paper_public[key] else 'private'
 claim_public={}
 for meta in sorted((corpus/'claims').glob('*/metadata.yaml')):
  d=read(meta);ok=d.get('visibility')=='public' and paper_public.get((d.get('paper_id'),d.get('paper_version')),False)
  claim_public[d.get('claim_id')]=ok;routes[meta.parent]='public' if ok else 'private'
 theorem_public={}
 for meta in sorted((corpus/'theorems').glob('*/metadata.yaml')):
  d=read(meta);sources=d.get('derived_from',[])+d.get('source_claim_ids',[])
  ok=d.get('visibility')=='public' and all(claim_public.get(x,False) for x in sources)
  for proof_meta in sorted((meta.parent/'proofs').glob('*/metadata.yaml')):
   proof=read(proof_meta)
   if proof.get('visibility')!='public':ok=False
   if not all(claim_public.get(x,False) for x in proof.get('derived_from',[])+proof.get('source_claim_ids',[])):ok=False
  theorem_public[d.get('theorem_id')]=ok;routes[meta.parent]='public' if ok else 'private'
 # Dependencies on private archive entities propagate until the routing settles.
 entity_public={**claim_public,**theorem_public}
 changed=True
 while changed:
  changed=False
  for meta in sorted((corpus/'theorems').glob('*/metadata.yaml')):
   if routes[meta.parent]!='public':continue
   rows=[read(meta)]+[read(p) for p in sorted((meta.parent/'proofs').glob('*/metadata.yaml'))]
   deps=[dep.get('id') if isinstance(dep,dict) else dep for row in rows for dep in row.get('dependencies',[])]
   if any(dep in entity_public and not entity_public[dep] for dep in deps):
    routes[meta.parent]='private';entity_public[read(meta).get('theorem_id')]=False;changed=True
 for folder in ['issues','reviews']:
  base=corpus/folder
  if not base.exists():continue
  for item in sorted(base.iterdir()):
   if item.is_dir():
    metadata=next(iter(item.glob('*.yaml')),None);data=read(metadata) if metadata else {}
   else:data=read(item) if item.suffix in {'.yaml','.yml','.json'} else {}
   ok=data.get('visibility')=='public' and data.get('publication_status')!='unpublished'
   pid=data.get('paper_id');cid=data.get('claim_id')
   if pid:ok=ok and any(p==pid and public for (p,v),public in paper_public.items())
   if cid:ok=ok and claim_public.get(cid,False)
   routes[item]='public' if ok else 'private'
 records=[]
 for origin,pool in routes.items():
  relative=origin.relative_to(corpus);target=corpus/pool/relative
  files=sorted(origin.rglob('*')) if origin.is_dir() else [origin]
  objects[pool][relative.parts[0]]=objects[pool].get(relative.parts[0],0)+1
  for source in files:
   if not source.is_file():continue
   if source.is_symlink():raise ValueError('Symlink in legacy corpus')
   destination=target/source.relative_to(origin) if origin.is_dir() else target
   destination.parent.mkdir(parents=True,exist_ok=True)
   old_hash=digest(source)
   if destination.exists() and digest(destination)!=old_hash:raise ValueError('Migration would overwrite changed active data: '+str(destination.relative_to(root)))
   if not destination.exists():shutil.copyfile(source,destination)
   if digest(destination)!=old_hash:raise ValueError('Migration checksum mismatch')
   records.append({'origin':source.relative_to(root).as_posix(),'target':destination.relative_to(root).as_posix(),'pool':pool,'original_sha256':old_hash,'target_sha256':digest(destination),'original_retained':True})
 relations={'public':{},'private':{}}
 for source in sorted(corpus.glob('relations*.yaml')):
  data=read(source)
  for relation in data.get('relations',[]):
   pool='public' if relation.get('visibility')=='public' and source.name not in {'relations-local-private.yaml','relations-manual-draft.yaml'} else 'private'
   key=relation.get('relation_id') or '|'.join(str(relation.get(k,'')) for k in ['from_id','to_id','relation_type','paper_version'])
   previous=relations[pool].get(key)
   if previous and previous['record']!=relation:raise ValueError('Conflicting legacy relation: '+key)
   if not previous:previous=relations[pool][key]={'record':dict(relation),'sources':[]}
   previous['sources'].append(source.relative_to(root).as_posix())
 for pool in ['public','private']:
  path=corpus/pool/'relations.yaml';path.parent.mkdir(parents=True,exist_ok=True)
  rows=[{**value['record'],'migration_sources':value['sources']} for value in relations[pool].values()]
  path.write_text(yaml.safe_dump({'schema_version':1,'relations':rows},allow_unicode=True,sort_keys=False))
  for folder in ['papers','claims','theorems','issues','reviews']:(corpus/pool/folder).mkdir(parents=True,exist_ok=True)
 # Capture original singleton files without changing them; the generated relation
 # union is auditable independently from byte-for-byte copies.
 legacy_rel=[{'origin':p.relative_to(root).as_posix(),'sha256':digest(p),'original_retained':True} for p in sorted(corpus.glob('relations*.yaml'))]
 report={'schema_version':1,'status':'passed','scope':'physical_migration_not_mathematical_review','active_object_counts':objects,'copied_file_count':len(records),'files':records,'relation_originals':legacy_rel,'relation_counts':{p:len(relations[p]) for p in ['public','private']},'missing_files':[],'hash_mismatches':[],'rollback':'Remove the newly created pool files listed in this report. All legacy originals remain at origin paths. Do not remove files modified after migration.'}
 # Detailed private identifiers remain local-only.
 write(corpus/'private/migration/report.json',report)
 summary={k:v for k,v in report.items() if k not in {'files','relation_originals'}}
 summary['public_files']=[x for x in records if x['pool']=='public'];summary['private_evidence_path']='corpus/private/migration/report.json'
 write(root/'reader/evidence/migration-summary.json',summary)
 return summary
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT)
 print(json.dumps(migrate(parser.parse_args().root),ensure_ascii=False,indent=2))
