# Investment Researcher — project memory

## Scope right now
The **Fundamentalist v0** module only. Nothing else.

## Architecture: hexagonal (ports & adapters)
- Package: `investment_researcher` (src layout).
- Ports (`ports.py`): `typing.Protocol` interfaces; adapters conform by shape.
- Domain (`domain/models.py`): pydantic v2 data contracts.
- Analytics core (`analytics.py`): PURE functions — no network, no LLM, no I/O, deterministic.
- Adapters (`adapters/`): the ONLY place network/LLM code may live.
- Dependencies point inward: domain and analytics never import adapters.

## Hard rules
- Deterministic spine (domain + analytics + fake adapter) must be green BEFORE any LLM code.
- Tests never touch the network or an LLM. Use Fake adapters / recorded responses.
- All public functions type-annotated. Units explicit in names/docstrings (e.g. `weight_pct` is 0..100).
- Use `uv`: `uv add`, `uv add --dev`, `uv run pytest`. Conventional Commits.

## Build order (do not skip ahead)
contract → analytics core + golden tests → fake adapter + wiring (green) → real data adapter → Ollama LLM layer.

## Working agreement
Implement ONLY what the current step asks. Do not pre-build adapters or the LLM layer.
After writing code, the code-reviewer subagent reviews before commit.