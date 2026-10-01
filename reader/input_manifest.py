"""Public reader input contract. Only entries in the explicit published manifest are active."""
import json
from pathlib import Path
from inventory_contract import accepted_paper_ids,validate_inventory,source_errors,issue_errors,control_character_errors
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'corpus/public/reader/input-manifest.json'
def project_path(value,required=True):
 value=Path(value)
 if value.is_absolute() or '..' in value.parts or any(x in value.parts for x in ['private','inbox','experimental']):raise ValueError('Input must be an explicit public project-relative path')
 path=ROOT/value
 if not path.resolve().is_relative_to(ROOT) or any(p.is_symlink() for p in [path,*path.parents] if p.is_relative_to(ROOT)):raise ValueError('Input escaped project or uses a symbolic link')
 if required and not path.is_file():raise ValueError('Missing configured input: '+str(value))
 return path

def load_manifest(read=None):
 read=read or (lambda p:json.loads(p.read_text()))
 manifest=read(MANIFEST)
 if manifest.get('visibility')!='public' or manifest.get('publication_status')!='published':raise ValueError('Reader requires public/formal manifest')
 ids=[x['paper_id'] for x in manifest.get('papers',[])]
 if not ids or len(ids)!=len(set(ids)):raise ValueError('Reader requires a nonempty explicit list of unique paper IDs')
 legacy_ids=accepted_paper_ids(read)
 for item in manifest['papers']:
  prefix='corpus/public/reader/'+item['paper_id']+'/'
  for key in ['metadata_path','inventory_path','content_path','symbols_path','issues_path']:
   if not item[key].startswith(prefix):raise ValueError('Paper input is outside its active directory')
   project_path(item[key])
  metadata=read(project_path(item['metadata_path']))
  if metadata['id']!=item['paper_id'] or metadata.get('visibility')!='public' or metadata.get('publication_status')!='published':raise ValueError('Configured paper is not a public formal entity')
  for source in metadata.get('sources',[]):
   if source.get('visibility')!='public' or source.get('publication_status')!='published':raise ValueError('Source is not formally published')
   path=project_path(source['local_path'])
   if source.get('sha256'):
    import hashlib
    if hashlib.sha256(path.read_bytes()).hexdigest()!=source['sha256']:raise ValueError('Formal source hash changed')
  if not metadata.get('sources'):raise ValueError('Formal source list is empty')
  if item['paper_id'] not in legacy_ids and source_errors(metadata):raise ValueError('Source metadata admission rejected: '+'; '.join(source_errors(metadata)))
  content=read(project_path(item['content_path']))
  validate_inventory(read(project_path(item['inventory_path'])),content,legacy=item['paper_id'] in legacy_ids)
  if item['paper_id'] not in legacy_ids:
   symbol_failures=control_character_errors(read(project_path(item['symbols_path'])),'symbols')
   if symbol_failures:raise ValueError('Symbol admission rejected: '+'; '.join(symbol_failures[:20]))
   listed=read(project_path(item['issues_path']));listed=listed.get('issues',[]) if isinstance(listed,dict) else listed
   issues=list(content.get('issues',[]))+listed
   failures=issue_errors(issues,metadata,content)
   if failures:raise ValueError('Issue admission rejected: '+'; '.join(failures[:20]))
 return manifest
