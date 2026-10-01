"""Physical boundary checks for public/private pools and immutable migration."""
from pathlib import Path
import importlib.util
import pytest
from archive.ingest import ingest_local, update_metadata
from archive.store import ArchiveStore
from archive.util import ArchiveError, write_data, sha256

def manuscript(root,name='same-paper',public=False):
 folder=root/'inbox'/('public-source' if public else 'private-source');folder.mkdir(parents=True,exist_ok=True)
 (folder/'main.md').write_text('# Theorem 1\n'+('Published source' if public else 'Private theorem secret text'))
 return ingest_local(root,folder,paper_id=name,metadata={'visibility':'public' if public else 'private','publication_status':'published' if public else 'unpublished'})

def test_same_id_separate_pools_and_public_never_opens_private(tmp_path,monkeypatch):
 manuscript(tmp_path);manuscript(tmp_path,public=True)
 original=Path.read_text
 def deny_private(path,*args,**kwargs):
  if 'private' in path.relative_to(tmp_path).parts:raise AssertionError('Public opened private: '+str(path))
  return original(path,*args,**kwargs)
 monkeypatch.setattr(Path,'read_text',deny_private)
 store=ArchiveStore(tmp_path)
 assert store.collection=='public'
 assert store.get_paper('same-paper')['visibility']=='public'
 assert store.get_paper('same-paper')['publication_status']=='published'
 assert len(store.list_papers())==1
 assert not store.search('Private theorem secret')
 assert store.search('Published source')==[]  # sources are indexed only after extraction
 with pytest.raises(ArchiveError):store.path('corpus/private/papers/same-paper/v1/manifest.yaml')

def test_import_default_and_explicit_private_search(tmp_path):
 from archive.extract import extract_paper
 paper=manuscript(tmp_path)
 assert (tmp_path/'corpus/private/papers/same-paper/v1/sources/main.md').is_file()
 assert not ArchiveStore(tmp_path).list_papers()
 extract_paper(tmp_path,paper['paper_id'],collection='private')
 assert ArchiveStore(tmp_path,collection='private').search('secret')
 assert not ArchiveStore(tmp_path).search('secret')
 with pytest.raises(ArchiveError,match='explicit promote'):
  update_metadata(tmp_path,paper['paper_id'],None,{'visibility':'public'},collection='private')

def migration_module():
 spec=importlib.util.spec_from_file_location('migration',Path(__file__).resolve().parents[1]/'scripts/migrate-corpus-pools.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def legacy(root):
 for name,visibility in [('public-paper','public'),('private-paper','private')]:
  d=root/'corpus/papers'/name/'v1';write_data(d/'manifest.yaml',{'paper_id':name,'version':'v1','visibility':visibility,'publication_status':'published' if visibility=='public' else 'unpublished'})
  (d/'original.txt').write_text(name)
 write_data(root/'corpus/claims/c1/metadata.yaml',{'claim_id':'c1','paper_id':'public-paper','paper_version':'v1','visibility':'public'})
 write_data(root/'corpus/claims/c2/metadata.yaml',{'claim_id':'c2','paper_id':'private-paper','paper_version':'v1','visibility':'private'})
 relation={'from_id':'c1','to_id':'public-paper','relation_type':'source','visibility':'public'}
 for file in ['relations.yaml','relations-public-draft.yaml']:write_data(root/'corpus'/file,{'relations':[relation]})
 return relation

def test_migration_hash_conservation_and_stable_relation_dedup(tmp_path):
 legacy(tmp_path);m=migration_module();report=m.migrate(tmp_path)
 assert report['relation_counts']=={'public':1,'private':0}
 assert report['active_object_counts']['public']=={'papers':1,'claims':1}
 assert report['active_object_counts']['private']=={'papers':1,'claims':1}
 assert m.migrate(tmp_path)['copied_file_count']==report['copied_file_count']
 from archive.util import load_data
 evidence=load_data(tmp_path/'corpus/private/migration/report.json')
 assert all(sha256(tmp_path/x['origin'])==sha256(tmp_path/x['target'])==x['original_sha256'] for x in evidence['files'])

def test_migration_relation_conflict_fails(tmp_path):
 r=legacy(tmp_path);write_data(tmp_path/'corpus/relations-public-draft.yaml',{'relations':[{**r,'review_status':'conflict'}]})
 with pytest.raises(ValueError,match='Conflicting'):migration_module().migrate(tmp_path)

def test_migration_private_proof_taints_parent_and_public_unpublished_quarantined(tmp_path):
 legacy(tmp_path)
 write_data(tmp_path/'corpus/theorems/t/metadata.yaml',{'theorem_id':'t','visibility':'public'})
 write_data(tmp_path/'corpus/theorems/t/proofs/p/metadata.yaml',{'proof_id':'p','visibility':'private'})
 write_data(tmp_path/'corpus/papers/ambiguous/v1/manifest.yaml',{'paper_id':'ambiguous','version':'v1','visibility':'public','publication_status':'unpublished'})
 migration_module().migrate(tmp_path)
 assert (tmp_path/'corpus/private/theorems/t/proofs/p/metadata.yaml').is_file()
 assert not (tmp_path/'corpus/public/theorems/t').exists()
 assert (tmp_path/'corpus/private/papers/ambiguous/v1/manifest.yaml').is_file()

def test_private_references_public_library_without_search_or_copy(tmp_path):
 from archive.extract import extract_paper
 from archive.validate import validate_archive
 from archive.util import load_data
 p=manuscript(tmp_path);extract_paper(tmp_path,p['paper_id'],collection='private')
 public=tmp_path/'corpus/public/theorems/common'
 write_data(public/'metadata.yaml',{'theorem_id':'common','visibility':'public','derived_from':[]})
 (public/'statement.tex').write_text('x=x')
 write_data(public/'proofs/common-proof/metadata.yaml',{'proof_id':'common-proof','theorem_id':'common','visibility':'public'})
 (public/'proofs/common-proof/proof.zh.md').write_text('Reflexivity common-public-marker')
 claim_meta=next((tmp_path/'corpus/private/claims').glob('*/metadata.yaml'))
 d=load_data(claim_meta);d.update(theorem_ids=['common'],proof_ids=['common-proof']);write_data(claim_meta,d)
 write_data(tmp_path/'corpus/private/relations.yaml',{'relations':[{'from_id':d['claim_id'],'to_id':'common','visibility':'private'}]})
 private=ArchiveStore(tmp_path,collection='private')
 assert private.get_theorem('common')['collection']=='public'
 assert private.get_proof('common-proof')['collection']=='public'
 assert private.list_theorems()==[]
 assert not private.search('common-public-marker')
 assert not (tmp_path/'corpus/private/theorems/common').exists()
 assert validate_archive(tmp_path,collection='private')['status']=='passed'
 assert not ArchiveStore(tmp_path).get_claim(d['claim_id'])
