"""Readiness scoring for open-model releases."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRelease:
    name: str
    weights_available: bool
    license_clear: bool
    context_tokens: int
    parameter_billion: float
    serving_integrations: tuple[str, ...]
    hardware_notes: bool
    provenance_notes: bool
    safety_notes: bool
    commercial_constraints: bool


def readiness_score(release: ModelRelease) -> float:
    """Return a transparent 0..1 readiness score."""
    score = 0.0
    score += 0.18 if release.weights_available else 0.0
    score += 0.16 if release.license_clear else 0.0
    score += 0.10 if release.context_tokens >= 128_000 else 0.04 if release.context_tokens >= 32_000 else 0.0
    score += 0.08 if release.parameter_billion > 0 else 0.0
    score += min(0.16, 0.04 * len(set(release.serving_integrations)))
    score += 0.10 if release.hardware_notes else 0.0
    score += 0.10 if release.provenance_notes else 0.0
    score += 0.08 if release.safety_notes else 0.0
    score += 0.04 if not release.commercial_constraints else 0.0
    return round(min(1.0, score), 3)


def rank_releases(releases: list[ModelRelease]) -> list[tuple[ModelRelease, float]]:
    ranked = [(release, readiness_score(release)) for release in releases]
    ranked.sort(key=lambda pair: (-pair[1], pair[0].name.lower()))
    return ranked


def sample_releases() -> list[ModelRelease]:
    return [
        ModelRelease("Kimi K3", True, True, 1_000_000, 2800.0, ("vllm", "sglang"), True, True, True, True),
        ModelRelease("Nemotron 3 Nano Omni", True, True, 128_000, 30.0, ("trt-llm",), True, True, True, False),
        ModelRelease("Unverified Frontier Drop", True, False, 32_000, 0.0, (), False, False, False, False),
    ]
