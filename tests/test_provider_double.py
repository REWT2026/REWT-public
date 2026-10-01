from rewt_public.facade import PublicRewtFacade
from rewt_public.forest import PublicForest
from rewt_public.models import PublicTreeTurnRequest
from rewt_public.provider_double import DemonstrationProvider


def test_provider_double_receives_only_a_bounded_public_request(tmp_path):
    facade = PublicRewtFacade(PublicForest(tmp_path))
    owner = facade.create_owner()
    tree = facade.create_tree(owner)
    provider = DemonstrationProvider()

    result = facade.turn(tree, "input is opaque to the demonstration provider", provider)

    assert result.accepted
    assert len(provider.requests) == 1
    assert provider.requests[0].tree_id == tree.tree_id
    assert provider.requests[0].owner_id == owner.value
    assert not hasattr(provider, "save")
    assert tuple(PublicTreeTurnRequest.__dataclass_fields__) == (
        "request_id", "tree_id", "owner_id", "input_text", "prior_fruit"
    )
