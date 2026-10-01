import ast
from pathlib import Path

import rewt_public
from rewt_public.models import PublicTreeSnapshot


def test_public_package_does_not_import_private_package_or_forbidden_modules():
    package = Path(rewt_public.__file__).parent
    forbidden = {
        "pipeline", "semantic_contract", "tree_turn_contract", "active_state",
        "objective", "sufficiency", "validity", "materiality", "refinement",
        "continuation", "lifecycle",
    }
    for path in package.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [item.name for item in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                assert not (name == "rewt" or name.startswith("rewt."))
                assert not any(part in forbidden for part in name.split("."))


def test_public_models_and_source_contain_no_private_state_or_prompt_builder():
    assert tuple(PublicTreeSnapshot.__dataclass_fields__) == (
        "schema_version", "tree_id", "owner_id", "current_fruit", "fruit_history"
    )
    package = Path(rewt_public.__file__).parent
    forbidden_text = ("system_instructions", "semantic_method", "TreeTurnRequestBuilder")
    for path in package.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert not any(item in text for item in forbidden_text)
