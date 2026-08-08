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


@dataclass(frozen=True)
class DeploymentPolicy:
    min_readiness: float = 0.82
    min_context_tokens: int = 128_000
    required_integrations: tuple[str, ...] = ("vllm",)
    require_safety_notes: bool = True
    allow_commercial_constraints: bool = False


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


def deployment_decision(release: ModelRelease, policy: DeploymentPolicy = DeploymentPolicy()) -> dict[str, object]:
    """Return a policy decision with auditable blockers."""
    score = readiness_score(release)
    integrations = {name.lower() for name in release.serving_integrations}
    missing_integrations = tuple(name for name in policy.required_integrations if name.lower() not in integrations)
    blockers: list[str] = []
    warnings: list[str] = []
    if not release.weights_available:
        blockers.append("weights_not_available")
    if not release.license_clear:
        blockers.append("license_unclear")
    if score < policy.min_readiness:
        blockers.append("readiness_below_policy")
    if missing_integrations:
        blockers.append("missing_required_serving_integration")
    if policy.require_safety_notes and not release.safety_notes:
        blockers.append("missing_safety_notes")
    if release.commercial_constraints and not policy.allow_commercial_constraints:
        blockers.append("commercial_constraints")
    if release.context_tokens < policy.min_context_tokens:
        warnings.append("context_below_target_workload")
    if not release.hardware_notes:
        warnings.append("hardware_envelope_unclear")
    decision = "approve_for_prototype" if not blockers else "needs_review"
    if "weights_not_available" in blockers or "license_unclear" in blockers:
        decision = "do_not_deploy"
    return {
        "model": release.name,
        "readiness_score": score,
        "decision": decision,
        "blockers": tuple(blockers),
        "warnings": tuple(warnings),
        "missing_integrations": missing_integrations,
        "serving_maturity": round(min(1.0, len(integrations) / max(1, len(policy.required_integrations) + 2)), 3),
    }


def rank_releases(releases: list[ModelRelease]) -> list[tuple[ModelRelease, float]]:
    ranked = [(release, readiness_score(release)) for release in releases]
    ranked.sort(key=lambda pair: (-pair[1], pair[0].name.lower()))
    return ranked


def rank_deployment_decisions(
    releases: list[ModelRelease],
    policy: DeploymentPolicy = DeploymentPolicy(),
) -> list[dict[str, object]]:
    decisions = [deployment_decision(release, policy) for release in releases]
    decisions.sort(key=lambda item: (-float(item["readiness_score"]), len(item["blockers"]), str(item["model"]).lower()))
    return decisions


def sample_releases() -> list[ModelRelease]:
    return [
        ModelRelease("Kimi K3", True, True, 1_000_000, 2800.0, ("vllm", "sglang"), True, True, True, True),
        ModelRelease("Nemotron 3 Nano Omni", True, True, 128_000, 30.0, ("trt-llm",), True, True, True, False),
        ModelRelease("Unverified Frontier Drop", True, False, 32_000, 0.0, (), False, False, False, False),
    ]
