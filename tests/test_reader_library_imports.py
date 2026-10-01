"""Actual public extension API metadata and application/public boundaries."""
import sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reader/architecture'))
from paper_agent import PaperPackage,public_extension_import

def test_extension_lookup_returns_a_current_type_and_its_real_public_import():
    rows=PaperPackage().library('Harsanyi.Robustness.interaction_dummy')
    row=next(row for row in rows if row['name']=='Harsanyi.Robustness.interaction_dummy')
    assert row['import']=='Harsanyi.Extensions.RobustnessFinite'
    assert (ROOT/row['source_path']).is_file()
    assert row['signature'] and row['current_evidence']['freshness']=='current'
    assert row['current_evidence']['compilation']=='passed'

def test_paper_application_is_not_classified_as_a_public_module_by_its_name():
    assert public_extension_import('corpus/public/reader/icml2022-transformation/lean/PaperTransformation.lean') is None
    assert public_extension_import('lean/PaperProofs/PaperProofs/PaperDynamics.lean') is None
    assert public_extension_import('lean/HarsanyiLib/Harsanyi/Extensions/TransformationRefinement.lean')=='Harsanyi.Extensions.TransformationRefinement'

def test_an_inductive_network_type_keeps_its_actual_kind_and_callable_import():
    row=next(row for row in PaperPackage().library('Harsanyi.Network.Expr') if row['name']=='Harsanyi.Network.Expr')
    assert row['kind']=='inductive'
    assert row['signature'].startswith('Type')
    assert row['import']=='Harsanyi.Extensions.HarsanyiNetwork'
    assert row['current_evidence']['freshness']=='current'

@pytest.mark.parametrize('source',[
    'lean/HarsanyiLib/Harsanyi/Extensions/../../PaperProofs/Adapter.lean',
    'lean/HarsanyiLib/Harsanyi/Extensions/RobustnessFinite.json',
])
def test_malformed_public_source_cannot_produce_a_callable_module(source):
    with pytest.raises(ValueError):public_extension_import(source)

def test_all_admitted_extension_rows_resolve_to_existing_public_modules():
    rows=PaperPackage().library()['extension_declarations']
    assert rows
    for row in rows:
        assert row['import']==public_extension_import(row['source_path'])
        assert (ROOT/'lean/HarsanyiLib'/Path(*row['import'].split('.')).with_suffix('.lean')).is_file()
        assert row['source_role']=='public_library_extension'
