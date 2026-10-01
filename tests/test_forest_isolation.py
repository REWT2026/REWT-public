import pytest

from rewt_public.facade import PublicRewtFacade
from rewt_public.forest import PublicForest, PublicForestError
from rewt_public.models import PublicTreeId
from rewt_public.provider_double import DemonstrationProvider


def test_tree_a_tree_b_tree_a_and_cross_owner_isolation(tmp_path):
    facade = PublicRewtFacade(PublicForest(tmp_path))
    owner_a = facade.create_owner()
    owner_b = facade.create_owner()
    tree_a = facade.turn(facade.create_tree(owner_a), "a", DemonstrationProvider()).snapshot
    tree_b = facade.turn(facade.create_tree(owner_a), "b", DemonstrationProvider()).snapshot

    assert facade.restore(PublicTreeId(tree_a.tree_id), owner_a) == tree_a
    assert facade.restore(PublicTreeId(tree_b.tree_id), owner_a) == tree_b
    assert facade.restore(PublicTreeId(tree_a.tree_id), owner_a) == tree_a
    with pytest.raises(PublicForestError, match="owner_identity_mismatch"):
        facade.restore(PublicTreeId(tree_a.tree_id), owner_b)
