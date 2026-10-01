"""Explicit public/formal inputs shared by aggregation and preview building."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=Path(__file__).resolve().with_name('input-manifest.json')

def project_path(value,required=True):
    value=Path(value)
    if value.is_absolute() or 'inbox' in value.parts or value.parts[:1]==('..',):
        raise ValueError('Input must be an explicit public project-relative path')
    path=ROOT/value
    if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
        raise ValueError('Input escaped project or is a symbolic link')
    if required and not path.is_file():raise ValueError('Missing configured input: '+str(value))
    return path

def load_manifest(read=None):
    read=read or (lambda p:json.loads(p.read_text()))
    manifest=read(MANIFEST)
    if manifest.get('visibility')!='public' or manifest.get('publication_status')!='published':
        raise ValueError('This preview requires an explicitly public, formal manifest')
    if not manifest.get('papers'):raise ValueError('No configured formal papers')
    seen=set()
    for item in manifest['papers']:
        if item['paper_id'] in seen:raise ValueError('Duplicate configured paper ID')
        seen.add(item['paper_id'])
        for key in ('metadata_path','inventory_path','content_path'):
            project_path(item[key])
        metadata=read(project_path(item['metadata_path']))
        if metadata['id']!=item['paper_id'] or metadata.get('visibility')!='public' or metadata.get('publication_status')!='published':
            raise ValueError('Configured paper is not the stated public formal entity')
        for source in metadata.get('sources',[]):
            if source.get('visibility')!='public' or source.get('publication_status')!='published':
                raise ValueError('Source is not public and formally published')
            project_path(source['local_path'])
        if not metadata.get('sources'):raise ValueError('Formal source list is empty')
    return manifest
