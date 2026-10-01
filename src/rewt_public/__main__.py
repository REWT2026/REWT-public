"""Run an offline structural demonstration."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from rewt_public.facade import PublicRewtFacade
from rewt_public.forest import PublicForest
from rewt_public.models import PublicTreeId
from rewt_public.provider_double import DemonstrationProvider


def main() -> int:
    with TemporaryDirectory() as directory:
        facade = PublicRewtFacade(PublicForest(Path(directory)))
        owner = facade.create_owner()
        tree = facade.create_tree(owner)
        result = facade.turn(tree, "offline demonstration input", DemonstrationProvider())
        restored = facade.restore(PublicTreeId(result.snapshot.tree_id), owner)
        if not result.accepted or restored != result.snapshot:
            return 1
    print("Offline public architecture demonstration completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
