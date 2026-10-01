from rewt_public.facade import PublicRewtFacade
from rewt_public.forest import PublicForest


def test_owner_and_tree_identity_are_independent(tmp_path):
    facade = PublicRewtFacade(PublicForest(tmp_path))
    owner = facade.create_owner()
    tree = facade.create_tree(owner)

    assert tree.owner_id == owner.value
    assert tree.tree_id != owner.value
