"""Publication keeps local relation data out of public reads."""
from archive.store import ArchiveStore


def test_public_relations_never_read_local_private_file(tmp_path, monkeypatch):
    store = ArchiveStore(tmp_path, public=True)
    public_relation = {"from_id": "published-claim", "to_id": "shared-proof", "visibility": "public"}
    reads = []

    def read(relative, default=None):
        reads.append(relative)
        assert relative != "corpus/private/relations.yaml"
        return {"relations": [public_relation]}

    monkeypatch.setattr(store, "_data", read)
    monkeypatch.setattr(store, "_any_public", lambda entity_id: True)
    assert store.relations() == [public_relation]
    assert reads == ["corpus/public/relations.yaml"]


def test_local_relations_merge_and_filter_optional_private_data(tmp_path, monkeypatch):
    store = ArchiveStore(tmp_path, collection="private")
    public_relation = {"from_id": "published-claim", "to_id": "shared-proof", "visibility": "public"}
    private_relation = {"from_id": "local-claim", "to_id": "shared-proof", "visibility": "private"}

    def read(relative, default=None):
        assert relative == "corpus/private/relations.yaml"
        return {"relations": [private_relation]}

    monkeypatch.setattr(store, "_data", read)
    assert store.relations() == [private_relation]
    assert store.relations("local-claim") == [private_relation]


def test_local_relations_work_without_optional_private_file(tmp_path):
    store = ArchiveStore(tmp_path, collection="private")
    assert store.relations() == []
