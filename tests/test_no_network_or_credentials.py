import os

from rewt_public.facade import PublicRewtFacade
from rewt_public.forest import PublicForest
from rewt_public.provider_double import DemonstrationProvider


def test_demonstration_path_requires_no_credential_or_network(tmp_path, monkeypatch):
    monkeypatch.delenv("REWT_LLM_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    facade = PublicRewtFacade(PublicForest(tmp_path))
    owner = facade.create_owner()

    result = facade.turn(facade.create_tree(owner), "offline", DemonstrationProvider())

    assert result.accepted
    assert "REWT_LLM_API_KEY" not in os.environ
    assert "OPENAI_API_KEY" not in os.environ
