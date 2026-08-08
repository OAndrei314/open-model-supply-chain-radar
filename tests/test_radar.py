from model_supply_chain_radar import ModelRelease, readiness_score, rank_releases


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
