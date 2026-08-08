"""CLI for open-model release readiness scoring."""
from __future__ import annotations

from .radar import rank_deployment_decisions, rank_releases, sample_releases


def main(argv: list[str] | None = None) -> int:
    _ = argv
    for release, score in rank_releases(sample_releases()):
        print(f"{score:.3f} {release.name}")
    print("")
    for decision in rank_deployment_decisions(sample_releases()):
        blockers = ",".join(decision["blockers"]) or "none"
        print(f"{decision['decision']} {decision['model']} blockers={blockers}")
    return 0
