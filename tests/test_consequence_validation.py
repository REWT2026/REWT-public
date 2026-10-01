from rewt_public.facade import PublicRewtFacade
from rewt_public.forest import PublicForest
from rewt_public.models import PublicConsequenceEnvelope, PublicTreeId
from rewt_public.provider_double import DemonstrationProvider


class WrongTreeProvider:
    def tree_turn(self, request):
        return PublicConsequenceEnvelope(request.request_id, "other-tree", request.owner_id, "result", "x")


class WrongOwnerProvider:
    def tree_turn(self, request):
        return PublicConsequenceEnvelope(request.request_id, request.tree_id, "other-owner", "result", "x")


def test_malformed_provider_output_is_rejected_without_mutation(tmp_path):
    facade = PublicRewtFacade(PublicForest(tmp_path))
    owner = facade.create_owner()
    tree = facade.create_tree(owner)

    result = facade.turn(tree, "x", DemonstrationProvider(malformed=True))

    assert not result.accepted
    assert result.snapshot == tree
    assert facade.restore(PublicTreeId(tree.tree_id), owner) is None


def test_wrong_tree_and_owner_are_rejected(tmp_path):
    facade = PublicRewtFacade(PublicForest(tmp_path))
    owner = facade.create_owner()
    tree = facade.create_tree(owner)

    assert facade.turn(tree, "x", WrongTreeProvider()).rejection_code == "tree_id_mismatch"
    assert facade.turn(tree, "x", WrongOwnerProvider()).rejection_code == "owner_id_mismatch"
