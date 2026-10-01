from rewt_public.facade import PublicRewtFacade
from rewt_public.forest import PublicForest
from rewt_public.models import PublicTreeId
from rewt_public.provider_double import DemonstrationProvider


def test_accepted_result_persists_and_restores_exact_snapshot(tmp_path):
    first = PublicRewtFacade(PublicForest(tmp_path))
    owner = first.create_owner()
    tree = first.create_tree(owner)
    accepted = first.turn(tree, "opaque input", DemonstrationProvider())

    restarted = PublicRewtFacade(PublicForest(tmp_path))
    restored = restarted.restore(PublicTreeId(accepted.snapshot.tree_id), owner)

    assert accepted.accepted
    assert restored == accepted.snapshot
    assert restored.current_fruit is not None
    assert restored.current_fruit.tree_id == tree.tree_id
