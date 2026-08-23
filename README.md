# investment-researcher

A CLI that analyzes ETF expense ratios and holdings concentration, with optional local LLM interpretation.

## Architecture

This project uses hexagonal architecture (ports & adapters):

- **Domain** (`domain/models.py`): Pydantic v2 data contracts for `FundData`, `Concentration`, and `FundamentalReport`.
- **Analytics core** (`analytics.py`): Pure, deterministic functions with no network, LLM, or I/O. Computes concentration metrics (HHI, top-10 weight) and classifies expense ratios and concentration levels.
- **Ports** (`ports.py`): `FundDataSource` and `LLMClient` protocols define external interfaces.
- **Adapters** (`adapters/`):
  - `AlphaVantageFundData`: fetches fund data from the Alpha Vantage ETF_PROFILE endpoint.
  - `OllamaClient`: sends analysis to a local Ollama instance for interpretation.

Dependencies point inward only: domain and analytics never import adapters.

## Requirements

- Python 3.12 or later
- `uv` (package manager)
- Alpha Vantage API key (free tier: 25 requests/day). Get one at https://www.alphavantage.co/
- **Optional**: Ollama with the `llama3.2` model, to enable the `--interpret` flag. See https://ollama.ai/

## Install

```bash
git clone https://github.com/jmalaverri/investment-researcher.git
cd investment-researcher
uv sync
cp .env.example .env
```

Then edit `.env` and set your Alpha Vantage API key:

```
FUND_API_KEY=your_actual_api_key_here
```

## Usage

Analyze an ETF:

```bash
uv run investment-researcher VOO
```

Output:

```
Ticker: VOO
Expense ratio: 0.03% (low)
Holdings count: 509
Top 10 weight: 36.32%
HHI: 193.4
```

With a local LLM interpretation (requires Ollama running with `llama3.2` pulled):

```bash
uv run investment-researcher VOO --interpret
```

This prints the same report, plus an interpretation section (adds ~30s of local latency; a progress note is printed to stderr while it generates):

```
Ticker: VOO
Expense ratio: 0.03% (low)
Holdings count: 509
Top 10 weight: 36.32%
HHI: 193.4

Interpretation:
This fund has very low costs and holds a broad set of 509 positions, minimizing idiosyncratic risk.
The HHI of 193.4 indicates a well-diversified portfolio with no dominant holdings.
```

If the LLM call fails, the report still prints normally, with a note on stderr that the interpretation is unavailable.

### Exit codes

- `0`: success.
- `1`: `FUND_API_KEY` is not set.
- `2`: ticker not found.
- `3`: fund data unavailable (network error, rate limit, or provider error).

## Metrics

**Expense ratio** — annual cost to investors, as a percent (e.g. VOO ≈ 0.03%).
- `low`: < 0.20%
- `moderate`: 0.20% – 0.50%
- `high`: > 0.50%

**Holdings concentration** — the Herfindahl-Hirschman Index (HHI) on a standard 0–10,000 scale over holding weights, plus the top-10 weight percentage.
- `low`: HHI < 1,500
- `moderate`: HHI 1,500 – 2,500
- `high`: HHI > 2,500

## Development

```bash
uv run pytest -q                                      # run tests
uv run ruff check --fix . && uv run ruff format .     # lint + format
```

Tests never touch the network or an LLM — they run against fake adapters and recorded/mock transports only.

## Limitations

- v0 (Fundamentalist) covers exactly two metrics: expense ratio and holdings concentration.
- `--interpret` is optional and adds ~30s of local latency; it requires Ollama running locally.
- Not investment advice.
