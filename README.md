# open-model-supply-chain-radar

Maintained by: codex-daily-routine

A deterministic tracker for open-model release and deployment risk signals. It does not
benchmark models. Instead, it scores whether a release has enough supply-chain,
licensing, serving and governance metadata to be trusted in an engineering workflow.

## Research + Money Thesis

Open-weight models are now a strategic infrastructure variable. The money question is not
only "which model scores highest?" but also "which release can be audited, hosted,
distilled, governed and paid for without surprises?" This project turns release metadata
into a transparent readiness score.

## Signals Tracked

- weight availability and license clarity
- context length and parameter scale
- serving integration maturity
- hardware envelope clarity
- provenance and safety documentation
- commercial-use constraints

## Quickstart

```powershell
pip install -r requirements-dev.txt
pip install -e .
python -m pytest -q
python -m model_supply_chain_radar
```

## Silicon Valley Interview Hook

The `deployment_decision()` API converts release metadata into an approval-style decision
with blockers, warnings and missing serving integrations. It is designed for the actual
platform question behind open-weight hype: which model can move from benchmark slide to
prototype without license, safety or infrastructure surprises?

## Status

MVP: metadata model, readiness scoring, deployment policy decisions, ranking and tests.
Next steps: add parsers for release cards and a dated research-note exporter.

## License

MIT - see [LICENSE](LICENSE).
