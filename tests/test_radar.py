from model_supply_chain_radar import DeploymentPolicy, ModelRelease, deployment_decision, readiness_score, rank_deployment_decisions, rank_releases


def test_readiness_rewards_auditable_release_metadata():
    strong = ModelRelease("auditable", True, True, 1_000_000, 2800.0, ("vllm", "sglang"), True, True, True, False)
    weak = ModelRelease("opaque", True, False, 8_000, 0.0, (), False, False, False, True)

    assert readiness_score(strong) > readiness_score(weak)
    assert readiness_score(strong) >= 0.8


def test_rank_releases_sorts_by_score_then_name():
    releases = [
        ModelRelease("b", False, False, 0, 0.0, (), False, False, False, False),
        ModelRelease("a", False, False, 0, 0.0, (), False, False, False, False),
    ]

    assert [release.name for release, _ in rank_releases(releases)] == ["a", "b"]


def test_deployment_decision_exposes_policy_blockers():
    release = ModelRelease("viral-drop", True, False, 1_000_000, 2800.0, ("vllm",), True, True, True, False)

    decision = deployment_decision(release)

    assert decision["decision"] == "do_not_deploy"
    assert "license_unclear" in decision["blockers"]


def test_rank_deployment_decisions_keeps_best_candidate_first():
    policy = DeploymentPolicy(required_integrations=("vllm",), allow_commercial_constraints=True)
    strong = ModelRelease("strong", True, True, 1_000_000, 2800.0, ("vllm", "sglang"), True, True, True, True)
    weak = ModelRelease("weak", True, False, 32_000, 0.0, (), False, False, False, False)

    assert rank_deployment_decisions([weak, strong], policy)[0]["model"] == "strong"
