# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv run pytest                        # run all tests
uv run pytest tests/test_contract.py # run a single test file
uv run pytest -k test_name           # run tests matching a name pattern
uv add <pkg>                         # add a runtime dependency
uv add --dev <pkg>                   # add a dev dependency
```

## Scope right now
The **Fundamentalist v0** module only. Nothing else.

## Architecture: hexagonal (ports & adapters)

- Package: `investment_researcher` (src layout under `src/`).
- `domain/models.py`: Pydantic v2 data contracts. `weight_pct` and all `*_pct` fields are 0–100 floats.
- `ports.py`: `typing.Protocol` interfaces (`FundDataSource`, `LLMClient`). Adapters conform by shape, no inheritance.
- `analytics.py` *(not yet created)*: PURE functions — no network, no LLM, no I/O, deterministic.
- `adapters/` *(not yet created)*: the ONLY place network/LLM code may live.
- Dependencies point inward: domain and analytics never import adapters.

## Hard rules

- Deterministic spine (domain + analytics + fake adapter) must be green BEFORE any LLM code.
- Tests never touch the network or an LLM — use Fake adapters or recorded responses.
- All public functions type-annotated. Units explicit in names/docstrings (`weight_pct` means 0..100).
- Conventional Commits for all commit messages.

## Build order (do not skip ahead)
contract → analytics core + golden tests → fake adapter + wiring (green) → real data adapter → Ollama LLM layer.

## Working agreement

Implement ONLY what the current step asks. Do not pre-build adapters or the LLM layer.
After writing code, the code-reviewer subagent reviews before commit.

## Decisions (ADR-lite)
- LLM port deferred to the Ollama step; do not define it in the contract.
- `Concentration.hhi`: standard 0–10,000 HHI on percent weights (not normalized 0–1).
- `expense_ratio_pct`: percent convention (VOO ≈ 0.03). No magic upper bound; guard via an adapter unit test.
- `FundDataSource` is synchronous; parallelism, if ever needed, lives in the orchestrator.
